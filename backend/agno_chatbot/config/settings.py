"""
Configuration settings for AgnoChat Bot
"""

import os
from typing import Optional
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Database Configuration
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is required")

# API Keys - All required for the application to function
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY environment variable is required")

ZEP_API_KEY = os.getenv("ZEP_API_KEY")
if not ZEP_API_KEY:
    raise ValueError("ZEP_API_KEY environment variable is required")

MEM0_API_KEY = os.getenv("MEM0_API_KEY")
if not MEM0_API_KEY:
    raise ValueError("MEM0_API_KEY environment variable is required")

# JWT Configuration
SECRET_KEY = os.getenv("SECRET_KEY")
if not SECRET_KEY:
    raise ValueError("SECRET_KEY environment variable is required")

ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

# Server Configuration
HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", "8000"))
DEBUG = os.getenv("DEBUG", "true").lower() == "true"

# Zep Configuration
ZEP_BASE_URL = os.getenv("ZEP_BASE_URL", "https://api.getzep.com")

# Mem0 Configuration
MEM0_BASE_URL = os.getenv("MEM0_BASE_URL", "https://api.mem0.ai")

# CORS Configuration
ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", '["*"]')

# Agno Configuration
AGNO_MODEL_ID = "gemini-2.0-flash"
AGNO_MEMORY_TABLE = "agno_memories"
AGNO_SESSION_TABLE = "agno_sessions"

def setup_environment():
    """Set up environment variables for Agno framework."""
    # These are guaranteed to be strings due to the validation above
    os.environ["GOOGLE_API_KEY"] = str(GEMINI_API_KEY)
    os.environ["ZEP_API_KEY"] = str(ZEP_API_KEY)
    os.environ["MEM0_API_KEY"] = str(MEM0_API_KEY) 