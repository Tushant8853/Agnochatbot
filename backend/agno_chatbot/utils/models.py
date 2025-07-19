"""
Pydantic models for AgnoChat Bot API
"""

from datetime import datetime
from typing import Dict, Optional
from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    """Model for user creation."""
    email: EmailStr
    password: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None

class UserLogin(BaseModel):
    """Model for user login."""
    email: EmailStr
    password: str

class Token(BaseModel):
    """Model for JWT token."""
    access_token: str
    token_type: str

class ChatMessage(BaseModel):
    """Model for chat messages."""
    user_id: str
    session_id: str
    message: str

class ChatResponse(BaseModel):
    """Model for chat responses."""
    response: str
    session_id: str
    user_id: str
    timestamp: datetime

class MemoryRequest(BaseModel):
    """Model for memory requests."""
    user_id: str
    session_id: Optional[str] = None

class MemoryResponse(BaseModel):
    """Model for memory responses."""
    user_id: str
    session_id: Optional[str] = None
    zep_memory: Dict
    mem0_memory: Dict
    consolidated_memory: str

class HealthResponse(BaseModel):
    """Model for health check response."""
    status: str
    timestamp: str
    services: Dict[str, str]

class ChatHistoryItem(BaseModel):
    """Model for individual chat history items."""
    id: str
    user_id: str
    session_id: str
    message: str
    response: str
    timestamp: datetime
    message_type: str = "user"  # "user" or "assistant"

class ChatHistoryResponse(BaseModel):
    """Model for chat history response."""
    user_id: str
    total_messages: int
    sessions: Dict[str, list[ChatHistoryItem]]
    last_activity: datetime
    history_summary: Dict[str, int]  # session_id -> message_count 