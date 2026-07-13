import time
from fastapi import APIRouter

router = APIRouter()

@router.get("/health", tags=["System"])
async def health_check():
    """Returns the current health status of the API"""
    return {
        "status": "online",
        "service": "RAG Engine",
        "version": "1.0.0",
        "timestamp": time.time()
    }
