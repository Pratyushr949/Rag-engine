from typing import List, Dict
from langchain_core.messages import HumanMessage, SystemMessage

from backend.utils.logger import get_logger
from backend.config.config import config
from backend.services.memory import MemoryService
from backend.services.vectorstore import VectorStoreService
from backend.services.llm import LLMService

logger = get_logger(__name__)

class ChatService:
    def __init__(self):
        self.db = VectorStoreService.get_vector_store()
        self.model = LLMService.get_llm()
        logger.info(f"ChatService initialized with {config.MODEL_NAME}")

    def ask_question(self, user_question: str, history: List[Dict[str, str]]) -> dict:
        logger.info(f"Received question: {user_question}")
        
        if not self.db:
            return {
                "answer": "The document database is empty. Please upload some documents first.",
                "sources": [],
                "page_numbers": [],
                "confidence": None
            }
            
        # 1. Format history using the reusable MemoryService
        chat_history = MemoryService.format_history(history)
        
        # 2. Get history-aware standalone question
        search_question = MemoryService.get_standalone_question(
            model=self.model, 
            user_question=user_question, 
            chat_history=chat_history
        )
            
        logger.info(f"Using strategy: {config.RETRIEVAL_STRATEGY}")
        
        # 3. Retrieve relevant chunks using Strategy Pattern
        from backend.services.retrieval import get_retrieval_strategy
        strategy = get_retrieval_strategy(config.RETRIEVAL_STRATEGY)
        docs = strategy.retrieve(self.db, self.model, search_question)
        
        # Extract sources and page numbers
        sources = list(set([doc.metadata.get("source", "Unknown") for doc in docs]))
        page_numbers = list(set([doc.metadata.get("page", 0) + 1 for doc in docs if "page" in doc.metadata]))
        
        combined_input = f"""Based on the following documents, please answer this question: {user_question}

Documents:
{chr(10).join([f"- {doc.page_content}" for doc in docs])}

Please provide a clear, helpful answer using only the information from these documents. If you can't find the answer in the documents, say "I don't have enough information to answer that question based on the provided documents."
"""
        
        logger.info("Generating answer...")
        messages = [
            SystemMessage(content="You are a helpful assistant that answers questions based on provided documents and conversation history."),
        ] + chat_history + [
            HumanMessage(content=combined_input)
        ]
        
        result = self.model.invoke(messages)
        logger.info("Answer generated successfully.")
        
        return {
            "answer": result.content,
            "sources": sources,
            "page_numbers": page_numbers,
            "confidence": getattr(result, "response_metadata", {}).get("finish_reason", None)
        }
