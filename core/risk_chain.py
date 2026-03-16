from core.schema import RiskIntelligence

class RiskChain:

    def __init__(self, model):
        self.model = model

    def invoke(self, context):

        prompt = f"""
Extract key risk factors from the following context.

Return JSON with:
risk_factors
outlook
confidence

Return only valid JSON. Do not include markdown fences or extra text.

Context:
{context}
"""

        structured_model = self.model.with_structured_output(RiskIntelligence)

        result = structured_model.invoke(prompt)

        return result.model_copy(
            update={"risk_factors": result.risk_factors[:5]}
        )