"""Configuration system for the FastAPI backend."""

import os
from functools import cache
from pathlib import Path
from typing import Any

from dotenv import load_dotenv
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv()


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        case_sensitive=True,
        extra='allow'
    )
    
    # API Configuration
    OPENAI_API_KEY: str = Field(default='')
    ANTHROPIC_API_KEY: str = Field(default='')
    GOOGLE_API_KEY: str = Field(default='')
    DEEPSEEK_API_KEY: str = Field(default='')
    
    # Application Configuration
    APP_NAME: str = Field(default='ChatKit Backend')
    APP_VERSION: str = Field(default='1.0.0')
    DEBUG: bool = Field(default=False)
    
    # CORS Configuration
    CORS_ORIGINS: list[str] = Field(default=['http://localhost:3000', 'https://*.vercel.app'])
    
    # Logging Configuration
    LOG_LEVEL: str = Field(default='info')
    
    # File Upload Configuration
    MAX_UPLOAD_SIZE: int = Field(default=10 * 1024 * 1024)  # 10MB
    ALLOWED_EXTENSIONS: list[str] = Field(default=['.pdf', '.txt', '.doc', '.docx', '.png', '.jpg', '.jpeg'])


@cache
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()


# Global settings instance
CONFIG = get_settings()
