# data_ingestion/sec_fetcher.py

import requests
from bs4 import BeautifulSoup


HEADERS = {
    "User-Agent": "Company Intelligence Engine (your_email@example.com)"
}


def fetch_latest_10k_html(cik):
    url = f"https://data.sec.gov/submissions/CIK{cik}.json"
    response = requests.get(url, headers=HEADERS)
    data = response.json()

    filings = data["filings"]["recent"]

    for i, form in enumerate(filings["form"]):
        if form == "10-K":
            accession = filings["accessionNumber"][i].replace("-", "")
            primary_doc = filings["primaryDocument"][i]

            filing_url = (
                f"https://www.sec.gov/Archives/edgar/data/{int(cik)}/"
                f"{accession}/{primary_doc}"
            )

            filing_response = requests.get(filing_url, headers=HEADERS)
            return filing_response.text

    raise ValueError("No 10-K found.")

def extract_item_1a(html_text):
    soup = BeautifulSoup(html_text, "lxml")
    text = soup.get_text(separator="\n")

    lower_text = text.lower()

    occurrences = []
    idx = 0

    while True:
        idx = lower_text.find("item 1a", idx)
        if idx == -1:
            break
        occurrences.append(idx)
        idx += 1

    if len(occurrences) < 2:
        raise ValueError("Could not find full Item 1A section.")

    # Use second occurrence (skip TOC)
    start = occurrences[1]

    end = lower_text.find("item 1b", start)

    if end == -1:
        end = start + 200000  # fallback large slice

    return text[start:end]