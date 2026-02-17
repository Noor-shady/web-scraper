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