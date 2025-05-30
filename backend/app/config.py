import os
from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

class Settings(BaseSettings):
    APP_NAME: str = "AI Reflection API"
    GEMINI_API_KEY: str
    BACKEND_ORIGINS: list[str]

    model_config = SettingsConfigDict(
        env_file=os.path.join(BASE_DIR, ".env"),
        env_file_encoding='utf-8',
        extra='ignore'
    )

settings = Settings()

if not settings.GEMINI_API_KEY:
   print("CRITICAL ERROR: GEMINI_API_KEY not found. Check your .env file and config.py.")
