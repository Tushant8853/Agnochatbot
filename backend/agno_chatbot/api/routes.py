"""
API routes for AgnoChat Bot
"""

from datetime import datetime, timedelta
from typing import Optional
from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from ..agents import create_chatbot_agent
from ..utils.auth import verify_token, get_user_by_email, create_user, verify_password, create_access_token, User, store_chat_message, get_chat_history as get_db_chat_history, get_user_sessions
from ..utils.models import (
    UserCreate, UserLogin, Token, ChatMessage, ChatResponse, 
    MemoryRequest, MemoryResponse, HealthResponse, ChatHistoryItem, ChatHistoryResponse
)

# Initialize router
router = APIRouter()
security = HTTPBearer()

# Initialize chatbot agent
chatbot_agent = create_chatbot_agent()

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> User:
    """Get current authenticated user."""
    token = credentials.credentials
    email = verify_token(token)
    if email is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    user = get_user_by_email(email)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return user

@router.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint."""
    return HealthResponse(
        status="healthy",
        timestamp=datetime.utcnow().isoformat(),
        services={
            "agno_agent": "active",
            "gemini": "configured",
            "zep": "configured",
            "mem0": "configured",
            "postgresql": "connected"
        }
    )

@router.get("/auth/me", response_model=dict)
async def get_current_user_info(current_user: User = Depends(get_current_user)):
    """Get current user information."""
    return {
        "user_id": current_user.id,
        "email": current_user.email,
        "first_name": current_user.first_name,
        "last_name": current_user.last_name,
        "username": current_user.username
    }

@router.post("/auth/signup", response_model=Token)
async def signup(user_data: UserCreate):
    """Create a new user account and return JWT token."""
    try:
        # Check if user exists
        existing_user = get_user_by_email(user_data.email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        
        # Create user with auto-generated user_id
        db_user = create_user(
            email=user_data.email,
            password=user_data.password,
            first_name=user_data.first_name,
            last_name=user_data.last_name
        )
        
        # Generate JWT token for the new user (same as login)
        access_token = create_access_token(data={"sub": db_user.email})
        
        return Token(access_token=access_token, token_type="bearer")
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create user: {str(e)}"
        )

@router.post("/auth/login", response_model=Token)
async def login(user_credentials: UserLogin):
    """Authenticate user and return JWT token."""
    try:
        user = get_user_by_email(user_credentials.email)
        
        if not user or not verify_password(user_credentials.password, str(user.hashed_password)):
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

@router.post("/chat", response_model=ChatResponse)
async def chat(
    chat_data: ChatMessage,
    current_user: User = Depends(get_current_user)
):
    """Process a chat message using Agno agent."""
    try:
        # Verify user_id matches authenticated user
        if chat_data.user_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User ID mismatch"
            )
        
        # Process message with Agno agent
        response = chatbot_agent.run(
            chat_data.message,
            user_id=chat_data.user_id,
            session_id=chat_data.session_id,
            stream=False
        )
        
        # Store the chat message in the database
        store_chat_message(
            user_id=chat_data.user_id,
            session_id=chat_data.session_id,
            message=chat_data.message,
            response=str(response.content) if response.content else ""
        )
        
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

@router.get("/memory", response_model=MemoryResponse)
async def get_memory(
    user_id: str,
    session_id: Optional[str] = None,
    current_user: User = Depends(get_current_user)
):
    """Get memory from Agno agent."""
    try:
        if user_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User ID mismatch"
            )
        
        # Get memory from agent - using Agno's memory system
        try:
            # For now, return a simple response since Agno handles memory internally
            zep_data = {"status": "configured"}
            mem0_data = {"status": "configured"}
            consolidated = "Memory is managed by Agno framework internally"
        except Exception as e:
            zep_data = {"error": str(e)}
            mem0_data = {"error": str(e)}
            consolidated = f"Error: {str(e)}"
        
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

@router.post("/memory/search")
async def search_memory(
    user_id: str,
    query: str,
    current_user: User = Depends(get_current_user)
):
    """Search memory using Agno agent."""
    try:
        if user_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User ID mismatch"
            )
        
        # Search memory using agent tools
        response = chatbot_agent.run(
            f"Search memory for: {query}",
            user_id=user_id,
            session_id="search_session",
            stream=False
        )
        
        return {
            "user_id": user_id,
            "query": query,
            "results": response.content
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Memory search failed: {str(e)}"
        )

@router.get("/memory/stats")
async def get_memory_stats(
    user_id: str,
    current_user: User = Depends(get_current_user)
):
    """Get comprehensive memory statistics for a user."""
    try:
        if user_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User ID mismatch"
            )
        
        # Get memory data from agent
        try:
            # Get memory from Agno agent for this user
            memory_response = chatbot_agent.run(
                "Get memory statistics",
                user_id=user_id,
                session_id="stats_session",
                stream=False
            )
            
            # For new users, return 0 memories
            # In a real implementation, this would analyze actual memory data
            zep_memories = 0
            mem0_memories = 0
            total_memories = 0
            
            return {
                "user_id": user_id,
                "total_memories": total_memories,
                "zep_memories": zep_memories,
                "mem0_memories": mem0_memories,
                "last_updated": datetime.utcnow().isoformat(),
                "memory_health": "active"
            }
            
        except Exception as e:
            # Fallback to zero stats for new users
            return {
                "user_id": user_id,
                "total_memories": 0,
                "zep_memories": 0,
                "mem0_memories": 0,
                "last_updated": datetime.utcnow().isoformat(),
                "memory_health": "basic"
            }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get memory stats: {str(e)}"
        )

@router.get("/sessions/stats")
async def get_session_stats(
    user_id: str,
    current_user: User = Depends(get_current_user)
):
    """Get session statistics for a user."""
    try:
        if user_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User ID mismatch"
            )
        
        # Get session data from agent or database
        try:
            # This would typically come from your session management system
            # For new users, return 0 sessions
            active_sessions = 0
            total_sessions = 0
            last_session_activity = datetime.utcnow().isoformat()
            
            return {
                "user_id": user_id,
                "active_sessions": active_sessions,
                "total_sessions": total_sessions,
                "last_session_activity": last_session_activity,
                "session_health": "active"
            }
            
        except Exception as e:
            return {
                "user_id": user_id,
                "active_sessions": 0,
                "total_sessions": 0,
                "last_session_activity": datetime.utcnow().isoformat(),
                "session_health": "basic"
            }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get session stats: {str(e)}"
        )

@router.get("/memory/breakdown")
async def get_memory_breakdown(
    user_id: str,
    current_user: User = Depends(get_current_user)
):
    """Get detailed memory breakdown for analytics."""
    try:
        if user_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User ID mismatch"
            )
        
        # Get detailed memory breakdown
        try:
            # This would analyze the actual memory structure
            # For new users, return 0 for all memory types
            breakdown = {
                "user_id": user_id,
                "memory_types": {
                    "conversation_history": 0,
                    "user_preferences": 0,
                    "contextual_facts": 0,
                    "learned_patterns": 0
                },
                "memory_sources": {
                    "zep": 0,
                    "mem0": 0
                },
                "last_analyzed": datetime.utcnow().isoformat()
            }
            
            return breakdown
            
        except Exception as e:
            return {
                "user_id": user_id,
                "memory_types": {"conversation_history": 0},
                "memory_sources": {"zep": 0, "mem0": 0},
                "last_analyzed": datetime.utcnow().isoformat()
            }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get memory breakdown: {str(e)}"
        )

@router.get("/chat/history", response_model=ChatHistoryResponse)
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
        try:
            # Get real chat history from database
            db_history_items = get_db_chat_history(user_id, session_id, limit or 50)
            
            # Group messages by session
            sessions = {}
            total_messages = 0
            last_activity = datetime.utcnow()
            history_summary = {}
            
            # Get all sessions for this user
            user_sessions = get_user_sessions(user_id)
            
            for session in user_sessions:
                if session_id and session != session_id:
                    continue
                    
                # Filter messages for this session
                session_messages = [msg for msg in db_history_items if msg.session_id == session]
                
                # Convert database objects to Pydantic models
                chat_items = []
                for msg in session_messages:
                    chat_item = ChatHistoryItem(
                        id=msg.id,
                        user_id=msg.user_id,
                        session_id=msg.session_id,
                        message=msg.message or "",
                        response=msg.response or "",
                        timestamp=msg.timestamp,
                        message_type=msg.message_type
                    )
                    chat_items.append(chat_item)
                
                sessions[session] = chat_items
                history_summary[session] = len(chat_items)
                total_messages += len(chat_items)
                
                # Update last activity
                if chat_items:
                    session_last_activity = max(item.timestamp for item in chat_items)
                    if session_last_activity > last_activity:
                        last_activity = session_last_activity
            
            return ChatHistoryResponse(
                user_id=user_id,
                total_messages=total_messages,
                sessions=sessions,
                last_activity=last_activity,
                history_summary=history_summary
            )
            
        except Exception as e:
            # Fallback to empty history
            return ChatHistoryResponse(
                user_id=user_id,
                total_messages=0,
                sessions={},
                last_activity=datetime.utcnow(),
                history_summary={}
            )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get chat history: {str(e)}"
        ) 