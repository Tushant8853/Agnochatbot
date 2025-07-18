from typing import List, Dict, Any, Optional
from config import settings
from utils.logger import logger

try:
    from mem0 import MemoryClient
    MEM0_AVAILABLE = True
except ImportError:
    MEM0_AVAILABLE = False

class Mem0MemoryService:
    def __init__(self):
        if MEM0_AVAILABLE and settings.mem0_api_key and settings.mem0_api_key != "your_mem0_api_key_here":
            self.client = MemoryClient(api_key=settings.mem0_api_key)
            self.use_real = True
            logger.info("Using real Mem0 API client.")
        else:
            self.client = None
            self.use_real = False
            logger.warning("Mem0 API client not available or API key missing. Using in-memory mock.")
        self._mock_memories = {}  # fallback
    
    async def add_messages(self, user_id: str, messages: List[Dict[str, str]], metadata: Optional[Dict[str, Any]] = None) -> bool:
        try:
            if self.use_real:
                # Use v2 API as recommended in documentation
                for msg in messages:
                    result = self.client.add([
                        {
                            "role": msg.get("role", "user"),
                            "content": msg.get("content", "")
                        }
                    ], user_id=user_id, metadata=metadata or {}, version="v2")
                    logger.info(f"Added message to Mem0 for user: {user_id}, result: {result}")
                logger.info(f"Added {len(messages)} messages to Mem0 for user: {user_id}")
                return True
            else:
                # Fallback: in-memory
                if user_id not in self._mock_memories:
                    self._mock_memories[user_id] = []
                for msg in messages:
                    self._mock_memories[user_id].append({
                        "role": msg.get("role", "user"),
                        "content": msg.get("content", "")
                    })
                logger.info(f"[MOCK] Added {len(messages)} messages to Mem0 for user: {user_id}")
                return True
        except Exception as e:
            logger.error(f"Failed to add messages to Mem0 for user {user_id}: {e}")
            return False
    
    async def search_memories(self, user_id: str, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        try:
            if self.use_real:
                # Use v2 API with proper filters structure
                filters = {"user_id": user_id}
                results = self.client.search(query, version="v2", filters=filters, limit=limit)
                return [
                    {
                        "content": m.get("memory", m.get("content", "")),  # Try memory field first, then content
                        "role": "system",  # Default to system since these are stored memories
                        "metadata": m.get("metadata", {}),
                        "score": m.get("score", 0.0),
                        "id": m.get("id"),
                        "user_id": m.get("user_id")
                    }
                    for m in results
                ]
            else:
                # Fallback: in-memory
                memories = self._mock_memories.get(user_id, [])
                return memories[:limit]
        except Exception as e:
            logger.error(f"Failed to search Mem0 memories for user {user_id}: {e}")
            return []
    
    async def get_all_memories(self, user_id: str, page: int = 1, page_size: int = 50) -> List[Dict[str, Any]]:
        try:
            if self.use_real:
                # Use v2 API with proper filters structure as per documentation
                filters = {"user_id": user_id}
                all_memories = self.client.get_all(version="v2", filters=filters, page=page, page_size=page_size)
                
                # Handle response structure
                if isinstance(all_memories, dict):
                    memories_list = all_memories.get('results', [])
                    if isinstance(memories_list, list):
                        logger.info(f"Found {len(memories_list)} memories for user {user_id}")
                        return [
                            {
                                "content": m.get("memory", "") if isinstance(m, dict) else str(m),  # Use 'memory' field for content
                                "role": "system",  # Default to system since these are stored memories
                                "metadata": m.get("metadata", {}) if isinstance(m, dict) else {},
                                "created_at": m.get("created_at") if isinstance(m, dict) else None,
                                "id": m.get("id") if isinstance(m, dict) else None,
                                "user_id": m.get("user_id") if isinstance(m, dict) else None
                            }
                            for m in memories_list
                        ]
                elif isinstance(all_memories, list):
                    logger.info(f"Found {len(all_memories)} memories for user {user_id}")
                    return [
                        {
                            "content": m.get("memory", "") if isinstance(m, dict) else str(m),  # Use 'memory' field for content
                            "role": "system",  # Default to system since these are stored memories
                            "metadata": m.get("metadata", {}) if isinstance(m, dict) else {},
                            "created_at": m.get("created_at") if isinstance(m, dict) else None,
                            "id": m.get("id") if isinstance(m, dict) else None,
                            "user_id": m.get("user_id") if isinstance(m, dict) else None
                        }
                        for m in all_memories
                    ]
                
                logger.warning(f"No memories found for user {user_id}")
                return []
            else:
                memories = self._mock_memories.get(user_id, [])
                start = (page - 1) * page_size
                end = start + page_size
                return memories[start:end]
        except Exception as e:
            logger.error(f"Failed to get all Mem0 memories for user {user_id}: {e}")
            return []
    
    async def count_memories(self, user_id: str) -> int:
        """Get the count of memories for a user."""
        try:
            if self.use_real:
                # Get actual count by retrieving all memories and counting them
                memories = await self.get_all_memories(user_id, page=1, page_size=1000)
                return len(memories)
            else:
                return len(self._mock_memories.get(user_id, []))
        except Exception as e:
            logger.error(f"Failed to count Mem0 memories for user {user_id}: {e}")
            return 0

    async def add_fact(self, user_id: str, fact: str, metadata: Optional[Dict[str, Any]] = None) -> bool:
        try:
            if self.use_real:
                # Use v2 API as recommended in documentation
                result = self.client.add([
                    {"role": "system", "content": fact}
                ], user_id=user_id, metadata=metadata or {}, version="v2")
                logger.info(f"Added fact to Mem0 for user: {user_id}, result: {result}")
                return True
            else:
                if user_id not in self._mock_memories:
                    self._mock_memories[user_id] = []
                self._mock_memories[user_id].append({"role": "system", "content": fact})
                logger.info(f"[MOCK] Added fact to Mem0 for user: {user_id}")
                return True
        except Exception as e:
            logger.error(f"Failed to add fact to Mem0 for user {user_id}: {e}")
            return False

    async def get_memory(self, memory_id: str) -> Optional[Dict[str, Any]]:
        """Get a specific memory by ID."""
        try:
            if self.use_real:
                memory = self.client.get(memory_id=memory_id)
                return {
                    "id": memory.get("id"),
                    "memory": memory.get("memory"),
                    "user_id": memory.get("user_id"),
                    "agent_id": memory.get("agent_id"),
                    "app_id": memory.get("app_id"),
                    "run_id": memory.get("run_id"),
                    "hash": memory.get("hash"),
                    "metadata": memory.get("metadata", {}),
                    "created_at": memory.get("created_at"),
                    "updated_at": memory.get("updated_at")
                }
            else:
                # Mock implementation
                return None
        except Exception as e:
            logger.error(f"Failed to get memory {memory_id}: {e}")
            return None

    async def get_memory_history(self, memory_id: str) -> List[Dict[str, Any]]:
        """Get the history of changes for a specific memory."""
        try:
            if self.use_real:
                history = self.client.history(memory_id)
                return [
                    {
                        "id": entry.get("id"),
                        "memory_id": entry.get("memory_id"),
                        "input": entry.get("input", []),
                        "old_memory": entry.get("old_memory"),
                        "new_memory": entry.get("new_memory"),
                        "user_id": entry.get("user_id"),
                        "event": entry.get("event"),
                        "metadata": entry.get("metadata", {}),
                        "created_at": entry.get("created_at"),
                        "updated_at": entry.get("updated_at")
                    }
                    for entry in history
                ]
            else:
                # Mock implementation
                return []
        except Exception as e:
            logger.error(f"Failed to get memory history for {memory_id}: {e}")
            return []

# Global instance
mem0_memory = Mem0MemoryService() 