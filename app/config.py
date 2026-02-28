"""Application configuration using environment variables."""
from pydantic import BaseSettings


class Settings(BaseSettings):
    OPENAI_API_KEY: str
    APP_HOST: str = "127.0.0.1"
    APP_PORT: int = 8000
    ENV: str = "production"

    class Config:
        env_file = ".env"


settings = Settings()
