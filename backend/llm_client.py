from langchain_groq import ChatGroq
from .settings import settings

def get_llm() -> ChatGroq:
    return ChatGroq(
        model=settings.LLM_MODEL,
        temperature=settings.LLM_TEMPERATURE,
        max_tokens=settings.LLM_MAX_TOKENS,
        api_key=settings.GROK_API_KEY,
    )