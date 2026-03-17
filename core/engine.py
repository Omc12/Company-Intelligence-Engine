from core.model import get_model
from core.schema import CompanyIntelligence
from core.features import compute_features

from core.risk_chain import RiskChain
from core.business_chain import BusinessChain

from reasoning.router import SectionRouter
from reasoning.query_planner import QueryPlanner

from rag.reranker import rerank_documents
from rag.hybrid_retriever import hybrid_retrieve

from data_ingestion.sec_indexer import build_or_load_indexes


def deduplicate(docs):

    seen=set()
    unique=[]

    for d in docs:
        t=d.page_content.strip()
        if t not in seen:
            seen.add(t)
            unique.append(d)

    return unique


def analyze_company(company, cik, query, status_callback=None):

    def log_status(msg):
        if status_callback:
            status_callback(msg)

    log_status("Initializing query router and planner...")
    router = SectionRouter()
    planner = QueryPlanner()

    sections = router.route(query)
    subqueries = planner.plan(query)

    log_status(f"Loading SEC EDGAR 10-K indexes for {company}...")
    indexes = build_or_load_indexes(cik)

    risk_docs = []
    business_docs = []

    log_status("Executing semantic retrieval across filings...")
    if sections["risk"] > 0.5:
        r = indexes["risk"].as_retriever(search_kwargs={"k": 15})
        for q in subqueries:
            risk_docs.extend(r.invoke(q))

    if sections["business"] > 0.5:
        b = indexes["business"].as_retriever(search_kwargs={"k": 15})
        for q in subqueries:
            business_docs.extend(b.invoke(q))

    log_status("Deduplicating retrieved fragments...")
    risk_docs = deduplicate(risk_docs)
    business_docs = deduplicate(business_docs)

    log_status("Re-ranking context for maximum relevance...")
    risk_docs = rerank_documents(query, risk_docs)
    business_docs = rerank_documents(query, business_docs)

    risk_context = "\n\n".join([d.page_content for d in risk_docs])
    business_context = "\n\n".join([d.page_content for d in business_docs])

    risk_chain = RiskChain(get_model())
    business_chain = BusinessChain(get_model(temperature=0.15))

    log_status("Synthesizing corporate risk factors...")
    risk = risk_chain.invoke(risk_context)
    
    log_status("Extracting business intelligence and competitive moats...")
    business = business_chain.invoke(business_context)

    confidence = min(risk.confidence, business.confidence)

    log_status("Compiling final intelligence assessment...")
    summary = f"""
{company} operates with strengths such as {business.strengths[0]}.
It faces risks including {risk.risk_factors[0]}.
Overall outlook is {risk.outlook.value}.
"""

    result = CompanyIntelligence(
        summary=summary,
        strengths=business.strengths,
        weaknesses=business.weaknesses,
        competitive_advantage=business.competitive_advantage,
        risk_factors=risk.risk_factors,
        outlook=risk.outlook,
        confidence=confidence
    )

    features = compute_features(result)

    log_status("Engine execution complete.")
    return result, features