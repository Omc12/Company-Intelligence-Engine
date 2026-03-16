from core.model import get_model

class QueryPlanner:

    def __init__(self):
        self.model = get_model(temperature=0)

    def plan(self, query):

        prompt=f"""
Break the query into 3 retrieval subqueries.

Query:
{query}
"""

        try:
            response=self.model.invoke(prompt).content
        except Exception as e:
            print(f"[query_planner] Falling back to heuristic subqueries: {e}")
            return [
                query,
                f"{query} risk factors",
                f"{query} business outlook"
            ]

        lines=response.split("\n")

        queries=[]

        for l in lines:
            if "." in l:
                queries.append(l.split(".",1)[1].strip())

        if not queries:
            return [
                query,
                f"{query} risk factors",
                f"{query} business outlook"
            ]

        return queries