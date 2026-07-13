import os
from typing import List
from langchain_chroma import Chroma
from langchain_core.documents import Document
from backend.utils.logger import get_logger
from backend.config.config import config
from backend.services.embeddings import EmbeddingsService

logger = get_logger(__name__)

class VectorStoreService:
    @staticmethod
    def get_vector_store() -> Chroma | None:
        persist_directory = config.CHROMA_DB_PATH
        if not os.path.exists(persist_directory):
            logger.warning(f"Chroma DB directory {persist_directory} does not exist.")
            return None
        return Chroma(
            persist_directory=persist_directory, 
            embedding_function=EmbeddingsService.get_embeddings()
        )

    @staticmethod
    def create_vector_store(chunks: List[Document]) -> Chroma:
        persist_directory = config.CHROMA_DB_PATH
        logger.info("Creating embeddings and storing in ChromaDB...")
        vectorstore = Chroma.from_documents(
            documents=chunks,
            embedding=EmbeddingsService.get_embeddings(),
            persist_directory=persist_directory, 
            collection_metadata=config.VECTOR_DB_COLLECTION_METADATA
        )
        logger.info(f"Vector store created and saved to {persist_directory}")
        return vectorstore
