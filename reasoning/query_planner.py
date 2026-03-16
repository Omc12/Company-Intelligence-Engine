from core.model import get_model


class QueryPlanner:

    def __init__(self):
        self.model = get_model(temperature=0)

    def plan(self, query: str):

        prompt = f"""
Break the following query into 2–4 focused subqueries that help retrieve evidence.

Query:
{query}

Return a numbered list of subqueries.
"""

        response = self.model.invoke(prompt).content

        lines = response.split("\n")
        subqueries = []

        for line in lines:
            if "." in line:
                subqueries.append(line.split(".",1)[1].strip())

        return subqueries