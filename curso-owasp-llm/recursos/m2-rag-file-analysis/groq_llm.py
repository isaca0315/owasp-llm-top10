from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def get_groq_model():
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError("GROQ_API_KEY not set in environment variables or .env file.")

    return ChatGroq(
        groq_api_key=api_key,
        model="llama-3.1-8b-instant",
        temperature=0.1,
        max_tokens=2000
    )

