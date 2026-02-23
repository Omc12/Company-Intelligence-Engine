TASK_KEYWORDS = [
    "risk",
    "weakness",
    "competition",
    "strength",
    "partnership",
    "infrastructure",
    "safety",
    "regulatory"
]

def compute_precision_at_k(query, retrieved_docs, k=3):
    relevant_count = 0

    for doc in retrieved_docs[:k]:
        content = doc.page_content.lower()
        if any(keyword in content for keyword in TASK_KEYWORDS):
            relevant_count += 1

    return relevant_count / k