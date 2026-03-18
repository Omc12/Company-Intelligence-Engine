from core.model import get_model

class SectionRouter:
    def __init__(self):
        self.model = get_model()

    def route(self, query):

        prompt = f"""
                    Decide which sections are relevant.

                    Options:
                    risk
                    business

                    Return JSON scores.

                    Query:
                    {query}
                """

        try:
            response = self.model.invoke(prompt).content.lower()
        except Exception as e:
            print(f"[router] Falling back to default section scores: {e}")
            return {"risk":0.9,"business":0.9}

        scores = {"risk":0.5,"business":0.5}

        if "risk" in response:
            scores["risk"]=0.9

        if "business" in response:
            scores["business"]=0.9

        return scores