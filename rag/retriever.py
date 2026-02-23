from rag.vector_store import build_vector_store

vector_store = build_vector_store()

def get_retriever():
    return vector_store.as_retriever(
        search_kwargs={"k":6}
    )