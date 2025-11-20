import requests
from bs4 import BeautifulSoup
import pandas as pd
import json
import re
import webbrowser

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}


def get_soup(url):
    try:
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
        response.encoding = 'utf-8'  # Fix encoding for currency symbols
        return BeautifulSoup(response.text, 'html.parser')
    except requests.exceptions.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return None


def scrape_books():
    url = "http://books.toscrape.com/catalogue/category/books/science_22/index.html"
    print(f"Scraping {url}...")
    print("Opening page in browser...")

    webbrowser.open(url)

    soup = get_soup(url)
    if not soup:
        return []

    books_data = []
    products = soup.find_all('article', class_='product_pod')

    for product in products:
        title = product.find('h3').find('a')['title']
        price_text = product.find('p', class_='price_color').text

        # Extract number only using Regex
        price_match = re.search(r"\d+\.\d+", price_text)
        price = float(price_match.group()) if price_match else 0.0

        availability = product.find('p', class_='instock availability').text.strip()

        books_data.append({
            'title': title,
            'price': price,
            'currency': 'GBP',
            'availability': availability,
            'source': 'BooksToScrape'
        })

    return books_data


def save_data(data):
    if not data:
        print("No data found.")
        return

    df = pd.DataFrame(data)
    df.to_csv('scraped_products.csv', index=False)
    print(f"Saved {len(data)} items to 'scraped_products.csv'")

    with open('scraped_products.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    print(f"Saved {len(data)} items to 'scraped_products.json'")

    print("\n--- Price Comparison ---")
    if not df.empty:
        cheapest = df.loc[df['price'].idxmin()]
        expensive = df.loc[df['price'].idxmax()]

        print(f"Cheapest: '{cheapest['title']}' (£{cheapest['price']})")
        print(f"Most Expensive: '{expensive['title']}' (£{expensive['price']})")


if __name__ == "__main__":
    data = scrape_books()
    save_data(data)