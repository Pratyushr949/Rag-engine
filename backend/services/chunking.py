from typing import List
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from utils.logger import get_logger
from config.config import config

logger = get_logger(__name__)

class DocumentChunker:
    @staticmethod
    def split_documents(documents: List[Document]) -> List[Document]:
        logger.info("Splitting documents into chunks...")
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=config.CHUNK_SIZE, 
            chunk_overlap=config.CHUNK_OVERLAP
        )
        chunks = text_splitter.split_documents(documents)
        logger.info(f"Created {len(chunks)} chunks.")
        return chunks
