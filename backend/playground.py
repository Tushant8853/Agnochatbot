#!/usr/bin/env python3
"""
AgnoChat Bot Playground using Agno Framework
"""

from agno_chatbot.config.settings import setup_environment
from agno_chatbot.agents import create_chatbot_agent, create_memory_agent, create_research_agent
from agno.playground import Playground

def main():
    """Create and serve the Agno playground."""
    
    # Set up environment variables
    setup_environment()
    
    print("🚀 Creating AgnoChat Bot Playground...")
    print("=" * 50)
    
    # Create agents
    chatbot_agent = create_chatbot_agent()
    memory_agent = create_memory_agent()
    research_agent = create_research_agent()
    
    # Create playground
    playground_app = Playground(
        agents=[chatbot_agent, memory_agent, research_agent]
    )
    
    print("✅ AgnoChat Bot Playground created successfully!")
    print("📖 Available agents:")
    print("   - AgnoChatBot: Main chatbot with memory capabilities")
    print("   - Memory Agent: Specialized memory management")
    print("   - Research Agent: Web search and research capabilities")
    print()
    print("🌐 Playground will be available at: http://localhost:7777")
    print("📚 API documentation at: http://localhost:7777/docs")
    print()
    print("🔧 Starting playground server...")
    
    # Serve the playground
    playground_app.serve("playground:app", reload=True)

if __name__ == "__main__":
    main() 