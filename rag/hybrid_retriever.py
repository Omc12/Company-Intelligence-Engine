from rank_bm25 import BM25Okapi

def hybrid_retrieve(vector_retriever, docs, queries):

    corpus=[d.page_content.split() for d in docs]

    bm25=BM25Okapi(corpus)

    results=[]

    for q in queries:

        vec_docs=vector_retriever.invoke(q)

        tokenized=q.split()

        bm25_scores=bm25.get_scores(tokenized)

        bm_docs=[docs[i] for i in sorted(range(len(bm25_scores)), key=lambda x: bm25_scores[x], reverse=True)[:10]]

        results.extend(vec_docs)
        results.extend(bm_docs)

    return results