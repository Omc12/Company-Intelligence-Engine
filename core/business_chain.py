from langchain_core.output_parsers import PydanticOutputParser
from core.schema import BusinessIntelligence


class BusinessChain:
    def __init__(self, model):
        self.model = model
        self.parser = PydanticOutputParser(pydantic_object=BusinessIntelligence)

    def build_prompt(self, context):
        format_instructions = self.parser.get_format_instructions()

        return f"""
            You are analyzing the Business section of a 10-K filing.

            From the BUSINESS CONTEXT below:

            - Identify strengths clearly described in the filing.
            - Identify weaknesses or limitations mentioned.
            - Identify competitive advantages described.

            Do NOT invent generic traits.
            Use only what is supported in the context.

            Provide between 1 and 5 items for each category.
            Do NOT return placeholders.

            BUSINESS CONTEXT:
            {context}

            {format_instructions}
        """

    def invoke(self, context):
        prompt = self.build_prompt(context)
        response = self.model.invoke(prompt)
        return self.parser.parse(response.content)