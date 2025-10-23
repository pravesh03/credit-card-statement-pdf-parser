"""
Configuration settings for the application
"""

import os
from typing import List
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """Application settings"""
    
    # API Settings
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Credit Card Statement Parser"
    
    # Database
    DATABASE_URL: str = "sqlite:///./credit_card_parser.db"
    
    # File Upload
    UPLOAD_DIR: str = "uploads"
    MAX_FILE_SIZE: int = 10 * 1024 * 1024  # 10MB
    ALLOWED_EXTENSIONS: List[str] = [".pdf"]
    
    # CORS
    ALLOWED_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:5173",
        "http://frontend:3000"
    ]
    
    # AI Provider
    AI_PROVIDER: str = "mock"  # mock, openai, anthropic
    OPENAI_API_KEY: str = ""
    ANTHROPIC_API_KEY: str = ""
    
    # OCR Settings
    TESSERACT_LANG: str = "eng"
    OCR_CONFIDENCE_THRESHOLD: float = 0.6
    
    # Security
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    class Config:
        env_file = ".env"
        case_sensitive = False

settings = Settings()
