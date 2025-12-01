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

# API 키 설정
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=GOOGLE_API_KEY)

# 2. 모델 설정 (gemini-1.5-flash 또는 gemini-1.5-pro 사용 권장)
model = genai.GenerativeModel('gemini-2.0-flash')

# 3. 질문 보내기
response = model.generate_content("Marvel Comics Main Crossover event timeline sorted by time form 2004 to 2025.")

translated_text = model.generate_content(f"{response.text} \n Translate this to Korean.")

# 4. 답변 출력
print(translated_text.text)