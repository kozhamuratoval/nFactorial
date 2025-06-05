from openai import OpenAI
import os

# Initialize OpenAI client with API key
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY", "your-api
)

def upload_file():
    try:
        # Upload the file
        with open("new/data/calculus_basics.txt", "rb") as file:
            file_response = client.files.create(
                file=file,
                purpose="assistants"
            )
        
        print(f"✅ File uploaded successfully with ID: {file_response.id}")
        
        # Save the file ID
        with open(".file_id", "w") as f:
            f.write(file_response.id)
            
        return file_response.id
    
    except Exception as e:
        print(f"❌ Error uploading file: {str(e)}")
        return None

if __name__ == "__main__":
    file_id = upload_file() 