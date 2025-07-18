from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    # Database - Use Railway DATABASE_URL if available, otherwise fallback to local PostgreSQL
    database_url: str = "postgresql://postgres:BBHybyJPpEPOSxzROzNJosWcOhrjuANY@trolley.proxy.rlwy.net:22479/railway"
    
    # JWT
    secret_key: str = "your_secret_key_here_make_it_long_and_secure"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # Google Gemini
    gemini_api_key: str = "your_gemini_api_key_here"
    
    # Zep
    zep_api_key: str = "your_zep_api_key_here"
    zep_base_url: str = "https://api.getzep.com"
    
    # Mem0
    mem0_api_key: str = "your_mem0_api_key_here"
    mem0_api_url: str = "https://api.mem0.ai"
    
    # Application
    debug: bool = True
    host: str = "0.0.0.0"
    port: int = 8000
    
    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings() 