import csv
import json
import os
import time
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

if not GOOGLE_API_KEY:
    print("Warning: GOOGLE_API_KEY not found in .env file. AI explanations will be skipped.")
else:
    genai.configure(api_key=GOOGLE_API_KEY)

def calculate_ppc(row):
    try:
        price_str = row.get('price', '0').replace(',', '')
        page_str = row.get('page', '0').replace(',', '')
        
        price = float(price_str) if price_str else 0
        page = float(page_str) if page_str else 0
        
        if price > 0:
            return (page / price) * 100 # Percentage as requested
        return 0
    except:
        return 0

def generate_explanation(model, title, original_title, stock_status, page_per_cost):
    if not model:
        return "AI explanation not available (API Key missing)."
        
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
        return response.text.strip()
    except Exception as e:
        print(f"Error generating explanation for {title}: {e}")
        return "설명을 불러오는 중 오류가 발생했습니다."

def convert_csv_to_json():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(base_dir, 'updated_detailed_books2.csv')
    json_path = os.path.join(base_dir, 'books.json')

    # Initialize model
    model = None
    if GOOGLE_API_KEY:
        try:
            model = genai.GenerativeModel('gemini-2.0-flash')
        except Exception as e:
            print(f"Error initializing model: {e}")

    try:
        books = []
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            rows = list(reader)
            total_rows = len(rows)
            
            print(f"Found {total_rows} books. Starting conversion and AI generation...")
            
            for i, row in enumerate(rows):
                # Calculate page_per_cost
                ppc = calculate_ppc(row)
                
                title = row.get('title', 'Unknown Title')
                original_title = row.get('original_title', '')
                stock_status = row.get('stock_status', 'Unknown')
                
                # Generate Explanation
                print(f"[{i+1}/{total_rows}] Processing: {title}")
                explanation = generate_explanation(model, title, original_title, stock_status, ppc)
                
                # Create book object
                book = {
                    "index": i,
                    "title": title,
                    "original_title": original_title,
                    "image_url": row.get('image_url', ''),
                    "stock_status": stock_status,
                    "page_per_cost": ppc,
                    "explanation": explanation,
                    "total": 0 # Will update later
                }
                books.append(book)
                
                # Rate limiting to be safe (though Flash is fast)
                # time.sleep(0.5) 

        # Update total count
        total_books = len(books)
        for book in books:
            book['total'] = total_books

        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(books, f, ensure_ascii=False, indent=4)
            
        print(f"Successfully converted {len(books)} books to {json_path}")
        
    except Exception as e:
        print(f"Error converting data: {e}")

if __name__ == "__main__":
    convert_csv_to_json()
