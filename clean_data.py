import pandas as pd
import re
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def clean_books_data(raw_books):
    df = pd.DataFrame(raw_books)

    # Clean price (remove any non-numeric chars)
    df["price"] = (
        df["price"]
        .astype(str)
        .str.replace(r"[^\d\.]", "", regex=True)
        .astype(float)
    )

    rating_map = {
        "One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5 
    }
    df["rating"] = df["rating"].map(rating_map)

    return df

def normalize_text(df):
    text_cols = ["title", "availability", "category"]

    for col in text_cols:
        df[col] = (
            df[col]
            .str.lower()
            .str.strip()
        )

    return df
def handle_missing(df):
    df["availability"].fillna("unknown", inplace=True)
    df["rating"].fillna(0, inplace=True)
    return df
def remove_duplicates(df):
    df.drop_duplicates(subset="url", inplace=True)
    return df
def add_price_bucket(df):
    df["price_category"] = pd.qcut(
        df["price"],
        q=3,
        labels=["low", "medium", "high"]
    )
    return df
def clean_books_pipeline(raw_books):
    df = clean_books_data(raw_books)
    df = normalize_text(df)
    df = handle_missing(df)
    df = remove_duplicates(df)
    df = add_price_bucket(df)
    return df
def clean_geo_data(raw_geo):
    df = pd.DataFrame(raw_geo)

    df["experiment_type"] = df["experiment_type"].str.lower().str.strip()
    df.fillna("unknown", inplace=True)

    df.drop_duplicates(subset="geo_id", inplace=True)

    return df
if __name__ == "__main__":
    from scraping.books_scraper import scrape_books

    raw_books = scrape_books()
    clean_df = clean_books_pipeline(raw_books)

    print("CLEANED DATA SAMPLE:")
    print(clean_df.head())

    print("\nDATA TYPES:")
    print(clean_df.dtypes)

    print("\nPRICE CATEGORY COUNT:")
    print(clean_df["price_category"].value_counts())
