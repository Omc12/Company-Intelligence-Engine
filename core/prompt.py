from langchain_core.prompts import ChatPromptTemplate


def get_prompt(format_instructions: str):
    prompt = ChatPromptTemplate.from_messages([
(
            "system",
            "You are a strategic company intelligence analyst.\n"
            "Use only the provided context to generate your analysis.\n"
            "If the context is insufficient, state uncertainty.\n"
            "Follow the output format strictly.\n"
            "{format_instructions}"
        ),
        (
            "system",
            "Context:\n{context}"
        ),
        (
            "user",
            "Analyze the company: {company_name}"
        )
    ])

    return prompt.partial(format_instructions=format_instructions)
