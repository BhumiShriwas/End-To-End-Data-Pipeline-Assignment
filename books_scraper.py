import requests
from bs4 import BeautifulSoup
import time
import re

BASE_URL = "https://books.toscrape.com/"

def scrape_books(pages=10):
    all_books = []

    rating_map = {
        "One": 1,
        "Two": 2,
        "Three": 3,
        "Four": 4,
        "Five": 5
    }

    for page in range(1, pages + 1):
        print(f"Scraping page {page}")

        url = f"{BASE_URL}catalogue/page-{page}.html"
        response = requests.get(url)
        response.encoding = "utf-8"
        soup = BeautifulSoup(response.text, "html.parser")

        books = soup.find_all("article", class_="product_pod")

        for book in books:
            title = book.h3.a["title"]

            
            price_text = book.find("p", class_="price_color").text
            price_match = re.search(r"\d+\.\d+", price_text)
            price = float(price_match.group()) if price_match else None

            
            rating_text = book.p["class"][1]
            rating = rating_map.get(rating_text, None)

            
            availability = book.find(
                "p", class_="instock availability"
            ).text.strip()

            link = book.h3.a["href"]
            full_url = BASE_URL + "catalogue/" + link

            try:
                detail_response = requests.get(full_url)
                detail_response.encoding = "utf-8"
                detail_soup = BeautifulSoup(detail_response.text, "html.parser")

                category = (
                    detail_soup
                    .find("ul", class_="breadcrumb")
                    .find_all("li")[2]
                    .text
                    .strip()
                )
            except Exception:
                category = None

            all_books.append({
                "title": title,
                "price": price,
                "rating": rating,
                "availability": availability,
                "category": category,
                "book_url": full_url
            })

            time.sleep(0.5) 

        time.sleep(1)

    return all_books
