from core.model import get_model

class QueryPlanner:

    def __init__(self):
        self.model = get_model(temperature=0)

    def plan(self, query):

        prompt = f"""
Break the query into 2-4 retrieval subqueries.

Query:
{query}
"""

        response = self.model.invoke(prompt).content

        lines = response.split("\n")

        queries = []

        for l in lines:
            if "." in l:
                queries.append(l.split(".",1)[1].strip())

        return queries