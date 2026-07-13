import os
from dotenv import load_dotenv
from backend.config.settings import settings

# Explicitly load python-dotenv
load_dotenv()

class Config:
    """
    Central configuration object mapping environment settings
    to application specific constants. Never hardcodes values.
    """
    GOOGLE_API_KEY = settings.GOOGLE_API_KEY
    MODEL_NAME = settings.MODEL_NAME
    RETRIEVAL_STRATEGY = settings.RETRIEVAL_STRATEGY
    CHUNK_SIZE = settings.CHUNK_SIZE
    CHUNK_OVERLAP = settings.CHUNK_OVERLAP
    TOP_K = settings.TOP_K
    UPLOAD_FOLDER = settings.UPLOAD_FOLDER
    CHROMA_DB_PATH = settings.CHROMA_DB_PATH
    HOST = settings.HOST
    PORT = settings.PORT

    # Derived or static configuration
    VECTOR_DB_COLLECTION_METADATA = {"hnsw:space": "cosine"}
    EMBEDDING_MODEL = "models/gemini-embedding-001" # Google standard embeddings

config = Config()
