"""
Main AgnoChat Bot Agent using Agno Framework
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
    AGNO_MODEL_ID, AGNO_MEMORY_TABLE, AGNO_SESSION_TABLE
)

def create_chatbot_agent() -> Agent:
    """Create the main AgnoChat Bot agent with memory and tools."""
    
    # Initialize Agno memory with PostgreSQL
    memory = Memory(
        db=PostgresMemoryDb(
            table_name=AGNO_MEMORY_TABLE,
            db_url=DATABASE_URL
        )
    )
    
    # Initialize Zep tools
    zep_tools = ZepTools(
        api_key=ZEP_API_KEY,
        add_instructions=True
    )
    
    # Initialize Mem0 tools
    mem0_tools = Mem0Tools(
        api_key=MEM0_API_KEY,
        add_instructions=True
    )
    
    # Create the main Agno agent
    agent = Agent(
        name="AgnoChatBot",
        model=Gemini(id=AGNO_MODEL_ID),
        tools=[
            zep_tools,
            mem0_tools
        ],
        memory=memory,
        storage=PostgresStorage(
            table_name=AGNO_SESSION_TABLE,
            db_url=DATABASE_URL
        ),
        enable_user_memories=True,
        enable_session_summaries=True,
        add_datetime_to_instructions=True,
        add_history_to_messages=True,
        num_history_responses=5,
        markdown=True,
        show_tool_calls=True,
        instructions=[
            "Your name is Agno chat bot.",
            "You are an intelligent AI assistant with memory capabilities.",
            "Use Zep tools to store and retrieve temporal memory and chat history.",
            "Use Mem0 tools to store and retrieve fact-based memory.",
            "",
            "CRITICAL MEMORY ISOLATION RULES:",
            "1. ALWAYS check the user_id parameter before accessing any memories",
            "2. NEVER access or reference memories from other users",
            "3. When a new user starts a conversation, start completely fresh",
            "4. If you don't have memories for the current user_id, say so clearly",
            "5. Always prefix memory operations with the specific user_id",
            "6. Do not assume any information about users you haven't interacted with",
            "",
            "Memory Operations:",
            "- Store memories only for the current user_id",
            "- Retrieve memories only for the current user_id",
            "- Search memories only for the current user_id",
            "- Update memories only for the current user_id",
            "",
            "Response Guidelines:",
            "- Always provide helpful, context-aware responses",
            "- Base responses ONLY on the current user's memories",
            "- If no memories exist for the user, clearly state this",
            "- Never reference other users' information or preferences"
        ]
    )
    
    return agent 