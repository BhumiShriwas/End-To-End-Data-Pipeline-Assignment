import pandas as pd
import requests
from bs4 import BeautifulSoup
import time

def scrape_geo():
    df = pd.read_csv("data/database.csv")
    geo_ids = df.iloc[:, 0].tolist()

    all_geo_data = []

    for geo_id in geo_ids:
        print(f"Scraping {geo_id}")

        url = f"https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc={geo_id}"
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")

        try:
            experiment_type = soup.find(text="Experiment type").find_next("td").text
        except:
            experiment_type = None

        citations = [a.text for a in soup.find_all("a") if "pubmed" in a.get("href", "")]
        platforms = [a.text for a in soup.find_all("a") if a.text.startswith("GPL")]
        samples = [a.text for a in soup.find_all("a") if a.text.startswith("GSM")]

        all_geo_data.append({
            "geo_id": geo_id,
            "experiment_type": experiment_type,
            "citations": ", ".join(citations),
            "platforms": ", ".join(platforms),
            "samples": ", ".join(samples)
        })

        time.sleep(1)

    return all_geo_data
