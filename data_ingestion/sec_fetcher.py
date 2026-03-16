# data_ingestion/sec_fetcher.py

import requests
from bs4 import BeautifulSoup


HEADERS = {
    "User-Agent": "Company Intelligence Engine (omchimurkar45@gmail.com)"
}


def fetch_latest_10k_sections(cik):
    url = f"https://data.sec.gov/submissions/CIK{cik}.json"
    print("Fetching submission JSON:", url)

    response = requests.get(url, headers=HEADERS)
    data = response.json()
    filings = data["filings"]["recent"]

    for i, form in enumerate(filings["form"]):
        if form == "10-K":
            accession = filings["accessionNumber"][i].replace("-", "")
            primary_doc = filings["primaryDocument"][i]

            filing_url = (
                f"https://www.sec.gov/Archives/edgar/data/"
                f"{int(cik)}/{accession}/{primary_doc}"
            )

            print("Fetching filing:", filing_url)

            filing_response = requests.get(filing_url, headers=HEADERS)
            html = filing_response.text

            soup = BeautifulSoup(html, "html.parser")

            # Extract business section
            business_anchor = soup.find(id=lambda x: x and "item_1" in x.lower())
            risk_anchor = soup.find(id=lambda x: x and "item_1a" in x.lower())

            if not risk_anchor:
                raise ValueError("Risk section anchor not found.")

            # Extract text starting from anchor
            business_text = ""
            risk_text = ""

            if business_anchor:
                business_text = business_anchor.find_parent().get_text(separator="\n")

            risk_text = risk_anchor.find_parent().get_text(separator="\n")

            return business_text, risk_text

    raise ValueError("No 10-K found.")