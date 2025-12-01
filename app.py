from flask import Flask, jsonify, request, send_from_directory
import pandas as pd
import google.generativeai as genai
import os
import random
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
base_dir = os.path.dirname(os.path.abspath(__file__))

# Configuration
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-2.0-flash')

# Load Data
try:
    csv_path = os.path.join(base_dir, 'updated_detailed_books2.csv')
    df = pd.read_csv(csv_path)
    # Fill NaN with empty strings to avoid JSON errors
    df = df.fillna('')
    
    # Calculate page_per_cost
    def calculate_ppc(row):
        try:
            price = float(str(row['price']).replace(',', ''))
            page = float(str(row['page']).replace(',', ''))
            if price > 0:
                return (page / price) * 100 # Percentage as requested
            return 0
        except:
            return 0

    df['page_per_cost'] = df.apply(calculate_ppc, axis=1)
    
    books = df.to_dict('records')
    print(f"Loaded {len(books)} books.")
except Exception as e:
    print(f"Error loading CSV: {e}")
    books = []

@app.route('/')
def index():
    return send_from_directory(base_dir, 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory(base_dir, path)

@app.route('/api/book/<int:index>')
def get_book(index):
    if not books:
        return jsonify({"error": "No data loaded"}), 500
    
    # Ensure index wraps around
    safe_index = index % len(books)
    book = books[safe_index]
    
    return jsonify({
        "index": safe_index,
        "total": len(books),
        "title": book.get('title', 'Unknown Title'),
        "original_title": book.get('original_title', ''),
        "image_url": book.get('image_url', ''),
        "stock_status": book.get('stock_status', 'Unknown'),
        "page_per_cost": book.get('page_per_cost', 0)
    })

@app.route('/api/explain')
def explain_book():
    original_title = request.args.get('original_title')
    title = request.args.get('title')
    stock_status = request.args.get('stock_status', 'Unknown')
    page_per_cost = request.args.get('page_per_cost', '0')
    
    if not original_title and not title:
        return jsonify({"description": "정보가 부족하여 설명을 생성할 수 없습니다."})

    query_title = original_title if original_title else title
    
    prompt = f"""
    Explain the comic book '{query_title}' briefly in Korean.
    The current stock status is: {stock_status}.
    The page per cost value is: {page_per_cost} (higher means better value).
    
    - Do NOT include spoilers.
    - Focus on the premise and mood.
    - Keep it under 5 sentences.
    - It is important to know what weight the story holds within a certain worldview.
    - Don't raise expectations too much.
    - Explain the causal relationship between the circumstances within the given worldview
    - Using polite language
    - Do NOT mention that you are an AI.
    - Reflecting on people's evaluations of this book, I analyze and comment on whether it is worth reading objectively.
    - Talk about the pros and cons with an eye toward evaluation.
    - If stock_status is 'out of stock', mention it regretfully. If 'in stock', mention it is available.
    - If page_per_cost is high (e.g., > 1.0), mention it is a "hyeoja" (good value) item. If low, mention it might be pricey but worth it if the content is good.
    """
    
    try:
        response = model.generate_content(prompt)
        return jsonify({"description": response.text})
    except Exception as e:
        print(f"AI Error: {e}")
        return jsonify({"description": "AI 통신 중 오류가 발생했습니다."})

if __name__ == '__main__':
    app.run(debug=True, port=8000)
