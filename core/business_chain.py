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

        try:
            parsed = structured_model.invoke(prompt)
            return parsed.model_copy(
                update={
                    "strengths": parsed.strengths[:5],
                    "weaknesses": parsed.weaknesses[:5],
                    "competitive_advantage": parsed.competitive_advantage[:5],
                }
            )
        except Exception as e:
            # Fallback if the LLM fails to output valid tool calls (e.g., Groq 400 Bad Request)
            print(f"BusinessChain Extraction Error: {e}")
            return BusinessIntelligence(
                strengths=["Data extraction failed or model output invalid format."],
                weaknesses=["Could not parse LLM response."],
                competitive_advantage=["N/A"],
                confidence=0.0
            )