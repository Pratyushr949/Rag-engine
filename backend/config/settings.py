from pydantic_settings import BaseSettings
from pydantic import Field, validator

class Settings(BaseSettings):
    APP_NAME: str = Field(default="RAG Application API", min_length=1)
    DEBUG_MODE: bool = Field(default=True)
    LOG_LEVEL: str = Field(default="INFO")
    
    # API Keys & Models
    GOOGLE_API_KEY: str = Field(..., min_length=10, description="Google Gemini API Key is required")
    MODEL_NAME: str = Field(default="gemini-2.5-flash", min_length=1)
    
    # RAG Config
    RETRIEVAL_STRATEGY: str = Field(default="standard", description="standard, multi_query, hybrid, or reranker")
    CHUNK_SIZE: int = Field(default=1000, gt=0, le=5000)
    CHUNK_OVERLAP: int = Field(default=200, ge=0, le=1000)
    TOP_K: int = Field(default=3, gt=0, le=20)
    
    # Paths
    UPLOAD_FOLDER: str = Field(default="backend/uploads")
    CHROMA_DB_PATH: str = Field(default="backend/vector_db")
    
    # Server
    HOST: str = Field(default="0.0.0.0")
    PORT: int = Field(default=8000, gt=0, le=65535)

    @validator('CHUNK_OVERLAP')
    def overlap_must_be_less_than_chunk_size(cls, v, values):
        if 'CHUNK_SIZE' in values and v >= values['CHUNK_SIZE']:
            raise ValueError('CHUNK_OVERLAP must be less than CHUNK_SIZE')
        return v

    class Config:
        env_file = "backend/.env"

settings = Settings()
