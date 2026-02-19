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

def analyze_company(company_name: str):
    docs = retriever.invoke(company_name)

    context = "\n\n".join([doc.page_content for doc in docs])

    intel = chain.invoke({
        "company_name": company_name,
        "context": context
        })
        
    features = compute_features(intel)

    return intel, features