from langchain_groq import ChatGroq
from dotenv import load_dotenv

load_dotenv()

def get_model(temperature=0.0):
    return ChatGroq(
        model="llama-3.3-70b-versatile",
        temperature=temperature
    )
