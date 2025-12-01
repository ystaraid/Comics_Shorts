import csv
import json
import os

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

def convert_csv_to_json():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(base_dir, 'updated_detailed_books2.csv')
    json_path = os.path.join(base_dir, 'books.json')

    try:
        books = []
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for i, row in enumerate(reader):
                # Calculate page_per_cost
                ppc = calculate_ppc(row)
                
                # Create book object
                book = {
                    "index": i,
                    "title": row.get('title', 'Unknown Title'),
                    "original_title": row.get('original_title', ''),
                    "image_url": row.get('image_url', ''),
                    "stock_status": row.get('stock_status', 'Unknown'),
                    "page_per_cost": ppc,
                    # Include other fields if needed, matching the previous API response
                    "total": 0 # Will update later
                }
                books.append(book)

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
