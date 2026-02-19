from model import get_model
from parser import get_base_parser
from prompt import get_prompt
from features import compute_features

model = get_model()
base_parser = get_base_parser()
format_instructions = base_parser.get_format_instructions()
prompt = get_prompt(format_instructions)

chain = prompt | model | base_parser

def analyze_company(company_name: str):
    intel = chain.invoke({"company_name": company_name})
    features = compute_features(intel)

    return intel, features