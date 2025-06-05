from openai import OpenAI
from dotenv import load_dotenv
import os
import time

load_dotenv()

client = OpenAI()  # This will automatically use OPENAI_API_KEY from environment

# Ask a question
question = "What do strings mean?"
print(f"\n❓ Question: {question}")

# Get response using Chat Completions API
response = client.chat.completions.create(
    model="gpt-4-turbo",
    messages=[
        {"role": "system", "content": "You are a helpful tutor. Please explain concepts clearly and concisely."},
        {"role": "user", "content": question}
    ]
)

print("\n💬 Assistant Response:\n" + "-" * 40)
print(response.choices[0].message.content)