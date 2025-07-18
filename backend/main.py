from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import uuid
from datetime import datetime
from typing import List, Optional

from config import settings
from auth.deps import get_db, get_current_user_id
from auth.auth_routes import router as auth_router
from auth.models import User, ChatSession, ChatMessage
from agno_agent.agent import agno_agent, ChatMessage as AgentChatMessage
from services.agno_agent_service import agno_agent_service
from utils.logger import logger
from memory.hybrid_memory import hybrid_memory

# Create FastAPI app
app = FastAPI(
    title="Agno Chatbot Backend",
    description="FastAPI backend for Agno Chatbot with Gemini, Zep, and Mem0 integration",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include auth routes
app.include_router(auth_router)

# Pydantic models for API
from pydantic import BaseModel

class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = None
    use_memory: bool = True

class ChatResponse(BaseModel):
    message: str
    session_id: str
    memory_context: dict
    timestamp: datetime

class SessionInfo(BaseModel):
    session_id: str
    title: str
    created_at: datetime
    is_active: str

class MemorySearchRequest(BaseModel):
    query: str
    search_type: str = "hybrid"  # hybrid, temporal, factual

class MemorySummary(BaseModel):
    user_id: str
    zep_facts_count: int
    mem0_memories_count: int
    key_facts: List[str]

# Chat routes
@app.post("/chat", response_model=ChatResponse)
async def chat(
    request: ChatRequest,
    user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db)
):
    """Process a chat message using Agno framework and return response with memory context."""
    print(f"🔵 [CHAT API] Request received - User: {user_id}, Message: {request.message[:50]}...")
    try:
        # Get or create session
        session_id = request.session_id
        if not session_id:
            # Create new session
            session_id = str(uuid.uuid4())
            print(f"🟡 [CHAT API] Creating new session: {session_id}")
        
        # Check if session exists in database
        stmt = select(ChatSession).where(
            ChatSession.session_id == session_id,
            ChatSession.user_id == user_id
        )
        result = await db.execute(stmt)
        existing_session = result.scalar_one_or_none()
        
        if not existing_session:
            # Create new session
            print(f"🟡 [CHAT API] Creating new session in database: {session_id}")
            
            # Get user info for memory creation
            stmt = select(User).where(User.id == user_id)
            result = await db.execute(stmt)
            user = result.scalar_one_or_none()
            
            if user:
                # Create session in database
                db_session = ChatSession(
                    session_id=session_id,
                    user_id=user_id,
                    title=f"Chat Session {datetime.utcnow().strftime('%Y-%m-%d %H:%M')}"
                )
                db.add(db_session)
                await db.commit()
                print(f"✅ [CHAT API] Session created in database: {session_id}")
        
        # Process message with Agno framework
        print(f"🟡 [CHAT API] Processing message with Agno framework...")
        agno_result = await agno_agent_service.process_message_with_agno(
            user_id=user_id,
            message=request.message,
            session_id=session_id
        )
        
        if not agno_result["success"]:
            print(f"❌ [CHAT API] Agno processing failed")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to process message with Agno"
            )
        
        print(f"✅ [CHAT API] Agno processing successful")
        
        # Get memory context from Agno
        memory_context = {}
        if request.use_memory:
            print(f"🟡 [CHAT API] Getting memory context...")
            memories = await agno_agent_service.get_user_memories(user_id=user_id)
            memory_context = {
                "agno_memories": memories.get("memories", []),
                "memory_count": memories.get("count", 0),
                "reasoning_steps": agno_result.get("reasoning_steps"),
                "tool_calls": agno_result.get("tool_calls")
            }
            print(f"✅ [CHAT API] Memory context retrieved: {len(memories.get('memories', []))} memories")
        
        # Save message to database
        user_msg = ChatMessage(
            session_id=session_id,
            role="user",
            content=request.message
        )
        assistant_msg = ChatMessage(
            session_id=session_id,
            role="assistant",
            content=agno_result["agno_response"]
        )
        
        db.add(user_msg)
        db.add(assistant_msg)
        await db.commit()
        print(f"✅ [CHAT API] Messages saved to database")
        
        response = ChatResponse(
            message=agno_result["agno_response"],
            session_id=session_id,
            memory_context=memory_context,
            timestamp=datetime.utcnow()
        )
        
        print(f"✅ [CHAT API] Success - Response sent to user: {user_id}")
        return response
        
    except HTTPException:
        print(f"❌ [CHAT API] HTTP Exception raised")
        raise
    except Exception as e:
        print(f"❌ [CHAT API] Error: {e}")
        logger.error(f"Chat error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )

@app.post("/sessions", response_model=SessionInfo)
async def create_session(
    request: dict,
    user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db)
):
    """Create a new chat session for the current user."""
    print(f"🔵 [CREATE SESSION API] Request received - User: {user_id}, Session ID: {request.get('session_id', 'auto')}")
    try:
        session_id = request.get("session_id", str(uuid.uuid4()))
        title = request.get("title", f"New Chat {datetime.utcnow().strftime('%H:%M')}")
        
        print(f"🟡 [CREATE SESSION API] Checking if session exists: {session_id}")
        
        # Check if session already exists
        stmt = select(ChatSession).where(
            ChatSession.session_id == session_id,
            ChatSession.user_id == user_id
        )
        result = await db.execute(stmt)
        existing_session = result.scalar_one_or_none()
        
        if existing_session:
            print(f"✅ [CREATE SESSION API] Session already exists, returning existing session")
            return SessionInfo(
                session_id=str(existing_session.session_id),
                title=str(existing_session.title),
                created_at=existing_session.created_at if existing_session.created_at is not None else datetime.utcnow(),
                is_active=str(existing_session.is_active)
            )
        
        # Create new session
        print(f"🟡 [CREATE SESSION API] Creating new session: {session_id}")
        new_session = ChatSession(
            session_id=session_id,
            user_id=user_id,
            title=title,
            created_at=datetime.utcnow(),
            is_active="active"
        )
        
        db.add(new_session)
        await db.commit()
        await db.refresh(new_session)
        
        print(f"✅ [CREATE SESSION API] Session created successfully: {session_id}")
        
        return SessionInfo(
            session_id=str(new_session.session_id),
            title=str(new_session.title),
            created_at=new_session.created_at,
            is_active=str(new_session.is_active)
        )
        
    except Exception as e:
        print(f"❌ [CREATE SESSION API] Error: {e}")
        logger.error(f"Failed to create session for user {user_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )

@app.get("/sessions", response_model=List[SessionInfo])
async def get_user_sessions(
    user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db)
):
    """Get all chat sessions for the current user."""
    try:
        stmt = select(ChatSession).where(
            ChatSession.user_id == user_id
        ).order_by(ChatSession.created_at.desc())
        
        result = await db.execute(stmt)
        sessions = result.scalars().all()
        
        return [
            SessionInfo(
                session_id=str(session.session_id),
                title=str(session.title),
                created_at=session.created_at if session.created_at is not None else datetime.utcnow(),
                is_active=str(session.is_active)
            )
            for session in sessions
        ]
        
    except Exception as e:
        logger.error(f"Failed to get sessions for user {user_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )

@app.get("/sessions/{session_id}/history", response_model=List[dict])
async def get_session_history(
    session_id: str,
    user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db)
):
    """Get conversation history for a specific session."""
    try:
        # Verify session belongs to user
        stmt = select(ChatSession).where(
            ChatSession.session_id == session_id,
            ChatSession.user_id == user_id
        )
        result = await db.execute(stmt)
        session = result.scalar_one_or_none()
        
        if not session:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Session not found"
            )
        
        # Get messages from database
        stmt = select(ChatMessage).where(
            ChatMessage.session_id == session_id
        ).order_by(ChatMessage.timestamp)
        
        result = await db.execute(stmt)
        messages = result.scalars().all()
        
        return [
            {
                "role": msg.role,
                "content": msg.content,
                "timestamp": msg.timestamp
            }
            for msg in messages
        ]
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get session history for {session_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )

async def ensure_user_in_memory_systems(user_id: str, db: AsyncSession):
    """Ensure user exists in memory systems, create if not."""
    try:
        # Get user from database
        stmt = select(User).where(User.id == user_id)
        result = await db.execute(stmt)
        user = result.scalar_one_or_none()
        
        if user:
            # Try to create user in memory systems (will fail silently if already exists)
            await hybrid_memory.create_user_memory(
                user_id=str(user.id),
                email=str(user.email),
                first_name=str(user.first_name) if user.first_name is not None else "",
                last_name=str(user.last_name) if user.last_name is not None else ""
            )
            logger.info(f"Ensured user {user.username} exists in memory systems")
    except Exception as e:
        logger.warning(f"Failed to ensure user {user_id} in memory systems: {e}")

@app.post("/memory/search", response_model=dict)
async def search_memory(
    request: MemorySearchRequest,
    user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db)
):
    """Search user's memory for relevant information."""
    try:
        # Ensure user exists in memory systems
        await ensure_user_in_memory_systems(user_id, db)
        
        results = await agno_agent.search_memory(
            user_id=user_id,
            query=request.query,
            search_type=request.search_type
        )
        return results
        
    except Exception as e:
        logger.error(f"Failed to search memory for user {user_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )

@app.get("/memory/summary", response_model=MemorySummary)
async def get_memory_summary(
    user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db)
):
    """Get a summary of user's memory."""
    print(f"🔵 [MEMORY SUMMARY API] Request received - User: {user_id}")
    try:
        # Ensure user exists in memory systems
        print(f"🟡 [MEMORY SUMMARY API] Ensuring user exists in memory systems...")
        await ensure_user_in_memory_systems(user_id, db)
        
        print(f"🟡 [MEMORY SUMMARY API] Getting memory summary from Agno agent...")
        summary = await agno_agent.get_memory_summary(user_id)
        
        print(f"✅ [MEMORY SUMMARY API] Memory summary retrieved - Zep: {summary.get('zep_facts_count', 0)}, Mem0: {summary.get('mem0_memories_count', 0)}")
        
        return MemorySummary(**summary)
        
    except Exception as e:
        print(f"❌ [MEMORY SUMMARY API] Error: {e}")
        logger.error(f"Failed to get memory summary for user {user_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )

@app.post("/memory/facts")
async def add_custom_fact(
    fact: str,
    fact_type: str = "custom",
    user_id: str = Depends(get_current_user_id)
):
    """Add a custom fact to user's memory."""
    print(f"🔵 [ADD MEMORY FACT API] Request received - User: {user_id}, Fact: {fact[:50]}..., Type: {fact_type}")
    try:
        print(f"🟡 [ADD MEMORY FACT API] Adding fact to memory system...")
        success = await agno_agent.add_custom_fact(user_id, fact, fact_type)
        
        if success:
            print(f"✅ [ADD MEMORY FACT API] Fact added successfully")
            return {"message": "Fact added successfully"}
        else:
            print(f"❌ [ADD MEMORY FACT API] Failed to add fact")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to add fact"
            )
        
    except HTTPException:
        print(f"❌ [ADD MEMORY FACT API] HTTP Exception raised")
        raise
    except Exception as e:
        print(f"❌ [ADD MEMORY FACT API] Error: {e}")
        logger.error(f"Failed to add fact for user {user_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )

# Mem0 Specific Endpoints
@app.get("/memory/{memory_id}")
async def get_memory(
    memory_id: str,
    user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db)
):
    """Get a specific memory by ID."""
    try:
        from memory.mem0_memory import mem0_memory
        
        memory = await mem0_memory.get_memory(memory_id)
        if not memory:
            raise HTTPException(status_code=404, detail="Memory not found")
        
        # Ensure user can only access their own memories
        if memory.get("user_id") != user_id:
            raise HTTPException(status_code=403, detail="Access denied")
        
        return memory
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get memory {memory_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/memory/{memory_id}/history")
async def get_memory_history(
    memory_id: str,
    user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db)
):
    """Get the history of changes for a specific memory."""
    try:
        from memory.mem0_memory import mem0_memory
        
        # First get the memory to verify ownership
        memory = await mem0_memory.get_memory(memory_id)
        if not memory:
            raise HTTPException(status_code=404, detail="Memory not found")
        
        if memory.get("user_id") != user_id:
            raise HTTPException(status_code=403, detail="Access denied")
        
        history = await mem0_memory.get_memory_history(memory_id)
        return {"history": history}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get memory history for {memory_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

# Agno Framework Endpoints
@app.post("/chat/agno", response_model=ChatResponse)
async def chat_agno(
    request: ChatRequest,
    user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db)
):
    """Process a chat message using Agno framework and return response with memory context."""
    print(f"🔵 [CHAT/AGNO API] Request received - User: {user_id}, Message: {request.message[:50]}...")
    try:
        # Get or create session
        session_id = request.session_id
        if not session_id:
            # Create new session
            session_id = str(uuid.uuid4())
            print(f"🟡 [CHAT/AGNO API] Creating new session: {session_id}")
        
        # Check if session exists in database
        stmt = select(ChatSession).where(
            ChatSession.session_id == session_id,
            ChatSession.user_id == user_id
        )
        result = await db.execute(stmt)
        existing_session = result.scalar_one_or_none()
        
        if not existing_session:
            # Create new session
            print(f"🟡 [CHAT/AGNO API] Creating new session in database: {session_id}")
            
            # Get user info for memory creation
            stmt = select(User).where(User.id == user_id)
            result = await db.execute(stmt)
            user = result.scalar_one_or_none()
            
            if user:
                # Create session in database
                db_session = ChatSession(
                    session_id=session_id,
                    user_id=user_id,
                    title=f"Chat Session {datetime.utcnow().strftime('%Y-%m-%d %H:%M')}"
                )
                db.add(db_session)
                await db.commit()
                print(f"✅ [CHAT/AGNO API] Session created in database: {session_id}")
        
        # Process message with Agno framework
        print(f"🟡 [CHAT/AGNO API] Processing message with Agno framework...")
        agno_result = await agno_agent_service.process_message_with_agno(
            user_id=user_id,
            message=request.message,
            session_id=session_id
        )
        
        if not agno_result["success"]:
            print(f"❌ [CHAT/AGNO API] Agno processing failed")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to process message with Agno"
            )
        
        print(f"✅ [CHAT/AGNO API] Agno processing successful")
        
        # Get memory context from Agno
        memory_context = {}
        if request.use_memory:
            print(f"🟡 [CHAT/AGNO API] Getting memory context...")
            memories = await agno_agent_service.get_user_memories(user_id=user_id)
            memory_context = {
                "agno_memories": memories.get("memories", []),
                "memory_count": memories.get("count", 0),
                "reasoning_steps": agno_result.get("reasoning_steps"),
                "tool_calls": agno_result.get("tool_calls")
            }
            print(f"✅ [CHAT/AGNO API] Memory context retrieved: {len(memories.get('memories', []))} memories")
        
        # Save message to database
        user_msg = ChatMessage(
            session_id=session_id,
            role="user",
            content=request.message
        )
        assistant_msg = ChatMessage(
            session_id=session_id,
            role="assistant",
            content=agno_result["agno_response"]
        )
        
        db.add(user_msg)
        db.add(assistant_msg)
        await db.commit()
        print(f"✅ [CHAT/AGNO API] Messages saved to database")
        
        response = ChatResponse(
            message=agno_result["agno_response"],
            session_id=session_id,
            memory_context=memory_context,
            timestamp=datetime.utcnow()
        )
        
        print(f"✅ [CHAT/AGNO API] Success - Response sent to user: {user_id}")
        return response
        
    except HTTPException:
        print(f"❌ [CHAT/AGNO API] HTTP Exception raised")
        raise
    except Exception as e:
        print(f"❌ [CHAT/AGNO API] Error: {e}")
        logger.error(f"Chat/Agno error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )

@app.post("/agno/chat", response_model=dict)
async def agno_chat(
    request: ChatRequest,
    user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db)
):
    """Process a chat message using Agno framework."""
    try:
        # Create or get session
        session_id = request.session_id
        if not session_id:
            session_id = str(uuid.uuid4())
        
        # Check if session exists in database
        stmt = select(ChatSession).where(
            ChatSession.session_id == session_id,
            ChatSession.user_id == user_id
        )
        result = await db.execute(stmt)
        session = result.scalar_one_or_none()
        
        if not session:
            # Create new session
            new_session = ChatSession(
                session_id=session_id,
                user_id=user_id,
                title=f"Chat {datetime.utcnow().strftime('%H:%M')}",
                created_at=datetime.utcnow(),
                is_active="active"
            )
            db.add(new_session)
            await db.commit()
        
        # Process message with Agno
        result = await agno_agent_service.process_message_with_agno(
            user_id=user_id,
            message=request.message,
            session_id=session_id
        )
        
        # Save message to database
        user_message = ChatMessage(
            session_id=session_id,
            role="user",
            content=request.message,
            timestamp=datetime.utcnow()
        )
        db.add(user_message)
        
        if result["success"]:
            ai_message = ChatMessage(
                session_id=session_id,
                role="assistant",
                content=result["agno_response"],
                timestamp=datetime.utcnow()
            )
            db.add(ai_message)
        
        await db.commit()
        
        return {
            "success": result["success"],
            "message": result["agno_response"] if result["success"] else result["message"],
            "session_id": session_id,
            "agno_metadata": {
                "reasoning_steps": result.get("reasoning_steps"),
                "tool_calls": result.get("tool_calls")
            },
            "timestamp": datetime.utcnow()
        }
        
    except Exception as e:
        logger.error(f"Agno chat error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@app.get("/agno/memories", response_model=dict)
async def get_agno_memories(
    user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db)
):
    """Get user memories from Agno memory system."""
    try:
        # Ensure user exists in memory systems
        await ensure_user_in_memory_systems(user_id, db)
        
        memories = await agno_agent_service.get_user_memories(user_id=user_id)
        return {
            "success": True,
            "memories": memories["memories"],
            "count": memories["count"],
            "timestamp": datetime.utcnow()
        }
        
    except Exception as e:
        logger.error(f"Failed to get Agno memories for user {user_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@app.post("/agno/memories", response_model=dict)
async def add_agno_memory(
    request: dict,
    user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db)
):
    """Add custom memory to Agno memory system."""
    try:
        # Ensure user exists in memory systems
        await ensure_user_in_memory_systems(user_id, db)
        
        content = request.get("content")
        memory_type = request.get("memory_type", "fact")
        
        if not content:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Content is required"
            )
        
        success = await agno_agent_service.add_custom_memory(
            user_id=user_id,
            content=content,
            memory_type=memory_type
        )
        
        return {
            "success": success,
            "message": "Memory added successfully" if success else "Failed to add memory",
            "timestamp": datetime.utcnow()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to add Agno memory for user {user_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@app.delete("/agno/agent", response_model=dict)
async def clear_agno_agent(
    user_id: str = Depends(get_current_user_id)
):
    """Clear user's Agno agent from cache."""
    try:
        success = agno_agent_service.clear_user_agent(user_id=user_id)
        
        return {
            "success": success,
            "message": "Agent cleared successfully" if success else "No agent found to clear",
            "timestamp": datetime.utcnow()
        }
        
    except Exception as e:
        logger.error(f"Failed to clear Agno agent for user {user_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow(),
        "version": "1.0.0"
    }


@app.get("/test")
async def test_endpoint():
    """Simple test endpoint to verify basic functionality."""
    return {
        "message": "Test endpoint working!",
        "timestamp": datetime.utcnow()
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug
    ) 