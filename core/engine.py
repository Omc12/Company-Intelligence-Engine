from core.model import get_model
from core.parser import get_base_parser
from core.prompt import get_prompt
from core.features import compute_features

from data_ingestion.sec_indexer import build_or_load_index
from rag.reranker import rerank_documents


# Initialize once
model = get_model()
base_parser = get_base_parser()
format_instructions = base_parser.get_format_instructions()
prompt = get_prompt(format_instructions)

chain = prompt | model | base_parser


def analyze_company(company_name: str, cik: str):
    # 1️⃣ Build or load persistent index
    vector_store = build_or_load_index(cik)

    # 2️⃣ Create retriever dynamically
    retriever = vector_store.as_retriever(search_kwargs={"k": 6})

    retrieval_query = (
        f"Analyze the key risks, weaknesses, strengths "
        f"and competitive position of {company_name}"
    )

    # 3️⃣ Retrieve
    docs = retriever.invoke(retrieval_query)

    # 4️⃣ Rerank
    docs = rerank_documents(retrieval_query, docs, top_k=3)

    print("\n--- Final Retrieved Chunks After Reranking ---\n")
    for i, doc in enumerate(docs, 1):
        print(f"\nChunk {i}:\n{doc.page_content[:500]}\n")

    # 5️⃣ Build context
    context = "\n\n".join([doc.page_content for doc in docs])

    # 6️⃣ Run structured chain
    intel = chain.invoke({
        "company_name": company_name,
        "context": context
    })

    # 7️⃣ Deterministic features
    features = compute_features(intel)

    return intel, features