from langchain_google_genai import ChatGoogleGenerativeAI
from backend.config.config import config


class LLMService:
    @staticmethod
    def get_llm() -> ChatGoogleGenerativeAI:
        return ChatGoogleGenerativeAI(
            model=config.MODEL_NAME,
            google_api_key=config.GOOGLE_API_KEY,
            temperature=0
        )