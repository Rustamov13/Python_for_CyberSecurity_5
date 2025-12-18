import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

BASE_URL = "https://books.toscrape.com/"

def fetch_html(url):
    r = requests.get(url, timeout=20)
    r.raise_for_status()
    return r.text

def get_books_from_page(page_url):
    html = fetch_html(page_url)
    soup = BeautifulSoup(html, "html.parser")
    return soup.select("article.product_pod")

def extract_book_links(books, page_url):
    links = []
    for b in books:
        a = b.select_one("h3 a")
        if a and a.get("href"):
            links.append(urljoin(page_url, a["href"]))
    return links

def get_books_with_titles_and_links(page_url):
    html = fetch_html(page_url)
    soup = BeautifulSoup(html, "html.parser")

    items = []
    for pod in soup.select("article.product_pod"):
        a = pod.select_one("h3 a")
        if not a or not a.get("href"):
            continue
        title = a.get("title") or a.get_text(strip=True)
        link = urljoin(page_url, a["href"])
        items.append((title, link))
    return items

def parse_book_page(book_url):
    html = fetch_html(book_url)
    soup = BeautifulSoup(html, "html.parser")

    title_el = soup.select_one("div.product_main h1")
    price_el = soup.select_one("div.product_main p.price_color")
    availability_el = soup.select_one("div.product_main p.availability")
    desc_el = soup.select_one("#product_description + p")
    category_el = soup.select_one("ul.breadcrumb li:nth-of-type(3) a")
    img_el = soup.select_one("div.item.active img")

    rating_el = soup.select_one("div.product_main p.star-rating")
    rating = None
    if rating_el:
        classes = rating_el.get("class", [])
        rating = next((c for c in classes if c != "star-rating"), None)

    upc = None
    for row in soup.select("table.table.table-striped tr"):
        th = row.select_one("th")
        td = row.select_one("td")
        if th and td and th.get_text(strip=True) == "UPC":
            upc = td.get_text(strip=True)
            break

    result = {
        "url": book_url,
        "title": title_el.get_text(strip=True) if title_el else None,
        "price": price_el.get_text(strip=True) if price_el else None,
        "availability": availability_el.get_text(" ", strip=True) if availability_el else None,
        "description": desc_el.get_text(" ", strip=True) if desc_el else None,
        "category": category_el.get_text(strip=True) if category_el else None,
        "rating": rating,
        "upc": upc,
        "image_url": urljoin(book_url, img_el["src"]) if img_el and img_el.get("src") else None,
    }
    return result

def main():
    page_url = urljoin(BASE_URL, "catalogue/page-1.html")

    books = get_books_with_titles_and_links(page_url)
    links = [link for _, link in books]

    print("Page:", page_url)
    print("Books found:", len(books))
    print("\nBook titles and URLs:\n")

    for i, (title, link) in enumerate(books, 1):
        print(f"{i}. {title}")
        print(f"   {link}")

    if links:
        details = parse_book_page(links[0])
        print("\nParsed specific book:")
        for k, v in details.items():
            print(f"{k}: {v}")

if __name__ == "__main__":
    main()
