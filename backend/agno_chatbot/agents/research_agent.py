"""
Research Agent with Web Search using Agno Framework
"""

from agno.agent import Agent
from agno.models.google import Gemini
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.storage.postgres import PostgresStorage

from ..config.settings import DATABASE_URL, AGNO_MODEL_ID

def create_research_agent() -> Agent:
    """Create a research agent with web search capabilities."""
    
    agent = Agent(
        name="Research Agent",
        model=Gemini(id=AGNO_MODEL_ID),
        tools=[DuckDuckGoTools()],
        storage=PostgresStorage(
            table_name="research_agent_sessions",
            db_url=DATABASE_URL
        ),
        add_datetime_to_instructions=True,
        add_history_to_messages=True,
        num_history_responses=3,
        markdown=True,
        show_tool_calls=True,
        instructions=[
            "You are a research assistant with web search capabilities.",
            "Use DuckDuckGo to search for current information.",
            "Always include sources in your responses.",
            "Provide comprehensive, well-researched answers.",
            "Cite your sources properly."
        ]
    )
    
    return agent 