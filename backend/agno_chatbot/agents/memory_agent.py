"""
Specialized Memory Management Agent using Agno Framework
"""

from agno.agent import Agent
from agno.models.google import Gemini
from agno.tools.zep import ZepTools
from agno.tools.mem0 import Mem0Tools
from agno.storage.postgres import PostgresStorage
from agno.memory.v2.db.postgres import PostgresMemoryDb
from agno.memory.v2.memory import Memory

from ..config.settings import (
    DATABASE_URL, ZEP_API_KEY, MEM0_API_KEY, 
    AGNO_MODEL_ID
)

def create_memory_agent() -> Agent:
    """Create a specialized memory management agent."""
    
    memory = Memory(
        db=PostgresMemoryDb(
            table_name="memory_agent_memories",
            db_url=DATABASE_URL
        )
    )
    
    zep_tools = ZepTools(
        api_key=ZEP_API_KEY,
        add_instructions=True
    )
    
    mem0_tools = Mem0Tools(
        api_key=MEM0_API_KEY,
        add_instructions=True
    )
    
    agent = Agent(
        name="Memory Agent",
        model=Gemini(id=AGNO_MODEL_ID),
        tools=[
            zep_tools,
            mem0_tools
        ],
        memory=memory,
        storage=PostgresStorage(
            table_name="memory_agent_sessions",
            db_url=DATABASE_URL
        ),
        enable_user_memories=True,
        enable_session_summaries=True,
        add_datetime_to_instructions=True,
        add_history_to_messages=True,
        num_history_responses=3,
        markdown=True,
        show_tool_calls=True,
        instructions=[
            "You are a specialized memory management assistant.",
            "Focus on storing, retrieving, and organizing user information.",
            "Use Zep for temporal memory and chat history.",
            "Use Mem0 for fact-based memory and long-term knowledge.",
            "Help users understand what information is stored about them.",
            "Provide memory consolidation and search capabilities."
        ]
    )
    
    return agent 