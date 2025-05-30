import os
from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path

# Determine the base directory of your project (backend folder)
# This helps in reliably finding the .env file
BASE_DIR = Path(__file__).resolve().parent.parent # This should point to the 'backend' directory

class Settings(BaseSettings):
    APP_NAME: str = "AI Reflection API"
    GEMINI_API_KEY: str # Pydantic will raise an error if this is not set

    # Add other settings as needed
    # API_V1_STR: str = "/api/v1"
    # DEBUG_MODE: bool = False

    model_config = SettingsConfigDict(
        env_file=os.path.join(BASE_DIR, ".env"), # Explicitly point to your .env file
        env_file_encoding='utf-8',
        extra='ignore' # Ignore extra environment variables not defined in Settings
    )

settings = Settings()

if not settings.GEMINI_API_KEY:
   print("CRITICAL ERROR: GEMINI_API_KEY not found. Check your .env file and config.py.")
