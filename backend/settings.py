from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    CHROMA_HOST: str = "localhost"
    CHROMA_PORT: int = 8000
    CHROMA_COLLECTION: str = "docs"

    EMBEDDING_MODEL: str = "sentence-transformers/all-MiniLM-L6-v2"
    EMBEDDING_DIM: int = 384

    GROK_API_KEY: str
    LLM_MODEL: str = "grok-2-latest"
    LLM_TEMPERATURE: float = 0.2
    LLM_MAX_TOKENS: int = 800

    HOST: str = "0.0.0.0"
    PORT: int = 8000
    ALLOWED_ORIGINS: str = "*"

    CHUNK_SIZE: int = 1200
    CHUNK_OVERLAP: int = 150

    class Config:
        env_file = ".env"

settings = Settings()