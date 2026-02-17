from langchain_core.output_parsers import PydanticOutputParser
from schema import CompanyIntelligence


def get_base_parser():
    return PydanticOutputParser(pydantic_object=CompanyIntelligence)
