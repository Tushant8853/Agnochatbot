#!/usr/bin/env python3
"""
Startup script for Agno Chatbot Backend
Initializes database and starts the FastAPI server
"""

import asyncio
import os
import sys
from pathlib import Path

# Add the current directory to Python path
sys.path.append(str(Path(__file__).parent))

from database import init_database
from config import settings
from utils.logger import logger


async def main():
    """Main startup function."""
    try:
        logger.info("Starting Agno Chatbot Backend...")
        
        # Check if .env file exists
        if not os.path.exists(".env"):
            logger.warning(".env file not found. Please copy env.example to .env and configure it.")
            logger.info("You can still run the server, but some features may not work without proper configuration.")
        
        # Initialize database
        logger.info("Initializing database...")
        await init_database()
        logger.info("Database initialized successfully!")
        
        # Start the server
        logger.info(f"Starting server on {settings.host}:{settings.port}")
        logger.info(f"Debug mode: {settings.debug}")
        logger.info("API documentation available at: http://localhost:8000/docs")
        
        # Import and run uvicorn
        import uvicorn
        uvicorn.run(
            "main:app",
            host=settings.host,
            port=settings.port,
            reload=settings.debug,
            log_level="info"
        )
        
    except KeyboardInterrupt:
        logger.info("Server stopped by user")
    except Exception as e:
        logger.error(f"Failed to start server: {e}")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main()) 