from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    document_service_url: str = "http://127.0.0.1:8001"
    mcp_server_url: str = "http://127.0.0.1:3001"
    adk_port: int = 8080
    google_api_key: str = ""


@lru_cache
def get_settings() -> Settings:
    return Settings()
