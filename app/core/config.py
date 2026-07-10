from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )

    environment: str = "development"
    app_name: str = "DocumentAnalyserAPI"
    database_url: str = "sqlite+aiosqlite:///./cbam.db"
    api_v1_prefix: str = "/api/v1"
