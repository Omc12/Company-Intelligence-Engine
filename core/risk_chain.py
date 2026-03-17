from core.schema import RiskIntelligence

class RiskChain:

    def __init__(self, model):
        self.model = model

    def invoke(self, context):

        prompt = f"""
Extract key risk factors and evaluate the overall outlook from the following context.

Context:
{context}
"""

        structured_model = self.model.with_structured_output(RiskIntelligence)

        try:
            parsed = structured_model.invoke(prompt)
            return parsed.model_copy(
                update={"risk_factors": parsed.risk_factors[:5]}
            )
        except Exception as e:
            # Fallback if the LLM fails to output valid tool calls
            print(f"RiskChain Extraction Error: {e}")
            from core.schema import Outlook
            return RiskIntelligence(
                risk_factors=["Data extraction failed or model output invalid format."],
                outlook=Outlook.neutral,
                confidence=0.0
            )