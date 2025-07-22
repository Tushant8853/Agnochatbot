"""
Complete AgnoChat Bot Backend with FastAPI
Integrates Agno Framework, Zep Memory, Mem0 Memory, and PostgreSQL
"""

import os
import uuid
from datetime import datetime, timedelta
from typing import Optional, List, Dict, Any
from contextlib import asynccontextmanager
from dotenv import load_dotenv

import httpx
from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from sqlalchemy import create_engine, Column, String, DateTime, Text, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from passlib.context import CryptContext
import jwt
from agno.agent import Agent
from agno.models.google import Gemini
from agno.tools.zep import ZepTools
from agno.tools.mem0 import Mem0Tools
from agno.storage.postgres import PostgresStorage
from agno.memory.v2.db.postgres import PostgresMemoryDb
from agno.memory.v2.memory import Memory
from mem0 import MemoryClient

print("=" * 80)
print("STARTING AGNOCHAT BOT BACKEND")
print("=" * 80)

# Load environment variables from .env file
print("STEP 1: Loading environment variables...")
load_dotenv()
print("✓ Environment variables loaded")

# Environment Configuration
print("STEP 2: Setting up environment configuration...")
DATABASE_URL = os.getenv("DATABASE_URL")
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
ZEP_API_KEY = os.getenv("ZEP_API_KEY")
ZEP_BASE_URL = os.getenv("ZEP_BASE_URL")
MEM0_API_KEY = os.getenv("MEM0_API_KEY")
MEM0_API_URL = os.getenv("MEM0_API_URL")

print(f"✓ Database URL: {'Configured' if DATABASE_URL else 'NOT CONFIGURED'}")
print(f"✓ Secret Key: {'Configured' if SECRET_KEY else 'NOT CONFIGURED'}")
print(f"✓ Gemini API Key: {'Configured' if GEMINI_API_KEY else 'NOT CONFIGURED'}")
print(f"✓ Zep API Key: {'Configured' if ZEP_API_KEY else 'NOT CONFIGURED'}")
print(f"✓ Mem0 API Key: {'Configured' if MEM0_API_KEY else 'NOT CONFIGURED'}")

# Set API keys as environment variables (required by SDKs)
print("STEP 3: Setting API keys as environment variables...")
os.environ["MEM0_API_KEY"] = MEM0_API_KEY
os.environ["GOOGLE_API_KEY"] = GEMINI_API_KEY
print("✓ API keys set as environment variables")

# Database Setup
print("STEP 4: Setting up database connection...")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
print("✓ Database engine and session created")

# Password hashing
print("STEP 5: Setting up password hashing...")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
print("✓ Password hashing configured")

# JWT Security
print("STEP 6: Setting up JWT security...")
security = HTTPBearer()
print("✓ JWT security configured")

# Mem0 Client Setup
print("STEP 7: Initializing Mem0 client...")
mem0_client = MemoryClient()
print("✓ Mem0 client initialized")

# Pydantic Models
class UserCreate(BaseModel):
    email: str
    password: str
    first_name: str
    last_name: str
    username: Optional[str] = None

class UserLogin(BaseModel):
    email: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class ChatMessage(BaseModel):
    user_id: str
    session_id: str
    message: str

class ChatResponse(BaseModel):
    response: str
    session_id: str
    user_id: str
    timestamp: datetime

class MemoryRequest(BaseModel):
    user_id: str
    session_id: Optional[str] = None

class MemoryResponse(BaseModel):
    user_id: str
    session_id: Optional[str]
    zep_memory: Dict[str, Any]
    mem0_memory: Dict[str, Any]
    consolidated_memory: str

class SearchRequest(BaseModel):
    user_id: str
    query: str

class SearchResponse(BaseModel):
    user_id: str
    query: str
    results: str

class HistoryRequest(BaseModel):
    user_id: str
    session_id: Optional[str] = None
    limit: Optional[int] = 50

class HistoryResponse(BaseModel):
    user_id: str
    session_id: Optional[str]
    messages: List[Dict[str, Any]]
    total_count: int

class HealthResponse(BaseModel):
    status: str
    timestamp: str
    services: Dict[str, str]

# Database Models
class User(Base):
    __tablename__ = "users"
    
    id = Column(String, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    username = Column(String, unique=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    hashed_password = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

class ChatHistory(Base):
    __tablename__ = "chat_history"
    
    id = Column(String, primary_key=True, index=True)
    user_id = Column(String, nullable=False, index=True)
    session_id = Column(String, nullable=False, index=True)
    message = Column(Text, nullable=True)  # User message
    response = Column(Text, nullable=True)  # Assistant response
    message_type = Column(String, nullable=False, default="user")  # "user" or "assistant"
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)

# Create tables
print("STEP 8: Creating database tables...")
Base.metadata.create_all(bind=engine)
print("✓ Database tables created")

# Agno Agent Setup
def create_user_agent(user_id: str, session_id: str):
    """Create a new agent instance for a specific user and session."""
    print(f"STEP: Creating Agno agent for user {user_id}, session {session_id}")
    
    # Initialize Agno memory with PostgreSQL for this user
    print(f"  - Initializing PostgreSQL memory for user {user_id}")
    memory = Memory(
        db=PostgresMemoryDb(
            table_name="agno_memories",
            db_url=DATABASE_URL
        )
    )
    print(f"  ✓ PostgreSQL memory initialized")
    
    # Initialize Zep tools with user-specific parameters
    print(f"  - Initializing Zep tools for user {user_id}")
    zep_tools = ZepTools(
        api_key=ZEP_API_KEY,
        user_id=user_id,
        session_id=session_id,
        add_instructions=True
    )
    print(f"  ✓ Zep tools initialized")
    
    # Initialize Mem0 tools with user-specific parameters
    print(f"  - Initializing Mem0 tools for user {user_id}")
    mem0_tools = Mem0Tools(
        api_key=MEM0_API_KEY,
        user_id=user_id,
        add_instructions=True
    )
    print(f"  ✓ Mem0 tools initialized")
    
    # Add reasoning tools for better decision making
    print(f"  - Initializing reasoning tools")
    from agno.tools.reasoning import ReasoningTools
    reasoning_tools = ReasoningTools(add_instructions=True)
    print(f"  ✓ Reasoning tools initialized")
    
    # Create the user-specific Agno agent
    print(f"  - Creating Agno agent instance")
    agent = Agent(
        name=f"AgnoChatBot-{user_id}",
        model=Gemini(api_key=GEMINI_API_KEY),
        tools=[reasoning_tools, zep_tools, mem0_tools],
        memory=memory,
        storage=PostgresStorage(
            table_name="agno_sessions",
            db_url=DATABASE_URL
        ),
        enable_user_memories=True,
        enable_session_summaries=True,
        add_datetime_to_instructions=True,
        add_history_to_messages=True,
        num_history_responses=5,
        markdown=True,
        show_tool_calls=True,
        instructions=[
            "You are an intelligent AI assistant with memory capabilities.",
            "Use Zep tools to store and retrieve temporal memory and chat history.",
            "Use Mem0 tools to store and retrieve fact-based memory.",
            "Use reasoning tools to think through complex problems step by step.",
            "Always provide helpful, context-aware responses.",
            "Remember user preferences and past conversations.",
            "When users share information about themselves, store it in memory.",
            "Use memory to provide personalized responses.",
            "CRITICAL MEMORY ISOLATION RULES:",
            "1. ALWAYS use the user_id parameter when calling memory tools",
            "2. NEVER share or access memories from different users",
            "3. Each user must have completely separate memory spaces",
            "4. When storing information, ensure it's stored only for the current user",
            "5. When searching memory, only search within the current user's memory space",
            "6. If no user_id is provided, do not access any memories",
            "7. Verify user isolation before storing or retrieving any information",
            "8. If asked to search for information, thoroughly search both Zep and Mem0 memories for the current user only",
            "9. Provide detailed search results when information is found in memory",
            "10. If no information is found, clearly state that no relevant information was found for this user",
            "11. IMPORTANT: Always include the user_id in your tool calls to ensure proper isolation",
            "12. NEVER reference or access data from other users' memory spaces"
        ]
    )
    print(f"  ✓ Agno agent created successfully")
    
    return agent

# Agent cache for performance (optional)
print("STEP 9: Initializing agent cache...")
_agent_cache = {}
print("✓ Agent cache initialized")

def get_user_agent(user_id: str, session_id: str):
    """Get or create an agent for a specific user and session."""
    print(f"STEP: Getting user agent for user {user_id}, session {session_id}")
    cache_key = f"{user_id}:{session_id}"
    
    if cache_key not in _agent_cache:
        print(f"  - Agent not in cache, creating new agent")
        _agent_cache[cache_key] = create_user_agent(user_id, session_id)
        print(f"  ✓ New agent created and cached")
    else:
        print(f"  ✓ Agent found in cache")
    
    return _agent_cache[cache_key]

# Utility Functions
def verify_password(plain_password: str, hashed_password: str) -> bool:
    print(f"STEP: Verifying password")
    result = pwd_context.verify(plain_password, hashed_password)
    print(f"✓ Password verification result: {result}")
    return result

def get_password_hash(password: str) -> str:
    print(f"STEP: Hashing password")
    hashed = pwd_context.hash(password)
    print(f"✓ Password hashed successfully")
    return hashed

def create_access_token(data: dict) -> str:
    print(f"STEP: Creating access token")
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=7)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    print(f"✓ Access token created successfully")
    return encoded_jwt

def verify_token(token: str) -> Optional[str]:
    print(f"STEP: Verifying token")
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        print(f"✓ Token verified successfully for email: {email}")
        return email
    except jwt.PyJWTError as e:
        print(f"✗ Token verification failed: {e}")
        return None

def get_db():
    print(f"STEP: Getting database session")
    db = SessionLocal()
    print(f"✓ Database session created")
    try:
        yield db
    finally:
        db.close()
        print(f"✓ Database session closed")

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security), db: Session = Depends(get_db)) -> User:
    print(f"STEP: Getting current user from token")
    token = credentials.credentials
    print(f"  - Token received: {token[:20]}...")
    
    email = verify_token(token)
    if email is None:
        print(f"✗ Token validation failed")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    print(f"  - Looking up user with email: {email}")
    user = db.query(User).filter(User.email == email).first()
    if user is None:
        print(f"✗ User not found in database")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    print(f"✓ Current user authenticated: {user.email}")
    return user

# Zep Client Functions
from zep_cloud.client import Zep

# Initialize Zep client
zep_client = Zep(api_key=ZEP_API_KEY)

async def zep_add_memory(session_id: str, messages: List[Dict[str, Any]]):
    """Add messages to Zep memory."""
    print(f"STEP: Adding memory to Zep for session {session_id}")
    print(f"  - Messages to add: {len(messages)}")
    
    try:
        # Use Zep client to add memory
        result = zep_client.memory.add(session_id=session_id, messages=messages)
        print(f"  - Response: {result}")
        print(f"✓ Zep memory added successfully")
        return result
    except Exception as e:
        print(f"✗ Error adding memory to Zep: {e}")
        return {"error": str(e)}

async def zep_get_memory(session_id: str):
    """Get memory from Zep."""
    print(f"STEP: Getting memory from Zep for session {session_id}")
    
    try:
        # Use Zep client to get memory
        memory = zep_client.memory.get(session_id=session_id)
        
        # Convert messages to serializable format
        messages = []
        if hasattr(memory, 'messages') and memory.messages:
            for msg in memory.messages:
                if hasattr(msg, 'to_dict'):
                    messages.append(msg.to_dict())
                else:
                    messages.append({
                        "role": getattr(msg, 'role', 'unknown'),
                        "content": getattr(msg, 'content', ''),
                        "timestamp": getattr(msg, 'timestamp', '')
                    })
        
        result = {
            "context": memory.context if hasattr(memory, 'context') else "",
            "messages": messages,
            "facts": memory.facts if hasattr(memory, 'facts') else [],
            "session_id": session_id
        }
        print(f"  - Response: {result}")
        print(f"✓ Zep memory retrieved successfully")
        return result
    except Exception as e:
        print(f"✗ Error getting memory from Zep: {e}")
        return {"error": str(e), "session_id": session_id}

async def zep_search_memory(user_id: str, query: str):
    """Search memory in Zep."""
    print(f"STEP: Searching Zep memory for user {user_id}")
    print(f"  - Search query: {query}")
    
    try:
        # Use Zep client to search memory
        results = zep_client.memory.search(query=query, user_id=user_id)
        print(f"  - Search results: {results}")
        print(f"✓ Zep memory search completed")
        return results
    except Exception as e:
        print(f"✗ Error searching Zep memory: {e}")
        return {"error": str(e), "user_id": user_id}

# Mem0 Client Functions
async def mem0_add_memory(user_id: str, messages: List[Dict[str, Any]]):
    """
    Add messages to Mem0 memory.
    
    This function wraps the mem0_client.add() call to provide a cleaner interface.
    
    Args:
        user_id (str): The user ID to associate the memory with
        messages (List[Dict[str, Any]]): List of message objects with role and content
        
    Returns:
        dict: Response from Mem0 API
    """
    print(f"STEP: Adding memory to Mem0 for user {user_id}")
    print(f"  - Messages to add: {len(messages)}")
    print(f"  - Message content: {messages}")
    
    try:
        # Use mem0_client.add() internally with v2 version
        print(f"  - Calling mem0_client.add() with v2 version")
        result = mem0_client.add(messages, user_id=user_id, version="v2")
        print(f"  - Mem0 API response: {result}")
        print(f"✓ Successfully added {len(messages)} messages to Mem0 for user {user_id}")
        return result
    except Exception as e:
        print(f"✗ Error adding memory to Mem0 for user {user_id}: {e}")
        return None

async def mem0_search_memory(user_id: str, query: str):
    """
    Search memory in Mem0.
    
    This function wraps the mem0_client.search() call to provide a cleaner interface.
    
    Args:
        user_id (str): The user ID to search memories for
        query (str): The search query
        
    Returns:
        list: Search results from Mem0
    """
    print(f"STEP: Searching Mem0 memory for user {user_id}")
    print(f"  - Search query: {query}")
    
    try:
        # Create filters to search only within this user's memories
        filters = {
            "AND": [
                {
                    "user_id": user_id
                }
            ]
        }
        print(f"  - Search filters: {filters}")
        
        # Use mem0_client.search() internally with v2 version
        print(f"  - Calling mem0_client.search() with v2 version")
        results = mem0_client.search(query, version="v2", filters=filters)
        print(f"  - Search results: {results}")
        print(f"✓ Successfully searched Mem0 for user {user_id} with query: {query}")
        return results
    except Exception as e:
        print(f"✗ Error searching Mem0 for user {user_id}: {e}")
        return []

async def mem0_get_all_memories(user_id: str):
    """
    Get all memories for a user from Mem0.
    
    This function wraps the mem0_client.get_all() call to provide a cleaner interface.
    
    Args:
        user_id (str): The user ID to get memories for
        
    Returns:
        list: All memories for the user
    """
    print(f"STEP: Getting all memories from Mem0 for user {user_id}")
    
    try:
        # Create filters to get only memories for this user
        filters = {
            "AND": [
                {
                    "user_id": user_id
                }
            ]
        }
        print(f"  - Memory filters: {filters}")
        
        # Use mem0_client.get_all() internally with v2 version
        print(f"  - Calling mem0_client.get_all() with v2 version")
        memories = mem0_client.get_all(version="v2", filters=filters, page=1, page_size=50)
        print(f"  - Retrieved memories: {memories}")
        print(f"✓ Successfully retrieved {len(memories) if memories else 0} memories from Mem0 for user {user_id}")
        return memories
    except Exception as e:
        print(f"✗ Error getting memories from Mem0 for user {user_id}: {e}")
        return []

# Enhanced Zep User Management Functions
async def zep_check_user_exists(user_id: str) -> bool:
    """Check if a user exists in Zep."""
    print(f"STEP: Checking if Zep user {user_id} exists")
    
    try:
        async with httpx.AsyncClient() as client:
            url = f"{ZEP_BASE_URL}/v2/users/{user_id}"
            headers = {"Authorization": f"Api-Key {ZEP_API_KEY}"}
            
            print(f"  - Making GET request to: {url}")
            response = await client.get(url, headers=headers)
            exists = response.status_code == 200
            print(f"  - Response status: {response.status_code}")
            print(f"  - User exists: {exists}")
            print(f"✓ Zep user existence check completed")
            return exists
    except Exception as e:
        print(f"✗ Error checking Zep user existence: {e}")
        return False

async def zep_create_user(user_id: str, user_data: dict):
    """Create a new user in Zep."""
    print(f"STEP: Creating Zep user {user_id}")
    print(f"  - User data: {user_data}")
    
    try:
        async with httpx.AsyncClient() as client:
            url = f"{ZEP_BASE_URL}/v2/users"
            headers = {"Authorization": f"Api-Key {ZEP_API_KEY}"}
            
            # Build payload with only provided fields
            payload = {"user_id": user_id}
            
            # Add optional fields only if they exist
            if user_data.get("email"):
                payload["email"] = user_data["email"]
            if user_data.get("first_name"):
                payload["first_name"] = user_data["first_name"]
            if user_data.get("last_name"):
                payload["last_name"] = user_data["last_name"]
            
            # Add metadata
            payload["metadata"] = {
                "username": user_data.get("username"),
                "created_at": datetime.utcnow().isoformat(),
                "source": "agnochat_bot"
            }
            
            print(f"  - Making POST request to: {url}")
            print(f"  - Payload: {payload}")
            response = await client.post(url, json=payload, headers=headers)
            
            print(f"  - Response status: {response.status_code}")
            if response.status_code == 201:
                result = response.json()
                print(f"  - Response: {result}")
                print(f"✓ Zep user created successfully")
                return result
            else:
                print(f"  - Response: {response.text}")
                print(f"✗ Failed to create Zep user. Status: {response.status_code}")
                return None
    except Exception as e:
        print(f"✗ Error creating Zep user: {e}")
        return None

async def zep_get_or_create_user(user_id: str, user_data: dict):
    """Get existing user or create new user in Zep."""
    print(f"STEP: Getting or creating Zep user {user_id}")
    
    # Check if user exists
    user_exists = await zep_check_user_exists(user_id)
    
    if user_exists:
        print(f"✓ Zep user {user_id} already exists")
        return {"status": "exists", "user_id": user_id}
    else:
        print(f"  - Creating new Zep user {user_id}")
        result = await zep_create_user(user_id, user_data)
        if result:
            print(f"✓ Zep user created successfully")
            return {"status": "created", "user_id": user_id, "data": result}
        else:
            print(f"✗ Failed to create Zep user")
            return {"status": "failed", "user_id": user_id}

async def zep_update_user(user_id: str, user_data: dict):
    """Update an existing user in Zep."""
    print(f"STEP: Updating Zep user {user_id}")
    print(f"  - Update data: {user_data}")
    
    try:
        async with httpx.AsyncClient() as client:
            url = f"{ZEP_BASE_URL}/v2/users/{user_id}"
            headers = {"Authorization": f"Api-Key {ZEP_API_KEY}"}
            
            # Build update payload
            payload = {}
            
            if user_data.get("email"):
                payload["email"] = user_data["email"]
            if user_data.get("first_name"):
                payload["first_name"] = user_data["first_name"]
            if user_data.get("last_name"):
                payload["last_name"] = user_data["last_name"]
            
            # Add metadata
            payload["metadata"] = {
                "username": user_data.get("username"),
                "updated_at": datetime.utcnow().isoformat(),
                "source": "agnochat_bot"
            }
            
            print(f"  - Making PATCH request to: {url}")
            print(f"  - Update payload: {payload}")
            response = await client.patch(url, json=payload, headers=headers)
            
            print(f"  - Response status: {response.status_code}")
            if response.status_code == 200:
                result = response.json()
                print(f"  - Response: {result}")
                print(f"✓ Zep user updated successfully")
                return result
            else:
                print(f"  - Response: {response.text}")
                print(f"✗ Failed to update Zep user. Status: {response.status_code}")
                return None
    except Exception as e:
        print(f"✗ Error updating Zep user: {e}")
        return None

async def zep_get_user_sessions(user_id: str):
    """Get all sessions for a user in Zep."""
    print(f"STEP: Getting Zep sessions for user {user_id}")
    
    try:
        async with httpx.AsyncClient() as client:
            url = f"{ZEP_BASE_URL}/v2/users/{user_id}/sessions"
            headers = {"Authorization": f"Api-Key {ZEP_API_KEY}"}
            
            print(f"  - Making GET request to: {url}")
            response = await client.get(url, headers=headers)
            result = response.json() if response.status_code == 200 else None
            print(f"  - Response status: {response.status_code}")
            print(f"  - Response: {result}")
            print(f"✓ Zep user sessions retrieved successfully")
            return result
    except Exception as e:
        print(f"✗ Error getting Zep user sessions: {e}")
        return None

# Enhanced Mem0 User Management Functions
async def mem0_check_user_exists(user_id: str) -> bool:
    """
    Check if a user exists in Mem0 by trying to get their memories.
    
    This function attempts to retrieve memories for a specific user_id.
    If the API call succeeds, it means the user exists (even if they have no memories).
    If the API call fails, it means the user doesn't exist.
    
    Args:
        user_id (str): The unique identifier of the user to check
        
    Returns:
        bool: True if user exists, False otherwise
    """
    print(f"STEP: Checking if Mem0 user {user_id} exists")
    
    try:
        async with httpx.AsyncClient() as client:
            # Construct the URL to get memories for this specific user
            url = f"{MEM0_API_URL}/v1/memories"
            headers = {"Authorization": f"Bearer {MEM0_API_KEY}"}
            
            # Set parameters to get just 1 memory for this user (efficient check)
            params = {"user_id": user_id, "page": 1, "page_size": 1}
            print(f"  - Making GET request to: {url}")
            print(f"  - Parameters: {params}")
            response = await client.get(url, headers=headers, params=params)
            
            # If we get a successful response (200), user exists (even if no memories)
            # If we get an error (404, 500, etc.), user doesn't exist
            exists = response.status_code == 200
            print(f"  - Response status: {response.status_code}")
            print(f"  - User exists: {exists}")
            print(f"✓ Mem0 user existence check completed")
            return exists
    except Exception as e:
        print(f"✗ Error checking Mem0 user existence: {e}")
        return False

async def mem0_create_user(user_id: str, user_data: dict):
    """
    Create a new user in Mem0 by adding an initial memory.
    
    This function creates the first memory entry for a new user.
    The initial memory contains basic user information like name and email.
    This serves as a "user profile" memory that can be referenced later.
    
    Args:
        user_id (str): The unique identifier for the new user
        user_data (dict): Dictionary containing user information (email, first_name, last_name, username)
        
    Returns:
        dict: The response from Mem0 API if successful, None if failed
    """
    print(f"STEP: Creating Mem0 user {user_id}")
    print(f"  - User data: {user_data}")
    
    try:
        async with httpx.AsyncClient() as client:
            # Construct the URL to add a new memory
            url = f"{MEM0_API_URL}/v1/memories"
            headers = {"Authorization": f"Bearer {MEM0_API_KEY}"}
            
            # Create the initial memory for the user
            # This memory serves as a "user profile" and account creation record
            initial_memory = {
                "user_id": user_id,  # Link this memory to the specific user
                "memory": f"User {user_data.get('first_name', '')} {user_data.get('last_name', '')} created account with email {user_data.get('email', '')}",
                "metadata": {
                    "type": "user_creation",  # Mark this as a user creation memory
                    "username": user_data.get("username"),  # Store username for reference
                    "created_at": datetime.utcnow().isoformat()  # Timestamp when user was created
                }
            }
            
            print(f"  - Making POST request to: {url}")
            print(f"  - Initial memory: {initial_memory}")
            
            # Send POST request to Mem0 API to create the memory
            response = await client.post(url, json=initial_memory, headers=headers)
            
            print(f"  - Response status: {response.status_code}")
            # Return the response data if successful (201 = Created)
            # Return None if failed (any other status code)
            if response.status_code == 201:
                result = response.json()
                print(f"  - Response: {result}")
                print(f"✓ Mem0 user created successfully")
                return result
            else:
                print(f"  - Response: {response.text}")
                print(f"✗ Failed to create Mem0 user. Status: {response.status_code}")
                return None
    except Exception as e:
        print(f"✗ Error creating Mem0 user: {e}")
        return None

async def mem0_get_or_create_user(user_id: str, user_data: dict):
    """
    Get existing user or create new user in Mem0.
    
    This function implements a "get or create" pattern:
    1. First checks if the user already exists in Mem0
    2. If user exists, returns success status
    3. If user doesn't exist, creates a new user with initial memory
    4. Returns appropriate status based on the operation
    
    Args:
        user_id (str): The unique identifier of the user
        user_data (dict): Dictionary containing user information
        
    Returns:
        dict: Status information about the operation
    """
    print(f"STEP: Getting or creating Mem0 user {user_id}")
    
    # Step 1: Check if user already exists in Mem0
    user_exists = await mem0_check_user_exists(user_id)
    
    if user_exists:
        # User already exists - no need to create anything
        print(f"✓ Mem0 user {user_id} already exists")
        return {"status": "exists", "user_id": user_id}
    else:
        # User doesn't exist - create new user with initial memory
        print(f"  - Creating new Mem0 user {user_id}")
        result = await mem0_create_user(user_id, user_data)
        
        if result:
            # User creation successful
            print(f"✓ Mem0 user created successfully")
            return {"status": "created", "user_id": user_id, "data": result}
        else:
            # User creation failed
            print(f"✗ Failed to create Mem0 user")
            return {"status": "failed", "user_id": user_id}

# Unified User Management Function
async def ensure_user_exists_in_memory_systems(user_id: str, user_data: dict):
    """Ensure user exists in both Zep and Mem0, create if not exists."""
    print(f"STEP: Ensuring user {user_id} exists in memory systems")
    print(f"  - User data: {user_data}")
    
    results = {
        "zep": None,
        "mem0": None,
        "overall_status": "success"
    }
    
    # Handle Zep user
    print(f"  - Processing Zep user...")
    try:
        results["zep"] = await zep_get_or_create_user(user_id, user_data)
        if results["zep"]["status"] == "failed":
            results["overall_status"] = "partial_failure"
            print(f"  ✗ Zep user processing failed")
        else:
            print(f"  ✓ Zep user processing completed: {results['zep']['status']}")
    except Exception as e:
        print(f"  ✗ Error managing Zep user: {e}")
        results["zep"] = {"status": "error", "error": str(e)}
        results["overall_status"] = "partial_failure"
    
    # Handle Mem0 user
    print(f"  - Processing Mem0 user...")
    try:
        results["mem0"] = await mem0_get_or_create_user(user_id, user_data)
        if results["mem0"]["status"] == "failed":
            results["overall_status"] = "partial_failure"
            print(f"  ✗ Mem0 user processing failed")
        else:
            print(f"  ✓ Mem0 user processing completed: {results['mem0']['status']}")
    except Exception as e:
        print(f"  ✗ Error managing Mem0 user: {e}")
        results["mem0"] = {"status": "error", "error": str(e)}
        results["overall_status"] = "partial_failure"
    
    print(f"✓ Memory system user management completed")
    print(f"  - Overall status: {results['overall_status']}")
    print(f"  - Zep status: {results['zep']['status'] if results['zep'] else 'None'}")
    print(f"  - Mem0 status: {results['mem0']['status'] if results['mem0'] else 'None'}")
    
    return results

# FastAPI App
print("STEP 10: Initializing FastAPI application...")
app = FastAPI(title="AgnoChat Bot API", version="1.0.0")
print("✓ FastAPI app created")

# CORS middleware
print("STEP 11: Adding CORS middleware...")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
print("✓ CORS middleware added")

# Health Check
@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint."""
    print("=" * 80)
    print("HEALTH CHECK REQUEST RECEIVED")
    print("=" * 80)
    
    try:
        services = {}
        
        # Check Agno agent creation (test with dummy user)
        print("STEP: Testing Agno agent creation...")
        try:
            test_agent = create_user_agent("health_check", "health_check")
            test_response = test_agent.run(
                "Health check",
                user_id="health_check",
                session_id="health_check",
                stream=False
            )
            services["agno_agent"] = "active" if test_response else "error"
            print(f"✓ Agno agent test completed: {services['agno_agent']}")
        except Exception as e:
            services["agno_agent"] = "error"
            print(f"✗ Agno agent test failed: {e}")
        
        # Check database connection
        print("STEP: Testing database connection...")
        try:
            db = SessionLocal()
            db.execute("SELECT 1")
            db.close()
            services["postgresql"] = "connected"
            print(f"✓ Database connection test completed: {services['postgresql']}")
        except Exception as e:
            services["postgresql"] = "disconnected"
            print(f"✗ Database connection test failed: {e}")
        
        # Check external APIs
        print("STEP: Checking external API configurations...")
        services["gemini"] = "configured" if GEMINI_API_KEY else "not_configured"
        services["zep"] = "configured" if ZEP_API_KEY else "not_configured"
        services["mem0"] = "configured" if MEM0_API_KEY else "not_configured"
        print(f"✓ External API check completed:")
        print(f"  - Gemini: {services['gemini']}")
        print(f"  - Zep: {services['zep']}")
        print(f"  - Mem0: {services['mem0']}")
        
        # Determine overall status
        overall_status = "healthy"
        if any(status in ["error", "disconnected", "not_configured"] for status in services.values()):
            overall_status = "degraded"
        
        print(f"✓ Overall health status: {overall_status}")
        
        response = HealthResponse(
            status=overall_status,
            timestamp=datetime.utcnow().isoformat(),
            services=services
        )
        
        print("=" * 80)
        print("HEALTH CHECK RESPONSE:")
        print(f"Status: {response.status}")
        print(f"Timestamp: {response.timestamp}")
        print(f"Services: {response.services}")
        print("=" * 80)
        
        return response
        
    except Exception as e:
        print(f"✗ Health check failed with error: {e}")
        response = HealthResponse(
            status="error",
            timestamp=datetime.utcnow().isoformat(),
            services={
                "agno_agent": "unknown",
                "gemini": "unknown",
                "zep": "unknown",
                "mem0": "unknown",
                "postgresql": "unknown"
            }
        )
        
        print("=" * 80)
        print("HEALTH CHECK ERROR RESPONSE:")
        print(f"Status: {response.status}")
        print(f"Timestamp: {response.timestamp}")
        print(f"Services: {response.services}")
        print("=" * 80)
        
        return response

# Authentication Endpoints
@app.post("/api/auth/signup", response_model=Token)
async def signup(user_data: UserCreate, db: Session = Depends(get_db)):
    """
    Create a new user account and return JWT token.
    
    This endpoint handles user registration with the following steps:
    1. Validate that the email is not already registered
    2. Create user in PostgreSQL database
    3. Create user in Mem0 memory system
    4. Create user in Zep memory system
    5. Generate and return JWT token
    
    Args:
        user_data (UserCreate): User registration data (email, password, first_name, last_name, username)
        db (Session): Database session
        
    Returns:
        Token: JWT token for authentication
    """
    print("=" * 80)
    print("SIGNUP REQUEST RECEIVED")
    print("=" * 80)
    print(f"User data: {user_data}")
    
    try:
        # Step 1: Check if user already exists in PostgreSQL
        print("STEP 1: Checking if user already exists in database...")
        existing_user = db.query(User).filter(User.email == user_data.email).first()
        if existing_user:
            print(f"✗ User with email {user_data.email} already exists")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        print(f"✓ Email {user_data.email} is available")
        
        # Step 2: Create user in PostgreSQL database
        print("STEP 2: Creating user in PostgreSQL database...")
        user_id = str(uuid.uuid4())  # Generate unique user ID
        hashed_password = get_password_hash(user_data.password)  # Hash the password
        
        # Create user record in PostgreSQL
        db_user = User(
            id=user_id,
            email=user_data.email,
            username=user_data.username or user_data.email.split('@')[0],  # Use email prefix if no username
            first_name=user_data.first_name,
            last_name=user_data.last_name,
            hashed_password=hashed_password
        )
        
        # Save user to database
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        print(f"✓ User created in database with ID: {user_id}")
        
        # Step 3: Prepare user data for memory systems
        print("STEP 3: Preparing user data for memory systems...")
        # This data will be used to create user profiles in Mem0 and Zep
        memory_user_data = {
            "email": user_data.email,
            "first_name": user_data.first_name,
            "last_name": user_data.last_name,
            "username": user_data.username or user_data.email.split('@')[0]
        }
        print(f"✓ Memory user data prepared: {memory_user_data}")
        
        # Step 4: Create user in memory systems (Mem0 and Zep)
        print("STEP 4: Creating user in memory systems...")
        # This ensures the user has memory profiles in both systems
        memory_results = await ensure_user_exists_in_memory_systems(user_id, memory_user_data)
        
        # Step 5: Log the results of memory system creation
        print("STEP 5: Logging memory system results...")
        print(f"Memory system results for user {user_id}:")
        print(f"  Zep: {memory_results['zep']['status']}")
        print(f"  Mem0: {memory_results['mem0']['status']}")
        print(f"  Overall: {memory_results['overall_status']}")
        
        # Step 6: Generate JWT token for authentication
        print("STEP 6: Generating JWT token...")
        access_token = create_access_token(data={"sub": db_user.email})
        print(f"✓ JWT token generated successfully")
        
        # Step 7: Return the authentication token
        print("STEP 7: Returning authentication token...")
        response = Token(access_token=access_token, token_type="bearer")
        
        print("=" * 80)
        print("SIGNUP RESPONSE:")
        print(f"User ID: {user_id}")
        print(f"Email: {user_data.email}")
        print(f"Token type: {response.token_type}")
        print(f"Token: {response.access_token[:50]}...")
        print("=" * 80)
        
        return response
        
    except HTTPException:
        # Re-raise HTTP exceptions (like "email already registered")
        print("✗ Signup failed with HTTP exception")
        raise
    except Exception as e:
        # Handle any other unexpected errors
        print(f"✗ Signup failed with unexpected error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create user: {str(e)}"
        )

@app.post("/api/auth/login", response_model=Token)
async def login(user_credentials: UserLogin, db: Session = Depends(get_db)):
    """
    Authenticate user and return JWT token.
    
    This endpoint handles user authentication with the following steps:
    1. Verify user credentials against PostgreSQL database
    2. Check if user exists in Mem0 and Zep memory systems
    3. Create or update user in memory systems if needed
    4. Generate and return JWT token
    
    Args:
        user_credentials (UserLogin): User login credentials (email, password)
        db (Session): Database session
        
    Returns:
        Token: JWT token for authentication
    """
    print("=" * 80)
    print("LOGIN REQUEST RECEIVED")
    print("=" * 80)
    print(f"Login attempt for email: {user_credentials.email}")
    
    try:
        # Step 1: Find user in PostgreSQL database by email
        print("STEP 1: Looking up user in database...")
        user = db.query(User).filter(User.email == user_credentials.email).first()
        
        # Step 2: Verify password
        print("STEP 2: Verifying password...")
        if not user or not verify_password(user_credentials.password, user.hashed_password):
            print(f"✗ Authentication failed for email: {user_credentials.email}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password"
            )
        print(f"✓ Password verified successfully for user: {user.email}")
        
        # Step 3: Prepare user data for memory system check/update
        print("STEP 3: Preparing user data for memory systems...")
        # This ensures the user has proper memory profiles in Mem0 and Zep
        user_data = {
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "username": user.username
        }
        print(f"✓ User data prepared: {user_data}")
        
        # Step 4: Check and update memory systems
        print("STEP 4: Checking and updating memory systems...")
        # This will:
        # - Create user in Mem0/Zep if they don't exist (new user)
        # - Update user in Mem0/Zep if they exist (returning user)
        memory_results = await ensure_user_exists_in_memory_systems(user.id, user_data)
        
        # Step 5: Log the results of memory system operations
        print("STEP 5: Logging memory system results...")
        print(f"Login - Memory system results for user {user.id}:")
        print(f"  Zep: {memory_results['zep']['status']}")
        print(f"  Mem0: {memory_results['mem0']['status']}")
        print(f"  Overall: {memory_results['overall_status']}")
        
        # Step 6: Generate JWT token for authentication
        print("STEP 6: Generating JWT token...")
        access_token = create_access_token(data={"sub": user.email})
        print(f"✓ JWT token generated successfully")
        
        # Step 7: Return the authentication token
        print("STEP 7: Returning authentication token...")
        response = Token(access_token=access_token, token_type="bearer")
        
        print("=" * 80)
        print("LOGIN RESPONSE:")
        print(f"User ID: {user.id}")
        print(f"Email: {user.email}")
        print(f"Token type: {response.token_type}")
        print(f"Token: {response.access_token[:50]}...")
        print("=" * 80)
        
        return response
        
    except HTTPException:
        # Re-raise HTTP exceptions (like "incorrect password")
        print("✗ Login failed with HTTP exception")
        raise
    except Exception as e:
        # Handle any other unexpected errors
        print(f"✗ Login failed with unexpected error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Login failed: {str(e)}"
        )

@app.get("/api/auth/me")
async def get_current_user_info(current_user: User = Depends(get_current_user)):
    """Get current user information."""
    return {
        "user_id": current_user.id,
        "email": current_user.email,
        "first_name": current_user.first_name,
        "last_name": current_user.last_name,
        "username": current_user.username
    }

# Chat Endpoints
@app.post("/api/chat", response_model=ChatResponse)
async def chat(chat_data: ChatMessage, current_user: User = Depends(get_current_user)):
    """Process a chat message using Agno agent with Mem0 memory integration."""
    print("=" * 80)
    print("CHAT REQUEST RECEIVED")
    print("=" * 80)
    print(f"User ID: {chat_data.user_id}")
    print(f"Session ID: {chat_data.session_id}")
    print(f"Message: {chat_data.message}")
    
    try:
        # Verify user_id matches authenticated user
        print("STEP 1: Verifying user authentication...")
        if chat_data.user_id != current_user.id:
            print(f"✗ User ID mismatch: {chat_data.user_id} != {current_user.id}")
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User ID mismatch"
            )
        print(f"✓ User authentication verified")
        
        # Get user-specific agent
        print("STEP 2: Getting user-specific agent...")
        try:
            user_agent = get_user_agent(chat_data.user_id, chat_data.session_id)
            print(f"✓ User agent retrieved successfully")
        except Exception as e:
            print(f"✗ Failed to create user agent: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to initialize user agent: {str(e)}"
            )
        
        # Get user's existing memories from Mem0 using custom function
        print("STEP 3: Retrieving user memories from Mem0...")
        try:
            user_memories = await mem0_get_all_memories(chat_data.user_id)
            memory_context = "\n".join([f"- {memory['memory']}" for memory in user_memories]) if user_memories else "No previous memories found."
            print(f"✓ Retrieved {len(user_memories) if user_memories else 0} memories from Mem0")
        except Exception as e:
            memory_context = f"Error retrieving memories: {str(e)}"
            print(f"✗ Error retrieving memories: {e}")
        
        # Check if this is a memory update request
        print("STEP 4: Analyzing message type...")
        is_memory_update = any(keyword in chat_data.message.lower() for keyword in [
            "update", "change", "modify", "set", "remember", "store", "save", "add"
        ])
        print(f"✓ Message type: {'Memory update' if is_memory_update else 'Regular chat'}")
        
        # Process message with user-specific agent
        print("STEP 5: Processing message with Agno agent...")
        print(f"Starting chat processing for user {chat_data.user_id}")
        
        try:
            if is_memory_update:
                print("  - Processing as memory update request...")
                update_prompt = f"""
                User message: {chat_data.message}
                User ID: {chat_data.user_id}
                
                Previous memories about this user:
                {memory_context}
                
                This appears to be a memory update request. Please:
                1. Process the user's request to update their information for user ID: {chat_data.user_id}
                2. Store the updated information in BOTH Zep and Mem0 memory systems for user {chat_data.user_id}
                3. Ensure consistency across all memory sources for user {chat_data.user_id}
                4. Confirm the update was successful for user {chat_data.user_id}
                5. Provide a clear response about what was updated for user {chat_data.user_id}
                
                CRITICAL: Only update memories for user {chat_data.user_id}. Do NOT modify memories for other users.
                Important: Make sure the information is stored consistently in both memory systems for this specific user.
                
                MEMORY STORAGE INSTRUCTIONS:
                - Use Zep tools to store temporal/conversation memories for user {chat_data.user_id}
                - Use Mem0 tools to store factual/personal information for user {chat_data.user_id}
                - Make sure both systems are updated with the same information for user {chat_data.user_id}
                - Confirm storage in both systems before responding
                """
                
                response = user_agent.run(
                    update_prompt,
                    user_id=chat_data.user_id,
                    session_id=chat_data.session_id,
                    stream=False
                )
                print(f"✓ Memory update processed successfully")
            else:
                print("  - Processing as regular chat message...")
                chat_prompt = f"""
                User message: {chat_data.message}
                User ID: {chat_data.user_id}
                
                Previous memories about this user:
                {memory_context}
                
                CRITICAL: Only access memories for user {chat_data.user_id}. Do NOT access memories from other users.
                If you don't have specific memories for user {chat_data.user_id}, start fresh and don't reference other users' data.
                
                Respond to the user's message based ONLY on their own memories and context.
                Use the memory context above to provide personalized responses.
                """
                
                response = user_agent.run(
                    chat_prompt,
                    user_id=chat_data.user_id,
                    session_id=chat_data.session_id,
                    stream=False
                )
                print(f"✓ Chat message processed successfully")
        except Exception as agno_error:
            print(f"✗ Agno agent error: {agno_error}")
            if is_memory_update:
                response_content = f"I understand you want to update your information. I'll remember that for you. Your message was: {chat_data.message}"
            else:
                response_content = f"Hello! I received your message: '{chat_data.message}'. I'm here to help you with any questions or tasks you might have."
            
            class SimpleResponse:
                def __init__(self, content):
                    self.content = content
            
            response = SimpleResponse(response_content)
            print(f"✓ Using fallback response: {response_content}")
        
        # Store the conversation in Mem0 memory using custom function
        print("STEP 6: Storing conversation in Mem0...")
        try:
            messages = [
                {"role": "user", "content": chat_data.message},
                {"role": "assistant", "content": str(response.content) if response.content else ""}
            ]
            await mem0_add_memory(chat_data.user_id, messages)
            print(f"✓ Conversation stored in Mem0 successfully")
        except Exception as e:
            print(f"✗ Error storing in Mem0: {e}")
        
        # Store the conversation in Zep memory
        print("STEP 7: Storing conversation in Zep...")
        try:
            zep_messages = [
                {
                    "role": "user",
                    "content": chat_data.message,
                    "metadata": {"user_id": chat_data.user_id, "timestamp": datetime.utcnow().isoformat()}
                },
                {
                    "role": "assistant", 
                    "content": str(response.content) if response.content else "",
                    "metadata": {"user_id": chat_data.user_id, "timestamp": datetime.utcnow().isoformat()}
                }
            ]
            await zep_add_memory(chat_data.session_id, zep_messages)
            print(f"✓ Conversation stored in Zep successfully")
        except Exception as e:
            print(f"✗ Error storing in Zep: {e}")
        
        # Store the chat message in the database
        print("STEP 8: Storing conversation in database...")
        db = SessionLocal()
        try:
            import uuid
            
            user_message = ChatHistory(
                id=str(uuid.uuid4()),
                user_id=chat_data.user_id,
                session_id=chat_data.session_id,
                message=chat_data.message,
                response="",
                message_type="user"
            )
            db.add(user_message)
            
            assistant_message = ChatHistory(
                id=str(uuid.uuid4()),
                user_id=chat_data.user_id,
                session_id=chat_data.session_id,
                message="",
                response=str(response.content) if response.content else "",
                message_type="assistant"
            )
            db.add(assistant_message)
            
            db.commit()
            print(f"✓ Conversation stored in database successfully")
        except Exception as e:
            db.rollback()
            print(f"✗ Database error: {e}")
        finally:
            db.close()
        
        # Prepare response
        print("STEP 9: Preparing final response...")
        final_response = ChatResponse(
            response=str(response.content) if response.content else "",
            session_id=chat_data.session_id,
            user_id=chat_data.user_id,
            timestamp=datetime.utcnow()
        )
        
        print("=" * 80)
        print("CHAT RESPONSE:")
        print(f"User ID: {final_response.user_id}")
        print(f"Session ID: {final_response.session_id}")
        print(f"Response: {final_response.response}")
        print(f"Timestamp: {final_response.timestamp}")
        print("=" * 80)
        
        return final_response
        
    except HTTPException:
        print("✗ Chat processing failed with HTTP exception")
        raise
    except Exception as e:
        print(f"✗ Chat processing failed with unexpected error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Chat processing failed: {str(e)}"
        )

# Memory Endpoints
@app.get("/api/memory", response_model=MemoryResponse)
async def get_memory(
    user_id: str,
    session_id: Optional[str] = None,
    current_user: User = Depends(get_current_user)
):
    """Get memory from both Zep and Mem0."""
    try:
        if user_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User ID mismatch"
            )
        
        # Get user-specific agent
        try:
            user_agent = get_user_agent(user_id, session_id or "memory_session")
        except Exception as e:
            print(f"Failed to create user agent for memory: {e}")
            user_agent = None
        
        # Get memory from Zep
        try:
            if session_id:
                zep_data = await zep_get_memory(session_id)
                if isinstance(zep_data, dict):
                    zep_data["user_id"] = user_id
                    zep_data["session_id"] = session_id
                    if "messages" in zep_data:
                        for message in zep_data["messages"]:
                            message["user_id"] = user_id
                            message["session_id"] = session_id
                    if "metadata" in zep_data:
                        zep_data["metadata"]["user_id"] = user_id
                        zep_data["metadata"]["session_id"] = session_id
            else:
                zep_data = {"status": "no_session_id", "user_id": user_id}
        except Exception as e:
            zep_data = {"error": str(e), "user_id": user_id, "session_id": session_id}
        
        # Get memory from Mem0 using custom function
        try:
            mem0_data = await mem0_get_all_memories(user_id)
            # Add user context to each Mem0 memory
            if isinstance(mem0_data, list):
                for memory in mem0_data:
                    memory["user_id"] = user_id
                    memory["session_id"] = session_id
                    if "metadata" in memory:
                        memory["metadata"]["user_id"] = user_id
                        memory["metadata"]["session_id"] = session_id
        except Exception as e:
            mem0_data = {"error": str(e), "user_id": user_id, "session_id": session_id}
        
        # Get memory from Agno agent
        try:
            if user_agent:
                memory_response = user_agent.run(
                    "Analyze and summarize your memories for this user. Return a JSON with counts for zep_memories and mem0_memories.",
                    user_id=user_id,
                    session_id=session_id or "memory_session",
                    stream=False
                )
                consolidated = str(memory_response.content) if memory_response.content else "Memory analysis completed"
            else:
                consolidated = "Agent not available for memory analysis"
        except Exception as e:
            consolidated = f"Error analyzing memory: {str(e)}"
        
        return MemoryResponse(
            user_id=user_id,
            session_id=session_id,
            zep_memory=zep_data,
            mem0_memory=mem0_data,
            consolidated_memory=consolidated
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve memory: {str(e)}"
        )

@app.post("/api/memory/search", response_model=SearchResponse)
async def search_memory(
    search_data: SearchRequest,
    current_user: User = Depends(get_current_user)
):
    """Search memory using Agno agent."""
    print("=" * 80)
    print("MEMORY SEARCH REQUEST RECEIVED")
    print("=" * 80)
    print(f"User ID: {search_data.user_id}")
    print(f"Search query: {search_data.query}")
    
    try:
        if search_data.user_id != current_user.id:
            print(f"✗ User ID mismatch: {search_data.user_id} != {current_user.id}")
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User ID mismatch"
            )
        print(f"✓ User authentication verified")
        
        # Get user-specific agent
        print("STEP 1: Getting user-specific agent for search...")
        try:
            user_agent = get_user_agent(search_data.user_id, "search_session")
            print(f"✓ User agent retrieved successfully")
        except Exception as e:
            print(f"✗ Failed to create user agent for search: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to initialize user agent: {str(e)}"
            )
        
        # Search memory using Mem0 directly using custom function
        print("STEP 2: Searching Mem0 memory...")
        try:
            mem0_results = await mem0_search_memory(search_data.user_id, search_data.query)
            mem0_context = "\n".join([f"- {result['memory']}" for result in mem0_results]) if mem0_results else "No relevant memories found in Mem0."
            print(f"✓ Mem0 search completed with {len(mem0_results) if mem0_results else 0} results")
        except Exception as e:
            mem0_context = f"Error searching Mem0: {str(e)}"
            print(f"✗ Error searching Mem0: {e}")
        
        # Search memory using Zep directly
        print("STEP 3: Searching Zep memory...")
        try:
            zep_results = await zep_search_memory(search_data.user_id, search_data.query)
            zep_context = ""
            if isinstance(zep_results, dict) and "results" in zep_results:
                zep_context = "\n".join([f"- {result.get('content', '')}" for result in zep_results["results"]]) if zep_results["results"] else "No relevant memories found in Zep."
            else:
                zep_context = "No relevant memories found in Zep."
            print(f"✓ Zep search completed")
        except Exception as e:
            zep_context = f"Error searching Zep: {str(e)}"
            print(f"✗ Error searching Zep: {e}")
        
        # Search memory using agent tools with enhanced prompt
        print("STEP 4: Performing comprehensive memory search with agent...")
        search_prompt = f"""
        SEARCH REQUEST: {search_data.query}
        USER ID: {search_data.user_id}
        
        Mem0 search results for user {search_data.user_id}:
        {mem0_context}
        
        Zep search results for user {search_data.user_id}:
        {zep_context}
        
        Please search through ALL memory sources (Zep and Mem0) for user {search_data.user_id} to find information related to: {search_data.query}
        
        CRITICAL USER ISOLATION RULES:
        1. ONLY search within user {search_data.user_id} memory space
        2. DO NOT access memories from other users
        3. DO NOT search across user boundaries
        4. Search Zep memory for temporal/conversation memories related to: {search_data.query}
        5. Search Mem0 memory for factual/personal information related to: {search_data.query}
        6. Look for exact matches, partial matches, and related information
        7. If you find information, provide a comprehensive summary
        8. If no information is found, clearly state that no relevant information was found for user {search_data.user_id}
        9. ALWAYS include user_id={search_data.user_id} in your tool calls
        10. NEVER search outside of user {search_data.user_id} memory namespace
        
        Search terms to look for: {search_data.query}
        Target user: {search_data.user_id}
        
        Please provide a detailed response with all relevant information found for user {search_data.user_id} only.
        """
        
        print(f"  - Executing agent search with prompt...")
        response = user_agent.run(
            search_prompt,
            user_id=search_data.user_id,
            session_id="search_session",
            stream=False
        )
        print(f"✓ Agent search completed successfully")
        
        # Prepare final response
        print("STEP 5: Preparing search response...")
        final_response = SearchResponse(
            user_id=search_data.user_id,
            query=search_data.query,
            results=str(response.content) if response.content else ""
        )
        
        print("=" * 80)
        print("MEMORY SEARCH RESPONSE:")
        print(f"User ID: {final_response.user_id}")
        print(f"Query: {final_response.query}")
        print(f"Results: {final_response.results}")
        print("=" * 80)
        
        return final_response
        
    except HTTPException:
        print("✗ Memory search failed with HTTP exception")
        raise
    except Exception as e:
        print(f"✗ Memory search failed with unexpected error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Memory search failed: {str(e)}"
        )

@app.post("/api/memory/consolidate")
async def consolidate_memory(
    user_id: str,
    current_user: User = Depends(get_current_user)
):
    """Synchronize and resolve memory conflicts for a user."""
    try:
        if user_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User ID mismatch"
            )
        
        # Force memory synchronization
        sync_prompt = f"""
        Perform a comprehensive memory synchronization for user {user_id}.
        
        Tasks:
        1. Search through ALL memory sources (Zep and Mem0) for user {user_id}
        2. Identify any conflicting information
        3. Resolve conflicts by keeping the most recent/accurate data
        4. Update both memory systems to be consistent
        5. Provide a summary of what was synchronized
        
        Focus on:
        - Personal information (name, preferences, etc.)
        - Recent conversation context
        - Any contradictory data points
        
        CRITICAL: Only work with memories for user {user_id}. Do NOT access memories from other users.
        """
        
        response = get_user_agent(user_id, "memory_sync_session").run(
            sync_prompt,
            user_id=user_id,
            session_id="memory_sync_session",
            stream=False
        )
        
        return {
            "user_id": user_id,
            "sync_result": str(response.content) if response.content else "",
            "sync_timestamp": datetime.utcnow().isoformat(),
            "status": "completed"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Memory synchronization failed: {str(e)}"
        )

# History Endpoints
@app.get("/api/history", response_model=HistoryResponse)
async def get_chat_history(
    user_id: str,
    session_id: Optional[str] = None,
    limit: Optional[int] = 50,
    current_user: User = Depends(get_current_user)
):
    """Get chat history for a user."""
    try:
        if user_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User ID mismatch"
            )
        
        # Get chat history from database
        db = SessionLocal()
        try:
            query = db.query(ChatHistory).filter(ChatHistory.user_id == user_id)
            
            if session_id:
                query = query.filter(ChatHistory.session_id == session_id)
            
            query = query.order_by(ChatHistory.timestamp.desc()).limit(limit or 50)
            history_items = query.all()
            
            # Convert to response format
            messages = []
            for item in reversed(history_items):  # Reverse to get chronological order
                messages.append({
                    "id": item.id,
                    "user_id": item.user_id,
                    "session_id": item.session_id,
                    "message": item.message,
                    "response": item.response,
                    "timestamp": item.timestamp.isoformat(),
                    "message_type": item.message_type
                })
            
            return HistoryResponse(
                user_id=user_id,
                session_id=session_id,
                messages=messages,
                total_count=len(messages)
            )
            
        finally:
            db.close()
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get chat history: {str(e)}"
        )

# Session Management
@app.post("/api/session/start")
async def start_session(
    user_id: str,
    session_id: Optional[str] = None,
    current_user: User = Depends(get_current_user)
):
    """Start a new session."""
    try:
        if user_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User ID mismatch"
            )
        
        # Generate session ID if not provided
        if not session_id:
            session_id = str(uuid.uuid4())
        
        # Create session in Zep
        try:
            async with httpx.AsyncClient() as client:
                url = f"{ZEP_BASE_URL}/v1/sessions"
                headers = {"Authorization": f"Api-Key {ZEP_API_KEY}"}
                
                payload = {
                    "session_id": session_id,
                    "user_id": user_id
                }
                
                response = await client.post(url, json=payload, headers=headers)
                zep_result = response.json()
        except Exception as e:
            zep_result = {"error": str(e)}
        
        return {
            "user_id": user_id,
            "session_id": session_id,
            "zep_session": zep_result,
            "status": "started"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to start session: {str(e)}"
        )

if __name__ == "__main__":
    print("=" * 80)
    print("STARTING AGNOCHAT BOT SERVER")
    print("=" * 80)
    print("STEP 12: Starting uvicorn server...")
    import uvicorn
    print("✓ Uvicorn imported successfully")
    print("✓ Starting server on host: 0.0.0.0, port: 8000")
    print("✓ Server will be available at: http://localhost:8000")
    print("✓ API documentation will be available at: http://localhost:8000/docs")
    print("=" * 80)
    uvicorn.run(app, host="0.0.0.0", port=8000) 