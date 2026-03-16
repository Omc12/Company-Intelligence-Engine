def retrieve_documents(retriever, queries):

    docs = []

    for q in queries:
        docs.extend(retriever.invoke(q))

    return docs