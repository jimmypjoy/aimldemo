from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    database_url: str = "postgresql+asyncpg://postgres:password@localhost:5432/postgres"
    openai_api_key: str = ""
    embedding_model: str = "text-embedding-3-small"
    embedding_dimensions: int = 1536
    documents_base_path: str = r"C:\workspace\agentic-ai\testdocuments"
    chunk_size: int = 500
    chunk_overlap: int = 50
    mcp_server_url: str = "http://127.0.0.1:3001"
    adk_port: int = 8080


@lru_cache
def get_settings() -> Settings:
    return Settings()
