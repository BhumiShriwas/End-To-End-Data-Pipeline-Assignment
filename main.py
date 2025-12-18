import os
from scraping.books_scraper import scrape_books
from scraping.geo_scraper import scrape_geo
from cleaning.clean_data import clean_books_data

def run_pipeline():
    print("Starting pipeline...")

    books = scrape_books(pages=10)
    geo_data = scrape_geo()

    print("Books scraped:", len(books))
    print("GEO records scraped:", len(geo_data))

    books_clean = clean_books_data(books)

    os.makedirs("data", exist_ok=True)
    books_clean.to_csv("data/books_output.csv", index=False)

    print("Cleaned data saved to data/books_output.csv")
    print("Data prepared for MySQL storage")

if __name__ == "__main__":
    run_pipeline()

