import os
from langchain_postgres import PGVector
from langchain_text_splitters import RecursiveCharacterTextSplitter

from rag.embeddings import get_embeddings
from data_ingestion.sec_fetcher import fetch_latest_10k_sections

def get_supabase_vectorstore(cik, section):
    uri = os.getenv("SUPABASE_URI")
    vectorstore = PGVector(
        embeddings=get_embeddings(),
        collection_name=f"cik_{cik}_{section}",
        connection=uri,
        use_jsonb=True,
    )
    return vectorstore

def check_index_exists(cik, section):
    vectorstore = get_supabase_vectorstore(cik, section)
    try:
        results = vectorstore.similarity_search("test", k=1)
        return len(results) > 0
    except Exception:
        return False

def build_or_load_indexes(cik, status_callback=None):
    """
    Checks if Supabase already has embeddings for this CIK.
    If not, fetches the 10-K, splits it, and pushes it to Supabase.
    Returns a dictionary of ready-to-use vectorstores.
    """
    risk_exists = check_index_exists(cik, "risk")
    business_exists = check_index_exists(cik, "business")
    
    risk_store = get_supabase_vectorstore(cik, "risk")
    business_store = get_supabase_vectorstore(cik, "business")

    if risk_exists and business_exists:
        if status_callback:
            status_callback(f"Found existing Intelligence Indexes in Supabase Cloud for {cik}.")
        return {
            "risk": risk_store,
            "business": business_store
        }

    if status_callback:
        status_callback(f"No existing cloud index found. Fetching live 10-K filing for {cik}...")
        
    business_text, risk_text = fetch_latest_10k_sections(cik)

    if status_callback:
        status_callback("Chunking SEC document into semantic blocks...")
        
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=150
    )

    business_docs = splitter.create_documents([business_text])
    risk_docs = splitter.create_documents([risk_text])

    if status_callback:
        status_callback(f"Upserting {len(business_docs) + len(risk_docs)} chunks into Supabase pgvector...")

    # We use add_documents to push to the existing configured vector store instances
    business_store.add_documents(business_docs)
    risk_store.add_documents(risk_docs)

    if status_callback:
        status_callback(f"Successfully committed {len(business_docs) + len(risk_docs)} Intelligence chunks to Supabase Cloud.")

    return {
        "risk": risk_store,
        "business": business_store
    }
