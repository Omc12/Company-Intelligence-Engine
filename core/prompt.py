from langchain_core.prompts import ChatPromptTemplate


def get_prompt(format_instructions: str):
    prompt = ChatPromptTemplate.from_messages([
        (
            "system",
            "You are a strategic company intelligence analyst.\n"
            "Provide structured analysis only.\n"
            "Follow the output format strictly.\n"
            "{format_instructions}"
        ),
        (
            "user",
            "Analyze the company: {company_name}"
        )
    ])

    return prompt.partial(format_instructions=format_instructions)
