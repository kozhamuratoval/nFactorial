import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()

def get_client():
    
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("❌ Error: OPENAI_API_KEY not found in environment variables.")
        print("   Please copy .env.example to .env and add your API key.")
        sys.exit(1)
    
    org_id = os.getenv("OPENAI_ORG")
    client_kwargs = {"api_key": api_key}
    if org_id:
        client_kwargs["organization"] = org_id
    
    return OpenAI(**client_kwargs)

def load_assistant_id():
    """Load existing assistant ID from .assistant file if it exists."""
    assistant_file = Path(".assistant")
    if assistant_file.exists():
        return assistant_file.read_text().strip()
    return None

def save_assistant_id(assistant_id):
    """Save assistant ID to .assistant file for reuse."""
    assistant_file = Path(".assistant")
    assistant_file.write_text(assistant_id)
    print(f"💾 Assistant ID saved to {assistant_file}")

def create_or_update_assistant(client):
    """Create a new assistant or update existing one."""
    existing_id = load_assistant_id()
    
    assistant_config = {
        "name": "Practice Lab Assistant",
        "model": "gpt-4o-mini",
        "instructions": """You are a helpful lab assistant for OpenAI API practice sessions.

You can help with:
- Explaining API concepts and responses
- Analyzing uploaded documents using file_search
- Providing structured outputs in JSON format
- Demonstrating various OpenAI API capabilities

Always be clear, concise, and educational in your responses. When working with files, 
provide specific citations and references to the source material.""",
        "tools": [{"type": "file_search"}],  # Enable built-in RAG
        "temperature": 0.7,
        "top_p": 1.0
    }
    
    try:
        if existing_id:
            print(f"🔄 Updating existing assistant: {existing_id}")
            assistant = client.beta.assistants.update(
                assistant_id=existing_id,
                **assistant_config
            )
            print("✅ Assistant updated successfully!")
        else:
            print("🆕 Creating new assistant...")
            assistant = client.beta.assistants.create(**assistant_config)
            save_assistant_id(assistant.id)
            print("✅ Assistant created successfully!")
        
        print(f"📋 Assistant Details:")
        print(f"   ID: {assistant.id}")
        print(f"   Name: {assistant.name}")
        print(f"   Model: {assistant.model}")
        print(f"   Tools: {[tool.type for tool in assistant.tools]}")
        
        return assistant
        
    except Exception as e:
        print(f"❌ Error creating/updating assistant: {e}")
        sys.exit(1)

def main():
    """Main function to bootstrap the assistant."""
    print("🚀 OpenAI Practice Lab - Assistant Bootstrap")
    print("=" * 50)
    
    # Initialize client
    client = get_client()
    print("✅ OpenAI client initialized")
  
    assistant = create_or_update_assistant(client)
    
    print("\n🎯 Next Steps:")
    print("   1. Run: python scripts/01_responses_api.py")
    print("   2. Or explore other lab modules in the scripts/ directory")
    print("\n💡 Tip: Use 'python scripts/99_cleanup.py' to clean up resources when done")

if __name__ == "__main__":
    main() 
    
    
    
'''import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

def get_client():
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("❌ OPENAI_API_KEY not found.")
        sys.exit(1)
    
    org_id = os.getenv("OPENAI_ORG")
    client_kwargs = {"api_key": api_key}
    if org_id:
        client_kwargs["organization"] = org_id

    return OpenAI(**client_kwargs)

def load_assistant_id():
    path = Path(".assistant")
    return path.read_text().strip() if path.exists() else None

def save_assistant_id(assistant_id):
    Path(".assistant").write_text(assistant_id)
    print(f"💾 Assistant ID saved to .assistant")

def save_vectorstore_id(vectorstore_id):
    Path(".vectorstore").write_text(vectorstore_id)
    print(f"💾 Vector Store ID saved to .vectorstore")

def create_or_update_assistant(client):
    existing_id = load_assistant_id()
    config = {
        "name": "Practice Lab Assistant",
        "model": "gpt-4-turbo",
        "instructions": """You are a helpful lab assistant for OpenAI API practice sessions.
You can help with:
- Explaining API concepts and responses
- Analyzing uploaded documents using file_search
- Providing structured outputs in JSON format
- Demonstrating various OpenAI API capabilities
Always be clear, concise, and educational in your responses. When working with files, 
provide specific citations and references to the source material.""",
        "tools": [{"type": "file_search"}],
        "temperature": 0.7,
        "top_p": 1.0
    }

    if existing_id:
        print(f"🔄 Updating existing assistant: {existing_id}")
        assistant = client.beta.assistants.update(assistant_id=existing_id, **config)
    else:
        print("🆕 Creating new assistant...")
        assistant = client.beta.assistants.create(**config)
        save_assistant_id(assistant.id)

    print(f"✅ Assistant ready! ID: {assistant.id}")
    return assistant

def upload_file_to_vector_store(client, file_path):
    print("📂 Uploading file...")
    file = client.files.create(file=open(file_path, "rb"), purpose="assistants")
    
    vector_store = client.vector_stores.create(name="study_pdf_vector_store")
    print(f"📚 Vector Store Created: {vector_store.id}")

    client.vector_stores.files.create(vector_store_id=vector_store.id, file_id=file.id)
    print(f"📎 File {file.id} attached to Vector Store.")

    save_vectorstore_id(vector_store.id)
    return vector_store.id

def link_vectorstore_to_assistant(client, assistant_id, vectorstore_id):
    print(f"🔗 Linking Vector Store {vectorstore_id} to Assistant {assistant_id}...")
    client.beta.assistants.update(
        assistant_id="asst_LwL0pB4sxXTFIA7k9p4xPQgU",
        tool_resources={
            "file_search": {
                "vector_store_ids": [vectorstore_id]
            }
        }
    )
    print("✅ Assistant linked to vector store.")

def main():
    print("🚀 OpenAI Practice Lab - Assistant Bootstrap")
    print("=" * 50)

    client = get_client()
    print("✅ OpenAI client initialized")

    assistant = create_or_update_assistant(client)

    pdf_path = Path("calculus.pdf")
    if not pdf_path.exists():
        print(f"❌ PDF file not found: {pdf_path}")
        sys.exit(1)

    vectorstore_id = upload_file_to_vector_store(client, pdf_path)
    link_vectorstore_to_assistant(client, assistant.id, vectorstore_id)

    print("\n🎯 All set! You can now run:")
    print("   python scripts/03_qna_from_pdf.py")

if __name__ == "__main__":
    main()
    '''
