from pydantic import BaseSettings, Field
from functools import lru_cache


class Settings(BaseSettings):
    # Project settings
    PROJECT_NAME: str = "Journal Reflection API"
    API_V1_STR: str = "/api/v1"

    # OpenAI
    OPENAI_API_KEY: str = Field(..., env="OPENAI_API_KEY")
    OPENAI_MODEL: str = "gpt-4"

    # Server
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    RELOAD: bool = True  # Set to False in production

    # Other integrations (future-proofing)
    LANGCHAIN_TRACING: bool = False

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache()
def get_settings() -> Settings:
    return Settings()



