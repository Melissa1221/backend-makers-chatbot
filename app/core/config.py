"""Application settings and configuration."""
from functools import lru_cache
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """Application settings."""
    # API Settings
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "E-commerce Chatbot API"
    
    # OpenAI Settings
    OPENAI_API_KEY: str
    
    # Supabase Settings
    SUPABASE_URL: str
    SUPABASE_KEY: str
    
    # Database Settings
    DATABASE_URL: str
    
    # Security
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    class Config:
        """Pydantic config."""
        env_file = ".env"
        case_sensitive = True
        extra = "allow"  # Allow extra fields in the settings

@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings() 