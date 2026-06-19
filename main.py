from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

stream = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=[
        {
            "role":"user",
            "content":"Tell me a story"
        }
    ],
    stream=True
)

for chunk in stream:
    print(chunk.choices[0].delta.content or "", end="")