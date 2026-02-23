from core.model import get_model
from core.parser import get_base_parser
from core.prompt import get_prompt
from core.features import compute_features

from rag.retriever import get_retriever

model = get_model()
base_parser = get_base_parser()
format_instructions = base_parser.get_format_instructions()
prompt = get_prompt(format_instructions)

retriever = get_retriever()

chain = prompt | model | base_parser

from rag.reranker import rerank_documents

def analyze_company(company_name: str):
    retrieval_query = f"Analyze the risks, weaknesses, strengths and competitive position of {company_name}"

    docs = retriever.invoke(retrieval_query)
    docs = rerank_documents(retrieval_query, docs, top_k=3)

    print("\n--- Final Retrieved Chunks After Reranking ---\n")
    for i, doc in enumerate(docs, 1):
        print(f"\nChunk {i}:\n{doc.page_content}\n")

    context = "\n\n".join([doc.page_content for doc in docs])

    intel = chain.invoke({
        "company_name": company_name,
        "context": context
    })

    features = compute_features(intel)
    return intel, features, docs