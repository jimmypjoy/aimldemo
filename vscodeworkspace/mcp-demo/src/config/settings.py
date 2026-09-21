from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    mcp_host: str = "127.0.0.1"
    mcp_port: int = 3001
    document_service_url: str = "http://127.0.0.1:8001"
    llm_service_url: str = "http://127.0.0.1:8000"
    web_search_model: str = "gpt-5-search-api"


@lru_cache
def get_settings() -> Settings:
    return Settings()
