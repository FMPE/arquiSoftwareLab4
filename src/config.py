import os
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    app_name: str = os.getenv("APP_NAME", "Paperly UTEC")
    app_version: str = os.getenv("APP_VERSION", "1.0.0")
    debug: bool = os.getenv("DEBUG", "false").lower() == "true"
    
    # Database
    database_url: str = os.getenv("DATABASE_URL", "sqlite:///./data/paperly.db")
    
    # JWT
    jwt_secret_key: str = os.getenv("JWT_SECRET_KEY", "fallback-secret-key")
    jwt_algorithm: str = os.getenv("JWT_ALGORITHM", "HS256")
    access_token_expire_minutes: int = 30
    
    # Mock API
    mock_enabled: bool = os.getenv("MOCK_ENABLED", "true").lower() == "true"

    class Config:
        env_file = ".env"

settings = Settings()
