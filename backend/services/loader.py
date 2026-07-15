import os
from typing import List
from langchain_core.documents import Document
from langchain_community.document_loaders import DirectoryLoader, PyPDFLoader
from utils.logger import get_logger

logger = get_logger(__name__)

class DocumentLoader:
    @staticmethod
    def load_documents(docs_path: str) -> List[Document]:
        logger.info(f"Loading documents from {docs_path}...")
        if not os.path.exists(docs_path):
            os.makedirs(docs_path, exist_ok=True)
            logger.warning(f"Created directory {docs_path}.")
            
        loader = DirectoryLoader(
            path=docs_path,
            glob="*.pdf",
            loader_cls=PyPDFLoader
        )
        
        documents = loader.load()
        if len(documents) == 0:
            logger.warning(f"No .pdf files found in {docs_path}.")
            
        logger.info(f"Loaded {len(documents)} documents.")
        return documents

    @staticmethod
    def load_document(file_path: str) -> List[Document]:
        logger.info(f"Loading document from {file_path}...")
        if not os.path.exists(file_path):
            logger.error(f"File {file_path} does not exist.")
            return []
            
        loader = PyPDFLoader(file_path)
        documents = loader.load()
        logger.info(f"Loaded {len(documents)} pages from {file_path}.")
        return documents
