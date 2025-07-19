#!/usr/bin/env python3
"""
Main FastAPI application for AgnoChat Bot using Agno Framework
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from agno_chatbot.config.settings import setup_environment
from agno_chatbot.api.routes import router

# Set up environment variables
setup_environment()

# Create FastAPI app
app = FastAPI(
    title="AgnoChat Bot API",
    description="Production-ready AI chatbot using Agno Framework with Gemini, Zep, and Mem0",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(router, prefix="/api")

@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "AgnoChat Bot API",
        "version": "1.0.0",
        "framework": "Agno",
        "features": ["Gemini AI", "Zep Memory", "Mem0 Memory", "PostgreSQL Storage"]
    }

if __name__ == "__main__":
    import uvicorn
    from agno_chatbot.config.settings import HOST, PORT, DEBUG
    
    uvicorn.run(
        "main:app",
        host=HOST,
        port=PORT,
        reload=DEBUG,
        log_level="info"
    ) 