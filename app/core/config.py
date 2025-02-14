from pydantic_settings import BaseSettings
from pydantic import ConfigDict
from pathlib import Path
from typing import Optional

class Settings(BaseSettings):
    """Application settings."""
    
    model_config = ConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore"  # This will ignore extra fields from env file
    )
    
    # Application
    ENVIRONMENT: str = "development"
    APP_NAME: str = "AI Document Search & Q&A"
    DEBUG: bool = True
    APP_PORT: int = 8000
    APP_HOST: str = "0.0.0.0"
    API_V1_STR: str = "/api/v1"
    
    # Document Processing
    UPLOAD_DIR: Path = Path("data/uploads")
    MAX_UPLOAD_SIZE: int = 10 * 1024 * 1024  # 10MB
    
    # Vector Store
    CHROMA_DB_DIR: Path = Path("data/chromadb")
    COLLECTION_NAME: str = "documents"
    VECTOR_DB_HOST: str = "vectordb"
    VECTOR_DB_PORT: int = 8001
    
    # Embedding
    EMBEDDING_MODEL_NAME: str = "sentence-transformers/all-MiniLM-L6-v2"
    CHUNK_SIZE: int = 512
    CHUNK_OVERLAP: int = 50
    
    # LLM settings
    LLM_MODEL_NAME: str = "mistralai/Mistral-7B-Instruct-v0.2"
    MAX_NEW_TOKENS: int = 512
    TEMPERATURE: float = 0.7
    TOP_P: float = 0.95
    CONTEXT_WINDOW: int = 4096

    # Security
    API_KEY_HEADER: str = "X-API-Key"
    RATE_LIMIT_REQUESTS: int = 100
    RATE_LIMIT_PERIOD: int = 3600  # 1 hour in seconds

    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

settings = Settings() 