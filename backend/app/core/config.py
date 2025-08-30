from typing import List, Optional, Union
from pydantic_settings import BaseSettings
from pydantic import field_validator
import secrets
import os

class Settings(BaseSettings):
    # Project Info
    PROJECT_NAME: str = "PicoBrain Healthcare System"
    APP_NAME: str = "PicoBrain"
    APP_VERSION: str = "1.0.0"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    # Environment
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    
    # Security
    SECRET_KEY: str = os.getenv(
        "SECRET_KEY",
        secrets.token_urlsafe(32)  # Generate a random key if not set
    )
    ENCRYPTION_KEY: str = os.getenv(
        "ENCRYPTION_KEY",
        secrets.token_urlsafe(32)
    )
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8  # 8 days
    JWT_ALGORITHM: str = "HS256"
    ALGORITHM: str = "HS256"  # Alias for compatibility
    
    # Database
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL", 
        "postgresql://edo@localhost/picobraindb"
    )
    DATABASE_URL_RENDER: Optional[str] = None  # For Render deployment
    
    # AWS S3 Configuration
    AWS_ACCESS_KEY_ID: Optional[str] = None
    AWS_SECRET_ACCESS_KEY: Optional[str] = None
    AWS_S3_BUCKET: str = "picobrain-photos"
    AWS_REGION: str = "us-west-2"
    
    # CORS
    BACKEND_CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:3001",
        "http://localhost:8000",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:8000",
    ]
    CORS_ORIGINS: Optional[List[str]] = None  # Alternative CORS setting
    
    # Pagination
    DEFAULT_PAGE_SIZE: int = 20
    MAX_PAGE_SIZE: int = 100
    
    # Email Configuration (Optional)
    SMTP_HOST: Optional[str] = "smtp.gmail.com"
    SMTP_PORT: int = 587
    SMTP_USER: Optional[str] = None
    SMTP_PASSWORD: Optional[str] = None
    
    @field_validator("BACKEND_CORS_ORIGINS", mode="before")
    @classmethod
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)
    
    @field_validator("CORS_ORIGINS", mode="before")
    @classmethod
    def parse_cors_origins(cls, v: Union[str, List[str], None]) -> Optional[List[str]]:
        if v is None:
            return None
        if isinstance(v, str):
            if v.startswith("["):
                # Parse JSON-like string
                import json
                try:
                    return json.loads(v)
                except:
                    pass
            return [i.strip() for i in v.split(",")]
        return v
    
    class Config:
        case_sensitive = True
        env_file = ".env"
        # Allow extra fields to prevent validation errors
        extra = "allow"

settings = Settings()
