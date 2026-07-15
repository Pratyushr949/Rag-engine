from typing import List, Dict
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage, BaseMessage
from utils.logger import get_logger

logger = get_logger(__name__)

class MemoryService:
    """
    A reusable service to manage conversation history formatting 
    and history-aware prompt transformations.
    """
    
    @staticmethod
    def format_history(history: List[Dict[str, str]]) -> List[BaseMessage]:
        """Convert a list of dicts (role, content) to Langchain message objects."""
        formatted = []
        for msg in history:
            role = msg.get("role")
            content = msg.get("content")
            if role == "user":
                formatted.append(HumanMessage(content=content))
            elif role == "assistant":
                formatted.append(AIMessage(content=content))
        return formatted

    @staticmethod
    def get_standalone_question(model, user_question: str, chat_history: List[BaseMessage]) -> str:
        """
        Uses the LLM to rewrite a conversational follow-up question 
        into a standalone question suitable for vector search.
        """
        if not chat_history:
            return user_question
            
        logger.info("Rewriting question with context...")
        messages = [
            SystemMessage(content="Given the chat history, rewrite the new question to be standalone and searchable. Just return the rewritten question without any preamble."),
        ] + chat_history + [
            HumanMessage(content=f"New question: {user_question}")
        ]
        
        result = model.invoke(messages)
        search_question = result.content.strip()
        return search_question
