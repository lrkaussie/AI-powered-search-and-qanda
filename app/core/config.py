from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    CHROMA_DB_DIR: str = ".chroma"
    COLLECTION_NAME: str = "documents"
    EMBEDDING_MODEL_NAME: str = "BAAI/bge-small-en"
    CHUNK_SIZE: int = 500
    CHUNK_OVERLAP: int = 50

    # LLM settings
    LLM_MODEL_NAME: str = "mistralai/Mistral-7B-Instruct-v0.2"
    MAX_NEW_TOKENS: int = 512
    TEMPERATURE: float = 0.7
    TOP_P: float = 0.95
    CONTEXT_WINDOW: int = 4096

    class Config:
        env_file = ".env"

settings = Settings() 