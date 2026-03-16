from langchain_core.output_parsers import PydanticOutputParser
from core.schema import RiskIntelligence


class RiskChain:
    def __init__(self, model):
        self.model = model
        self.parser = PydanticOutputParser(pydantic_object=RiskIntelligence)

    def build_prompt(self, context):
        format_instructions = self.parser.get_format_instructions()

        return f"""
            You are analyzing the official Risk Factors section of a 10-K filing.

            From the RISK CONTEXT below:

            - Identify explicit risk statements.
            - Extract concrete risks mentioned in the filing.
            - Do NOT invent risks.
            - If risks are unclear, extract phrases directly from the text.

            Provide between 1 and 5 real risk factors mentioned in the filing.
            Do NOT return placeholders like "Unknown".

            RISK CONTEXT:
            {context}

            {format_instructions}
        """

    def invoke(self, context):
        prompt = self.build_prompt(context)
        response = self.model.invoke(prompt)
        return self.parser.parse(response.content)