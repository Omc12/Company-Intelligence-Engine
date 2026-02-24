import os 
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter

from rag.embeddings import get_embeddings
from data_ingestion.sec_fetcher import fetch_latest_10k_html, extract_item_1a

BASE_INDEX_PATH = "indexes"

def build_or_load_index(cik):
    os.makedirs(BASE_INDEX_PATH, exist_ok=True)
    index_path = os.path.join(BASE_INDEX_PATH, cik)

    embeddings = get_embeddings()

    if os.path.exists(index_path):
        return FAISS.load_local(index_path, embeddings, allow_dangerous_deserialization=True)
    
    html = fetch_latest_10k_html(cik)
    risk_text = extract_item_1a(html)

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=100
    )

    docs = splitter.create_documents([risk_text])

    vector_store = FAISS.from_documents(docs, embeddings)

    vector_store.save_local(index_path)

    return vector_store