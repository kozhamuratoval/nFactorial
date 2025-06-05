from openai import OpenAI
from pydantic import BaseModel, Field
import json
import os

# Define the Note schema
class Note(BaseModel):
    id: int = Field(..., ge=1, le=10)
    heading: str = Field(..., example="Mean Value Theorem")
    summary: str = Field(..., max_length=150)
    page_ref: int | None = Field(None, description="Page number in source PDF")

# Initialize OpenAI client
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY", "your-api-key-here"),
)

# Read the content of the file
with open("new/data/calculus_basics.txt", "r") as f:
    content = f.read()

# System prompt for JSON generation
system_prompt = (
    "You are a study summarizer. "
    "Return exactly 10 unique notes that will help prepare for the exam. "
    "Use the following content to create the notes:\n\n"
    f"{content}\n\n"
    "Respond *only* with valid JSON matching the Note[] schema with this structure: "
    '{"notes": [{"id": 1, "heading": "Topic", "summary": "Brief explanation", "page_ref": null}]}'
)

def generate_notes():
    try:
        # Make the API call
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": "Generate the study notes."}
            ],
            response_format={"type": "json_object"}
        )

        # Parse the response
        data = json.loads(response.choices[0].message.content)
        
        # Validate against schema
        notes = [Note(**item) for item in data["notes"]]
        
        # Save to file
        with open("exam_notes.json", "w") as f:
            json.dump({"notes": [note.model_dump() for note in notes]}, f, indent=2)
        
        # Print pretty notes
        print("\n📝 Generated Exam Notes:\n" + "=" * 40)
        for note in notes:
            print(f"\n{note.id}. {note.heading}")
            print("-" * 40)
            print(note.summary)
            if note.page_ref:
                print(f"[Page: {note.page_ref}]")
        
        return notes
    
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return None

if __name__ == "__main__":
    notes = generate_notes() 