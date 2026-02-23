import re
from core.model import get_model

model = get_model()

def rerank_documents(query, docs, top_k=3):
    prompt = f"""
You are ranking document relevance.

Query:
{query}

Rank the following documents from most relevant to least relevant.
Return only the indices in order, separated by commas.
Example: 0,2,1
Do not write anything else.

Documents:
"""

    for i, doc in enumerate(docs):
        prompt += f"\nDocument {i}:\n{doc.page_content}\n"

    response = model.invoke(prompt).content

    print("\n--- Reranker Raw Response ---")
    print(response)

    # Extract all integers from response
    indices = list(map(int, re.findall(r'\d+', response)))

    # Ensure valid range
    indices = [i for i in indices if 0 <= i < len(docs)]

    if not indices:
        # fallback: return first top_k
        return docs[:top_k]

    return [docs[i] for i in indices[:top_k]]