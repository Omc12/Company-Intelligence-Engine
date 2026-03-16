from sentence_transformers import CrossEncoder
import torch

device = "cuda" if torch.cuda.is_available() else "cpu"

reranker = CrossEncoder(
    "cross-encoder/ms-marco-MiniLM-L-6-v2",
    device=device
)

def rerank_documents(query, docs, top_k=5):

    pairs = [(query, d.page_content) for d in docs]

    scores = reranker.predict(pairs)

    scored = list(zip(docs, scores))

    ranked = sorted(scored, key=lambda x: x[1], reverse=True)

    return [d for d, _ in ranked[:top_k]]