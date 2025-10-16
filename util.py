import re
import sqlite3
from dotenv import load_dotenv
import google.generativeai as genai
import os


# LLM initialize
load_dotenv()

GOOGLE_API_KEY=os.getenv('GOOGLE_API_KEY')
genai.configure(api_key=GOOGLE_API_KEY)

model = genai.GenerativeModel("gemini-2.5-flash", generation_config=genai.types.GenerationConfig(
    temperature=0,
    candidate_count=1
    ))

def make_vec(title, body):
  result = genai.embed_content(
    model="models/gemini-embedding-001",
    content=body,
    task_type="retrieval_document",
    title=title)
  return result["embedding"]
  
def chat(prompt):
  response = None
  for retry in range(3):
    response = None
    try:
      chat = model.start_chat(history=[])
      response = chat.send_message(prompt)
    except Exception as e:
      print("Error in calling LLM")
      print(e)
      print(f"WARN: retry: {retry+1}")
      continue
    #print("response", response.text)
    break
  return response 
