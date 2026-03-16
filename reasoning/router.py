from core.model import get_model

class SectionRouter:

    def __init__(self):
        self.model = get_model()

    def route(self, query):

        prompt = f"""
Classify which section should be searched.

Options:
- business
- risk

Query:
{query}

Return JSON with scores for each section.
"""

        response = self.model.invoke(prompt).content.lower()

        scores = {
            "risk": 0.5,
            "business": 0.5
        }

        if "risk" in response:
            scores["risk"] = 0.9

        if "business" in response:
            scores["business"] = 0.9

        return scores