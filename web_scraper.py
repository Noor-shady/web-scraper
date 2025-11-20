import requests
from bs4 import BeautifulSoup
import pandas as pd
import json
# Imported regex to handle messy price strings
import re

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}


def get_soup(url):
    try:
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()

        # Force UTF-8 encoding to handle currency symbols like £ correctly
        response.encoding = 'utf-8'

        return BeautifulSoup(response.text, 'html.parser')
    except requests.exceptions.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return None


def scrape_books():
    url = "http://books.toscrape.com/catalogue/category/books/science_22/index.html"
    print(f"Scraping {url}...")

    soup = get_soup(url)
    if not soup:
        return []

    books_data = []
    products = soup.find_all('article', class_='product_pod')

    for product in products:
        title = product.find('h3').find('a')['title']
        price_text = product.find('p', class_='price_color').text

        # I Used Regex to extract ONLY the numbers (e.g., "51.77")
        price_match = re.search(r"\d+\.\d+", price_text)

        if price_match:
            price = float(price_match.group())
        else:
            price = 0.0

        availability = product.find('p', class_='instock availability').text.strip()

        book_info = {
            'title': title,
            'price': price,
            'currency': 'GBP',
            'availability': availability,
            'source': 'BooksToScrape'
        }
        books_data.append(book_info)

    return books_data


def save_data(data):
    if not data:
        print("No data found to save.")
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
    scraped_data = scrape_books()
    save_data(scraped_data)