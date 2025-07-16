from typing import Dict, Any, Optional
from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.models.anthropic import Claude
from agno.tools.reasoning import ReasoningTools
from agno.memory.v2.db.sqlite import SqliteMemoryDb
from agno.memory.v2.memory import Memory
from agno.storage.sqlite import SqliteStorage
from config import settings
from utils.logger import logger


class AgnoAgentService:
    """Agno framework agent service that works alongside existing system."""
    
    def __init__(self):
        self.agents = {}
        self.memory = None
        self.storage = None
        self._initialize_agno_components()
    
    def _initialize_agno_components(self):
        """Initialize Agno components."""
        try:
            # Initialize memory system
            self.memory = Memory(
                model=OpenAIChat(id="gpt-4o-mini"),  # Use OpenAI for memory management
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
            
            logger.info("Agno components initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize Agno components: {e}")
            self.memory = None
            self.storage = None
    
    def get_or_create_agent(self, user_id: str) -> Optional[Agent]:
        """Get or create an Agno agent for a user."""
        if user_id in self.agents:
            return self.agents[user_id]
        
        try:
            # Create a new Agno agent for the user
            agent = Agent(
                name=f"AgnoAgent_{user_id}",
                model=OpenAIChat(id="gpt-4o-mini"),
                tools=[ReasoningTools(add_instructions=True)],
                instructions=[
                    "You are an intelligent AI assistant with advanced reasoning capabilities.",
                    "Use reasoning to think through problems step by step.",
                    "Provide detailed, helpful responses.",
                    "Use tables and markdown formatting when appropriate.",
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
            logger.info(f"Created new Agno agent for user: {user_id}")
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
        """Process a message using Agno framework."""
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
            
            # Get memories for the user
            memories = await self.memory.get_memories(user_id=user_id)
            return {
                "memories": memories,
                "count": len(memories) if memories else 0
            }
            
        except Exception as e:
            logger.error(f"Failed to get Agno memories for user {user_id}: {e}")
            return {"memories": [], "count": 0}
    
    async def add_custom_memory(self, user_id: str, content: str, memory_type: str = "fact") -> bool:
        """Add custom memory to Agno memory system."""
        try:
            if not self.memory:
                return False
            
            # Add memory using Agno's memory system
            await self.memory.add_memory(
                user_id=user_id,
                content=content,
                memory_type=memory_type
            )
            
            logger.info(f"Added Agno memory for user {user_id}: {memory_type}")
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