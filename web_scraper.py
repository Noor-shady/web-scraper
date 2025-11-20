import requests
from bs4 import BeautifulSoup
import pandas as pd
import json

# Headers help the scraper look like a real browser
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

def get_soup(url):
    """
    Fetches the URL and returns a BeautifulSoup object to parse HTML.
    """
    try:
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
        return BeautifulSoup(response.text, 'html.parser')
    except requests.exceptions.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return None


def scrape_books():
    """
    Scrapes book data from books.toscrape.com.
    """
    url = "http://books.toscrape.com/catalogue/category/books/science_22/index.html"
    print(f"Scraping {url}...")

    soup = get_soup(url)
    if not soup:
        return []

    books_data = []

    # Find all book containers (articles with class 'product_pod')
    products = soup.find_all('article', class_='product_pod')

    for product in products:
        # 1. Extract Title
        title = product.find('h3').find('a')['title']

        # 2. Extract Price
        price_text = product.find('p', class_='price_color').text
        # Remove currency symbol and convert to float
        price = float(price_text.replace('£', '').replace('$', ''))

        # 3. Extract Availability
        availability = product.find('p', class_='instock availability').text.strip()

        # Store in a dictionary
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
    """
    Saves the scraped data to CSV and JSON files.
    """
    if not data:
        print("No data found to save.")
        return

    # Convert to Pandas DataFrame for easy saving
    df = pd.DataFrame(data)

    # Save to CSV (Excel compatible)
    df.to_csv('scraped_products.csv', index=False)
    print(f"Saved {len(data)} items to 'scraped_products.csv'")

    # Save to JSON
    with open('scraped_products.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    print(f"Saved {len(data)} items to 'scraped_products.json'")

    # Simple comparison logic (Cheapest vs Most Expensive)
    print("\n--- Price Comparison ---")
    cheapest = df.loc[df['price'].idxmin()]
    expensive = df.loc[df['price'].idxmax()]

    print(f"Cheapest: '{cheapest['title']}' (£{cheapest['price']})")
    print(f"Most Expensive: '{expensive['title']}' (£{expensive['price']})")


if __name__ == "__main__":
    # Run the scraper
    scraped_data = scrape_books()
    save_data(scraped_data)