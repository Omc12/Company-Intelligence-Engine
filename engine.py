from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq

from schema import CompanyIntelligence

from dotenv import load_dotenv
load_dotenv()

parser = PydanticOutputParser(pydantic_object=CompanyIntelligence)

format_instructions = parser.get_format_instructions()

prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        "You are a strategic company intelligence analyst.\n"
        "Provide structured analysis only.\n"
        "Follow the output format strictly.\n"
        "{format_instructions}"
    ),
    (
        "user",
        "Analyze the company: {company_name}"
    )
])

prompt = prompt.partial(format_instructions=format_instructions)

model = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0
)

#LCEL chain
chain = prompt | model | parser

def analyze_company(company_name: str):
    return chain.invoke({"company_name": company_name})