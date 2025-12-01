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

chat = model.start_chat(history=[])

response1 = chat.send_message("안녕, 나는 코딩을 배우고 있어.")
print(response1.text)

# Gemini가 위 문맥을 기억하고 답변합니다.
response2 = chat.send_message("내가 방금 뭐라고 했지?")
print(response2.text)