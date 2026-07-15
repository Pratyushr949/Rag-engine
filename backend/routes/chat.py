from fastapi import APIRouter, HTTPException
from models.schemas import ChatRequest, ChatResponse
from services.chat import ChatService
from utils.logger import get_logger

logger = get_logger(__name__)
router = APIRouter()

@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    try:
        chat_service = ChatService()
        result = chat_service.ask_question(user_question=request.message, history=request.history)
        return ChatResponse(
            answer=result["answer"],
            sources=result["sources"],
            page_numbers=result["page_numbers"],
            retrieved_chunks=result.get("retrieved_chunks", []),
            knowledge_facts=result.get("knowledge_facts", []),
            entity_list=result.get("entity_list", []),
            relationship_list=result.get("relationship_list", []),
            reasoning_summary=result.get("reasoning_summary", ""),
            confidence=result["confidence"]
        )
    except Exception as e:
        logger.error(f"Error during chat: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
