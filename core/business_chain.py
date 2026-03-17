from core.schema import BusinessIntelligence

class BusinessChain:

    def __init__(self, model):
        self.model = model

    def invoke(self, context):

        prompt = f"""
Extract company strengths, weaknesses and competitive advantages based on the following context.

Context:
{context}
"""

        structured_model = self.model.with_structured_output(BusinessIntelligence)

        result = structured_model.invoke(prompt)

        return result.model_copy(
            update={
                "strengths": result.strengths[:5],
                "weaknesses": result.weaknesses[:5],
                "competitive_advantage": result.competitive_advantage[:5],
            }
        )