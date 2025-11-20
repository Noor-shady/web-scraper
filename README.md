#  Books to Scrape - Science Category Scraper

A Python automation tool that scrapes book data from the **Science** category of *Books to Scrape*, analyzes the prices, and saves the results to your computer.

> **Target URL:** [http://books.toscrape.com/catalogue/category/books/science_22/index.html](http://books.toscrape.com/catalogue/category/books/science_22/index.html)

---

##  Table of Contents

1. [Project Overview](#-project-overview)
2. [Project Structure & Files](#-project-structure--files)
3. [Installation Guide](#-installation-guide)
4. [How to Run](#-how-to-run)
5. [Output Explanation](#-output-explanation)

---

## Project Overview

This project is a web scraper designed for the "Books to Scrape" sandbox. When executed, the script will:
1.  **Auto-open the website** in your browser so you can see what is being scraped.
2.  Fetch the HTML data using `requests`.
3.  Parse book titles, prices, and stock status using `BeautifulSoup`.
4.  Clean the price data (removing currency symbols like `£` to avoid errors).
5.  Export the data to **CSV** (Excel) and **JSON**.

---

# Web Scraper Project

## Project Structure & Files

Your project folder should contain these files:

### 1. `requirements.txt`
This file tells Python which libraries to install:

```text
requests
beautifulsoup4
pandas
```

### 2. `web_scraper.py`
This is the main engine. Make sure all the Python scraping code is inside this file.

### 3. `README.md`
This documentation file.

---

##  Installation Guide

Follow these steps to get the project running in PyCharm.

### Step 1: Create the Files
Make sure you have created:

- `web_scraper.py`
- `requirements.txt`

### Step 2: Install Dependencies
Open the terminal in PyCharm and run:

```bash
pip install -r requirements.txt
```

If that doesn’t work, try:

```bash
pip3 install -r requirements.txt
```

---

##  How to Run

Open `web_scraper.py` in PyCharm, right-click anywhere, and choose:

**Run 'web_scraper'**

Or run it through the terminal:

```bash
python web_scraper.py
```

### What will happen?

- The scraper will fetch data from Books To Scrape.
- You will see messages like:

```
Scraping http://books.toscrape.com/...
Saved 14 items to 'scraped_products.csv'
Saved 14 items to 'scraped_products.json'
```

- The console will also print:
  - Cheapest book  
  - Most expensive book

---

##  Output Explanation

Two new files will appear in your project folder:

| File Name                | Format      | Description |
|--------------------------|-------------|-------------|
| `scraped_products.csv`   | Spreadsheet | Open with Excel, Google Sheets, or PyCharm table viewer |
| `scraped_products.json`  | JSON        | Good for developers, APIs, or database imports |

---
