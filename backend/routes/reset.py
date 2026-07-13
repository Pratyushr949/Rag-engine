import os
import shutil
from fastapi import APIRouter, HTTPException
from backend.models.schemas import ResetResponse
from backend.utils.logger import get_logger
from backend.config.config import config

logger = get_logger(__name__)
router = APIRouter()

@router.delete("/reset", response_model=ResetResponse)
async def reset():
    """
    Deletes uploaded PDFs, vector database, and temporary files.
    Client is responsible for clearing chat history on its end.
    """
    try:
        # Delete uploads directory
        if os.path.exists(config.UPLOAD_FOLDER):
            shutil.rmtree(config.UPLOAD_FOLDER, ignore_errors=True)
            
        # Delete vector db directory
        if os.path.exists(config.CHROMA_DB_PATH):
            shutil.rmtree(config.CHROMA_DB_PATH, ignore_errors=True)
            
        # Recreate empty directories
        os.makedirs(config.UPLOAD_FOLDER, exist_ok=True)
        os.makedirs(config.CHROMA_DB_PATH, exist_ok=True)
        
        logger.info("Reset complete: Uploads and vector database cleared.")
        
        return ResetResponse(
            message="Successfully deleted uploaded PDFs, vector database, and temporary files.",
            status="success"
        )
    except Exception as e:
        logger.error(f"Error during reset: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
