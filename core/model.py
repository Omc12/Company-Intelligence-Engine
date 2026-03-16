from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os

load_dotenv()

def get_model(temperature=0.0):

    model_name = os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")
    timeout = float(os.getenv("GROQ_TIMEOUT", "45"))
    max_retries = int(os.getenv("GROQ_MAX_RETRIES", "1"))

    return ChatGroq(
        model=model_name,
        temperature=temperature,
        timeout=timeout,
        max_retries=max_retries,
        groq_api_key=os.getenv("GROQ_API_KEY")
    )