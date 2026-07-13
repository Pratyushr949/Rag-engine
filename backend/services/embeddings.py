from langchain_google_genai import GoogleGenerativeAIEmbeddings
from backend.config.config import config


class EmbeddingsService:
    @staticmethod
    def get_embeddings() -> GoogleGenerativeAIEmbeddings:
        return GoogleGenerativeAIEmbeddings(
            model=config.EMBEDDING_MODEL,
            google_api_key=config.GOOGLE_API_KEY
        )