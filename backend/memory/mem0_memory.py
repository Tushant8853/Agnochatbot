from typing import List, Dict, Any, Optional
from config import settings
from utils.logger import logger


class MockMemoryClient:
    """Mock implementation of Mem0 MemoryClient for development."""
    
    def __init__(self):
        self.memories = {}
    
    def add(self, messages, user_id=None, metadata=None):
        if user_id not in self.memories:
            self.memories[user_id] = []
        
        for msg in messages:
            memory = {
                "id": f"mem_{len(self.memories[user_id])}",
                "content": msg.get("content", ""),
                "role": msg.get("role", "user"),
                "metadata": metadata or {},
                "created_at": "2024-01-01T00:00:00Z"
            }
            self.memories[user_id].append(memory)
    
    def search(self, query, version="v2", filters=None, limit=5):
        user_id = None
        if filters and "AND" in filters:
            for condition in filters["AND"]:
                if "user_id" in condition:
                    user_id = condition["user_id"]
                    break
        
        if user_id and user_id in self.memories:
            # Simple mock search - return first few memories
            return self.memories[user_id][:limit]
        return []
    
    def get_all(self, version="v2", filters=None, page=1, page_size=50):
        user_id = None
        if filters and "AND" in filters:
            for condition in filters["AND"]:
                if "user_id" in condition:
                    user_id = condition["user_id"]
                    break
        
        if user_id and user_id in self.memories:
            start = (page - 1) * page_size
            end = start + page_size
            return self.memories[user_id][start:end]
        return []
    
    def delete(self, memory_id):
        # Mock delete - would need to implement proper ID tracking
        logger.info(f"Mock delete of memory: {memory_id}")
        return True
    
    def update(self, memory_id, metadata=None):
        # Mock update
        logger.info(f"Mock update of memory: {memory_id}")
        return True


class Mem0MemoryService:
    def __init__(self):
        self.client = MockMemoryClient()
    
    async def add_messages(self, user_id: str, messages: List[Dict[str, str]], metadata: Optional[Dict[str, Any]] = None) -> bool:
        """Add messages to Mem0 memory."""
        try:
            # Convert messages to Mem0 format
            mem0_messages = []
            for msg in messages:
                mem0_messages.append({
                    "role": msg.get("role", "user"),
                    "content": msg.get("content", "")
                })
            
            # Add to Mem0 with user_id filter
            filters = {
                "AND": [
                    {"user_id": user_id}
                ]
            }
            
            self.client.add(mem0_messages, user_id=user_id, metadata=metadata or {})
            logger.info(f"Added {len(messages)} messages to Mem0 for user: {user_id}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to add messages to Mem0 for user {user_id}: {e}")
            return False
    
    async def search_memories(self, user_id: str, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        """Search for relevant memories."""
        try:
            filters = {
                "AND": [
                    {"user_id": user_id}
                ]
            }
            
            results = self.client.search(
                query, 
                version="v2", 
                filters=filters,
                limit=limit
            )
            
            return [
                {
                    "content": memory.get("content", ""),
                    "role": memory.get("role", "user"),
                    "metadata": memory.get("metadata", {}),
                    "score": memory.get("score", 0.0)
                }
                for memory in results
            ]
            
        except Exception as e:
            logger.error(f"Failed to search Mem0 memories for user {user_id}: {e}")
            return []
    
    async def get_all_memories(self, user_id: str, page: int = 1, page_size: int = 50) -> List[Dict[str, Any]]:
        """Get all memories for a user."""
        try:
            filters = {
                "AND": [
                    {"user_id": user_id}
                ]
            }
            
            memories = self.client.get_all(
                version="v2", 
                filters=filters, 
                page=page, 
                page_size=page_size
            )
            
            return [
                {
                    "content": memory.get("content", ""),
                    "role": memory.get("role", "user"),
                    "metadata": memory.get("metadata", {}),
                    "created_at": memory.get("created_at")
                }
                for memory in memories
            ]
            
        except Exception as e:
            logger.error(f"Failed to get all Mem0 memories for user {user_id}: {e}")
            return []
    
    async def add_fact(self, user_id: str, fact: str, metadata: Optional[Dict[str, Any]] = None) -> bool:
        """Add a specific fact to memory."""
        try:
            message = {
                "role": "system",
                "content": fact
            }
            
            self.client.add([message], user_id=user_id, metadata=metadata or {})
            logger.info(f"Added fact to Mem0 for user: {user_id}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to add fact to Mem0 for user {user_id}: {e}")
            return False
    
    async def delete_memory(self, memory_id: str) -> bool:
        """Delete a specific memory."""
        try:
            self.client.delete(memory_id)
            logger.info(f"Deleted Mem0 memory: {memory_id}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to delete Mem0 memory {memory_id}: {e}")
            return False
    
    async def update_memory(self, memory_id: str, content: str, metadata: Optional[Dict[str, Any]] = None) -> bool:
        """Update a specific memory."""
        try:
            # Mem0 update method might have different parameters
            self.client.update(memory_id, metadata=metadata or {})
            logger.info(f"Updated Mem0 memory: {memory_id}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to update Mem0 memory {memory_id}: {e}")
            return False


# Global instance
mem0_memory = Mem0MemoryService() 