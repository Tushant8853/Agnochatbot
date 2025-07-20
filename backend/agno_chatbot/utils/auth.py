"""
Authentication utilities for AgnoChat Bot
"""

import uuid
import re
from datetime import datetime, timedelta
from typing import Optional
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from passlib.context import CryptContext
from jose import JWTError, jwt
from fastapi import HTTPException, status

from ..config.settings import (
    DATABASE_URL, SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
)

# Database setup
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    
    id = Column(String, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    first_name = Column(String(50), nullable=True)
    last_name = Column(String(50), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, onupdate=datetime.utcnow)

class ChatHistory(Base):
    __tablename__ = "chat_history"
    
    id = Column(String, primary_key=True, index=True)
    user_id = Column(String, nullable=False, index=True)
    session_id = Column(String, nullable=False, index=True)
    message = Column(String, nullable=True)  # User message
    response = Column(String, nullable=True)  # Assistant response
    message_type = Column(String, nullable=False)  # "user" or "assistant"
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)
    
    # Foreign key relationship (optional)
    # user = relationship("User", back_populates="chat_history")

# Create tables
Base.metadata.create_all(bind=engine)

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def generate_user_id(email: str, first_name: Optional[str] = None) -> str:
    """Generate a unique user ID based on email and name."""
    # Extract username from email (part before @)
    email_part = email.split('@')[0]
    
    # Clean the email part (remove special characters, keep alphanumeric)
    clean_email = re.sub(r'[^a-zA-Z0-9]', '', email_part)
    
    # Use first name if available, otherwise use email part
    if first_name and first_name.strip():
        clean_name = re.sub(r'[^a-zA-Z0-9]', '', first_name.lower())
        base_id = f"{clean_name}_{clean_email}"
    else:
        base_id = clean_email
    
    # Generate a shorter unique suffix (4 characters instead of 8)
    unique_suffix = str(uuid.uuid4())[:4]
    
    # Combine to create user_id
    user_id = f"{base_id}_{unique_suffix}"
    
    # Ensure it's not too long (max 30 characters for better memory compatibility)
    if len(user_id) > 30:
        user_id = user_id[:30]
    
    return user_id

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash."""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """Generate password hash."""
    return pwd_context.hash(password)

def create_access_token(data: dict) -> str:
    """Create JWT access token."""
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str) -> Optional[str]:
    """Verify JWT token and return email."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        return email
    except JWTError:
        return None

def get_user_by_email(email: str) -> Optional[User]:
    """Get user by email."""
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.email == email).first()
        return user
    finally:
        db.close()

def get_user_by_id(user_id: str) -> Optional[User]:
    """Get user by ID."""
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.id == user_id).first()
        return user
    finally:
        db.close()

def create_user(email: str, password: str, 
                first_name: Optional[str] = None, 
                last_name: Optional[str] = None) -> User:
    """Create a new user with auto-generated user_id."""
    db = SessionLocal()
    try:
        # Generate unique user_id
        user_id = generate_user_id(email, first_name)
        
        # Check if user_id already exists (very unlikely but possible)
        existing_user = get_user_by_id(user_id)
        if existing_user:
            # If collision, generate a new one
            user_id = generate_user_id(email, first_name)
        
        hashed_password = get_password_hash(password)
        db_user = User(
            id=user_id,
            username=user_id,
            email=email,
            hashed_password=hashed_password,
            first_name=first_name or None,
            last_name=last_name or None
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()

def store_chat_message(user_id: str, session_id: str, message: str, response: str) -> None:
    """Store a chat message and response in the database."""
    db = SessionLocal()
    try:
        import uuid
        
        # Store user message
        user_message = ChatHistory(
            id=str(uuid.uuid4()),
            user_id=user_id,
            session_id=session_id,
            message=message,
            response="",
            message_type="user"
        )
        db.add(user_message)
        
        # Store assistant response
        assistant_message = ChatHistory(
            id=str(uuid.uuid4()),
            user_id=user_id,
            session_id=session_id,
            message="",
            response=response,
            message_type="assistant"
        )
        db.add(assistant_message)
        
        db.commit()
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()

def get_chat_history(user_id: str, session_id: Optional[str] = None, limit: int = 50) -> list[ChatHistory]:
    """Get chat history for a user."""
    db = SessionLocal()
    try:
        query = db.query(ChatHistory).filter(ChatHistory.user_id == user_id)
        
        if session_id:
            query = query.filter(ChatHistory.session_id == session_id)
        
        # Order by timestamp (newest first) and limit results
        chat_history = query.order_by(ChatHistory.timestamp.desc()).limit(limit).all()
        
        return chat_history
    finally:
        db.close()

def get_user_sessions(user_id: str) -> list[str]:
    """Get all session IDs for a user."""
    db = SessionLocal()
    try:
        sessions = db.query(ChatHistory.session_id).filter(
            ChatHistory.user_id == user_id
        ).distinct().all()
        
        return [session[0] for session in sessions]
    finally:
        db.close() 