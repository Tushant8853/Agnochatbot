# Agno Chatbot Backend

A complete FastAPI backend for an intelligent chatbot that integrates Google Gemini, Zep (temporal memory), and Mem0 (factual memory) with hybrid memory routing.

## 🚀 Features

- **JWT Authentication**: Secure user signup/login with JWT tokens
- **Hybrid Memory System**: 
  - Zep for temporal/session-based memory with knowledge graphs
  - Mem0 for long-term factual memory with fast retrieval
  - Intelligent routing between memory systems
- **Google Gemini Integration**: Advanced LLM responses with context awareness
- **Session Management**: Persistent chat sessions with conversation history
- **Memory Search**: Search across both memory systems
- **PostgreSQL Database**: Async database operations with SQLAlchemy

## 📁 Project Structure

```
backend/
├── main.py                 # FastAPI application entry point
├── config.py              # Configuration and environment variables
├── requirements.txt       # Python dependencies
├── env.example           # Environment variables template
├── database.py           # Database initialization
├── auth/                 # Authentication module
│   ├── auth_routes.py    # Signup/login endpoints
│   ├── models.py         # Database models
│   ├── jwt_handler.py    # JWT token management
│   └── deps.py          # FastAPI dependencies
├── agno_agent/          # Agno agent module
│   └── agent.py         # Main agent logic
├── memory/              # Memory management
│   ├── zep_memory.py    # Zep integration
│   ├── mem0_memory.py   # Mem0 integration
│   └── hybrid_memory.py # Hybrid memory router
├── services/            # External services
│   └── gemini.py        # Google Gemini integration
└── utils/               # Utilities
    └── logger.py        # Logging configuration
```

## 🛠️ Setup Instructions

### 1. Prerequisites

- Python 3.8+
- PostgreSQL 15+
- API keys for:
  - Google Gemini
  - Zep
  - Mem0

### 2. Installation

```bash
# Clone the repository
git clone <repository-url>
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Environment Configuration

```bash
# Copy environment template
cp env.example .env

# Edit .env with your configuration
DATABASE_URL=postgresql+asyncpg://username:password@localhost:5432/agno_bot
SECRET_KEY=your_secure_secret_key
GEMINI_API_KEY=your_gemini_api_key
ZEP_API_KEY=your_zep_api_key
MEM0_API_KEY=your_mem0_api_key
```

### 4. Database Setup

```bash
# Create PostgreSQL database
createdb agno_bot

# Initialize database tables
python database.py
```

### 5. Run the Application

```bash
# Development mode
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Or use the built-in runner
python main.py
```

## 📚 API Documentation

### Authentication Endpoints

#### POST /auth/signup
Create a new user account.

**Request Body:**
```json
{
  "username": "john_doe",
  "email": "john@example.com",
  "password": "secure_password",
  "first_name": "John",
  "last_name": "Doe"
}
```

**Response:**
```json
{
  "access_token": "jwt_token_here",
  "token_type": "bearer",
  "user_id": "user_uuid",
  "username": "john_doe"
}
```

#### POST /auth/login
Authenticate existing user.

**Request Body:**
```json
{
  "username": "john_doe",
  "password": "secure_password"
}
```

### Chat Endpoints

#### POST /chat
Send a message and get AI response with memory context.

**Headers:** `Authorization: Bearer <jwt_token>`

**Request Body:**
```json
{
  "message": "Hello, how are you?",
  "session_id": "optional_session_id",
  "use_memory": true
}
```

**Response:**
```json
{
  "message": "Hello! I'm doing well, thank you for asking.",
  "session_id": "session_uuid",
  "memory_context": {
    "zep_context": "Recent conversation context...",
    "mem0_facts": [...],
    "combined_context": "Combined memory context..."
  },
  "timestamp": "2024-01-01T12:00:00Z"
}
```

#### GET /sessions
Get all chat sessions for the current user.

**Headers:** `Authorization: Bearer <jwt_token>`

**Response:**
```json
[
  {
    "session_id": "session_uuid",
    "title": "Chat Session 2024-01-01 12:00",
    "created_at": "2024-01-01T12:00:00Z",
    "is_active": "active"
  }
]
```

#### GET /sessions/{session_id}/history
Get conversation history for a specific session.

**Headers:** `Authorization: Bearer <jwt_token>`

**Response:**
```json
[
  {
    "role": "user",
    "content": "Hello",
    "timestamp": "2024-01-01T12:00:00Z"
  },
  {
    "role": "assistant",
    "content": "Hi there!",
    "timestamp": "2024-01-01T12:00:01Z"
  }
]
```

### Memory Endpoints

#### POST /memory/search
Search user's memory for relevant information.

**Headers:** `Authorization: Bearer <jwt_token>`

**Request Body:**
```json
{
  "query": "What did we talk about last time?",
  "search_type": "hybrid"
}
```

**Response:**
```json
{
  "zep_results": [...],
  "mem0_results": [...],
  "combined_results": [...]
}
```

#### GET /memory/summary
Get a summary of user's memory.

**Headers:** `Authorization: Bearer <jwt_token>`

**Response:**
```json
{
  "user_id": "user_uuid",
  "zep_facts_count": 15,
  "mem0_memories_count": 25,
  "key_facts": [
    "User likes coffee",
    "User works at Tech Corp",
    "User prefers morning meetings"
  ]
}
```

#### POST /memory/facts
Add a custom fact to user's memory.

**Headers:** `Authorization: Bearer <jwt_token>`

**Query Parameters:**
- `fact`: The fact to add
- `fact_type`: Type of fact (default: "custom")

## 🔧 Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `DATABASE_URL` | PostgreSQL connection string | - |
| `SECRET_KEY` | JWT secret key | - |
| `ALGORITHM` | JWT algorithm | HS256 |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | JWT token expiry | 30 |
| `GEMINI_API_KEY` | Google Gemini API key | - |
| `ZEP_API_KEY` | Zep API key | - |
| `MEM0_API_KEY` | Mem0 API key | - |
| `DEBUG` | Debug mode | True |
| `HOST` | Server host | 0.0.0.0 |
| `PORT` | Server port | 8000 |

## 🧠 Memory System Architecture

### Zep (Temporal Memory)
- Stores session-based conversations
- Builds knowledge graphs with entities and relationships
- Provides temporal context for recent interactions
- Handles complex querying with graph search

### Mem0 (Factual Memory)
- Stores long-term factual information
- Fast vector-based retrieval
- Extracts and stores key facts from conversations
- Provides persistent memory across sessions

### Hybrid Router
- Intelligently routes information to appropriate memory system
- Combines context from both systems for comprehensive responses
- Provides unified search across both memory types
- Maintains user isolation and privacy

## 🔒 Security Features

- JWT-based authentication
- Password hashing with bcrypt
- User session isolation
- Memory isolation per user
- CORS configuration
- Input validation with Pydantic

## 🚀 Deployment

### Docker (Recommended)

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Production Considerations

1. **Environment Variables**: Use secure environment variable management
2. **Database**: Use managed PostgreSQL service
3. **API Keys**: Secure storage for all API keys
4. **CORS**: Configure appropriate CORS origins
5. **Logging**: Implement proper logging and monitoring
6. **Rate Limiting**: Add rate limiting for API endpoints
7. **SSL/TLS**: Use HTTPS in production

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 🆘 Support

For support and questions:
- Create an issue in the repository
- Check the API documentation at `/docs` when running the server
- Review the logs for debugging information 