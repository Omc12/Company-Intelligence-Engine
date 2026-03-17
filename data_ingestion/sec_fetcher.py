import requests
import re
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
            text = soup.get_text(separator="\n", strip=True)

            item_1_iter = list(re.finditer(r"(?i)\bITEM\s+1\b", text))
            item_1a_iter = list(re.finditer(r"(?i)\bITEM\s+1A\b", text))
            item_1b_iter = list(re.finditer(r"(?i)\bITEM\s+1B\b", text))
            item_2_iter = list(re.finditer(r"(?i)\bITEM\s+2\b", text))

            business_text = ""
            risk_text = ""

            # Extract Business (Item 1 to Item 1A) using max gap
            if item_1_iter and item_1a_iter:
                max_dist = 0
                best_1 = None
                best_1a = None
                for m1 in item_1_iter:
                    for m1a in item_1a_iter:
                        if m1a.start() > m1.end():
                            dist = m1a.start() - m1.end()
                            if dist > max_dist:
                                max_dist = dist
                                best_1 = m1
                                best_1a = m1a
                if best_1 and best_1a:
                    business_text = text[best_1.end():best_1a.start()]

            # Extract Risk (Item 1A to Item 1B or Item 2) using max gap
            end_iters = item_1b_iter + item_2_iter
            if item_1a_iter and end_iters:
                max_dist = 0
                best_1a = None
                best_end = None
                for m1a in item_1a_iter:
                    for mend in end_iters:
                        if mend.start() > m1a.end():
                            dist = mend.start() - m1a.end()
                            if dist > max_dist:
                                max_dist = dist
                                best_1a = m1a
                                best_end = mend
                if best_1a and best_end:
                    risk_text = text[best_1a.end():best_end.start()]

            if not risk_text:
                raise ValueError("Risk section anchor not found or extraction failed.")

            return business_text, risk_text

    raise ValueError("No 10-K found.")