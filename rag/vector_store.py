from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter

from rag.embeddings import get_embeddings
from rag.knowledge_base import COMPANY_DOCS

def build_vector_store():
    embeddings = get_embeddings()

    text = list(COMPANY_DOCS.values())

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=100,
        chunk_overlap=20
    )

    chunks = splitter.create_documents(text)

    vector_store = FAISS.from_documents(
        chunks,
        embeddings
    )

    return vector_store