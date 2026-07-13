import os
import shutil
from fastapi import APIRouter, UploadFile, File, HTTPException
from backend.models.schemas import UploadResponse
from backend.services.loader import DocumentLoader
from backend.services.chunking import DocumentChunker
from backend.services.vectorstore import VectorStoreService
from backend.utils.logger import get_logger
from backend.config.config import config

logger = get_logger(__name__)
router = APIRouter()

@router.post("/upload", response_model=UploadResponse)
async def upload_document(file: UploadFile = File(...)):
    if not file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")
        
    try:
        os.makedirs(config.UPLOAD_FOLDER, exist_ok=True)
        file_path = os.path.join(config.UPLOAD_FOLDER, file.filename)
        
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        logger.info(f"File {file.filename} saved to {file_path}")
        
        documents = DocumentLoader.load_documents(config.UPLOAD_FOLDER)
        if not documents:
            raise Exception("Failed to extract any text from the PDF.")
            
        chunks = DocumentChunker.split_documents(documents)
        VectorStoreService.create_vector_store(chunks)
        
        distinct_files = len(set([doc.metadata.get("source") for doc in documents if doc.metadata.get("source")]))
        
        return UploadResponse(
            message=f"File '{file.filename}' uploaded and processed successfully.", 
            status="success",
            pages=len(documents),
            chunks=len(chunks),
            documents_indexed=distinct_files
        )
    except Exception as e:
        logger.error(f"Error during upload/ingestion: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
