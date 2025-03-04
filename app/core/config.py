"""Configuration settings for the application using Pydantic settings management."""

import os
from pathlib import Path
from typing import Any, Final

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",  # This will ignore extra fields from env file
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
    MAX_UPLOAD_SIZE: int = 10 * 1024 * 1024  # 10MB in bytes

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

    @field_validator("MAX_UPLOAD_SIZE", mode="before")
    @classmethod
    def validate_max_upload_size(cls, v: Any) -> int:
        """Validate and convert max upload size.

        Args:
            v: The value to validate

        Returns:
            int: The validated upload size in bytes
        """
        if isinstance(v, str):
            # Remove any comments and whitespace
            v = v.split("#")[0].strip()
            try:
                return int(v)
            except ValueError:
                return 10 * 1024 * 1024  # Default to 10MB
        elif isinstance(v, (int, float)):
            return int(v)
        return 10 * 1024 * 1024  # Default to 10MB if invalid type


def get_port() -> int:
    """Get the port number from environment variable or default.

    Returns:
        int: The port number to use
    """
    return int(os.getenv("PORT", 8000))


settings = Settings()

# Create required directories
settings.UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
settings.CHROMA_DB_DIR.mkdir(parents=True, exist_ok=True)

# Constants
MAX_CHUNK_SIZE: Final[int] = 1000
DEFAULT_BATCH_SIZE: Final[int] = 32
MODEL_CACHE_DIR: Final[Path] = Path("data/models")
