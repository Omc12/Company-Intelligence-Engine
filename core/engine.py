# core/engine.py

from core.model import get_model
from core.schema import CompanyIntelligence
from core.features import compute_features

from core.risk_chain import RiskChain
from core.business_chain import BusinessChain

from reasoning.query_planner import QueryPlanner

from data_ingestion.sec_indexer import build_or_load_indexes
from rag.reranker import rerank_documents


def analyze_company(company_name: str, cik: str, user_query: str):

    print("\n=== ANALYZING COMPANY ===\n")

    # --------------------------------------------------
    # MODELS
    # --------------------------------------------------

    risk_model = get_model(temperature=0.0)
    business_model = get_model(temperature=0.15)

    risk_chain = RiskChain(risk_model)
    business_chain = BusinessChain(business_model)

    # --------------------------------------------------
    # QUERY PLANNING
    # --------------------------------------------------

    planner = QueryPlanner()

    subqueries = planner.plan(user_query)

    print("\n--- SUBQUERIES ---\n")
    for q in subqueries:
        print("-", q)

    # --------------------------------------------------
    # LOAD INDEXES
    # --------------------------------------------------

    indexes = build_or_load_indexes(cik)

    risk_retriever = indexes["risk"].as_retriever(search_kwargs={"k": 5})
    business_retriever = indexes["business"].as_retriever(search_kwargs={"k": 5})

    # --------------------------------------------------
    # RETRIEVE DOCUMENTS
    # --------------------------------------------------

    risk_docs = []
    business_docs = []

    for q in subqueries:

        r_docs = risk_retriever.invoke(q)
        b_docs = business_retriever.invoke(q)

        risk_docs.extend(r_docs)
        business_docs.extend(b_docs)

    def deduplicate_docs(docs):
        seen = set()
        unique = []

        for d in docs:
            content = d.page_content.strip()
            if content not in seen:
                seen.add(content)
                unique.append(d)

        return unique
    
    risk_docs = deduplicate_docs(risk_docs)
    business_docs = deduplicate_docs(business_docs)

    # --------------------------------------------------
    # RERANK
    # --------------------------------------------------

    risk_docs = rerank_documents(user_query, risk_docs, top_k=5)
    business_docs = rerank_documents(user_query, business_docs, top_k=5)

    # --------------------------------------------------
    # CONTEXT BUILDING
    # --------------------------------------------------

    risk_context = "\n\n".join([doc.page_content for doc in risk_docs])
    business_context = "\n\n".join([doc.page_content for doc in business_docs])

    print("\n--- RISK CONTEXT ---\n")
    print(risk_context[:1200])

    print("\n--- BUSINESS CONTEXT ---\n")
    print(business_context[:1200])

    # --------------------------------------------------
    # RUN CHAINS
    # --------------------------------------------------

    risk_output = risk_chain.invoke(risk_context)
    business_output = business_chain.invoke(business_context)

    print("\nRisk factors:", risk_output.risk_factors)
    print("Strengths:", business_output.strengths)

    # --------------------------------------------------
    # CONFIDENCE MERGE
    # --------------------------------------------------

    confidence = min(risk_output.confidence, business_output.confidence)

    # --------------------------------------------------
    # DETERMINISTIC SUMMARY
    # --------------------------------------------------

    first_strength = (
        business_output.strengths[0]
        if business_output.strengths
        else "diverse capabilities"
    )

    first_risk = (
        risk_output.risk_factors[0]
        if risk_output.risk_factors
        else "market uncertainties"
    )

    summary = (
        f"{company_name} operates with strengths such as {first_strength}. "
        f"It faces risks including {first_risk}. "
        f"Overall outlook is {risk_output.outlook.value}."
    )

    # --------------------------------------------------
    # FINAL OBJECT
    # --------------------------------------------------

    final_output = CompanyIntelligence(
        summary=summary,
        strengths=business_output.strengths,
        weaknesses=business_output.weaknesses,
        competitive_advantage=business_output.competitive_advantage,
        risk_factors=risk_output.risk_factors,
        outlook=risk_output.outlook,
        confidence=confidence
    )

    # --------------------------------------------------
    # FEATURE ENGINEERING
    # --------------------------------------------------

    features = compute_features(final_output)

    return final_output, features