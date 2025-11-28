from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    """Application settings loaded from .env file"""
    
    # App Configuration
    APP_NAME: str = "Vox Maati Voice API"
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    
    # Database
    DATABASE_URL: str = "postgresql://vox_admin:dev_password123@localhost:5432/vox_maati_dev"
    
    # Google Cloud Platform
    GCP_PROJECT_ID: str = "vox-maati-dev"
    GCS_BUCKET_NAME: str = "vox-maati-audio-dev"
    GOOGLE_APPLICATION_CREDENTIALS: str = "./gcp-credentials.json"
    
    # Audio Settings
    MAX_AUDIO_DURATION: int = 120  # seconds
    MAX_AUDIO_SIZE_MB: int = 10
    
    # Redis & Celery
    REDIS_URL: str = "redis://localhost:6379/0"
    CELERY_BROKER_URL: str = "redis://localhost:6379/0"
    CELERY_RESULT_BACKEND: str = "redis://localhost:6379/1"
    
    class Config:
        env_file = ".env"
        case_sensitive = True

@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance"""
    return Settings()
