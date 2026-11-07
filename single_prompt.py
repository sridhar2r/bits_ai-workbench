import os
import sys
from dotenv import load_dotenv
from openai import OpenAI, AuthenticationError, APIConnectionError

# Load api key from .env file
load_dotenv()

api_key = os.getenv("OPEN_API_KEY")
if not api_key:
    print("Error: OPEN_API_KEY not found in environment variable")
    sys.exit

# Instantiate OpenAI Client
client = OpenAI(api_key=api_key)
MODEL = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")

#Sending prompt to OpenAI LLM
try:
   response = client.chat.completions.create(
       model = MODEL,
       messages = [
           {"role": "system", "content" : "You are a helpful assistant."},
           {"role": "user", "content": "Can you summarize, extract keywords and give a headline in following text: Generative AI is a branch of artificial intelligence that can create new content such as text, images, audio, video, and computer code. It uses large machine learning models trained on vast amounts of data to understand patterns and generate human-like outputs. Tools such as ChatGPT, Gemini, and Claude demonstrate how generative AI can support writing, research, programming, education, and creative work. However, generated content may contain errors, bias, or unsupported claims, so human review remains important. Organizations are increasingly using generative AI to automate tasks, improve productivity, personalize experiences, and build intelligent applications. Responsible use requires attention to privacy, security, accuracy, and ethics."}
       ],
       temperature=0.1,
       max_tokens=100
   )
  # print(f"Response: {response.choices[0].message.content}")
   #print(f"Tokens used: {response.usage.total_tokens}")
   print("Response: ", response.choices[0].message.content)
   print("Tokens used: ", response.usage.total_tokens)
except AuthenticationError as e:
    print("Error: Invalid API Key. Check your .env file.")
except APIConnectionError as e:
    print("Error: Cannot connect. Check your internet")
except Exception as e:
    print(f"Unexpected error: {e}")