def precision_at_k(relevant, retrieved, k=5):

    retrieved=retrieved[:k]

    hits=sum(1 for d in retrieved if d in relevant)

    return hits/k