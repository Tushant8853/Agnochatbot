import uuid
from typing import List, Dict, Any, Optional
from datetime import datetime
from pydantic import BaseModel

from memory.hybrid_memory import hybrid_memory
from services.gemini import gemini_service
from utils.logger import logger


class ChatMessage(BaseModel):
    role: str
    content: str
    timestamp: Optional[datetime] = None


class ChatResponse(BaseModel):
    message: str
    session_id: str
    memory_context: Dict[str, Any]
    timestamp: datetime


class AgnoAgent:
    def __init__(self):
        self.memory = hybrid_memory
        self.llm = gemini_service
        self.system_context = """You are Agno, an intelligent AI assistant with advanced memory capabilities. 
        You have access to both temporal memory (recent conversations and relationships) and long-term factual memory.
        Use this context to provide personalized, context-aware responses.
        
        Key capabilities:
        - Remember user preferences and past interactions
        - Provide consistent responses based on historical context
        - Adapt your communication style based on user patterns
        - Use factual memory for accurate information recall
        
        IMPORTANT INSTRUCTIONS:
        - Always provide direct, comprehensive answers to user questions
        - Don't ask if they want to hear more - just provide the information they requested
        - Be informative and detailed in your responses
        - Use the memory context to personalize your responses
        - Be helpful, friendly, and contextually aware
        - If asked about a topic, provide specific information and examples"""
    
    async def create_user_session(self, user_id: str, email: str, first_name: str = "", last_name: str = "") -> str:
        """Create a new user session with memory initialization."""
        try:
            # Create user in memory systems
            await self.memory.create_user_memory(user_id, email, first_name, last_name)
            
            # Generate session ID
            session_id = str(uuid.uuid4())
            
            # Create session in Zep
            await self.memory.create_session(session_id, user_id)
            
            logger.info(f"Created new session {session_id} for user {user_id}")
            return session_id
            
        except Exception as e:
            logger.error(f"Failed to create user session for {user_id}: {e}")
            raise
    
    async def process_message(
        self, 
        user_id: str, 
        session_id: str, 
        message: str,
        use_memory: bool = True
    ) -> ChatResponse:
        """Process a user message and generate a response with memory context."""
        try:
            # Get memory context
            memory_context = {}
            if use_memory:
                memory_context = await self.memory.get_memory_context(session_id, user_id, message)
            
            # Prepare context for LLM
            llm_context = self.system_context
            if memory_context.get("combined_context"):
                llm_context += f"\n\nMemory Context:\n{memory_context['combined_context']}"
            
            # Generate response using Gemini
            response = await self.llm.generate_response_without_chat(message, llm_context)
            
            # Prepare messages for memory storage
            messages = [
                {"role": "user", "content": message},
                {"role": "assistant", "content": response}
            ]
            
            # Store conversation in memory
            if use_memory:
                await self.memory.add_conversation_memory(session_id, user_id, messages)
            
            # Extract and store key facts
            await self._extract_and_store_facts(user_id, message, response)
            
            return ChatResponse(
                message=response,
                session_id=session_id,
                memory_context=memory_context,
                timestamp=datetime.utcnow()
            )
            
        except Exception as e:
            logger.error(f"Failed to process message for user {user_id}: {e}")
            return ChatResponse(
                message="I apologize, but I'm experiencing technical difficulties. Please try again.",
                session_id=session_id,
                memory_context={},
                timestamp=datetime.utcnow()
            )
    
    async def _extract_and_store_facts(self, user_id: str, user_message: str, assistant_response: str) -> None:
        """Extract key facts from conversation and store them."""
        try:
            # Simple fact extraction - in a real implementation, you might use NLP
            # to identify facts, preferences, or important information
            
            # Look for preference indicators
            preference_keywords = ["like", "love", "hate", "prefer", "favorite", "dislike"]
            for keyword in preference_keywords:
                if keyword in user_message.lower():
                    fact = f"User {keyword}: {user_message}"
                    await self.memory.add_fact(user_id, fact, "preference")
                    break
            
            # Look for factual information
            fact_indicators = ["is", "are", "was", "were", "have", "has", "work", "live", "study"]
            for indicator in fact_indicators:
                if indicator in user_message.lower():
                    # Extract the sentence containing the fact
                    sentences = user_message.split('.')
                    for sentence in sentences:
                        if indicator in sentence.lower() and len(sentence.strip()) > 10:
                            await self.memory.add_fact(user_id, sentence.strip(), "fact")
                            break
                    break
                    
        except Exception as e:
            logger.error(f"Failed to extract facts for user {user_id}: {e}")
    
    async def search_memory(self, user_id: str, query: str, search_type: str = "hybrid") -> Dict[str, Any]:
        """Search user's memory for relevant information."""
        return await self.memory.search_memory(user_id, query, search_type)
    
    async def get_memory_summary(self, user_id: str) -> Dict[str, Any]:
        """Get a summary of user's memory."""
        return await self.memory.get_user_memory_summary(user_id)
    
    async def get_conversation_history(self, session_id: str) -> List[Dict[str, Any]]:
        """Get conversation history for a session."""
        try:
            memory_context = await self.memory.get_memory_context(session_id, "", "")
            return memory_context.get("zep_messages", [])
        except Exception as e:
            logger.error(f"Failed to get conversation history for session {session_id}: {e}")
            return []
    
    async def add_custom_fact(self, user_id: str, fact: str, fact_type: str = "custom") -> bool:
        """Add a custom fact to user's memory."""
        return await self.memory.add_fact(user_id, fact, fact_type)
    
    async def generate_contextual_response(
        self, 
        user_id: str, 
        message: str, 
        context_type: str = "hybrid"
    ) -> str:
        """Generate a response with specific context type."""
        try:
            # Get memory based on context type
            if context_type == "temporal":
                memory_context = await self.memory.zep.search_graph(user_id, message, limit=3)
                context = "\n".join([fact.get("fact", "") for fact in memory_context])
            elif context_type == "factual":
                memory_context = await self.memory.mem0.search_memories(user_id, message, limit=3)
                context = "\n".join([fact.get("content", "") for fact in memory_context])
            else:  # hybrid
                memory_context = await self.memory.get_memory_context("", user_id, message)
                context = memory_context.get("combined_context", "")
            
            # Generate response
            full_context = f"{self.system_context}\n\nRelevant Context:\n{context}"
            response = await self.llm.generate_response_without_chat(message, full_context)
            
            return response
            
        except Exception as e:
            logger.error(f"Failed to generate contextual response for user {user_id}: {e}")
            return "I apologize, but I'm experiencing technical difficulties. Please try again."


# Global instance
agno_agent = AgnoAgent() 