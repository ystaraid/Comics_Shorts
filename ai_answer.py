'''
API key: AIzaSyDaVdwoe5rQEVhYLhpKyatWuN4QZDIAAn4
name: gemini_practice_251130
project name: projects/97252937750
project number: 97252937750
'''

import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

# 1. API 키 설정 (직접 입력하거나 환경변수 사용)
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=GOOGLE_API_KEY)

# 2. 모델 설정 (gemini-1.5-flash 또는 gemini-1.5-pro 사용 권장)
model = genai.GenerativeModel('gemini-2.0-flash')

def get_korean_answer(question):
    response = model.generate_content(question)
    translated_text = model.generate_content(f"{response.text} \n Translate this to Korean. Do not include any additional information other than the translation. Proper nouns and titles are all pronounced in Korean instead of translated.")
    return translated_text.text 


