# data_ingestion/sec_indexer.py

import os
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter

from rag.embeddings import get_embeddings
from data_ingestion.sec_fetcher import fetch_latest_10k_sections


BASE_INDEX_PATH = "indexes"


def build_or_load_indexes(cik):
    base_path = os.path.join(BASE_INDEX_PATH, cik)
    risk_path = os.path.join(base_path, "risk")
    business_path = os.path.join(base_path, "business")

    os.makedirs(base_path, exist_ok=True)

    embeddings = get_embeddings()

    if os.path.exists(risk_path) and os.path.exists(business_path):
        return {
            "risk": FAISS.load_local(risk_path, embeddings, allow_dangerous_deserialization=True),
            "business": FAISS.load_local(business_path, embeddings, allow_dangerous_deserialization=True)
        }

    business_text, risk_text = fetch_latest_10k_sections(cik)

    print("\n--- BUSINESS PREVIEW ---\n")
    print(business_text[:1000])

    print("\n--- RISK PREVIEW ---\n")
    print(risk_text[:1000])

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=150
    )

    business_docs = splitter.create_documents([business_text])
    risk_docs = splitter.create_documents([risk_text])

    business_store = FAISS.from_documents(business_docs, embeddings)
    risk_store = FAISS.from_documents(risk_docs, embeddings)

    business_store.save_local(business_path)
    risk_store.save_local(risk_path)

    return {
        "risk": risk_store,
        "business": business_store
    }