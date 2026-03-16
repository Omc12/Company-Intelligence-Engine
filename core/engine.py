from core.model import get_model
from core.schema import CompanyIntelligence
from core.features import compute_features

from core.risk_chain import RiskChain
from core.business_chain import BusinessChain

from reasoning.router import SectionRouter
from reasoning.query_planner import QueryPlanner

from rag.retriever import retrieve_documents
from rag.reranker import rerank_documents

from data_ingestion.sec_indexer import build_or_load_indexes


def deduplicate_docs(docs):

    seen = set()
    unique = []

    for d in docs:
        text = d.page_content.strip()

        if text not in seen:
            seen.add(text)
            unique.append(d)

    return unique


def analyze_company(company_name, cik, query):

    print("\n=== ANALYZING COMPANY ===")

    router = SectionRouter()
    planner = QueryPlanner()

    route_scores = router.route(query)

    print("\n--- ROUTER ---")
    print(route_scores)

    sections = []

    for s, score in route_scores.items():
        if score > 0.5:
            sections.append(s)

    print("\nSections selected:", sections)

    subqueries = planner.plan(query)

    print("\n--- SUBQUERIES ---")
    print(subqueries)

    indexes = build_or_load_indexes(cik)

    risk_docs = []
    business_docs = []

    for q in subqueries:

        if "risk" in sections:
            r = indexes["risk"].as_retriever(search_kwargs={"k":15})
            risk_docs.extend(r.invoke(q))

        if "business" in sections:
            b = indexes["business"].as_retriever(search_kwargs={"k":15})
            business_docs.extend(b.invoke(q))

    risk_docs = deduplicate_docs(risk_docs)
    business_docs = deduplicate_docs(business_docs)

    risk_docs = rerank_documents(query, risk_docs, top_k=5)
    business_docs = rerank_documents(query, business_docs, top_k=5)

    risk_context = "\n\n".join([d.page_content for d in risk_docs])
    business_context = "\n\n".join([d.page_content for d in business_docs])

    risk_chain = RiskChain(get_model(temperature=0))
    business_chain = BusinessChain(get_model(temperature=0.15))

    risk_output = risk_chain.invoke(risk_context)
    business_output = business_chain.invoke(business_context)

    confidence = min(risk_output.confidence, business_output.confidence)

    summary = f"""
{company_name} operates with strengths such as {business_output.strengths[0]}.
It faces risks including {risk_output.risk_factors[0]}.
Overall outlook is {risk_output.outlook.value}.
"""

    result = CompanyIntelligence(
        summary=summary,
        strengths=business_output.strengths,
        weaknesses=business_output.weaknesses,
        competitive_advantage=business_output.competitive_advantage,
        risk_factors=risk_output.risk_factors,
        outlook=risk_output.outlook,
        confidence=confidence
    )

    features = compute_features(result)

    return result, features