import os
import shutil
from fastapi import APIRouter, UploadFile, File, HTTPException
from typing import List
from models.schemas import UploadResponse
from services.loader import DocumentLoader
from services.chunking import DocumentChunker
from services.vectorstore import VectorStoreService
from services.entity_extractor import EntityExtractorService
from services.relationship_extractor import RelationshipExtractorService
from services.okf_generator import OKFGeneratorService
from utils.logger import get_logger
from config.config import config

logger = get_logger(__name__)
router = APIRouter()

@router.post("/upload", response_model=UploadResponse)
async def upload_documents(files: List[UploadFile] = File(...)):
    total_pages = 0
    total_chunks = 0
    processed_files = []
    
    try:
        os.makedirs(config.UPLOAD_FOLDER, exist_ok=True)
        
        for file in files:
            if not file.filename.endswith('.pdf'):
                logger.warning(f"Skipping {file.filename}, only PDF supported.")
                continue
                
            file_path = os.path.join(config.UPLOAD_FOLDER, file.filename)
            
            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
                
            logger.info(f"File {file.filename} saved to {file_path}")
            
            documents = DocumentLoader.load_document(file_path)
            if not documents:
                logger.warning(f"Failed to extract text from {file.filename}")
                continue
                
            chunks = DocumentChunker.split_documents(documents)
            VectorStoreService.create_vector_store(chunks)
            
            # Extract entities from the full document text
            full_text = "\n".join([doc.page_content for doc in documents])
            entities = EntityExtractorService.extract_entities(full_text)
            
            # Extract relationships
            relationships = RelationshipExtractorService.extract_relationships(full_text, entities)
            
            # Generate OKF file
            document_info = {
                "filename": file.filename,
                "pages": len(documents),
                "chunks": len(chunks)
            }
            OKFGeneratorService.generate_and_store(
                filename=file.filename,
                entities=entities,
                relationships=relationships,
                document_info=document_info
            )
            
            total_pages += len(documents)
            total_chunks += len(chunks)
            processed_files.append(file.filename)
            
        if not processed_files:
            raise HTTPException(status_code=400, detail="No valid PDF files were processed.")
            
        return UploadResponse(
            message=f"Successfully processed {len(processed_files)} files.", 
            status="success",
            pages=total_pages,
            chunks=total_chunks,
            documents_indexed=len(processed_files),
            files=processed_files
        )
    except Exception as e:
        logger.error(f"Error during upload/ingestion: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
