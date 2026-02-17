import logging
import json
import re
from typing import List, Dict, Optional

import requests
import pandas as pd
from bs4 import BeautifulSoup

# Configure professional logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class BookScraper:
    """A professional web scraper for extracting book data from BooksToScrape."""

    BASE_URL = "http://books.toscrape.com/catalogue/category/books/science_22/index.html"
    HEADERS = {
        'User-Agent': (
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
            'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        )
    }

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update(self.HEADERS)

    def fetch_soup(self, url: str) -> Optional[BeautifulSoup]:
        """Fetches HTML content and returns a BeautifulSoup object."""
        try:
            logger.info(f"Fetching URL: {url}")
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            # Fix encoding for currency symbols
            response.encoding = 'utf-8'
            return BeautifulSoup(response.text, 'html.parser')
        except requests.RequestException as e:
            logger.error(f"Failed to fetch {url}: {e}")
            return None

    def scrape_books(self) -> List[Dict[str, any]]:
        soup = self.fetch_soup(self.BASE_URL)
        if not soup:
            return []

        books_data = []
        products = soup.select('article.product_pod')

        for product in products:
            try:
                title = product.h3.a.get('title', 'Unknown Title')
                price_text = product.select_one('p.price_color').text

                # Extract number only using Regex
                price_match = re.search(r"(\d+\.\d+)", price_text)
                price = float(price_match.group(1)) if price_match else 0.0

                availability_node = product.select_one('.instock.availability')
                availability = availability_node.get_text(strip=True) if availability_node else "Unknown"

                books_data.append({
                    'title': title,
                    'price': price,
                    'currency': 'GBP',
                    'availability': availability,
                    'source': 'BooksToScrape'
                })
            except (AttributeError, TypeError) as e:
                logger.warning(f"Skipping a product due to parsing error: {e}")
                continue

        logger.info(f"Successfully parsed {len(books_data)} books.")
        return books_data

    @staticmethod
    def save_data(data: List[Dict[str, any]], csv_path: str = 'scraped_products.csv', json_path: str = 'scraped_products.json') -> None:
        """Saves scraped data to CSV/JSON and outputs a statistical summary."""
        if not data:
            logger.warning("No data found to save.")
            return

        df = pd.DataFrame(data)

        try:
            # Save to CSV
            df.to_csv(csv_path, index=False)
            logger.info(f"Saved {len(data)} items to '{csv_path}'")

            # Save to JSON
            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
            logger.info(f"Saved {len(data)} items to '{json_path}'")

            # Output Price Comparison
            logger.info("--- Price Comparison Summary ---")
            cheapest = df.loc[df['price'].idxmin()]
            expensive = df.loc[df['price'].idxmax()]

            logger.info(f"Cheapest: '{cheapest['title']}' (£{cheapest['price']})")
            logger.info(f"Most Expensive: '{expensive['title']}' (£{expensive['price']})")

        except IOError as e:
            logger.error(f"Failed to save data to disk: {e}")


if __name__ == "__main__":
    scraper = BookScraper()
    scraped_data = scraper.scrape_books()
    scraper.save_data(scraped_data)