from pydantic import BaseModel
from typing import List, Dict

from typing import List, Dict, Optional

class ChatRequest(BaseModel):
    message: str
    history: List[Dict[str, str]] = []

class ChatResponse(BaseModel):
    answer: str
    sources: List[str] = []
    page_numbers: List[int] = []
    confidence: Optional[str] = None

class UploadResponse(BaseModel):
    message: str
    status: str
    pages: int
    chunks: int
    documents_indexed: int

class ResetResponse(BaseModel):
    message: str
    status: str
