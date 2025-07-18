from typing import Dict, Any, Optional
from agno.agent import Agent
from agno.models.google import Gemini
from agno.tools.reasoning import ReasoningTools
from agno.memory.v2.db.sqlite import SqliteMemoryDb
from agno.memory.v2.memory import Memory
from agno.memory.v2.schema import UserMemory
from agno.storage.sqlite import SqliteStorage
from config import settings
from utils.logger import logger


class AgnoAgentService:
    """Agno framework agent service that works alongside existing system using Gemini."""
    
    def __init__(self):
        self.agents = {}
        self.memory = None
        self.storage = None
        self._initialize_agno_components()
    
    def _initialize_agno_components(self):
        """Initialize Agno components with Gemini."""
        try:
            # Initialize memory system with Gemini
            self.memory = Memory(
                model=Gemini(id="gemini-2.0-flash", api_key=settings.gemini_api_key),  # Use Gemini for memory management
                db=SqliteMemoryDb(
                    table_name="agno_user_memories", 
                    db_file="agno_memory.db"
                ),
                delete_memories=True,
                clear_memories=True,
            )
            
            # Initialize storage for session management
            self.storage = SqliteStorage(
                table_name="agno_sessions", 
                db_file="agno_sessions.db"
            )
            
            logger.info("Agno components initialized successfully with Gemini")
            
        except Exception as e:
            logger.error(f"Failed to initialize Agno components: {e}")
            self.memory = None
            self.storage = None
    
    def get_or_create_agent(self, user_id: str) -> Optional[Agent]:
        """Get or create an Agno agent for a user using Gemini."""
        if user_id in self.agents:
            return self.agents[user_id]
        
        try:
            # Create a new Agno agent for the user with Gemini
            agent = Agent(
                name=f"AgnoAgent_{user_id}",
                model=Gemini(id="gemini-2.0-flash", api_key=settings.gemini_api_key),
                tools=[ReasoningTools(add_instructions=True)],
                instructions=[
                    "You are an intelligent AI assistant with advanced reasoning capabilities powered by Gemini.",
                    "Use reasoning to think through problems step by step.",
                    "Provide detailed, helpful responses.",
                    "Use tables and markdown formatting when appropriate.",
                    "Leverage your knowledge to provide accurate and insightful answers.",
                ],
                memory=self.memory,
                storage=self.storage,
                user_id=user_id,
                enable_agentic_memory=True,
                add_datetime_to_instructions=True,
                add_history_to_messages=True,
                num_history_runs=3,
                markdown=True,
                show_tool_calls=True,
            )
            
            self.agents[user_id] = agent
            logger.info(f"Created new Agno agent for user: {user_id} with Gemini")
            return agent
            
        except Exception as e:
            logger.error(f"Failed to create Agno agent for user {user_id}: {e}")
            return None
    
    async def process_message_with_agno(
        self, 
        user_id: str, 
        message: str,
        session_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """Process a message using Agno framework with Gemini."""
        try:
            agent = self.get_or_create_agent(user_id)
            if not agent:
                return {
                    "success": False,
                    "message": "Failed to initialize Agno agent",
                    "agno_response": None
                }
            
            # Run the Agno agent
            response = agent.run(message, stream=False)
            
            return {
                "success": True,
                "message": "Agno agent processed successfully",
                "agno_response": response.content,
                "reasoning_steps": response.reasoning_steps if hasattr(response, 'reasoning_steps') else None,
                "tool_calls": response.tool_calls if hasattr(response, 'tool_calls') else None
            }
            
        except Exception as e:
            logger.error(f"Agno agent processing error for user {user_id}: {e}")
            return {
                "success": False,
                "message": f"Agno processing error: {str(e)}",
                "agno_response": None
            }
    
    async def get_user_memories(self, user_id: str) -> Dict[str, Any]:
        """Get user memories from Agno memory system."""
        try:
            if not self.memory:
                return {"memories": [], "count": 0}
            
            # Get memories for the user using the correct method
            memories = self.memory.get_user_memories(user_id=user_id)
            
            # Convert UserMemory objects to dictionaries for JSON serialization
            memory_list = []
            for memory in memories:
                memory_dict = {
                    "memory_id": memory.memory_id,
                    "memory": memory.memory,
                    "topics": memory.topics or [],
                    "input": memory.input,
                    "last_updated": str(memory.last_updated) if memory.last_updated else None
                }
                memory_list.append(memory_dict)
            
            return {
                "memories": memory_list,
                "count": len(memory_list)
            }
            
        except Exception as e:
            logger.error(f"Failed to get Agno memories for user {user_id}: {e}")
            return {"memories": [], "count": 0}
    
    async def add_custom_memory(self, user_id: str, content: str, memory_type: str = "fact") -> bool:
        """Add custom memory to Agno memory system."""
        try:
            if not self.memory:
                return False
            
            # Create a UserMemory object with the correct structure
            user_memory = UserMemory(
                memory=content,
                topics=[memory_type] if memory_type else None,
                input=content
            )
            
            # Add memory using Agno's memory system with the correct method
            memory_id = self.memory.add_user_memory(
                memory=user_memory,
                user_id=user_id
            )
            
            logger.info(f"Added Agno memory for user {user_id}: {memory_type} (ID: {memory_id})")
            return True
            
        except Exception as e:
            logger.error(f"Failed to add Agno memory for user {user_id}: {e}")
            return False
    
    def clear_user_agent(self, user_id: str) -> bool:
        """Clear a user's Agno agent from cache."""
        try:
            if user_id in self.agents:
                del self.agents[user_id]
                logger.info(f"Cleared Agno agent cache for user: {user_id}")
                return True
            return False
        except Exception as e:
            logger.error(f"Failed to clear Agno agent for user {user_id}: {e}")
            return False


# Global instance
agno_agent_service = AgnoAgentService()