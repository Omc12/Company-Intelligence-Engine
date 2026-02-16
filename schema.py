from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai.chat_models import ChatOpenAI

parser = PydanticOutputParser(pydantic_object=CompanyIntelligence)

format_instructions = parser.get_format_instructions()

prompt = ChatPromptTemplate.from_messages([
    ("system",
     "You are a strategic company intelligence analyst.\n"
     "Follow the output format strictly.\n"
     "{format_instructions}"
    ),
    ("user",
     "Analyze the company: {company_name}"
    )
])

prompt = prompt.partial(format_instructions=format_instructions)
