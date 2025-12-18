# Python_for_CyberSecurity_5
# Books to Scrape — Web Scraper (Python)

A simple Python web scraping script that retrieves book listings from **https://books.toscrape.com/**, extracts **book titles and absolute URLs**, and parses the page of a **specific book** to collect detailed information.

This project is intended for educational purposes and demonstrates basic HTML fetching and parsing using `requests` and `BeautifulSoup`.

---

## Features

- Retrieve an HTML page from `books.toscrape.com`
- Get the list of books displayed on a catalog page
- Extract each book’s **title** and convert the **relative link** into an **absolute URL**
- Parse a specific book page and extract:
  - Title
  - Price
  - Availability
  - Category
  - Rating (star-rating class)
  - UPC
  - Description (if available)
  - Image URL (absolute)

---

## Requirements

- Python 3.8+
- `requests`
- `beautifulsoup4`

Install dependencies:

```bash
pip install requests beautifulsoup4
