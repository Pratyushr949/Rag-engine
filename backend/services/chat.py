from typing import List, Dict
from pydantic import BaseModel
from langchain_core.messages import HumanMessage, SystemMessage

from utils.logger import get_logger
from config.config import config
from services.memory import MemoryService
from services.vectorstore import VectorStoreService
from services.llm import LLMService
from services.retrieval import get_retrieval_strategy
from services.fusion_retriever import FusionRetrieverService

class StructuredChatOutput(BaseModel):
    answer: str
    reasoning_summary: str
    entity_list: List[str]
    relationship_list: List[str]

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
        strategy = get_retrieval_strategy(config.RETRIEVAL_STRATEGY)
        docs = strategy.retrieve(self.db, self.model, search_question)
        
        # Extract sources and page numbers (still based on vector docs for provenance)
        sources = list(set([doc.metadata.get("source", "Unknown") for doc in docs]))
        page_numbers = list(set([doc.metadata.get("page", 0) + 1 for doc in docs if "page" in doc.metadata]))
        
        # 4. Hybrid Context Fusion
        fusion_result = FusionRetrieverService.get_fused_context(search_question, docs)
        fused_contexts = fusion_result["merged_context"]
        vector_chunks = fusion_result["vector_chunks"]
        knowledge_facts = fusion_result["knowledge_facts"]
        
        combined_input = f"""Based on the following documents and knowledge, please answer this question: {user_question}

Documents & Knowledge:
{chr(10).join([f"- {ctx}" for ctx in fused_contexts])}

Please provide a clear, helpful answer using only the information from these documents. If you can't find the answer in the documents, say "I don't have enough information to answer that question based on the provided documents."
"""
        
        logger.info("Generating answer...")
        messages = [
            SystemMessage(content="You are a helpful assistant that answers questions based on provided documents and conversation history."),
        ] + chat_history + [
            HumanMessage(content=combined_input)
        ]
        
        structured_llm = self.model.with_structured_output(StructuredChatOutput)
        result = structured_llm.invoke(messages)
        logger.info("Answer generated successfully.")
        
        return {
            "answer": result.answer,
            "sources": sources,
            "page_numbers": page_numbers,
            "retrieved_chunks": vector_chunks,
            "knowledge_facts": knowledge_facts,
            "entity_list": result.entity_list,
            "relationship_list": result.relationship_list,
            "reasoning_summary": result.reasoning_summary,
            "confidence": "High"  # Structured output doesn't return metadata directly
        }
