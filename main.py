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

# Load environment variables from .env file
load_dotenv()

# Environment Configuration
DATABASE_URL = os.getenv("DATABASE_URL")
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
ZEP_API_KEY = os.getenv("ZEP_API_KEY")
ZEP_BASE_URL = os.getenv("ZEP_BASE_URL")
MEM0_API_KEY = os.getenv("MEM0_API_KEY")
MEM0_API_URL = os.getenv("MEM0_API_URL")

# Set API keys as environment variables (required by SDKs)
os.environ["MEM0_API_KEY"] = MEM0_API_KEY
os.environ["GOOGLE_API_KEY"] = GEMINI_API_KEY

# Database Setup
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT Security
security = HTTPBearer()

# Mem0 Client Setup
mem0_client = MemoryClient()

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
Base.metadata.create_all(bind=engine)

# Agno Agent Setup
def create_agno_agent():
    """Create the main AgnoChat Bot agent with memory and tools."""
    
    # Initialize Agno memory with PostgreSQL
    memory = Memory(
        db=PostgresMemoryDb(
            table_name="agno_memories",
            db_url=DATABASE_URL
        )
    )
    
    # Initialize Zep tools
    zep_tools = ZepTools(
        api_key=ZEP_API_KEY,
        add_instructions=True
    )
    
    # Initialize Mem0 tools
    mem0_tools = Mem0Tools(
        api_key=MEM0_API_KEY,
        add_instructions=True
    )
    
    # Create the main Agno agent
    agent = Agent(
        name="AgnoChatBot",
        model=Gemini(api_key=GEMINI_API_KEY),
        tools=[zep_tools, mem0_tools],
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
    
    return agent

# Initialize Agno agent
try:
    agno_agent = create_agno_agent()
    print("Agno agent initialized successfully")
except Exception as e:
    print(f"Failed to initialize Agno agent: {e}")
    agno_agent = None

# Utility Functions
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=7)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str) -> Optional[str]:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        return email
    except jwt.PyJWTError:
        return None

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security), db: Session = Depends(get_db)) -> User:
    token = credentials.credentials
    email = verify_token(token)
    if email is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    user = db.query(User).filter(User.email == email).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return user

# Zep Client Functions
async def zep_add_memory(session_id: str, messages: List[Dict[str, Any]]):
    """Add messages to Zep memory."""
    async with httpx.AsyncClient() as client:
        url = f"{ZEP_BASE_URL}/v1/sessions/{session_id}/memory"
        headers = {"Authorization": f"Bearer {ZEP_API_KEY}"}
        
        payload = {
            "messages": messages
        }
        
        response = await client.post(url, json=payload, headers=headers)
        return response.json()

async def zep_get_memory(session_id: str):
    """Get memory from Zep."""
    async with httpx.AsyncClient() as client:
        url = f"{ZEP_BASE_URL}/v1/sessions/{session_id}/memory"
        headers = {"Authorization": f"Bearer {ZEP_API_KEY}"}
        
        response = await client.get(url, headers=headers)
        return response.json()

async def zep_search_memory(user_id: str, query: str):
    """Search memory in Zep."""
    async with httpx.AsyncClient() as client:
        url = f"{ZEP_BASE_URL}/v1/users/{user_id}/search"
        headers = {"Authorization": f"Bearer {ZEP_API_KEY}"}
        
        params = {"query": query}
        response = await client.get(url, headers=headers, params=params)
        return response.json()

# Mem0 Client Functions
async def mem0_add_memory(user_id: str, messages: List[Dict[str, Any]]):
    """Add messages to Mem0 memory."""
    async with httpx.AsyncClient() as client:
        url = f"{MEM0_API_URL}/v1/memories"
        headers = {"Authorization": f"Bearer {MEM0_API_KEY}"}
        
        payload = {
            "user_id": user_id,
            "messages": messages
        }
        
        response = await client.post(url, json=payload, headers=headers)
        return response.json()

async def mem0_search_memory(user_id: str, query: str):
    """Search memory in Mem0."""
    async with httpx.AsyncClient() as client:
        url = f"{MEM0_API_URL}/v1/memories/search"
        headers = {"Authorization": f"Bearer {MEM0_API_KEY}"}
        
        params = {"user_id": user_id, "query": query}
        response = await client.get(url, headers=headers, params=params)
        return response.json()

async def mem0_get_all_memories(user_id: str):
    """Get all memories for a user from Mem0."""
    async with httpx.AsyncClient() as client:
        url = f"{MEM0_API_URL}/v1/memories"
        headers = {"Authorization": f"Bearer {MEM0_API_KEY}"}
        
        params = {"user_id": user_id}
        response = await client.get(url, headers=headers, params=params)
        return response.json()

# FastAPI App
app = FastAPI(title="AgnoChat Bot API", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health Check
@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint."""
    try:
        services = {}
        
        # Check Agno agent
        try:
            test_response = agno_agent.run(
                "Health check",
                user_id="health_check",
                session_id="health_check",
                stream=False
            )
            services["agno_agent"] = "active" if test_response else "error"
        except Exception as e:
            services["agno_agent"] = "error"
        
        # Check database connection
        try:
            db = SessionLocal()
            db.execute("SELECT 1")
            db.close()
            services["postgresql"] = "connected"
        except Exception as e:
            services["postgresql"] = "disconnected"
        
        # Check external APIs
        services["gemini"] = "configured" if GEMINI_API_KEY else "not_configured"
        services["zep"] = "configured" if ZEP_API_KEY else "not_configured"
        services["mem0"] = "configured" if MEM0_API_KEY else "not_configured"
        
        # Determine overall status
        overall_status = "healthy"
        if any(status in ["error", "disconnected", "not_configured"] for status in services.values()):
            overall_status = "degraded"
        
        return HealthResponse(
            status=overall_status,
            timestamp=datetime.utcnow().isoformat(),
            services=services
        )
        
    except Exception as e:
        return HealthResponse(
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

# Authentication Endpoints
@app.post("/api/auth/signup", response_model=Token)
async def signup(user_data: UserCreate, db: Session = Depends(get_db)):
    """Create a new user account and return JWT token."""
    try:
        # Check if user exists
        existing_user = db.query(User).filter(User.email == user_data.email).first()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        
        # Create user
        user_id = str(uuid.uuid4())
        hashed_password = get_password_hash(user_data.password)
        
        db_user = User(
            id=user_id,
            email=user_data.email,
            username=user_data.username or user_data.email.split('@')[0],
            first_name=user_data.first_name,
            last_name=user_data.last_name,
            hashed_password=hashed_password
        )
        
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        
        # Generate JWT token
        access_token = create_access_token(data={"sub": db_user.email})
        
        return Token(access_token=access_token, token_type="bearer")
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create user: {str(e)}"
        )

@app.post("/api/auth/login", response_model=Token)
async def login(user_credentials: UserLogin, db: Session = Depends(get_db)):
    """Authenticate user and return JWT token."""
    try:
        user = db.query(User).filter(User.email == user_credentials.email).first()
        
        if not user or not verify_password(user_credentials.password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password"
            )
        
        access_token = create_access_token(data={"sub": user.email})
        return Token(access_token=access_token, token_type="bearer")
        
    except HTTPException:
        raise
    except Exception as e:
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
    try:
        # Verify user_id matches authenticated user
        if chat_data.user_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User ID mismatch"
            )
        
        # Get user's existing memories from Mem0
        try:
            filters = {
                "AND": [
                    {
                        "user_id": chat_data.user_id
                    }
                ]
            }
            user_memories = mem0_client.get_all(version="v2", filters=filters, page=1, page_size=50)
            memory_context = "\n".join([f"- {memory['memory']}" for memory in user_memories]) if user_memories else "No previous memories found."
        except Exception as e:
            memory_context = f"Error retrieving memories: {str(e)}"
        
        # Check if this is a memory update request
        is_memory_update = any(keyword in chat_data.message.lower() for keyword in [
            "update", "change", "modify", "set", "remember", "store", "save", "add"
        ])
        
        # Process message with Agno agent
        print(f"Starting chat processing for user {chat_data.user_id}")
        
        # Check if agent is available
        if agno_agent is None:
            print("Agno agent is not available, using fallback response")
            response_content = f"Hello! I received your message: '{chat_data.message}'. I'm here to help you with any questions or tasks you might have."
            class SimpleResponse:
                def __init__(self, content):
                    self.content = content
            response = SimpleResponse(response_content)
        else:
            try:
                if is_memory_update:
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
                    
                    response = agno_agent.run(
                        update_prompt,
                        user_id=chat_data.user_id,
                        session_id=chat_data.session_id,
                        stream=False
                    )
                else:
                    # Regular chat processing with user isolation and memory context
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
                    
                    response = agno_agent.run(
                        chat_prompt,
                        user_id=chat_data.user_id,
                        session_id=chat_data.session_id,
                        stream=False
                    )
            except Exception as agno_error:
                # Fallback response if Agno agent fails
                print(f"Agno agent error: {agno_error}")
                if is_memory_update:
                    response_content = f"I understand you want to update your information. I'll remember that for you. Your message was: {chat_data.message}"
                else:
                    response_content = f"Hello! I received your message: '{chat_data.message}'. I'm here to help you with any questions or tasks you might have."
                
                # Create a simple response object
                class SimpleResponse:
                    def __init__(self, content):
                        self.content = content
                
                response = SimpleResponse(response_content)
                print(f"Using fallback response: {response_content}")
        
        # Store the conversation in Mem0 memory
        try:
            messages = [
                {"role": "user", "content": chat_data.message},
                {"role": "assistant", "content": str(response.content) if response.content else ""}
            ]
            mem0_client.add(messages, user_id=chat_data.user_id)
        except Exception as e:
            print(f"Error storing in Mem0: {e}")
        
        # Store the chat message in the database
        db = SessionLocal()
        try:
            import uuid
            
            # Store user message
            user_message = ChatHistory(
                id=str(uuid.uuid4()),
                user_id=chat_data.user_id,
                session_id=chat_data.session_id,
                message=chat_data.message,
                response="",
                message_type="user"
            )
            db.add(user_message)
            
            # Store assistant response
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
        except Exception as e:
            db.rollback()
            print(f"Database error: {e}")
        finally:
            db.close()
        
        return ChatResponse(
            response=str(response.content) if response.content else "",
            session_id=chat_data.session_id,
            user_id=chat_data.user_id,
            timestamp=datetime.utcnow()
        )
        
    except HTTPException:
        raise
    except Exception as e:
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
        
        # Get memory from Zep
        try:
            if session_id:
                zep_data = await zep_get_memory(session_id)
                # Add user_id and session_id to Zep response
                if isinstance(zep_data, dict):
                    zep_data["user_id"] = user_id
                    zep_data["session_id"] = session_id
                    # Add user_id and session_id to each message
                    if "messages" in zep_data:
                        for message in zep_data["messages"]:
                            message["user_id"] = user_id
                            message["session_id"] = session_id
                    # Add to metadata
                    if "metadata" in zep_data:
                        zep_data["metadata"]["user_id"] = user_id
                        zep_data["metadata"]["session_id"] = session_id
            else:
                zep_data = {"status": "no_session_id", "user_id": user_id}
        except Exception as e:
            zep_data = {"error": str(e), "user_id": user_id, "session_id": session_id}
        
        # Get memory from Mem0
        try:
            filters = {
                "AND": [
                    {
                        "user_id": user_id
                    }
                ]
            }
            mem0_data = mem0_client.get_all(version="v2", filters=filters, page=1, page_size=50)
            # Add user_id and session_id to each Mem0 memory
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
            memory_response = agno_agent.run(
                "Analyze and summarize your memories for this user. Return a JSON with counts for zep_memories and mem0_memories.",
                user_id=user_id,
                session_id=session_id or "memory_session",
                stream=False
            )
            consolidated = str(memory_response.content) if memory_response.content else "Memory analysis completed"
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
    try:
        if search_data.user_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User ID mismatch"
            )
        
        # Search memory using Mem0 directly and agent tools
        try:
            # Search Mem0 directly using proper filters
            filters = {
                "AND": [
                    {
                        "user_id": search_data.user_id
                    }
                ]
            }
            mem0_results = mem0_client.search(search_data.query, version="v2", filters=filters)
            mem0_context = "\n".join([f"- {result['memory']}" for result in mem0_results]) if mem0_results else "No relevant memories found in Mem0."
        except Exception as e:
            mem0_context = f"Error searching Mem0: {str(e)}"
        
        # Search memory using agent tools with enhanced prompt
        search_prompt = f"""
        SEARCH REQUEST: {search_data.query}
        USER ID: {search_data.user_id}
        
        Mem0 search results for user {search_data.user_id}:
        {mem0_context}
        
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
        
        response = agno_agent.run(
            search_prompt,
            user_id=search_data.user_id,
            session_id="search_session",
            stream=False
        )
        
        return SearchResponse(
            user_id=search_data.user_id,
            query=search_data.query,
            results=str(response.content) if response.content else ""
        )
        
    except HTTPException:
        raise
    except Exception as e:
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
        
        response = agno_agent.run(
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
                headers = {"Authorization": f"Bearer {ZEP_API_KEY}"}
                
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
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 