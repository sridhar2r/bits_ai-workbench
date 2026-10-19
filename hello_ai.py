import os
import sys
from dotenv import load_dotenv
from openai import OpenAI, AuthenticationError, APIConnectionError

load_dotenv() # reads your .env file and makes those variable availabl in your program
#If load_dotenv() is not given, os.getenv() will return empty.
api_key = os.getenv("OPEN_API_KEY")
if not api_key:
    print("ERROR: OPEN_API_KEY not found!")
    print("Copy .env.example to .env to add your key.")
    sys.exit(1)
client = OpenAI(api_key=api_key)
MODEL = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")

# -- the call --

print("Sending prompt: What is generative AI in one sentence?")

try:
    response = client.chat.completions.create(
        model=MODEL,
        messages = [
               {"role": "system", "content" : "You are a helpful assistant. Be concise" },
               {"role": "user", "content": "What is generative AI in one sentence?"}
            ],
        temperature=0.7,
        max_tokens=100
    )
    #response + error
    print(f"Response:{response.choices[0].message.content}")
    print(f"Tokens used: {response.usage.total_tokens}")
except AuthenticationError:
    print("Error: Invalid API Key. Check your .env file.")
except APIConnectionError:
    print("Error: Cannot connect. Check your internet")
except Exception as e:
    print(f"Unexpected error: {e}")