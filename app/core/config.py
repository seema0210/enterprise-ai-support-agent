from functools import lru_cache
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    ollama_model: str
    ollama_base_url: str

    ollama_temperature: float = Field( default=0.0, ge=0.0, le=2.0 )

    model_config = SettingsConfigDict( env_file=".env", extra="ignore" )


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()