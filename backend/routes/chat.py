from fastapi import APIRouter, HTTPException
from backend.models.schemas import ChatRequest, ChatResponse
from backend.services.chat import ChatService
from backend.utils.logger import get_logger

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
            confidence=result["confidence"]
        )
    except Exception as e:
        logger.error(f"Error during chat: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
