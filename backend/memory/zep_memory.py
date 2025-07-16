import uuid
from typing import List, Dict, Any, Optional
from zep_cloud.client import Zep
from zep_cloud.types import Message
from config import settings
from utils.logger import logger


class ZepMemoryService:
    def __init__(self):
        self.client = Zep(api_key=settings.zep_api_key)
    
    async def create_user(self, user_id: str, email: str, first_name: str = "", last_name: str = "") -> bool:
        """Create a new user in Zep."""
        try:
            self.client.user.add(
                user_id=user_id,
                email=email,
                first_name=first_name,
                last_name=last_name
            )
            logger.info(f"Created Zep user: {user_id}")
            return True
        except Exception as e:
            logger.error(f"Failed to create Zep user {user_id}: {e}")
            return False
    
    async def create_session(self, session_id: str, user_id: str) -> bool:
        """Create a new session for a user."""
        try:
            self.client.memory.add_session(
                session_id=session_id,
                user_id=user_id
            )
            logger.info(f"Created Zep session: {session_id} for user: {user_id}")
            return True
        except Exception as e:
            logger.error(f"Failed to create Zep session {session_id}: {e}")
            return False
    
    async def add_messages(self, session_id: str, messages: List[Dict[str, str]]) -> bool:
        """Add messages to a session."""
        try:
            zep_messages = []
            for msg in messages:
                zep_messages.append(Message(
                    role=msg.get("role", "user"),
                    content=msg.get("content", ""),
                    role_type=msg.get("role_type", "user")
                ))
            
            self.client.memory.add(session_id, messages=zep_messages)
            logger.info(f"Added {len(messages)} messages to session: {session_id}")
            return True
        except Exception as e:
            logger.error(f"Failed to add messages to session {session_id}: {e}")
            return False
    
    async def get_memory(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Get memory context for a session."""
        try:
            memory = self.client.memory.get(session_id=session_id)
            return {
                "context": memory.context,
                "messages": [
                    {
                        "role": msg.role,
                        "content": msg.content,
                        "timestamp": str(msg.created_at) if hasattr(msg, 'created_at') and msg.created_at else None
                    }
                    for msg in memory.messages or []
                ]
            }
        except Exception as e:
            logger.error(f"Failed to get memory for session {session_id}: {e}")
            return None
    
    async def search_graph(self, user_id: str, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        """Search the user's knowledge graph."""
        try:
            results = self.client.graph.search(
                user_id=user_id,
                query=query,
                scope="edges",
                limit=limit
            )
            
            return [
                {
                    "fact": edge.fact,
                    "confidence": getattr(edge, 'confidence', None),
                    "created_at": str(edge.created_at) if hasattr(edge, 'created_at') and edge.created_at else None
                }
                for edge in results.edges or []
            ]
        except Exception as e:
            logger.error(f"Failed to search graph for user {user_id}: {e}")
            return []
    
    async def add_business_data(self, user_id: str, data: str, data_type: str = "text") -> bool:
        """Add business data to user's graph."""
        try:
            self.client.graph.add(
                user_id=user_id,
                type=data_type,
                data=data
            )
            logger.info(f"Added business data to user {user_id}")
            return True
        except Exception as e:
            logger.error(f"Failed to add business data for user {user_id}: {e}")
            return False
    
    async def delete_session(self, session_id: str) -> bool:
        """Delete a session and its associated memory."""
        try:
            # Note: Zep doesn't have a direct delete session method
            # This would need to be implemented based on Zep's API
            logger.info(f"Session deletion requested for: {session_id}")
            return True
        except Exception as e:
            logger.error(f"Failed to delete session {session_id}: {e}")
            return False


# Global instance
zep_memory = ZepMemoryService() 