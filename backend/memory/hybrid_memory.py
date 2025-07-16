from typing import List, Dict, Any, Optional
from memory.zep_memory import zep_memory
from memory.mem0_memory import mem0_memory
from utils.logger import logger


class HybridMemoryService:
    def __init__(self):
        self.zep = zep_memory
        self.mem0 = mem0_memory
    
    async def create_user_memory(self, user_id: str, email: str, first_name: str = "", last_name: str = "") -> bool:
        """Create user in both memory systems."""
        try:
            # Create user in Zep
            zep_success = await self.zep.create_user(user_id, email, first_name, last_name)
            
            # Mem0 doesn't require explicit user creation
            mem0_success = True
            
            if zep_success and mem0_success:
                logger.info(f"Created user memory systems for: {user_id}")
                return True
            else:
                logger.warning(f"Partial user creation for {user_id}: Zep={zep_success}, Mem0={mem0_success}")
                return False
                
        except Exception as e:
            logger.error(f"Failed to create user memory for {user_id}: {e}")
            return False
    
    async def create_session(self, session_id: str, user_id: str) -> bool:
        """Create a new session in Zep."""
        return await self.zep.create_session(session_id, user_id)
    
    async def add_conversation_memory(
        self, 
        session_id: str, 
        user_id: str, 
        messages: List[Dict[str, str]]
    ) -> bool:
        """Add conversation to both memory systems."""
        try:
            # Add to Zep for temporal/session-based memory
            zep_success = await self.zep.add_messages(session_id, messages)
            
            # Add to Mem0 for long-term factual memory
            mem0_success = await self.mem0.add_messages(user_id, messages)
            
            if zep_success and mem0_success:
                logger.info(f"Added conversation to both memory systems for session: {session_id}")
                return True
            else:
                logger.warning(f"Partial memory addition for session {session_id}: Zep={zep_success}, Mem0={mem0_success}")
                return False
                
        except Exception as e:
            logger.error(f"Failed to add conversation memory for session {session_id}: {e}")
            return False
    
    async def get_memory_context(self, session_id: str, user_id: str, query: str = "") -> Dict[str, Any]:
        """Get combined memory context from both systems."""
        try:
            context = {
                "zep_context": "",
                "zep_messages": [],
                "mem0_facts": [],
                "combined_context": ""
            }
            
            # Get Zep memory (temporal/session-based)
            zep_memory = await self.zep.get_memory(session_id)
            if zep_memory:
                context["zep_context"] = zep_memory.get("context", "")
                context["zep_messages"] = zep_memory.get("messages", [])
            
            # Get Mem0 facts (long-term factual)
            if query:
                mem0_facts = await self.mem0.search_memories(user_id, query, limit=3)
            else:
                mem0_facts = await self.mem0.get_all_memories(user_id, page=1, page_size=5)
            
            context["mem0_facts"] = mem0_facts
            
            # Combine contexts intelligently
            combined_parts = []
            
            if context["zep_context"]:
                combined_parts.append(f"Recent Context: {context['zep_context']}")
            
            if context["mem0_facts"]:
                fact_summary = "\n".join([
                    f"- {fact.get('content', '')}" 
                    for fact in context["mem0_facts"][:3]
                ])
                combined_parts.append(f"Relevant Facts:\n{fact_summary}")
            
            context["combined_context"] = "\n\n".join(combined_parts)
            
            return context
            
        except Exception as e:
            logger.error(f"Failed to get memory context for session {session_id}: {e}")
            return {
                "zep_context": "",
                "zep_messages": [],
                "mem0_facts": [],
                "combined_context": ""
            }
    
    async def add_fact(self, user_id: str, fact: str, fact_type: str = "general") -> bool:
        """Add a fact to the appropriate memory system."""
        try:
            # Route based on fact type
            if fact_type in ["temporal", "relationship", "session"]:
                # Use Zep for temporal/relational facts
                return await self.zep.add_business_data(user_id, fact, "text")
            else:
                # Use Mem0 for general facts
                return await self.mem0.add_fact(user_id, fact, {"type": fact_type})
                
        except Exception as e:
            logger.error(f"Failed to add fact for user {user_id}: {e}")
            return False
    
    async def search_memory(self, user_id: str, query: str, search_type: str = "hybrid") -> Dict[str, Any]:
        """Search both memory systems based on query type."""
        try:
            results = {
                "zep_results": [],
                "mem0_results": [],
                "combined_results": []
            }
            
            if search_type in ["hybrid", "temporal", "graph"]:
                # Search Zep for temporal/graph information
                zep_results = await self.zep.search_graph(user_id, query, limit=5)
                results["zep_results"] = zep_results
            
            if search_type in ["hybrid", "factual", "long_term"]:
                # Search Mem0 for factual information
                mem0_results = await self.mem0.search_memories(user_id, query, limit=5)
                results["mem0_results"] = mem0_results
            
            # Combine results
            combined = []
            for result in results["zep_results"]:
                combined.append({
                    "source": "zep",
                    "content": result.get("fact", ""),
                    "confidence": result.get("confidence", 0.0)
                })
            
            for result in results["mem0_results"]:
                combined.append({
                    "source": "mem0",
                    "content": result.get("content", ""),
                    "score": result.get("score", 0.0)
                })
            
            # Sort by relevance (confidence/score)
            combined.sort(key=lambda x: x.get("confidence", x.get("score", 0)), reverse=True)
            results["combined_results"] = combined[:10]  # Top 10 results
            
            return results
            
        except Exception as e:
            logger.error(f"Failed to search memory for user {user_id}: {e}")
            return {
                "zep_results": [],
                "mem0_results": [],
                "combined_results": []
            }
    
    async def get_user_memory_summary(self, user_id: str) -> Dict[str, Any]:
        """Get a summary of user's memory across both systems."""
        try:
            summary = {
                "user_id": user_id,
                "zep_facts_count": 0,
                "mem0_memories_count": 0,
                "recent_context": "",
                "key_facts": []
            }
            
            # Get recent Zep context
            zep_facts = await self.zep.search_graph(user_id, "", limit=10)
            summary["zep_facts_count"] = len(zep_facts)
            
            # Get recent Mem0 memories
            mem0_memories = await self.mem0.get_all_memories(user_id, page=1, page_size=10)
            summary["mem0_memories_count"] = len(mem0_memories)
            
            # Combine key facts
            key_facts = []
            for fact in zep_facts[:5]:
                key_facts.append(fact.get("fact", ""))
            
            for memory in mem0_memories[:5]:
                key_facts.append(memory.get("content", ""))
            
            summary["key_facts"] = key_facts
            
            return summary
            
        except Exception as e:
            logger.error(f"Failed to get memory summary for user {user_id}: {e}")
            return {
                "user_id": user_id,
                "zep_facts_count": 0,
                "mem0_memories_count": 0,
                "recent_context": "",
                "key_facts": []
            }


# Global instance
hybrid_memory = HybridMemoryService() 