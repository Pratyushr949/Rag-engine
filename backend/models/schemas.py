from pydantic import BaseModel
from typing import List, Dict

from typing import Optional

class ChatRequest(BaseModel):
    message: str
    history: List[Dict[str, str]] = []

class ChatResponse(BaseModel):
    answer: str
    sources: List[str] = []
    page_numbers: List[int] = []
    retrieved_chunks: List[str] = []
    knowledge_facts: List[str] = []
    entity_list: List[str] = []
    relationship_list: List[str] = []
    reasoning_summary: str = ""
    confidence: Optional[str] = None

class UploadResponse(BaseModel):
    message: str
    status: str
    pages: int
    chunks: int
    documents_indexed: int
    files: Optional[List[str]] = None
    entities: Optional[Dict] = None
    relationships: Optional[List[Dict]] = None

class ResetResponse(BaseModel):
    message: str
    status: str
