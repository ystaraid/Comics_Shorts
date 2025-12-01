import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-2.0-flash')

response = model.generate_content("인공지능의 미래에 대해 에세이를 써줘.", stream=True)

for chunk in response:
    print(chunk.text, end="")