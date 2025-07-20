Do not answer yet. This is just another part of the text I want to send you. Just receive and acknowledge as "Part 1/8 received" and wait for the next part.
[START PART 1/8]
Build a production-ready AI chatbot backend using Python and FastAPI with the following components and real integrations:

🧠 Objective:
Use the Agno Framework to handle chatbot routing and request processing.
Integrate Google Gemini API (real API key provided) for generating responses.
Integrate **Zep** for chat history & temporal knowledge graph memory.
Integrate **Mem0** for long-term fact-based memory and retrieval.
Use a hybrid memory strategy to consolidate and route memory intelligently.
Implement user authentication with JWT and PostgreSQL (Railway-hosted DB).

⚠️ Requirements (no mockups or stubs):
- Use the provided real API keys and endpoints for Zep, Mem0, and Gemini.
- Ensure all data is stored in the real Zep and Mem0 systems.
- Use real database connection for authentication and session management.
- Store and retrieve chat history from Zep.
- Extract, update, and search facts in Mem0.
- All endpoints must be real and testable, no simulated/dummy data.

🔐 Authentication:
- Signup (`/api/auth/signup`) - create user in PostgreSQL (Railway DB)
- Login (`/api/auth/login`) - validate credentials, return JWT token
- Logout (`/api/auth/logout`) - token invalidation (client-side logout)

🧩 Memory Roles:
- Zep: Temporal + relationship memory (e.g., user sessions, chat flow)
- Mem0: Fact-based memory (e.g., "I live in Delhi" → {location: Delhi})
- Hybrid logic:
   - Use Zep for session tracking, entity linking
   - Use Mem0 for retrieval like "Where do I live?"
   - Consolidate memory using `/api/memory/consolidate` to remove redundancy

📦 Environment:
- Python with FastAPI
- PostgreSQL DB on Railway (use `DATABASE_URL`)
- JWT-based auth (use provided secret & algorithm)
- Use requests or HTTPX to call real external APIs (Gemini, Zep, Mem0)
- Modular structure: routers for auth, chat, memory, history

📡 External API Configuration (use real keys):
DATABASE_URL=postgresql://postgres:BBHybyJPpEPOSxzROzNJosWcOhrjuANY@trolley.proxy.rlwy.net:22479/railway
SECRET_KEY=AgnoChatSuperSecretKey_2024_ChangeMe!
ALGORITHM=HS256
GEMINI_API_KEY=AIzaSyC4rm2apYeyP3_SbDWde2fZUjgtSRiVxqo
ZEP_API_KEY=z_1dWlkIjoiNGZmYzY0YWUtOGVjMC00MDZhLTliNzQtYzFiYTk3MWUwOGE0In0.bYSkQGYuRLUWZFI36aufjKeHC0eCivYnoMNwy7BHxFSmlF93jDh75sbEzOto1bk4gpZfowutc8cRZlrY8N26Zw
ZEP_BASE_URL=https://api.getzep.com
MEM0_API_KEY=m0-NVMJ3xOTkp80sy9jlcvplcufEb6OlCUe9u8EdOKD
MEM0_API_URL=https://api.mem0.ai

🚀 Required Endpoints:
1. `POST /api/chat`  
→ Accepts user message, calls Gemini, saves message to Zep, updates Mem0  
Input:
```json
{ "user_id": "user123", "session_id": "sess789", "message": "I live in Delhi and like chess." }


GET /api/memory?user_id=user123&session_id=sess789
→ View merged memory from Zep (entities) and Mem0 (facts)

POST /api/memory/consolidate
→ Deduplicate facts between Zep & Mem0, consolidate into Mem0

POST /api/session/start
→ Starts session in Zep with session_id

GET /api/history?user_id=user123&session_id=sess789
→ Fetch full chat history from Zep

POST /api/memory/search
→ Search facts in Mem0 using query like "Where do I live?"

POST /api/auth/signup
→ User registration in PostgreSQL

POST /api/auth/login
→ Returns JWT token

POST /api/auth/logout
→ Handles logout (token invalidation or frontend discard)

📑 Required Docs for Editor:
Please upload the following real documentation for reference:

Agno Framework Docs (core setup, routing logic)

Zep API Docs (ChatHistory, memory APIs, knowledge graph usage)

Mem0 API Docs (Fact extraction, update pipeline, search query model)

🧠 Memory Explanation (for the tool and docs):

Zep is responsible for capturing conversational context, temporal relationships, and entity linking. For example:

"My dog's name is Bruno" → creates a knowledge graph node dog → Bruno

Stored using Zep’s ChatHistory and GraphMemory

Mem0 handles fact extraction, long-term storage, and fast retrieval of statements:

"I live in Delhi" → fact: { location: "Delhi" }

These facts are used for context-aware responses across sessions

The hybrid memory system ensures:

Zep tracks how knowledge evolves over time.

Mem0 allows direct question-answering with facts.

Redundant data is consolidated via /api/memory/consolidate.

🛠 Development Guidelines:

Use async FastAPI endpoints with proper logging

Split modules: auth.py, chat.py, memory.py, zep_utils.py, mem0_utils.py

Use Pydantic models for request/response validation

Add comments for Zep + Mem0 API call payloads for debugging

Token authentication middleware with JWT for secured routes

🎯 Goals:

No dummy calls: all calls to Zep, Mem0, Gemini must work

Can test the flow: login → chat → memory view → search

Can see memory graphs and facts in Zep/Mem0 dashboards

Full session tracking and response generation

markdown
Copy
Edit


Mem0 home pagedark logo


Search...
⌘K

Documentation
Integrations
Overview
Langchain
LangGraph
LlamaIndex
Agno
Autogen
CrewAI
OpenAI Agents SDK
Google Agent Development Kit
Mastra
Vercel AI SDK
Livekit
Pipecat
ElevenLabs
AWS Bedrock
Flowise
Langchain Tools
AgentOps
Keywords AI
Dify
Raycast Extension
Your Dashboard
Documentation
OpenMemory
Examples
Integrations
API Reference
Changelog
Integrations
Agno
🔐 Mem0 is now SOC 2 and HIPAA compliant! We're committed to the highest standards of data security and privacy, enabling secure memory for enterprises, healthcare, and beyond. Learn more
This integration of Mem0 with [Agno](https://github.com/agno-agi/agno, enables persistent, multimodal memory for Agno-based agents - improving personalization, context awareness, and continuity across conversations.
​
Overview
Store and retrieve memories from Mem0 within Agno agents
Support for multimodal interactions (text and images)
Semantic search for relevant past conversations
Personalized responses based on user history
One-line memory integration via Mem0Tools
​
Prerequisites
Before setting up Mem0 with Agno, ensure you have:
Installed the required packages:

Copy

Ask AI
pip install agno mem0ai
Valid API keys:
Mem0 API Key
OpenAI API Key (for the agent model)
​
Quick Integration (Using Mem0Tools)
The simplest way to integrate Mem0 with Agno Agents is to use Mem0 as a tool using built-in Mem0Tools:

Copy

Ask AI
from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.tools.mem0 import Mem0Tools

agent = Agent(
    name="Memory Agent",
    model=OpenAIChat(id="gpt-4o-mini"),
    tools=[Mem0Tools()],
    description="An assistant that remembers and personalizes using Mem0 memory."
)
This enables memory functionality out of the box:
Persistent memory writing: Mem0Tools uses MemoryClient.add(...) to store messages from user-agent interactions, including optional metadata such as user ID or session.
Contextual memory search: Compatible queries use MemoryClient.search(...) to retrieve relevant past messages, improving contextual understanding.
Multimodal support: Both text and image inputs are supported, allowing richer memory records.
Mem0Tools uses the MemoryClient under the hood and requires no additional setup. You can customize its behavior by modifying your tools list or extending it in code.
​
Full Manual Example
Note: Mem0 can also be used with Agno Agents as a separate memory layer.
The following example demonstrates how to create an Agno agent with Mem0 memory integration, including support for image processing:

Copy

Ask AI
import base64
from pathlib import Path
from typing import Optional

from agno.agent import Agent
from agno.media import Image
from agno.models.openai import OpenAIChat
from mem0 import MemoryClient

# Initialize the Mem0 client
client = MemoryClient()

# Define the agent
agent = Agent(
    name="Personal Agent",
    model=OpenAIChat(id="gpt-4"),
    description="You are a helpful personal agent that helps me with day to day activities."
                "You can process both text and images.",
    markdown=True
)


def chat_user(
    user_input: Optional[str] = None,
    user_id: str = "user_123",
    image_path: Optional[str] = None
) -> str:
    """
    Handle user input with memory integration, supporting both text and images.

    Args:
        user_input: The user's text input
        user_id: Unique identifier for the user
        image_path: Path to an image file if provided

    Returns:
        The agent's response as a string
    """
    if image_path:
        # Convert image to base64
        with open(image_path, "rb") as image_file:
            base64_image = base64.b64encode(image_file.read()).decode("utf-8")

        # Create message objects for text and image
        messages = []

        if user_input:
            messages.append({
                "role": "user",
                "content": user_input
            })

        messages.append({
            "role": "user",
            "content": {
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/jpeg;base64,{base64_image}"
                }
            }
        })

        # Store messages in memory
        client.add(messages, user_id=user_id)
        print("✅ Image and text stored in memory.")

    if user_input:
        # Search for relevant memories
        memories = client.search(user_input, user_id=user_id)
        memory_context = "\n".join(f"- {m['memory']}" for m in memories)

        # Construct the prompt
        prompt = f"""
You are a helpful personal assistant who helps users with their day-to-day activities and keeps track of everything.

Your task is to:
1. Analyze the given image (if present) and extract meaningful details to answer the user's question.
2. Use your past memory of the user to personalize your answer.
3. Combine the image content and memory to generate a helpful, context-aware response.

Here is what I remember about the user:
{memory_context}

User question:
{user_input}
"""
        # Get response from agent
        if image_path:
            response = agent.run(prompt, images=[Image(filepath=Path(image_path))])
        else:
            response = agent.run(prompt)

        # Store the interaction in memory
        client.add(f"User: {user_input}\nAssistant: {response.content}", user_id=user_id)
        return response.content

    return "No user input or image provided."


# Example Usage
if __name__ == "__main__":
    response = chat_user(
        "This is the picture of what I brought with me in the trip to Bahamas",
        image_path="travel_items.jpeg",
        user_id="user_123"
    )
    print(response)
​
Key Features
​
1. Multimodal Memory Storage
The integration supports storing both text and image data:
Text Storage: Conversation history is saved in a structured format
Image Analysis: Agents can analyze images and store visual information
Combined Context: Memory retrieval combines both text and visual data
​
2. Personalized Agent Responses
Improve your agent’s context awareness:
Memory Retrieval: Semantic search finds relevant past interactions
User Preferences: Personalize responses based on stored user information
Continuity: Maintain conversation threads across multiple sessions
​
3. Flexible Configuration
Customize the integration to your needs:
Use Mem0Tools() for drop-in memory support
Use MemoryClient directly for advanced control
User Identification: Organize memories by user ID
Memory Search: Configure search relevance and result count
Memory Formatting: Support for various OpenAI message formats
​
Help & Resources
Agno Documentation
Mem0 Platform
Discord
Join our community
GitHub
Ask questions on GitHub
Support
Talk to founders
Was this page helpful?


Yes

No
Suggest edits
Raise issue
Previous
Autogen
Next
discord
x
github
linkedin
Powered by Mintlify
On this page
Overview
Prerequisites
Quick Integration (Using Mem0Tools)
Full Manual Example
Key Features
1. Multimodal Memory Storage
2. Personalized Agent Responses
3. Flexible Configuration
Help & Resources



Mem0 home pagedark logo


Search...
⌘K

Documentation
Getting Started
What is Mem0?
Quickstart
FAQs
Core Concepts
Memory Types
Memory Operations
Platform
Overview
Quickstart
Features
Open Source
Overview
Python SDK Quickstart
Node SDK Quickstart
Features
Graph Memory
LLMs
Vector Databases
Embedding Models
Contribution
Development
Documentation
Your Dashboard
Documentation
OpenMemory
Examples
Integrations
API Reference
Changelog
Getting Started
What is Mem0?
🔐 Mem0 is now SOC 2 and HIPAA compliant! We're committed to the highest standards of data security and privacy, enabling secure memory for enterprises, healthcare, and beyond. Learn more
Mem0 is a memory layer designed for modern AI agents. It acts as a persistent memory layer that agents can use to:
Recall relevant past interactions
Store important user preferences and factual context
Learn from successes and failures
It gives AI agents memory so they can remember, learn, and evolve across interactions. Mem0 integrates easily into your agent stack and scales from prototypes to production systems.
​
Stateless vs. Stateful Agents
Most current agents are stateless: they process a query, generate a response, and forget everything. Even with huge context windows, everything resets the next session.
Stateful agents, powered by Mem0, are different. They retain context, recall what matters, and behave more intelligently over time.

​
Where Memory Fits in the Agent Stack
Mem0 sits alongside your retriever, planner, and LLM. Unlike retrieval-based systems (like RAG), Mem0 tracks past interactions, stores long-term knowledge, and evolves the agent’s behavior.

Memory is not about pushing more tokens into a prompt but about intelligently remembering context that matters. This distinction matters:
Capability	Context Window	Mem0 Memory
Retention	Temporary	Persistent
Cost	Grows with input size	Optimized (only what matters)
Recall	Token proximity	Relevance + intent-based
Personalization	None	Deep, evolving profile
Behavior	Reactive	Adaptive
​
Memory vs. RAG: Complementary Tools
RAG (Retrieval-Augmented Generation) is great for fetching facts from documents. But it’s stateless. It doesn’t know who the user is, what they’ve asked before, or what failed last time.
Mem0 provides continuity. It stores decisions, preferences, and context—not just knowledge.
Aspect	RAG	Mem0 Memory
Statefulness	Stateless	Stateful
Recall Type	Document lookup	Evolving user context
Use Case	Ground answers in data	Guide behavior across time
Together, they’re stronger: RAG informs the LLM; Mem0 shapes its memory.
​
Types of Memory in Mem0
Mem0 supports different kinds of memory to mimic how humans
[END PART 1/8]
Remember not answering yet. Just acknowledge you received this part with the message "Part 1/8 received" and wait for the next part.












Do not answer yet. This is just another part of the text I want to send you. Just receive and acknowledge as "Part 2/8 received" and wait for the next part.
[START PART 2/8]
 store information:
Working Memory: short-term session awareness
Factual Memory: long-term structured knowledge (e.g., preferences, settings)
Episodic Memory: records specific past conversations
Semantic Memory: builds general knowledge over time
​
Why Developers Choose Mem0
Mem0 isn’t a wrapper around a vector store. It’s a full memory engine with:
LLM-based extraction: Intelligently decides what to remember
Filtering & decay: Avoids memory bloat, forgets irrelevant info
Costs Reduction: Save compute costs with smart prompt injection of only relevant memories
Dashboards & APIs: Observability, fine-grained control
Cloud and OSS: Use our platform version or our open-source SDK version
You plug Mem0 into your agent framework, it doesn’t replace your LLM or workflows. Instead, it adds a smart memory layer on top.
​
Core Capabilities
Reduced token usage and faster responses: sub-50 ms lookups
Semantic memory: procedural, episodic, and factual support
Multimodal support: handle both text and images
Graph memory: connect insights and entities across sessions
Host your way: either a managed service or a self-hosted version
​
Getting Started
Mem0 offers two powerful ways to leverage our technology: our managed platform and our open source solution.
Quickstart
Integrate Mem0 in a few lines of code
Playground
Mem0 in action
Examples
See what you can build with Mem0
​
Need help?
If you have any questions, please feel free to reach out to us using one of the following methods:
Discord
Join our community
GitHub
Ask questions on GitHub
Support
Talk to founders
Was this page helpful?


Yes

No
Suggest edits
Raise issue
Quickstart
Next
discord
x
github
linkedin
Powered by Mintlify
On this page
Stateless vs. Stateful Agents
Where Memory Fits in the Agent Stack
Memory vs. RAG: Complementary Tools
Types of Memory in Mem0
Why Developers Choose Mem0
Core Capabilities
Getting Started
Need help?
What is Mem0? - Mem0

Mem0 home pagedark logo


Search...
⌘K

Documentation
Getting Started
What is Mem0?
Quickstart
FAQs
Core Concepts
Memory Types
Memory Operations
Platform
Overview
Quickstart
Features
Open Source
Overview
Python SDK Quickstart
Node SDK Quickstart
Features
Graph Memory
LLMs
Vector Databases
Embedding Models
Contribution
Development
Documentation
Your Dashboard
Documentation
OpenMemory
Examples
Integrations
API Reference
Changelog
Getting Started
Quickstart
🔐 Mem0 is now SOC 2 and HIPAA compliant! We're committed to the highest standards of data security and privacy, enabling secure memory for enterprises, healthcare, and beyond. Learn more
Mem0 offers two powerful ways to leverage our technology: our managed platform and our open source solution.
Check out our Playground to see Mem0 in action.
Mem0 Platform (Managed Solution)
Better, faster, fully managed, and hassle free solution.
Mem0 Open Source
Self hosted, fully customizable, and open source.
​
Mem0 Platform (Managed Solution)
Our fully managed platform provides a hassle-free way to integrate Mem0’s capabilities into your AI agents and assistants. Sign up for Mem0 platform here.
The Mem0 SDK supports both Python and JavaScript, with full TypeScript support as well.
Follow the steps below to get started with Mem0 Platform:
Install Mem0
Add Memories
Retrieve Memories
​
1. Install Mem0
Install package

Get API Key

​
2. Add Memories
Instantiate client

Add memories

​
3. Retrieve Memories
Search for relevant memories

Get all memories of a user

Mem0 Platform
Learn more about Mem0 platform
​
Mem0 Open Source
Our open-source version is available for those who prefer full control and customization. You can self-host Mem0 on your infrastructure and integrate it with your AI agents and assistants. Checkout our GitHub repository
Follow the steps below to get started with Mem0 Open Source:
Install Mem0 Open Source
Add Memories
Retrieve Memories
​
1. Install Mem0 Open Source
Install package


pip

npm

Copy

Ask AI
pip install mem0ai
​
2. Add Memories 
Instantiate client


Python

TypeScript

Copy

Ask AI
from mem0 import Memory
m = Memory()
Add memories


Code

TypeScript

Output

Copy

Ask AI
# For a user
messages = [
    {
        "role": "user",
        "content": "I like to drink coffee in the morning and go for a walk"
    }
]
result = m.add(messages, user_id="alice", metadata={"category": "preferences"})
​
3. Retrieve Memories 
Search for relevant memories


Python

TypeScript

Output

Copy

Ask AI
related_memories = m.search("Should I drink coffee or tea?", user_id="alice")
Mem0 OSS Python SDK
Learn more about Mem0 OSS Python SDK
Mem0 OSS Node.js SDK
Learn more about Mem0 OSS Node.js SDK
Was this page helpful?


Yes

No
Suggest edits
Raise issue
Previous
FAQs
Next
discord
x
github
linkedin
Powered by Mintlify
On this page
Mem0 Platform (Managed Solution)
1. Install Mem0
2. Add Memories
3. Retrieve Memories
Mem0 Open Source
1. Install Mem0 Open Source
2. Add Memories 
3. Retrieve Memories 
Quickstart - Mem0


Mem0 home pagedark logo


Search...
⌘K

Documentation
Getting Started
What is Mem0?
Quickstart
FAQs
Core Concepts
Memory Types
Memory Operations
Platform
Overview
Quickstart
Features
Open Source
Overview
Python SDK Quickstart
Node SDK Quickstart
Features
Graph Memory
LLMs
Vector Databases
Embedding Models
Contribution
Development
Documentation
Your Dashboard
Documentation
OpenMemory
Examples
Integrations
API Reference
Changelog
Open Source
Python SDK Quickstart
Get started with Mem0 quickly!

🔐 Mem0 is now SOC 2 and HIPAA compliant! We're committed to the highest standards of data security and privacy, enabling secure memory for enterprises, healthcare, and beyond. Learn more
Welcome to the Mem0 quickstart guide. This guide will help you get up and running with Mem0 in no time.
​
Installation
To install Mem0, you can use pip. Run the following command in your terminal:

Copy

Ask AI
pip install mem0ai
​
Basic Usage
​
Initialize Mem0
Basic
Async
Advanced
Advanced (Graph Memory)

Copy

Ask AI
import os
from mem0 import Memory

os.environ["OPENAI_API_KEY"] = "your-api-key"

m = Memory()
​
Store a Memory

Code

Output

Copy

Ask AI
messages = [
    {"role": "user", "content": "I'm planning to watch a movie tonight. Any recommendations?"},
    {"role": "assistant", "content": "How about a thriller movies? They can be quite engaging."},
    {"role": "user", "content": "I'm not a big fan of thriller movies but I love sci-fi movies."},
    {"role": "assistant", "content": "Got it! I'll avoid thriller recommendations and suggest sci-fi movies in the future."}
]

# Store inferred memories (default behavior)
result = m.add(messages, user_id="alice", metadata={"category": "movie_recommendations"})

# Store raw messages without inference
# result = m.add(messages, user_id="alice", metadata={"category": "movie_recommendations"}, infer=False)
​
Retrieve Memories

Code

Output

Copy

Ask AI
# Get all memories
all_memories = m.get_all(user_id="alice")


Code

Output

Copy

Ask AI
# Get a single memory by ID
specific_memory = m.get("892db2ae-06d9-49e5-8b3e-585ef9b85b8e")
​
Search Memories

Code

Output

Copy

Ask AI
related_memories = m.search(query="What do you know about me?", user_id="alice")
​
Update a Memory

Code

Output

Copy

Ask AI
result = m.update(memory_id="892db2ae-06d9-49e5-8b3e-585ef9b85b8e", data="I love India, it is my favorite country.")
​
Memory History

Code

Output

Copy

Ask AI
history = m.history(memory_id="892db2ae-06d9-49e5-8b3e-585ef9b85b8e")
​
Delete Memory

Copy

Ask AI
# Delete a memory by id
m.delete(memory_id="892db2ae-06d9-49e5-8b3e-585ef9b85b8e")
# Delete all memories for a user
m.delete_all(user_id="alice")
​
Reset Memory

Copy

Ask AI
m.reset() # Reset all memories
​
Configuration Parameters
Mem0 offers extensive configuration options to customize its behavior according to your needs. These configurations span across different components like vector stores, language models, embedders, and graph stores.
Vector Store Configuration

Parameter	Description	Default
provider	Vector store provider (e.g., “qdrant”)	“qdrant”
host	Host address	”localhost”
port	Port number	6333
LLM Configuration

Parameter	Description	Provider
provider	LLM provider (e.g., “openai”, “anthropic”)	All
model	Model to use	All
temperature	Temperature of the model	All
api_key	API key to use	All
max_tokens	Tokens to generate	All
top_p	Probability threshold for nucleus sampling	All
top_k	Number of highest probability tokens to keep	All
http_client_proxies	Allow proxy server settings	AzureOpenAI
models	List of models	Openrouter
route	Routing strategy	Openrouter
openrouter_base_url	Base URL for Openrouter API	Openrouter
site_url	Site URL	Openrouter
app_name	Application name	Openrouter
ollama_base_url	Base URL for Ollama API	Ollama
openai_base_url	Base URL for OpenAI API	OpenAI
azure_kwargs	Azure LLM args for initialization	AzureOpenAI
deepseek_base_url	Base URL for DeepSeek API	DeepSeek
Embedder Configuration

Parameter	Description	Default
provider	Embedding provider	”openai”
model	Embedding model to use	”text-embedding-3-small”
api_key	API key for embedding service	None
Graph Store Configuration

Parameter	Description	Default
provider	Graph store provider (e.g., “neo4j”)	“neo4j”
url	Connection URL	None
username	Authentication username	None
password	Authentication password	None
General Configuration

Parameter	Description	Default
history_db_path	Path to the history database	”/history.db”
version	API version	”v1.1”
custom_fact_extraction_prompt	Custom prompt for memory processing	None
custom_update_memory_prompt	Custom prompt for update memory	None
Complete Configuration Example


Copy

Ask AI
config = {
    "vector_store": {
        "provider": "qdrant",
        "config": {
            "host": "localhost",
            "port": 6333
        }
    },
    "llm": {
        "provider": "openai",
        "config": {
            "api_key": "your-api-key",
            "model": "gpt-4"
        }
    },
    "embedder": {
        "provider": "openai",
        "config": {
            "api_key": "your-api-key",
            "model": "text-embedding-3-small"
        }
    },
    "graph_store": {
        "provider": "neo4j",
        "config": {
            "url": "neo4j+s://your-instance",
            "username": "neo4j",
            "password": "password"
        }
    },
    "history_db_path": "/path/to/history.db",
    "version": "v1.1",
    "custom_fact_extraction_prompt": "Optional custom prompt for fact extraction for memory",
    "custom_update_memory_prompt": "Optional custom prompt for update memory"
}
​
Run Mem0 Locally
Please refer to the example Mem0 with Ollama to run Mem0 locally.
​
Chat Completion
Mem0 can be easily integrated into chat applications to enhance conversational agents with structured memory. Mem0’s APIs are designed to be compatible with OpenAI’s, with the goal of making it easy to leverage Mem0 in applications you may have already built.
If you have a Mem0 API key, you can use it to initialize the client. Alternatively, you can initialize Mem0 without an API key if you’re using it locally.
Mem0 supports several language models (LLMs) through integration with various providers.
​
Use Mem0 Platform

Copy

Ask AI
from mem0.proxy.main import Mem0

client = Mem0(api_key="m0-xxx")

# First interaction: Storing user preferences
messages = [
  {
    "role": "user",
    "content": "I love indian food but I cannot eat pizza since allergic to cheese."
  },
]
user_id = "alice"
chat_completion = client.chat.completions.create(messages=messages, model="gpt-4o-mini", user_id=user_id)
# Memory saved after this will look like: "Loves Indian food. Allergic to cheese and cannot eat pizza."

# Second interaction: Leveraging stored memory
messages = [
  {
    "role": "user",
    "content": "Suggest restaurants in San Francisco to eat.",
  }
]

chat_completion = client.chat.completions.create(messages=messages, model="gpt-4o-mini", user_id=user_id)
print(chat_completion.choices[0].message.content)
# Answer: You might enjoy Indian restaurants in San Francisco, such as Amber India, Dosa, or Curry Up Now, which offer delicious options without cheese.
In this example, you can see how the second response is tailored based on the information provided in the first interaction. Mem0 remembers the user’s preference for Indian food and their cheese allergy, using this information to provide more relevant and personalized restaurant suggestions in San Francisco.
​
Use Mem0 OSS

Copy

Ask AI
config = {
    "vector_store": {
        "provider": "qdrant",
        "config": {
            "host": "localhost",
            "port": 6333,
        }
    },
}

client = Mem0(config=config)

chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": "What's the capital of France?",
        }
    ],
    model="gpt-4o",
)
​
APIs
Get started with using Mem0 APIs in your applications. For more details, refer to the Platform.
Here is an example of how to use Mem0 APIs:

Copy

Ask AI
import os
from mem0 import MemoryClient

os.environ["MEM0_API_KEY"] = "your-api-key"

client = MemoryClient() # get api_key from https://app.mem0.ai/

# Store messages
messages = [
    {"role": "user", "content": "Hi, I'm Alex. I'm a vegetarian and I'm allergic to nuts."},
    {"role": "assistant", "content": "Hello Alex! I've noted that you're a vegetarian and have a nut allergy. I'll keep this in mind for any food-related recommendations or discussions."}
]
result = client.add(messages, user_id="alex")
print(result)

# Retrieve memories
all_memories = client.get_all(user_id="alex")
print(all_memories)

# Search memories
query = "What do you know about me?"
related_memories = client.search(query, user_id="alex")

# Get memory history
history = client.history(memory_id="m1")
print(history)
​
Contributing
We welcome contributions to Mem0! Here’s how you can contribute:
Fork the repository and create your branch from main.
Clone the forked repository to your local machine.
Install the project dependencies:

Copy

Ask AI
poetry install
Install pre-commit hooks:

Copy

Ask AI
pip install pre-commit  # If pre-commit is not already installed
pre-commit install
Make your changes and ensure they adhere to the project’s coding standards.
Run the tests locally:

Copy

Ask AI
poetry run pytest
If all tests pass, commit your changes and push to your fork.
Open a pull request with a c
[END PART 2/8]
Remember not answering yet. Just acknowledge you received this part with the message "Part 2/8 received" and wait for the next part.










Do not answer yet. This is just another part of the text I want to send you. Just receive and acknowledge as "Part 3/8 received" and wait for the next part.
[START PART 3/8]
lear title and description.
Please make sure your code follows our coding conventions and is well-documented. We appreciate your contributions to make Mem0 better!
If you have any questions, please feel free to reach out to us using one of the following methods:
Discord
Join our community
GitHub
Ask questions on GitHub
Support
Talk to founders
Was this page helpful?


Yes

No
Suggest edits
Raise issue
Previous
Node SDK Quickstart
Get started with Mem0 quickly!
Next
discord
x
github
linkedin
Powered by Mintlify
On this page
Installation
Basic Usage
Initialize Mem0
Store a Memory
Retrieve Memories
Search Memories
Update a Memory
Memory History
Delete Memory
Reset Memory
Configuration Parameters
Run Mem0 Locally
Chat Completion
Use Mem0 Platform
Use Mem0 OSS
APIs
Contributing
Python SDK Quickstart - Mem0



Agno home pagedark logo

Search...
⌘K

Ask AI
Discord
Community
agno-agi/agno
30,268

User Guide
Examples
Workspaces
FAQs
API reference
Changelog
Introduction
What is Agno?
Your first Agents
Multi Agent Systems
Playground
Monitoring & Debugging
Community & Support
Concepts
Agents
Teams
Models
Tools
Reasoning
Memory
Knowledge
Chunking
Vector DBs
Storage
Embeddings
Evals
Workflows
Workflows v2 (Beta)
Applications
Other
Agent UI
Agent API
Observability
Testing
How to
Install & Setup
Contributing to Agno
Migrate from Phidata to Agno
Authenticate with Agno Platform
On this page
Getting Started
Why Agno?
Dive deeper
Introduction
What is Agno?

Copy page

Agno is a python framework for building multi-agent systems with shared memory, knowledge and reasoning.

Engineers and researchers use Agno to build:
Level 1: Agents with tools and instructions (example).
Level 2: Agents with knowledge and storage (example).
Level 3: Agents with memory and reasoning (example).
Level 4: Agent Teams that can reason and collaborate (example).
Level 5: Agentic Workflows with state and determinism (example).
Example: Level 1 Reasoning Agent that uses the YFinance API to answer questions:
Reasoning Finance Agent

Copy

Ask AI
from agno.agent import Agent
from agno.models.anthropic import Claude
from agno.tools.reasoning import ReasoningTools
from agno.tools.yfinance import YFinanceTools

reasoning_agent = Agent(
    model=Claude(id="claude-sonnet-4-20250514"),
    tools=[
        ReasoningTools(add_instructions=True),
        YFinanceTools(stock_price=True, analyst_recommendations=True, company_info=True, company_news=True),
    ],
    instructions="Use tables to display data.",
    markdown=True,
)
Watch the reasoning finance agent in action

​
Getting Started
If you’re new to Agno, learn how to build your first Agent, chat with it on the playground and monitor it on app.agno.com.
Your first Agents
Learn how to build Agents with Agno
Agent Playground
Chat with your Agents using a beautiful Agent UI
Agent Monitoring
Monitor your Agents on agno.com
After that, dive deeper into the concepts below or explore the examples gallery to build real-world applications with Agno.
​
Why Agno?
Agno will help you build best-in-class, highly-performant agentic systems, saving you hours of research and boilerplate. Here are some key features that set Agno apart:
Model Agnostic: Agno provides a unified interface to 23+ model providers, no lock-in.
Highly performant: Agents instantiate in ~3μs and use ~6.5Kib memory on average.
Reasoning is a first class citizen: Reasoning improves reliability and is a must-have for complex autonomous agents. Agno supports 3 approaches to reasoning: Reasoning Models, ReasoningTools or our custom chain-of-thought approach.
Natively Multi-Modal: Agno Agents are natively multi-modal, they accept text, image, audio and video as input and generate text, image, audio and video as output.
Advanced Multi-Agent Architecture: Agno provides an industry leading multi-agent architecture (Agent Teams) with reasoning, memory, and shared context.
Built-in Agentic Search: Agents can search for information at runtime using 20+ vector databases. Agno provides state-of-the-art Agentic RAG, fully async and highly performant.
Built-in Memory & Session Storage: Agents come with built-in Storage & Memory drivers that give your Agents long-term memory and session storage.
Structured Outputs: Agno Agents can return fully-typed responses using model provided structured outputs or json_mode.
Pre-built FastAPI Routes: After building your Agents, serve them using pre-built FastAPI routes. 0 to production in minutes.
Monitoring: Monitor agent sessions and performance in real-time on agno.com.
​
Dive deeper
Agno is a battle-tested framework with a state of the art reasoning and multi-agent architecture, read the following guides to learn more:
Agents
Learn how to build lightning fast Agents.
Teams
Build autonomous multi-agent teams.
Models
Use any model, any provider, no lock-in.
Tools
100s of tools to extend your Agents.
Reasoning
Make Agents “think” and “analyze”.
Knowledge
Give Agents domain-specific knowledge.
Vector Databases
Store and search your knowledge base.
Storage
Persist Agent session and state in a database.
Memory
Remember user details and session summaries.
Embeddings
Generate embeddings for your knowledge base.
Workflows
Deterministic, stateful, multi-agent workflows.
Evals
Evaluate, monitor and improve your Agents.
Was this page helpful?


Yes

No
Suggest edits
Raise issue
Your first Agents
x
github
discord
youtube
website
Powered by Mintlify



Agno home pagedark logo

Search...
⌘K

Ask AI
Discord
Community
agno-agi/agno
30,268

User Guide
Examples
Workspaces
FAQs
API reference
Changelog
Introduction
What is Agno?
Your first Agents
Multi Agent Systems
Playground
Monitoring & Debugging
Community & Support
Concepts
Agents
Teams
Models
Tools
Reasoning
Memory
Knowledge
Chunking
Vector DBs
Storage
Embeddings
Evals
Workflows
Workflows v2 (Beta)
Applications
Other
Agent UI
Agent API
Observability
Testing
How to
Install & Setup
Contributing to Agno
Migrate from Phidata to Agno
Authenticate with Agno Platform
On this page
Level 4: Agent Teams that can reason and collaborate
Level 5: Agentic Workflows with state and determinism
Next
Introduction
Multi Agent Systems

Copy page

Teams of Agents working together towards a common goal.

​
Level 4: Agent Teams that can reason and collaborate
Agents are the atomic unit of work, and work best when they have a narrow scope and a small number of tools. When the number of tools grows beyond what the model can handle or you need to handle multiple concepts, use a team of agents to spread the load.
Agno provides an industry leading multi-agent architecture that allows you to build Agent Teams that can reason, collaborate and coordinate. In this example, we’ll build a team of 2 agents to analyze the semiconductor market performance, reasoning step by step.
level_4_team.py

Copy

Ask AI
from agno.agent import Agent
from agno.models.anthropic import Claude
from agno.models.openai import OpenAIChat
from agno.team.team import Team
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.tools.reasoning import ReasoningTools
from agno.tools.yfinance import YFinanceTools

web_agent = Agent(
    name="Web Search Agent",
    role="Handle web search requests and general research",
    model=OpenAIChat(id="gpt-4.1"),
    tools=[DuckDuckGoTools()],
    instructions="Always include sources",
    add_datetime_to_instructions=True,
)

finance_agent = Agent(
    name="Finance Agent",
    role="Handle financial data requests and market analysis",
    model=OpenAIChat(id="gpt-4.1"),
    tools=[YFinanceTools(stock_price=True, stock_fundamentals=True,analyst_recommendations=True, company_info=True)],
    instructions=[
        "Use tables to display stock prices, fundamentals (P/E, Market Cap), and recommendations.",
        "Clearly state the company name and ticker symbol.",
        "Focus on delivering actionable financial insights.",
    ],
    add_datetime_to_instructions=True,
)

reasoning_finance_team = Team(
    name="Reasoning Finance Team",
    mode="coordinate",
    model=Claude(id="claude-sonnet-4-20250514"),
    members=[web_agent, finance_agent],
    tools=[ReasoningTools(add_instructions=True)],
    instructions=[
        "Collaborate to provide comprehensive financial and investment insights",
        "Consider both fundamental analysis and market sentiment",
        "Use tables and charts to display data clearly and professionally",
        "Present findings in a structured, easy-to-follow format",
        "Only output the final consolidated analysis, not individual agent responses",
    ],
    markdown=True,
    show_members_responses=True,
    enable_agentic_context=True,
    add_datetime_to_instructions=True,
    success_criteria="The team has provided a complete financial analysis with data, visualizations, risk assessment, and actionable investment recommendations supported by quantitative analysis and market research.",
)

if __name__ == "__main__":
    reasoning_finance_team.print_response("""Compare the tech sector giants (AAPL, GOOGL, MSFT) performance:
        1. Get financial data for all three companies
        2. Analyze recent news affecting the tech sector
        3. Calculate comparative metrics and correlations
        4. Recommend portfolio allocation weights""",
        stream=True,
        show_full_reasoning=True,
        stream_intermediate_steps=True,
    )
Install dependencies and run the Agent team
1
Install dependencies


Mac

Windows

Copy

Ask AI
uv pip install -U agno anthropic openai duckduckgo-search yfinance
2
Export your API keys


Mac

Windows

Copy

Ask AI
export ANTHROPIC_API_KEY=sk-***
export OPENAI_API_KEY=sk-***
3
Run the agent team


Copy

Ask AI
python level_4_team.py
​
Level 5: Agentic Workflows with state and determinism
Workflows are deterministic, stateful, multi-agent programs built for production applications. We write the workflow in pure python, giving us extreme control over the execution flow.
Having built 100s of agentic systems, no framework or step based approach will give you the flexibility and reliability of pure-python. Want loops - use while/for, want conditionals - use if/else, want exceptional handling - use try/except.
Because the workflow logic is a python function, AI code editors can vibe code workflows for you.
Add https://docs.agno.com as a document source and vibe away.
Here’s a simple workflow that caches previous outputs, you control every step: what gets cached, what gets streamed, what gets logged and what gets returned.
level_5_workflow.py

Copy

Ask AI
from typing import Iterator
from agno.agent import Agent, RunResponse
from agno.models.openai import OpenAIChat
from agno.utils.log import logger
from agno.utils.pprint import pprint_run_response
from agno.workflow import Workflow


class CacheWorkflow(Workflow):
    # Add agents or teams as attributes on the workflow
    agent = Agent(model=OpenAIChat(id="gpt-4o-mini"))

    # Write the logic in the `run()` method
    def run(self, message: str) -> Iterator[RunResponse]:
        logger.info(f"Checking cache for '{message}'")
        # Check if the output is already cached
        if self.session_state.get(message):
            logger.info(f"Cache hit for '{message}'")
            yield RunResponse(
                run_id=self.run_id, content=self.session_state.get(message)
            )
            return

        logger.info(f"Cache miss for '{message}'")
        # Run the agent and yield the response
        yield from self.agent.run(message, stream=True)

        # Cache the output after response is yielded
        self.session_state[message] = self.agent.run_response.content


if __name__ == "__main__":
    workflow = CacheWorkflow()
    # Run workflow (this is takes ~1s)
    response: Iterator[RunResponse] = workflow.run(message="Tell me a joke.")
    # Print the response
    pprint_run_response(response, markdown=True, show_time=True)
    # Run workflow again (this is immediate because of caching)
    response: Iterator[RunResponse] = workflow.run(message="Tell me a joke.")
    # Print the response
    pprint_run_response(response, markdown=True, show_time=True)
Run the workflow

Copy

Ask AI
python level_5_workflow.py
​
Next
Checkout the Agent Playground to interact with your Agents, Teams and Workflows.
Learn how to Monitor your Agents, Teams and Workflows.
Get help from the Community.
Was this page helpful?


Yes

No
Suggest edits
Raise issue
Your first Agents
Playground
x
github
discord
youtube
website
Powered by Mintlify
Multi Agent Systems - Agno


Agno home pagedark logo

Search...
⌘K

Ask AI
Discord
Community
agno-agi/agno
30,268

User Guide
Examples
Workspaces
FAQs
API reference
Changelog
Introduction
What is Agno?
Your first Agents
Multi Agent Systems
Playground
Monitoring & Debugging
Community & Support
Concepts
Agents
Overview
Running your Agent
Metrics
Sessions
Agent State
Memory
Tools
Structured Output
Multimodal Agents
User Control Flows
Prompts
Knowledge
Session Storage
Agent Context
Agent Teams [Deprecated]
Teams
Models
Tools
Reasoning
Memory
Knowledge
Chunking
Vector DBs
Storage
Embeddings
Evals
Workflows
Workflows v2 (Beta)
Applications
Other
Agent UI
Agent API
Observability
Testing
How to
Install & Setup
Contributing to Agno
Migrate from Phidata to Agno
Authenticate with Agno Platform
On this page
Example: Research Agent
Agents
What are Agents?

Copy page

Learn about Agno Agents and how they work.

Agents are AI programs that operate autonomously. Traditional software follows a pre-programmed sequence of steps. Agents dynamically determine their course of action using a machine learning model.
The core of an Agent is the model, tools and instructions:
Model: controls the flow of execution. It decides whether to reason, act or respond.
Tools: enable an Agent to take actions and interact with external systems.
Instructions: are how we program the Agent, teaching it how to use tools and respond.
Agents also have memory, knowledge, storage and the ability to reason:
Reasoning: enables Agents to “think” before responding and “analyze” the results of their actions (i.e. tool calls), this improves reliability and quality of responses.
Knowledge: is domain-specific information that the Agent can search at runtime to make better decisions and provide accurate responses (RAG). Knowledge is stored in a vector database and this search at runtime pattern is known as Agentic RAG/Agentic Search.
Storage: is used by Agents to save session history and 
[END PART 3/8]
Remember not answering yet. Just acknowledge you received this part with the message "Part 3/8 received" and wait for the next part.
















Do not answer yet. This is just another part of the text I want to send you. Just receive and acknowledge as "Part 4/8 received" and wait for the next part.
[START PART 4/8]
state in a database. Model APIs are stateless and storage enables us to continue conversations from where they left off. This makes Agents stateful, enabling multi-turn, long-term conversations.
Memory: gives Agents the ability to store and recall information from previous interactions, allowing them to learn user preferences and personalize their responses.

If this is your first time building agents, follow these examples before diving into advanced concepts.
​
Example: Research Agent
Let’s build a research agent using Exa to showcase how to guide the Agent to produce the report in a specific format. In advanced cases, we should use Structured Outputs instead.
The description and instructions are converted to the system message and the input is passed as the user message. Set debug_mode=True to view logs behind the scenes.
1
Create Research Agent

Create a file research_agent.py
research_agent.py

Copy

Ask AI
from datetime import datetime
from pathlib import Path
from textwrap import dedent

from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.tools.exa import ExaTools

today = datetime.now().strftime("%Y-%m-%d")

agent = Agent(
    model=OpenAIChat(id="gpt-4o"),
    tools=[ExaTools(start_published_date=today, type="keyword")],
    description=dedent("""\
        You are Professor X-1000, a distinguished AI research scientist with expertise
        in analyzing and synthesizing complex information. Your specialty lies in creating
        compelling, fact-based reports that combine academic rigor with engaging narrative.

        Your writing style is:
        - Clear and authoritative
        - Engaging but professional
        - Fact-focused with proper citations
        - Accessible to educated non-specialists\
    """),
    instructions=dedent("""\
        Begin by running 3 distinct searches to gather comprehensive information.
        Analyze and cross-reference sources for accuracy and relevance.
        Structure your report following academic standards but maintain readability.
        Include only verifiable facts with proper citations.
        Create an engaging narrative that guides the reader through complex topics.
        End with actionable takeaways and future implications.\
    """),
    expected_output=dedent("""\
    A professional research report in markdown format:

    # {Compelling Title That Captures the Topic's Essence}

    ## Executive Summary
    {Brief overview of key findings and significance}

    ## Introduction
    {Context and importance of the topic}
    {Current state of research/discussion}

    ## Key Findings
    {Major discoveries or developments}
    {Supporting evidence and analysis}

    ## Implications
    {Impact on field/society}
    {Future directions}

    ## Key Takeaways
    - {Bullet point 1}
    - {Bullet point 2}
    - {Bullet point 3}

    ## References
    - [Source 1](link) - Key finding/quote
    - [Source 2](link) - Key finding/quote
    - [Source 3](link) - Key finding/quote

    ---
    Report generated by Professor X-1000
    Advanced Research Systems Division
    Date: {current_date}\
    """),
    markdown=True,
    show_tool_calls=True,
    add_datetime_to_instructions=True,
)

# Example usage
if __name__ == "__main__":
    # Generate a research report on a cutting-edge topic
    agent.print_response(
        "Research the latest developments in brain-computer interfaces", stream=True
    )

# More example prompts to try:
"""
Try these research topics:
1. "Analyze the current state of solid-state batteries"
2. "Research recent breakthroughs in CRISPR gene editing"
3. "Investigate the development of autonomous vehicles"
4. "Explore advances in quantum machine learning"
5. "Study the impact of artificial intelligence on healthcare"
"""
2
Run the agent

Install libraries

Copy

Ask AI
pip install openai exa-py agno
Run the agent

Copy

Ask AI
python research_agent.py
Was this page helpful?


Yes

No
Suggest edits
Raise issue
Community & Support
Running your Agent
x
github
discord
youtube
website
Powered by Mintlify
What are Agents? - Agno


Agno home pagedark logo

Search...
⌘K

Ask AI
Discord
Community
agno-agi/agno
30,268

User Guide
Examples
Workspaces
FAQs
API reference
Changelog
Introduction
What is Agno?
Your first Agents
Multi Agent Systems
Playground
Monitoring & Debugging
Community & Support
Concepts
Agents
Overview
Running your Agent
Metrics
Sessions
Agent State
Memory
Tools
Structured Output
Multimodal Agents
User Control Flows
Prompts
Knowledge
Session Storage
Agent Context
Agent Teams [Deprecated]
Teams
Models
Tools
Reasoning
Memory
Knowledge
Chunking
Vector DBs
Storage
Embeddings
Evals
Workflows
Workflows v2 (Beta)
Applications
Other
Agent UI
Agent API
Observability
Testing
How to
Install & Setup
Contributing to Agno
Migrate from Phidata to Agno
Authenticate with Agno Platform
On this page
Running your Agent
RunResponse
Streaming Responses
Streaming Intermediate Steps
Handling Events
Storing Events
Event Types
Core Events
Control Flow Events
Tool Events
Reasoning Events
Memory Events
Structured Input
Agents
Running your Agent

Copy page

Learn how to run an agent and get the response.

The Agent.run() function runs the agent and generates a response, either as a RunResponse object or a stream of RunResponse objects.
Many of our examples use agent.print_response() which is a helper utility to print the response in the terminal. It uses agent.run() under the hood.
​
Running your Agent
Here’s how to run your agent. The response is captured in the response.

Copy

Ask AI
from typing import Iterator
from agno.agent import Agent, RunResponse
from agno.models.openai import OpenAIChat
from agno.utils.pprint import pprint_run_response

agent = Agent(model=OpenAIChat(id="gpt-4o-mini"))

# Run agent and return the response as a variable
response: RunResponse = agent.run("Tell me a 5 second short story about a robot")

# Print the response in markdown format
pprint_run_response(response, markdown=True)
​
RunResponse
The Agent.run() function returns a RunResponse object when not streaming. It has the following attributes:
Understanding Metrics
For a detailed explanation of how metrics are collected and used, please refer to the Metrics Documentation.
See detailed documentation in the RunResponse documentation.
​
Streaming Responses
To enable streaming, set stream=True when calling run(). This will return an iterator of RunResponseEvent objects instead of a single response.
From agno version 1.6.0, the Agent.run() function returns an iterator of RunResponseEvent, not of RunResponse objects.

Copy

Ask AI
from typing import Iterator
from agno.agent import Agent, RunResponseEvent
from agno.models.openai import OpenAIChat
from agno.utils.pprint import pprint_run_response

agent = Agent(model=OpenAIChat(id="gpt-4-mini"))

# Run agent and return the response as a stream
response_stream: Iterator[RunResponseEvent] = agent.run(
    "Tell me a 5 second short story about a lion",
    stream=True
)

# Print the response stream in markdown format
pprint_run_response(response_stream, markdown=True)
​
Streaming Intermediate Steps
For even more detailed streaming, you can enable intermediate steps by setting stream_intermediate_steps=True. This will provide real-time updates about the agent’s internal processes.

Copy

Ask AI
# Stream with intermediate steps
response_stream: Iterator[RunResponseEvent] = agent.run(
    "Tell me a 5 second short story about a lion",
    stream=True,
    stream_intermediate_steps=True
)
​
Handling Events
You can process events as they arrive by iterating over the response stream:

Copy

Ask AI
response_stream = agent.run("Your prompt", stream=True, stream_intermediate_steps=True)

for event in response_stream:
    if event.event == "RunResponseContent":
        print(f"Content: {event.content}")
    elif event.event == "ToolCallStarted":
        print(f"Tool call started: {event.tool}")
    elif event.event == "ReasoningStep":
        print(f"Reasoning step: {event.content}")
    ...
You can see this behavior in action in our Playground.
​
Storing Events
You can store all the events that happened during a run on the RunResponse object.

Copy

Ask AI
from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.utils.pprint import pprint_run_response

agent = Agent(model=OpenAIChat(id="gpt-4o-mini"), store_events=True)

response = agent.run("Tell me a 5 second short story about a lion", stream=True, stream_intermediate_steps=True)
pprint_run_response(response)

for event in agent.run_response.events:
    print(event.event)
By default the RunResponseContentEvent event is not stored. You can modify which events are skipped by setting the events_to_skip parameter.
For example:

Copy

Ask AI
agent = Agent(model=OpenAIChat(id="gpt-4o-mini"), store_events=True, events_to_skip=[RunEvent.run_started.value])
​
Event Types
The following events are yielded by the Agent.run() and Agent.arun() functions depending on the agent’s configuration:
​
Core Events
Event Type	Description
RunStarted	Indicates the start of a run
RunResponseContent	Contains the model’s response text as individual chunks
RunCompleted	Signals successful completion of the run
RunError	Indicates an error occurred during the run
RunCancelled	Signals that the run was cancelled
​
Control Flow Events
Event Type	Description
RunPaused	Indicates the run has been paused
RunContinued	Signals that a paused run has been continued
​
Tool Events
Event Type	Description
ToolCallStarted	Indicates the start of a tool call
ToolCallCompleted	Signals completion of a tool call, including tool call results
​
Reasoning Events
Event Type	Description
ReasoningStarted	Indicates the start of the agent’s reasoning process
ReasoningStep	Contains a single step in the reasoning process
ReasoningCompleted	Signals completion of the reasoning process
​
Memory Events
Event Type	Description
MemoryUpdateStarted	Indicates that the agent is updating its memory
MemoryUpdateCompleted	Signals completion of a memory update
See detailed documentation in the RunResponseEvent documentation.
​
Structured Input
An agent can be provided with structured input (i.e a pydantic model) by passing it in the Agent.run() or Agent.print_response() as the message parameter.

Copy

Ask AI
from typing import List

from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.tools.hackernews import HackerNewsTools
from pydantic import BaseModel, Field


class ResearchTopic(BaseModel):
    """Structured research topic with specific requirements"""

    topic: str
    focus_areas: List[str] = Field(description="Specific areas to focus on")
    target_audience: str = Field(description="Who this research is for")
    sources_required: int = Field(description="Number of sources needed", default=5)


# Define agents
hackernews_agent = Agent(
    name="Hackernews Agent",
    model=OpenAIChat(id="gpt-4o-mini"),
    tools=[HackerNewsTools()],
    role="Extract key insights and content from Hackernews posts",
)

hackernews_agent.print_response(
    message=ResearchTopic(
        topic="AI",
        focus_areas=["AI", "Machine Learning"],
        target_audience="Developers",
        sources_required=5,
    )
)
Was this page helpful?


Yes

No
Suggest edits
Raise issue
Overview
Metrics
x
github
discord
youtube
website
Powered by Mintlify
Running your Agent - Agno


Agno home pagedark logo

Search...
⌘K

Ask AI
Discord
Community
agno-agi/agno
30,268

User Guide
Examples
Workspaces
FAQs
API reference
Changelog
Introduction
What is Agno?
Your first Agents
Multi Agent Systems
Playground
Monitoring & Debugging
Community & Support
Concepts
Agents
Overview
Running your Agent
Metrics
Sessions
Agent State
Memory
Tools
Structured Output
Multimodal Agents
User Control Flows
Prompts
Knowledge
Session Storage
Agent Context
Agent Teams [Deprecated]
Teams
Models
Tools
Reasoning
Memory
Knowledge
Chunking
Vector DBs
Storage
Embeddings
Evals
Workflows
Workflows v2 (Beta)
Applications
Other
Agent UI
Agent API
Observability
Testing
How to
Install & Setup
Contributing to Agno
Migrate from Phidata to Agno
Authenticate with Agno Platform
On this page
Using a Toolkit
Writing your own Tools
Attributes
Developer Resources
Agents
Tools

Copy page

Learn how to use tools in Agno to build AI agents.

Agents use tools to take actions and interact with external systems.
Tools are functions that an Agent can run to achieve tasks. For example: searching the web, running SQL, sending an email or calling APIs. You can use any python function as a tool or use a pre-built toolkit. The general syntax is:

Copy

Ask AI
from agno.agent import Agent

agent = Agent(
    # Add functions or Toolkits
    tools=[...],
    # Show tool calls in the Agent response
    show_tool_calls=True
)
​
Using a Toolkit
Agno provides many pre-built toolkits that you can add to your Agents. For example, let’s use the DuckDuckGo toolkit to search the web.
You can find more toolkits in the Toolkits guide.
1
Create Web Search Agent

Create a file web_search.py
web_search.py

Copy

Ask AI
from agno.agent import Agent
from agno.tools.duckduckgo import DuckDuckGoTools

agent = Agent(tools=[DuckDuckGoTools()], show_tool_calls=True, markdown=True)
agent.print_response("Whats happening in France?", stream=True)
2
Run the agent

Install libraries

Copy

Ask AI
pip install openai duckduckgo-search agno
Run the agent

Copy

Ask AI
python web_search.py
​
Writing your own Tools
For more control, write your own python functions and add them as tools to an Agent. For example, here’s how to add a get_top_hackernews_stories tool to an Agent.
hn_agent.py

Copy

Ask AI
import json
import httpx

from agno.agent import Agent

def get_top_hackernews_stories(num_stories: int = 10) -> str:
    """Use this function to get top stories from Hacker News.

    Args:
        num_stories (int): Number of stories to return. Defaults to 10.

    Returns:
        str: JSON string of top stories.
    """

    # Fetch top story IDs
    response = httpx.get('https://hacker-news.firebaseio.com/v0/topstories.json')
    story_ids = response.json()

    # Fetch story details
    stories = []
    for story_id in story_ids[:num_stories]:
        story_response = httpx.get(f'https://hacker-news.firebaseio.com/v0/item/{story_id}.json')
        story = story_response.json()
        if "text" in story:
            story.po
[END PART 4/8]
Remember not answering yet. Just acknowledge you received this part with the message "Part 4/8 received" and wait for the next part.







Do not answer yet. This is just another part of the text I want to send you. Just receive and acknowledge as "Part 5/8 received" and wait for the next part.
[START PART 5/8]
p("text", None)
        stories.append(story)
    return json.dumps(stories)

agent = Agent(tools=[get_top_hackernews_stories], show_tool_calls=True, markdown=True)
agent.print_response("Summarize the top 5 stories on hackernews?", stream=True)
Read more about:
Available toolkits
Using functions as tools
​
Attributes
The following attributes allow an Agent to use tools
Parameter	Type	Default	Description
tools	List[Union[Tool, Toolkit, Callable, Dict, Function]]	-	A list of tools provided to the Model. Tools are functions the model may generate JSON inputs for.
show_tool_calls	bool	False	Print the signature of the tool calls in the Model response.
tool_call_limit	int	-	Maximum number of tool calls allowed for a single run.
tool_choice	Union[str, Dict[str, Any]]	-	Controls which (if any) tool is called by the model. “none” means the model will not call a tool and instead generates a message. “auto” means the model can pick between generating a message or calling a tool. Specifying a particular function via {"type": "function", "function": {"name": "my_function"}} forces the model to call that tool. “none” is the default when no tools are present. “auto” is the default if tools are present.
read_chat_history	bool	False	Add a tool that allows the Model to read the chat history.
search_knowledge	bool	False	Add a tool that allows the Model to search the knowledge base (aka Agentic RAG).
update_knowledge	bool	False	Add a tool that allows the Model to update the knowledge base.
read_tool_call_history	bool	False	Add a tool that allows the Model to get the tool call history.
​
Developer Resources
View Cookbook
Was this page helpful?


Yes

No
Suggest edits
Raise issue
Memory
Structured Output
x
github
discord
youtube
website
Powered by Mintlify
Tools - Agno



Agno home pagedark logo

Search...
⌘K

Ask AI
Discord
Community
agno-agi/agno
30,268

User Guide
Examples
Workspaces
FAQs
API reference
Changelog
Introduction
What is Agno?
Your first Agents
Multi Agent Systems
Playground
Monitoring & Debugging
Community & Support
Concepts
Agents
Overview
Running your Agent
Metrics
Sessions
Agent State
Memory
Tools
Structured Output
Multimodal Agents
User Control Flows
Prompts
Knowledge
Session Storage
Agent Context
Agent Teams [Deprecated]
Teams
Models
Tools
Overview
Writing your own tools
Exceptions
Hooks
Human in the loop
Toolkits
MCP
Reasoning Tools
Writing your own Toolkit
Selecting tools
Updating Tools
Async Tools
Tool Result Caching
Tool Call Limit
Reasoning
Memory
Knowledge
Chunking
Vector DBs
Storage
Embeddings
Evals
Workflows
Workflows v2 (Beta)
Applications
Other
Agent UI
Agent API
Observability
Testing
How to
Install & Setup
Contributing to Agno
Migrate from Phidata to Agno
Authenticate with Agno Platform
On this page
Using the Toolkit Class
Tools
What are Tools?

Copy page

Tools are functions that helps Agno Agents to interact with the external world.

Tools make agents - “agentic” by enabling them to interact with external systems like searching the web, running SQL, sending an email or calling APIs.
Agno comes with 80+ pre-built toolkits, but in most cases, you will write your own tools. The general syntax is:

Copy

Ask AI
import random

from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.tools import tool


@tool(show_result=True, stop_after_tool_call=True)
def get_weather(city: str) -> str:
    """Get the weather for a city."""
    # In a real implementation, this would call a weather API
    weather_conditions = ["sunny", "cloudy", "rainy", "snowy", "windy"]
    random_weather = random.choice(weather_conditions)

    return f"The weather in {city} is {random_weather}."


agent = Agent(
    model=OpenAIChat(model="gpt-4o-mini"),
    tools=[get_weather],
    markdown=True,
)
agent.print_response("What is the weather in San Francisco?", stream=True)
In the example above, the get_weather function is a tool. When it is called, the tool result will be shown in the output because we set show_result=True.
Then, the Agent will stop after the tool call because we set stop_after_tool_call=True.
​
Using the Toolkit Class
The Toolkit class provides a way to manage multiple tools with additional control over their execution. You can specify which tools should stop the agent after execution and which should have their results shown.

Copy

Ask AI
from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.tools.googlesearch import GoogleSearchTools

agent = Agent(
    model=OpenAIChat(id="gpt-4.5-preview"),
    tools=[
        GoogleSearchTools(
            stop_after_tool_call_tools=["google_search"],
            show_result_tools=["google_search"],
        )
    ],
    show_tool_calls=True,
)

agent.print_response("What's the latest about gpt 4.5?", markdown=True)
In this example, the GoogleSearchTools toolkit is configured to stop the agent after executing the google_search function and to show the result of this function.
Read more about:
Available Toolkits
Using functions as tools
Was this page helpful?


Yes

No
Suggest edits
Raise issue
xAI
Writing your own tools
x
github
discord
youtube
website
Powered by Mintlify
What are Tools? - Agno


🚀 Zep Is The New State of the Art In Agent Memory - Learn More 🚀


Logo
Search
/
Playground
Discord
Context Engineering
getzep/graphiti
14217
1196
Dashboard
Sign Up >

Welcome to Zep!

Copy page

Connect your AI coding assistant to Zep’s docs: MCP server & llms.txt

Zep is a context engineering platform that systematically assembles personalized context—user preferences, traits, and business data—for reliable agent applications. Zep combines agent memory, Graph RAG, and context assembly capabilities to deliver comprehensive personalized context that reduces hallucinations and improves accuracy.

Key Concepts
Learn about Zep’s context engineering platform, temporal knowledge graphs, and agent memory capabilities.

Quickstart
Get up and running with Zep in minutes, whether you code in Python, TypeScript, or Go.

Cookbooks
Discover practical recipes and patterns for common use cases with Zep.

SDK Reference
Comprehensive API documentation for Zep’s SDKs in Python, TypeScript, and Go.

Mem0 Migration
Migrate from Mem0 to Zep in minutes.

Graphiti
Learn about Graphiti, Zep’s open-source temporal knowledge graph framework.

Was this page helpful?
Yes
No
Built with



🚀 Zep Is The New State of the Art In Agent Memory - Learn More 🚀


Logo
Search
/
Playground
Discord
Context Engineering
getzep/graphiti
14217
1196
Dashboard
Sign Up >

Getting Started
Coding with LLMs
Key Concepts
Quickstart
Building an Agent Walkthrough
Memory
Projects
Users
Sessions
Groups
Working with the Graph
Understanding the Graph
Utilizing Facts and Summaries
Customizing Graph Structure
Adding Data to the Graph
Reading Data from the Graph
Searching the Graph
Deleting Data from the Graph
Debugging
Cookbook
Check Data Ingestion Status
Customize Your Memory Context String
Add User Specific Business Data to User Graphs
Share Memory Across Users Using Group Graphs
Get Most Relevant Facts for an Arbitrary Query
Find Facts Relevant to a Specific Node
Best Practices
Performance Best Practices
Adding JSON Best Practices
Ecosystem
LangGraph
Autogen
Migrations
Migrate from Mem0
FAQ
Frequently Asked Questions
Legal
Privacy Policy
Terms of Service
Website Terms of Use
On this page
Zep’s memory model in one minute
Unified customer record
Domain-depth ontology
Temporal facts & ratings
Hybrid & granular search
How Zep differs from Mem0
SDK support
Migrating your code
Basic flows
Practical tips
Side-by-side SDK cheat-sheet
Where to dig deeper
Migrations
Mem0 Migration

Copy page

Zep is a memory layer for AI agents that unifies chat and business data into a dynamic temporal knowledge graph for each user. It tracks entities, relationships, and facts as they evolve, enabling you to build prompts with only the most relevant information—reducing hallucinations, improving recall, and lowering LLM costs.

Zep provides high-level APIs like memory.get and deep search with graph.search, supports custom entity/edge types, fact ratings, hybrid search, and granular graph updates. Mem0, by comparison, offers basic add/get/search APIs and an optional graph, but lacks built-in data unification, ontology customization, temporal fact management, fact ratings, and fine-grained graph control.

Got lots of data to migrate? Contact us for a discount and increased API limits.

Zep’s memory model in one minute
Unified customer record
Messages sent via memory.add go straight into the user’s knowledge graph; business objects (JSON, docs, e-mails, CRM rows) flow in through graph.add. Zep automatically deduplicates entities and keeps every fact’s valid and invalid dates so you always see the latest truth.
Domain-depth ontology
You can define Pydantic-style custom entity and edge classes so the graph speaks your business language (Accounts, Policies, Devices, etc.).
Temporal facts & ratings
Every edge stores when a fact was created, became valid, was invalidated, and (optionally) expired; fact_ratings let you auto-label facts (e.g., “high-confidence KYC data”) and filter on retrieval.
Hybrid & granular search
graph.search supports hybrid BM25 + semantic queries, graph search, with pluggable rerankers (RRF, MMR, cross-encoder) and can target nodes, edges, episodes, or everything at once.
How Zep differs from Mem0
Capability	Zep	Mem0
Business-data ingestion	Native via graph.add (JSON or text); business facts merge with user graph	No direct ingestion API; business data must be rewritten as “memories” or loaded into external graph store
Knowledge-graph storage	Built-in temporal graph; zero infra for developers	Optional “Graph Memory” layer that requires Neo4j/Memgraph and extra config
Custom ontology	First-class entity/edge type system	Not exposed; relies on generic nodes/relationships
Fact life-cycle (valid/invalid)	Automatic and queryable	Not documented / not supported
Fact ratings & filtering	Yes (fact_ratings API)	Not available
Search	Hybrid vector + graph search with multiple rerankers	Vector search with filters; basic Cypher queries if graph layer enabled
Graph CRUD	Full node/edge CRUD & bulk episode ingest	Add/Delete memories; no low-level edge ops
Memory context string	Auto-generated, temporal, prompt-ready	You assemble snippets manually from search output
LLM integration	Returns ready-made memory.context; easily integrates with agentic tools	Returns raw strings you must format
SDK support
Zep offers Python, TypeScript, and Go SDKs. See Installation Instructions for more details.

Migrating your code
Basic flows
What you do in Mem0	Do this in Zep
client.add(messages, user_id=ID) → stores conversation snippets	zep.memory.add(session_id, messages=[...]) – keeps chat sequence and updates graph
client.add("json...", user_id=ID) (not really supported)	zep.graph.add(user_id, data=<JSON>) – drop raw business records right in
client.search(query, user_id=ID) – vector+filter search	Easy path: zep.memory.get(session_id) returns the memory.context + recent messages
Deep path: zep.graph.search(user_id, query, reranker="rrf")
client.get_all(user_id=ID) – list memories	zep.graph.search(user_id, '') or iterate graph.get_nodes/edges for full dump
client.update(memory_id, ...) / delete	zep.graph.edge.delete(uuid_="edge_uuid") or zep.graph.episode.delete(uuid_="episode_uuid") for granular edits. Facts may not be updated directly; new data automatically invalidates old.
Practical tips
Session mapping: Map Mem0’s user_id → Zep user_id, and create session_id per conversation thread.
Business objects: Convert external records to JSON or text and feed them through graph.add; Zep will handle entity linking automatically.
Prompting: Replace your custom “summary builder” with the memory.context string; it already embeds temporal ranges and entity summaries.
Quality filters: Use Fact Ratings and apply min_fact_rating when calling memory.get to exclude low-confidence facts instead of manual post-processing.
Search tuning: Start with the default rrf reranker; switch to mmr, node_distance, cross_encoder, or episode_mentions when you need speed or precision tweaks.
Side-by-side SDK cheat-sheet
Operation	Mem0 Method (Python)	Zep Method (Python)	Notes
Add chat messages	m.add(messages, user_id=...)	zep.memory.add(session_id, messages)	Zep expects ordered AI + user msgs per turn
Add business record	n/a (work-around)	zep.graph.add(user_id, data)	Direct ingestion of JSON/text
Retrieve context	m.search(query,... )	zep.memory.get(session_id)	Zep auto-selects facts; no prompt assembly
Semantic / hybrid search	m.search(query, ...)	zep.graph.search(..., reranker=...)	Multiple rerankers, node/edge scopes
List memories	m.get_all(user_id)	zep.graph.search(user_id, '')	Empty query lists entire graph
Update fact	m.update(id, ...)	Not directly supported - add new data to supersede	Facts are temporal; new data invalidates old
Delete fact	m.delete(id)	zep.graph.edge.delete(uuid_="edge_uuid")	Episode deletion removes associated edges
Rate / filter facts	not supported	min_fact_rating param on memory.get	—
Where to dig deeper
Quickstart
Graph Search guide
Entity / Edge customization
Fact ratings
Graph CRUD: Reading from the Graph | Adding to the Graph | Deleting from the Graph
For any questions, ping the Zep Discord or contact your account manager. Happy migrating!

Was this page helpful?
Yes
No
Previous
FAQ
Next
Built with
Mem0 Migration | Zep Documentation


🚀 Zep Is The New State of the Art In Agent Memory - Learn More 🚀


Logo
Search
/
Playground
Discord
Context Engineering
getzep/graphiti
14217
1196
Dashboard
Sign Up >

Getting Started
Coding with LLMs
Key Concepts
Quickstart
Building an Agent Walkthrough
Memory
Projects
Users
Sessions
Groups
Working with the Graph
Understanding the Graph
Utilizing Facts and Summaries
Customizing Graph Structure
Adding Data to the Graph
Reading Data from the Graph
Searching the Graph
Deleting Data from the Graph
Debugging
Cookbook
Check Data Ingestion Status
Customize Your Memory Context String
Add User Specific Business Data to User Graphs
Share Memory Across Users Using Group Graphs
Get Most Relevant Facts for an Arbitrary Query
Find Facts Relevant to a Specific Node
Best Practices
Performance Best Practices
Adding JSON Best Practices
Ecosystem
LangGraph
Autogen
Migrations
Migrate from Mem0
FAQ
Frequently Asked Questions
Legal
Privacy Policy
Terms of Service
Website Terms of Use
On this page
Obtain an API Key
Install the SDK
Python
TypeScript
Go
Initialize the Client

[END PART 5/8]
Remember not answering yet. Just acknowledge you received this part with the message "Part 5/8 received" and wait for the next part.

















Do not answer yet. This is just another part of the text I want to send you. Just receive and acknowledge as "Part 6/8 received" and wait for the next part.
[START PART 6/8]
Create a User and Session
Create a User
Create a Session
Add Messages with memory.add
Retrieve Context with memory.get
View your Knowledge Graph
Add Business Data to a Graph
Search the Graph
Use Zep as an Agentic Tool
Next Steps
Getting Started
Quickstart

Copy page

Looking for a more in-depth understanding? Check out our Key Concepts page.

This quickstart guide will help you get up and running with Zep quickly. We will:

Obtain an API key
Install the SDK
Initialize the client
Create a user and session
Add and retrieve messages
View your knowledge graph
Add business data to a user or group graph
Search for edges or nodes in the graph
Migrating from Mem0? Check out our Mem0 Migration guide.

Obtain an API Key
Create a free Zep account and you will be prompted to create an API key.

Install the SDK
Python
Set up your Python project, ideally with a virtual environment, and then:

pip
uv
pip install zep-cloud

TypeScript
Set up your TypeScript project and then:

npm
yarn
pnpm
npm install @getzep/zep-cloud

Go
Set up your Go project and then:

go get github.com/getzep/zep-go/v2

Initialize the Client
First, make sure you have a .env file with your API key:

ZEP_API_KEY=your_api_key_here

After creating your .env file, you’ll need to source it in your terminal session:

source .env

Then, initialize the client with your API key:


Python

TypeScript

Go

import os
from zep_cloud.client import Zep
API_KEY = os.environ.get('ZEP_API_KEY')
client = Zep(
    api_key=API_KEY,
)
The Python SDK Supports Async Use

The Python SDK supports both synchronous and asynchronous usage. For async operations, import AsyncZep instead of Zep and remember to await client calls in your async code.

Create a User and Session
Before adding messages, you need to create a user and a session. A session is a chat thread - a container for messages between a user and an assistant. A user can have multiple sessions (different conversation threads).

While messages are stored in sessions, the knowledge extracted from these messages is stored at the user level. This means that facts and entities learned in one session are available across all of the user’s sessions. When you use memory.get(), Zep returns the most relevant memory from the user’s entire knowledge graph, not just from the current session.

Create a User
It is important to provide at least the first name and ideally the last name of the user when calling user.add. Otherwise, Zep may not be able to correctly associate the user with references to the user in the data you add. If you don’t have this information at the time the user is created, you can add it later with our update user method.


Python

TypeScript

Go

# Create a new user
user_id = "user123"
new_user = client.user.add(
    user_id=user_id,
    email="user@example.com",
    first_name="Jane",
    last_name="Smith",
)
Create a Session

Python

TypeScript

Go

import uuid
# Generate a unique session ID
session_id = uuid.uuid4().hex
# Create a new session for the user
client.memory.add_session(
    session_id=session_id,
    user_id=user_id,
)
Add Messages with memory.add
Add chat messages to a session using the memory.add method. These messages will be stored in the session history and used to build the user’s knowledge graph.

It is important to provide the name of the user in the role field if possible, to help with graph construction. It’s also helpful to provide a meaningful name for the assistant in its role field.


Python

TypeScript

Go

# Define messages to add
from zep_cloud.types import Message
messages = [
    Message(
        role="Jane",
        content="Hi, my name is Jane Smith and I work at Acme Corp.",
        role_type="user",
    ),
    Message(
        role="AI Assistant",
        content="Hello Jane! Nice to meet you. How can I help you with Acme Corp today?",
        role_type="assistant",
    )
]
# Add messages to the session
client.memory.add(session_id, messages=messages)
Retrieve Context with memory.get
Use the memory.get method to retrieve relevant context for a session. This includes a context string with facts and entities and recent messages that can be used in your prompt.


Python

TypeScript

Go

# Get memory for the session
memory = client.memory.get(session_id=session_id)
# Access the context string (for use in prompts)
context_string = memory.context
print(context_string)
# Access recent messages
recent_messages = memory.messages
for msg in recent_messages:
    print(f"{msg.role}: {msg.content}")
View your Knowledge Graph
Since you’ve created memory, you can view your knowledge graph by navigating to the Zep Dashboard, then Users > “user123” > View Graph. You can also click the “View Episodes” button to see when data is finished being added to the knowledge graph.

Add Business Data to a Graph
You can add business data directly to a user’s graph or to a group graph using the graph.add method. This data can be in the form of messages, text, or JSON.


Python

TypeScript

Go

# Add text data to a user's graph
new_episode = client.graph.add(
    user_id=user_id,
    type="text",
    data="Jane Smith is a senior software engineer who has been with Acme Corp for 5 years."
)
print("New episode created:", new_episode)
# Add JSON data to a user's graph
import json
json_data = {
    "employee": {
        "name": "Jane Smith",
        "position": "Senior Software Engineer",
        "department": "Engineering",
        "projects": ["Project Alpha", "Project Beta"]
    }
}
client.graph.add(
    user_id=user_id,
    type="json",
    data=json.dumps(json_data)
)
# Add data to a group graph (shared across users)
group_id = "engineering_team"
client.graph.add(
    group_id=group_id,
    type="text",
    data="The engineering team is working on Project Alpha and Project Beta."
)
Search the Graph
Use the graph.search method to search for edges or nodes in the graph. This is useful for finding specific information about a user or group.


Python

TypeScript

Go

# Search for edges in a user's graph
edge_results = client.graph.search(
    user_id=user_id,
    query="What projects is Jane working on?",
    scope="edges",  # Default is "edges"
    limit=5
)
# Search for nodes in a user's graph
node_results = client.graph.search(
    user_id=user_id,
    query="Jane Smith",
    scope="nodes",
    limit=5
)
# Search in a group graph
group_results = client.graph.search(
    group_id=group_id,
    query="Project Alpha",
    scope="edges",
    limit=5
)
Use Zep as an Agentic Tool
Zep’s memory retrieval methods can be used as agentic tools, enabling your agent to query Zep for relevant information. The example below shows how to create a LangChain LangGraph tool to search for facts in a user’s graph.

Python

from zep_cloud.client import AsyncZep
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, MessagesState
from langgraph.prebuilt import ToolNode
zep = AsyncZep(api_key=os.environ.get('ZEP_API_KEY'))
@tool
async def search_facts(state: MessagesState, query: str, limit: int = 5):
    """Search for facts in all conversations had with a user.
    
    Args:
        state (MessagesState): The Agent's state.
        query (str): The search query.
        limit (int): The number of results to return. Defaults to 5.
    Returns:
        list: A list of facts that match the search query.
    """
    search_results = await zep.graph.search(
      user_id=state['user_name'], 
      query=query, 
      limit=limit, 
    )
    return [edge.fact for edge in search_results.edges]
tools = [search_facts]
tool_node = ToolNode(tools)
llm = ChatOpenAI(model='gpt-4o-mini', temperature=0).bind_tools(tools)
Next Steps
Now that you’ve learned the basics of using Zep, you can:

Learn more about Key Concepts
Explore the Graph API for adding and retrieving data
Understand Users and Sessions in more detail
Learn about Memory Context for building better prompts
Explore Graph Search for advanced search capabilities
Was this page helpful?
Yes
No
Previous
Building a Chatbot with Zep
Familiarize yourself with Zep and the Zep SDKs, culminating in building a simple chatbot.
Next
Built with
Quickstart | Zep Documentation


🚀 Zep Is The New State of the Art In Agent Memory - Learn More 🚀


Logo
Search
/
Playground
Discord
Context Engineering
getzep/graphiti
14217
1196
Dashboard
Sign Up >

Getting Started
Coding with LLMs
Key Concepts
Quickstart
Building an Agent Walkthrough
Memory
Projects
Users
Sessions
Groups
Working with the Graph
Understanding the Graph
Utilizing Facts and Summaries
Customizing Graph Structure
Adding Data to the Graph
Reading Data from the Graph
Searching the Graph
Deleting Data from the Graph
Debugging
Cookbook
Check Data Ingestion Status
Customize Your Memory Context String
Add User Specific Business Data to User Graphs
Share Memory Across Users Using Group Graphs
Get Most Relevant Facts for an Arbitrary Query
Find Facts Relevant to a Specific Node
Best Practices
Performance Best Practices
Adding JSON Best Practices
Ecosystem
LangGraph
Autogen
Migrations
Migrate from Mem0
FAQ
Frequently Asked Questions
Legal
Privacy Policy
Terms of Service
Website Terms of Use
On this page
Adding memory
Ignore assistant messages
Retrieving memory
Using memory
Customizing memory
Getting Started
Memory

Copy page

Zep’s agent memory capabilities make context engineering simple: you add memory with a single line, retrieve memory with a single line, and then can immediately use the retrieved memory in your next LLM call.

The Memory API is high-level and opinionated. For a more customizable, low-level way to add and retrieve memory, see the Graph API.

Adding memory
Add your chat history to Zep using the memory.add method. memory.add is session-specific and expects data in chat message format, including a role name (e.g., user’s real name), role_type (AI, human, tool), and message content. Zep stores the chat history and builds a user-level knowledge graph from the messages.

For best results, add chat history to Zep on every chat turn. That is, add both the AI and human messages in a single operation and in the order that the messages were created.

The example below adds messages to Zep’s memory for the user in the given session:


Python

TypeScript

Go

from zep_cloud.client import AsyncZep
from zep_cloud.types import Message
zep_client = AsyncZep(
    api_key=API_KEY,
)
messages = [
    Message(
        role="Jane",
        role_type="user",
        content="Who was Octavia Butler?",
    )
]
await zep_client.memory.add(session_id, messages=messages)
You can find additional arguments to memory.add in the SDK reference. Notably, for latency sensitive applications, you can set return_context to true which will make memory.add return a context string in the way that memory.get does (discussed below).

If you are looking to add JSON or unstructured text as memory to the graph, you will need to use our Graph API.

Ignore assistant messages
You can also pass in a list of role types to ignore when adding data to the graph using the ignore_roles argument. For example, you may not want assistant messages to be added to the user graph; providing the assistant messages in the memory.add call while setting ignore_roles to include “assistant” will make it so that only the user messages are ingested into the graph, but the assistant messages are still used to contextualize the user messages. This is important in case the user message itself does not have enough context, such as the message “Yes.” Additionally, the assistant messages will still be added to the session’s message history.

Retrieving memory
The memory.get() method is a user-friendly, high-level API for retrieving relevant context from Zep. It uses the latest messages of the given session to determine what information is most relevant from the user’s knowledge graph and returns that information in a context string for your prompt. Note that although memory.get() only requires a session ID, it is able to return memory derived from any session of that user. The session is just used to determine what’s relevant.

memory.get also returns recent chat messages and raw facts that may provide additional context for your agent. We recommend using these raw messages when you call your LLM provider (see below). The memory.get method is user and session-specific and cannot retrieve data from group graphs.

The example below gets the memory.context string for the given session:


Python

TypeScript

Go

memory = zep_client.memory.get(session_id="session_id")
# the context field described above
context = memory.context
You can find additional arguments to memory.get in the SDK reference. Notably, you can specify a minimum fact rating which will filter out any retrieved facts with a rating below the threshold, if you are using fact ratings.

If you are looking to customize how memory is retrieved, you will need to search the graph and construct a custom memory context string. For example, memory.get uses the last few messages as the search query on the graph, but using the graph API you can use whatever query you want, as well as experiment with other search parameters such as re-ranker used.

Using memory
Once you’ve retrieved the memory context string, or constructed your own context string by searching the graph, you can include this string in your system prompt:

MessageType	Content
System	Your system prompt

{Zep context string}
Assistant	An assistant message stored in Zep
User	A user message stored in Zep
…	…
User	The latest user message
You should also include the last 4 to 6 messages of the session when calling your LLM provider. Because Zep’s ingestion can take a few minutes, the context string may not include information from the last few messages; and so the context string acts as the “long-term memory,” and the last few messages serve as the raw, short-term memory.

In latency sensitive applications such as voice chat bots, you can use the context string returned from memory.add to avoid making two API calls.

Customizing memory
The Memory API is our high level, easy-to-use API for adding and retrieving memory. If you want to add business data or documents to memory, or further customize how memory is retrieved, you should refer to our Guides on using the graph, such as adding data to the graph and searching the graph. We also have a cookbook on creating a custom context string using the graph API.

Additionally, group graphs can be used to store non-user-specific memory.

Was this page helpful?
Yes
No
[END PART 6/8]
Remember not answering yet. Just acknowledge you received this part with the message "Part 6/8 received" and wait for the next part.




Do not answer yet. This is just another part of the text I want to send you. Just receive and acknowledge as "Part 7/8 received" and wait for the next part.
[START PART 7/8]

Previous
Projects
Next
Built with
Memory | Zep Documentation


🚀 Zep Is The New State of the Art In Agent Memory - Learn More 🚀


Logo
Search
/
Playground
Discord
Context Engineering
getzep/graphiti
14217
1196
Dashboard
Sign Up >

Getting Started
Coding with LLMs
Key Concepts
Quickstart
Building an Agent Walkthrough
Memory
Projects
Users
Sessions
Groups
Working with the Graph
Understanding the Graph
Utilizing Facts and Summaries
Customizing Graph Structure
Adding Data to the Graph
Reading Data from the Graph
Searching the Graph
Deleting Data from the Graph
Debugging
Cookbook
Check Data Ingestion Status
Customize Your Memory Context String
Add User Specific Business Data to User Graphs
Share Memory Across Users Using Group Graphs
Get Most Relevant Facts for an Arbitrary Query
Find Facts Relevant to a Specific Node
Best Practices
Performance Best Practices
Adding JSON Best Practices
Ecosystem
LangGraph
Autogen
Migrations
Migrate from Mem0
FAQ
Frequently Asked Questions
Legal
Privacy Policy
Terms of Service
Website Terms of Use
On this page
Ensuring your User data is correctly mapped to the Zep knowledge graph
Adding a User
Getting a User
Updating a User
Deleting a User
Getting a User’s Sessions
Listing Users
Get the User Node
Getting Started
Users

Copy page

A User represents an individual interacting with your application. Each User can have multiple Sessions associated with them, allowing you to track and manage their interactions over time.

The unique identifier for each user is their UserID. This can be any string value, such as a username, email address, or UUID.

The User object and its associated Sessions provide a powerful way to manage and understand user behavior. By associating Sessions with Users, you can track the progression of conversations and interactions over time, providing valuable context and history.

In the following sections, you will learn how to manage Users and their associated Sessions.

Users Enable Simple User Privacy Management

Deleting a User will delete all Sessions and session artifacts associated with that User with a single API call, making it easy to handle Right To Be Forgotten requests.

Ensuring your User data is correctly mapped to the Zep knowledge graph
Adding your user’s email, first_name, and last_name ensures that chat messages and business data are correctly mapped to the user node in the Zep knowledge graph.

For e.g., if business data contains your user’s email address, it will be related directly to the user node.

You can associate rich business context with a User:

user_id: A unique identifier of the user that maps to your internal User ID.
email: The user’s email.
first_name: The user’s first name.
last_name: The user’s last name.
Adding a User
You can add a new user by providing the user details.


Python

TypeScript

from zep_cloud.client import Zep
client = Zep(api_key=API_KEY)
new_user = client.user.add(
    user_id=user_id,
    email="user@example.com",
    first_name="Jane",
    last_name="Smith",
)
Learn how to associate Sessions with Users

Getting a User
You can retrieve a user by their ID.


Python

TypeScript

user = client.user.get("user123")
Updating a User
You can update a user’s details by providing the updated user details.


Python

TypeScript

updated_user = client.user.update(
    user_id=user_id,
    email="updated_user@example.com",
    first_name="Jane",
    last_name="Smith",
)
Deleting a User
You can delete a user by their ID.


Python

TypeScript

client.user.delete("user123")
Getting a User’s Sessions
You can retrieve all Sessions for a user by their ID.


Python

TypeScript

sessions = client.user.get_sessions("user123")
Listing Users
You can list all users, with optional limit and cursor parameters for pagination.


Python

TypeScript

# List the first 10 users
result = client.user.list_ordered(page_size=10, page_number=1)
Get the User Node
You can also retrieve the user’s node from their graph:


Python

TypeScript

results = client.user.get_node(user_id=user_id)
user_node = results.node
print(user_node.summary)
The user node might be used to get a summary of the user or to get facts related to the user (see “How to find facts relevant to a specific node”).

Was this page helpful?
Yes
No
Previous
Sessions
Next
Built with
Users | Zep Documentation


🚀 Zep Is The New State of the Art In Agent Memory - Learn More 🚀


Logo
Search
/
Playground
Discord
Context Engineering
getzep/graphiti
14217
1196
Dashboard
Sign Up >

Getting Started
Coding with LLMs
Key Concepts
Quickstart
Building an Agent Walkthrough
Memory
Projects
Users
Sessions
Groups
Working with the Graph
Understanding the Graph
Utilizing Facts and Summaries
Customizing Graph Structure
Adding Data to the Graph
Reading Data from the Graph
Searching the Graph
Deleting Data from the Graph
Debugging
Cookbook
Check Data Ingestion Status
Customize Your Memory Context String
Add User Specific Business Data to User Graphs
Share Memory Across Users Using Group Graphs
Get Most Relevant Facts for an Arbitrary Query
Find Facts Relevant to a Specific Node
Best Practices
Performance Best Practices
Adding JSON Best Practices
Ecosystem
LangGraph
Autogen
Migrations
Migrate from Mem0
FAQ
Frequently Asked Questions
Legal
Privacy Policy
Terms of Service
Website Terms of Use
On this page
Adding a Session
Getting a Session
Deleting a Session
Listing Sessions
Getting Started
Sessions

Copy page

Sessions represent a conversation. Each User can have multiple sessions, and each session is a sequence of chat messages.

Chat messages are added to sessions using memory.add, which both adds those messages to the session history and ingests those messages into the user-level knowledge graph. The user knowledge graph contains data from all of that user’s sessions to create an integrated understanding of the user.

The knowledge graph does not separate the data from different sessions, but integrates the data together to create a unified picture of the user. So the get session memory endpoint and the associated memory.get method don’t return memory derived only from that session, but instead return whatever user-level memory is most relevant to that session, based on the session’s most recent messages.

Adding a Session
SessionIDs are arbitrary identifiers that you can map to relevant business objects in your app, such as users or a conversation a user might have with your app. Before you create a session, make sure you have created a user first. Then create a session with:


Python

TypeScript

client = Zep(
    api_key=API_KEY,
)
session_id = uuid.uuid4().hex # A new session identifier
client.memory.add_session(
    session_id=session_id,
    user_id=user_id,
)
Getting a Session

Python

TypeScript

session = client.memory.get_session(session_id)
print(session.dict())
Deleting a Session
Deleting a session deletes it and its associated messages. It does not however delete the associated data in the user’s knowledge graph. To remove data from the graph, see deleting data from the graph.


Python

TypeScript

client.memory.delete(session_id)
Listing Sessions
You can list all Sessions in the Zep Memory Store with page_size and page_number parameters for pagination.


Python

TypeScript

# List the first 10 Sessions
result = client.memory.list_sessions(page_size=10, page_number=1)
for session in result.sessions:
    print(session)
Was this page helpful?
Yes
No
Previous
Groups
Group graphs can be used to create and manage additional non-user specific graphs.

Next
Built with
Sessions | Zep Documentation


🚀 Zep Is The New State of the Art In Agent Memory - Learn More 🚀


Logo
Search
/
Playground
Discord
Context Engineering
getzep/graphiti
14217
1196
Dashboard
Sign Up >

Getting Started
Coding with LLMs
Key Concepts
Quickstart
Building an Agent Walkthrough
Memory
Projects
Users
Sessions
Groups
Working with the Graph
Understanding the Graph
Utilizing Facts and Summaries
Customizing Graph Structure
Adding Data to the Graph
Reading Data from the Graph
Searching the Graph
Deleting Data from the Graph
Debugging
Cookbook
Check Data Ingestion Status
Customize Your Memory Context String
Add User Specific Business Data to User Graphs
Share Memory Across Users Using Group Graphs
Get Most Relevant Facts for an Arbitrary Query
Find Facts Relevant to a Specific Node
Best Practices
Performance Best Practices
Adding JSON Best Practices
Ecosystem
LangGraph
Autogen
Migrations
Migrate from Mem0
FAQ
Frequently Asked Questions
Legal
Privacy Policy
Terms of Service
Website Terms of Use
On this page
Adding a Session
Getting a Session
Deleting a Session
Listing Sessions
Getting Started
Sessions

Copy page

Sessions represent a conversation. Each User can have multiple sessions, and each session is a sequence of chat messages.

Chat messages are added to sessions using memory.add, which both adds those messages to the session history and ingests those messages into the user-level knowledge graph. The user knowledge graph contains data from all of that user’s sessions to create an integrated understanding of the user.

The knowledge graph does not separate the data from different sessions, but integrates the data together to create a unified picture of the user. So the get session memory endpoint and the associated memory.get method don’t return memory derived only from that session, but instead return whatever user-level memory is most relevant to that session, based on the session’s most recent messages.

Adding a Session
SessionIDs are arbitrary identifiers that you can map to relevant business objects in your app, such as users or a conversation a user might have with your app. Before you create a session, make sure you have created a user first. Then create a session with:


Python

TypeScript

client = Zep(
    api_key=API_KEY,
)
session_id = uuid.uuid4().hex # A new session identifier
client.memory.add_session(
    session_id=session_id,
    user_id=user_id,
)
Getting a Session

Python

TypeScript

session = client.memory.get_session(session_id)
print(session.dict())
Deleting a Session
Deleting a session deletes it and its associated messages. It does not however delete the associated data in the user’s knowledge graph. To remove data from the graph, see deleting data from the graph.


Python

TypeScript

client.memory.delete(session_id)
Listing Sessions
You can list all Sessions in the Zep Memory Store with page_size and page_number parameters for pagination.


Python

TypeScript

# List the first 10 Sessions
result = client.memory.list_sessions(page_size=10, page_number=1)
for session in result.sessions:
    print(session)
Was this page helpful?
Yes
No
Previous
Groups
Group graphs can be used to create and manage additional non-user specific graphs.

Next
Built with
Sessions | Zep Documentation




🚀 Zep Is The New State of the Art In Agent Memory - Learn More 🚀


Logo
Search
/
Playground
Discord
Context Engineering
getzep/graphiti
14217
1196
Dashboard
Sign Up >

SDK Reference

Thread

User
POST
Add User
GET
Get Users
GET
Get User
DEL
Delete User
PATCH
Update User
GET
Get User Node
GET
Get User Sessions

Group

Graph

Deprecated
SDK Reference
User
Get Users
GET
/api/v2/users-ordered

Python

from zep_cloud.client import Zep
client = Zep(
    api_key="YOUR_API_KEY",
)
client.user.list_ordered()

200
Retrieved

{
  "row_count": 1,
  "total_count": 1,
  "users": [
    {
      "created_at": "created_at",
      "deleted_at": "deleted_at",
      "email": "email",
      "first_name": "first_name",
      "id": 1,
      "last_name": "last_name",
      "metadata": {
        "key": "value"
      },
      "project_uuid": "project_uuid",
      "session_count": 1,
      "updated_at": "updated_at",
      "user_id": "user_id",
      "uuid": "uuid"
    }
  ]
}
Returns all users.
Headers
Authorization
string
Required
Header authentication of the form Api-Key <token>

Query parameters
pageNumber
integer
Optional
Page number for pagination, starting from 1
pageSize
integer
Optional
Number of users to retrieve per page
Response
Successfully retrieved list of users
row_count
integer or null
total_count
integer or null
users
list of objects or null

Show 13 properties
Errors

400
User List Ordered Request Bad Request Error

500
User List Ordered Request Internal Server Error
Was this page helpful?
Yes
No
Previous
Get User
Next
Built with
Get Users | Zep Documentation


🚀 Zep Is The New State of the Art In Agent Memory - Learn More 🚀


Logo
Search
/
Playground
Discord
Context Engineering
getzep/graphiti
14217
1196
Dashboard
Sign Up >

SDK Reference

Thread

User
POST
Add User
GET
Get Users
GET
Get User
DEL
Delete User
PATCH
Update User
GET
Get User Node
GET
Get User Sessions

Group

Graph

Deprecated
SDK Reference
User
Get User
GET
/api/v2/users/:userId

Python

from zep_cloud.client import Zep
client = Zep(
    api_key="YOUR_API_KEY",
)
client.user.get(
    user_id="userId",
)

200
Retrieved

{
  "created_at": "created_at",
  "deleted_at": "deleted_at",
  "email": "email",
  "fact_rating_instruction": {
    "examples": {
      "high": "high",
      "low": "low",
      "medium": "medium"
    },
    "instruction": "instruction"
  },
  "first_name": "first_name",
  "id": 1,
  "last_name": "last_name",
  "metadata": {
    "key": "value"
  },
  "project_uuid": "project_uuid",
  "session_count": 1,
  "updated_at": "updated_at",
  "user_id": "user_id",
  "uuid": "uuid"
}
Returns a user.
Path parameters
userId
string
Required
The user_id of the user to get.

Headers
Authorization
string
Required
Header authentication of the form Api-Key <token>

Response
The user that was retrieved.
created_at
string or null
deleted_at
string or null
email
string or null
fact_rating_instruction
object or null

Show 2 properties
first_name
string or null
id
integer or null
last_name
string or null
metadata
map from strings to any or null
Deprecated
project_uuid
string or null
session_count
integer or null
Deprecated
updated_at
string or null
Deprecated
user_id
string or null
uuid
string or null
Errors

404
User Get Request Not Found Error

500
User Get Request Internal Server Error
Was this page helpful?
Yes
No
Previous
Delete User
Next
Built with
Get User | Zep Documentation



🚀 Zep Is The New State of the Art In Agent Memory - Learn More 🚀


Logo
Search
/
Playgr
[END PART 7/8]
Remember not answering yet. Just acknowledge you received this part with the message "Part 7/8 received" and wait for the next part.















[START PART 8/8]
ound
Discord
Context Engineering
getzep/graphiti
14217
1196
Dashboard
Sign Up >

SDK Reference

Thread

User
POST
Add User
GET
Get Users
GET
Get User
DEL
Delete User
PATCH
Update User
GET
Get User Node
GET
Get User Sessions

Group

Graph

Deprecated
SDK Reference
User
Update User
PATCH
/api/v2/users/:userId

Python

from zep_cloud.client import Zep
client = Zep(
    api_key="YOUR_API_KEY",
)
client.user.update(
    user_id="userId",
)

200
Updated

{
  "created_at": "created_at",
  "deleted_at": "deleted_at",
  "email": "email",
  "fact_rating_instruction": {
    "examples": {
      "high": "high",
      "low": "low",
      "medium": "medium"
    },
    "instruction": "instruction"
  },
  "first_name": "first_name",
  "id": 1,
  "last_name": "last_name",
  "metadata": {
    "key": "value"
  },
  "project_uuid": "project_uuid",
  "session_count": 1,
  "updated_at": "updated_at",
  "user_id": "user_id",
  "uuid": "uuid"
}
Updates a user.
Path parameters
userId
string
Required
User ID
Headers
Authorization
string
Required
Header authentication of the form Api-Key <token>

Request
This endpoint expects an object.
email
string
Optional
The email address of the user.
fact_rating_instruction
object
Optional
Optional instruction to use for fact rating.

Show 2 properties
first_name
string
Optional
The first name of the user.
last_name
string
Optional
The last name of the user.
metadata
map from strings to any
Optional
The metadata to update
Response
The user that was updated.
created_at
string or null
deleted_at
string or null
email
string or null
fact_rating_instruction
object or null

Show 2 properties
first_name
string or null
id
integer or null
last_name
string or null
metadata
map from strings to any or null
Deprecated
project_uuid
string or null
session_count
integer or null
Deprecated
updated_at
string or null
Deprecated
user_id
string or null
uuid
string or null
Errors

400
User Update Request Bad Request Error

404
User Update Request Not Found Error

500
User Update Request Internal Server Error
Was this page helpful?
Yes
No
Previous
Get User Node
Next
Built with
Update User | Zep Documentation



🚀 Zep Is The New State of the Art In Agent Memory - Learn More 🚀


Logo
Search
/
Playground
Discord
Context Engineering
getzep/graphiti
14217
1196
Dashboard
Sign Up >

SDK Reference

Thread

User
POST
Add User
GET
Get Users
GET
Get User
DEL
Delete User
PATCH
Update User
GET
Get User Node
GET
Get User Sessions

Group

Graph

Deprecated
SDK Reference
User
Get User Sessions
GET
/api/v2/users/:userId/sessions

Python

from zep_cloud.client import Zep
client = Zep(
    api_key="YOUR_API_KEY",
)
client.user.get_sessions(
    user_id="userId",
)

200
Retrieved

[
  {
    "classifications": {
      "key": "value"
    },
    "created_at": "created_at",
    "deleted_at": "deleted_at",
    "ended_at": "ended_at",
    "fact_rating_instruction": {
      "instruction": "instruction"
    },
    "facts": [
      "facts"
    ],
    "id": 1,
    "metadata": {
      "key": "value"
    },
    "project_uuid": "project_uuid",
    "session_id": "session_id",
    "updated_at": "updated_at",
    "user_id": "user_id",
    "uuid": "uuid"
  }
]
Returns all sessions for a user.
Path parameters
userId
string
Required
User ID
Headers
Authorization
string
Required
Header authentication of the form Api-Key <token>

Response
OK
classifications
map from strings to strings or null
created_at
string or null
deleted_at
string or null
ended_at
string or null
fact_rating_instruction
object or null
Deprecated

Show 2 properties
facts
list of strings or null
Deprecated
id
integer or null
metadata
map from strings to any or null
Deprecated
project_uuid
string or null
session_id
string or null
updated_at
string or null
Deprecated
user_id
string or null
uuid
string or null
Errors

500
User Get Sessions Request Internal Server Error
Was this page helpful?
Yes
No
Previous
Create Group
Next
Built with
Get User Sessions | Zep Documentation
🚀 Zep Is The New State of the Art In Agent Memory - Learn More 🚀


Logo
Search
/
Playground
Discord
Context Engineering
getzep/graphiti
14217
1196
Dashboard
Sign Up >

SDK Reference

Thread

User
POST
Add User
GET
Get Users
GET
Get User
DEL
Delete User
PATCH
Update User
GET
Get User Node
GET
Get User Sessions

Group

Graph

Deprecated
SDK Reference
User
Get User Node
GET
/api/v2/users/:userId/node

Python

from zep_cloud.client import Zep
client = Zep(
    api_key="YOUR_API_KEY",
)
client.user.get_node(
    user_id="userId",
)

200
Retrieved

{
  "node": {
    "created_at": "created_at",
    "name": "name",
    "summary": "summary",
    "uuid": "uuid",
    "attributes": {
      "key": "value"
    },
    "labels": [
      "labels"
    ]
  }
}
Returns a user's node.
Path parameters
userId
string
Required
The user_id of the user to get the node for.

Headers
Authorization
string
Required
Header authentication of the form Api-Key <token>

Response
Response object containing the User node.
node
object or null

Show 6 properties
Errors

404
User Get Node Request Not Found Error

500
User Get Node Request Internal Server Error
Was this page helpful?
Yes
No
Previous
Get User Sessions
Next
Built with
Get User Node | Zep Documentation

[END PART 8/8]
ALL PARTS SENT. Now you can continue processing the request.












