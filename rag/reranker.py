from sentence_transformers import CrossEncoder
import torch

device = "cuda" if torch.cuda.is_available() else "cpu"
_reranker = None

def rerank_documents(query,docs,top_k=5):

    if not docs:
        return []

    global _reranker

    if _reranker is None:
        try:
            _reranker = CrossEncoder(
                "cross-encoder/ms-marco-MiniLM-L-6-v2",
                device=device
            )
        except Exception as e:
            print(f"[reranker] Falling back to original retrieval order: {e}")
            return docs[:top_k]

    pairs=[(query,d.page_content) for d in docs]

    try:
        scores=_reranker.predict(pairs)
    except Exception as e:
        print(f"[reranker] Prediction failed, using original retrieval order: {e}")
        return docs[:top_k]

    ranked=sorted(zip(docs,scores), key=lambda x:x[1], reverse=True)

    return [d for d,_ in ranked[:top_k]]