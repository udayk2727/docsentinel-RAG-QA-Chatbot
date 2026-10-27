"""Central settings, loaded from environment variables or a .env file."""
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    llm_provider: str = "anthropic"
    llm_model: str = "claude-sonnet-5-5"
    anthropic_api_key: str = ""
    openai_api_key: str = ""
    groq_api_key: str = ""

    embedding_model: str = "BAAI/bge-small-en-v1.5"
    qdrant_url: str = ":memory:"
    collection_name: str = "docsentinel"

    chunk_size: int = 800       # characters per chunk
    chunk_overlap: int = 120    # characters shared between neighbouring chunks
    top_k: int = 5              # chunks sent to the LLM


settings = Settings()
