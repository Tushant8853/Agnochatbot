# 🤖 AgnoChat Bot

A production-ready AI chatbot built with **Agno Framework**, featuring advanced memory capabilities, multi-agent architecture, and a modern React frontend.


## 🚀 Features

### 🧠 **Advanced AI Capabilities**
- **Google Gemini 2.0 Flash** - State-of-the-art AI model for intelligent conversations
- **Multi-Agent Architecture** - Specialized agents for different tasks
- **Reasoning & Analysis** - Built-in reasoning capabilities for complex problem-solving
- **Multi-Modal Support** - Handle text, images, audio, and video inputs

### 💾 **Intelligent Memory System**
- **Dual Memory Architecture** - Zep (temporal) + Mem0 (factual) memory
- **User Isolation** - Complete memory separation between users
- **Memory Operations** - Store, retrieve, search, sync, and clear memories
- **Memory Analytics** - Comprehensive statistics and breakdowns
- **Hybrid Memory Strategy** - Intelligent routing between memory systems

### 🔐 **Security & Authentication**
- **JWT Authentication** - Secure token-based authentication
- **User Management** - Registration, login, and session management
- **Password Hashing** - bcrypt for secure password storage
- **CORS Support** - Configurable cross-origin access

### 🏗️ **Production-Ready Architecture**
- **FastAPI Backend** - High-performance, async API framework
- **PostgreSQL Database** - Persistent storage for users and sessions
- **Modular Design** - Clean separation of concerns
- **Health Monitoring** - Comprehensive health checks
- **Error Handling** - Robust error management

### 🎨 **Modern Frontend**
- **React 18** - Latest React features and performance
- **TypeScript** - Type-safe development
- **Tailwind CSS** - Modern, responsive design
- **Real-time Chat** - Live message streaming
- **Memory Analytics** - Visual memory insights
- **Theme Support** - Dark/light mode toggle

## 📋 Table of Contents

- [Quick Start](#quick-start)
- [Architecture](#architecture)
- [API Documentation](#api-documentation)
- [Memory System](#memory-system)
- [Development](#development)
- [Deployment](#deployment)
- [Contributing](#contributing)

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Node.js 16+
- PostgreSQL database
- API keys for:
  - Google Gemini
  - Zep Cloud
  - Mem0 AI

### Backend Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/agnochat-bot.git
   cd agnochat-bot
   ```

2. **Set up Python environment**
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Configure environment variables**
   ```bash
   cp .env.example .env
   ```
   
   Edit `.env` with your API keys:
   ```env
   DATABASE_URL=postgresql://user:pass@localhost/dbname
   GEMINI_API_KEY=your_gemini_api_key
   ZEP_API_KEY=your_zep_api_key
   MEM0_API_KEY=your_mem0_api_key
   SECRET_KEY=your_jwt_secret_key
   HOST=0.0.0.0
   PORT=8000
   DEBUG=true
   ```

4. **Run the backend**
   ```bash
   python main.py
   ```

### Frontend Setup

1. **Install dependencies**
   ```bash
   cd agnochat-frontend
   npm install
   ```

2. **Start development server**
   ```bash
   npm start
   ```

3. **Open your browser**
   Navigate to `http://localhost:3000`

## 🏗️ Architecture

### Backend Structure

```
backend/
├── main.py                 # FastAPI application entry point
├── requirements.txt        # Python dependencies
├── agno_chatbot/
│   ├── __init__.py
│   ├── agents/            # AI agents
│   │   ├── chatbot_agent.py
│   │   ├── memory_agent.py
│   │   └── research_agent.py
│   ├── api/               # API routes
│   │   └── routes.py
│   ├── config/            # Configuration
│   │   └── settings.py
│   └── utils/             # Utilities
│       ├── auth.py
│       └── models.py
└── playground.py          # Development playground
```

### Frontend Structure

```
agnochat-frontend/
├── public/
├── src/
│   ├── components/        # React components
│   │   ├── ChatBubble.tsx
│   │   ├── ChatHistory.tsx
│   │   ├── MemoryAnalytics.tsx
│   │   └── ...
│   ├── pages/            # Page components
│   │   ├── Chat.tsx
│   │   ├── Login.tsx
│   │   └── Signup.tsx
│   ├── context/          # React context
│   │   └── AuthContext.tsx
│   └── services/         # API services
│       └── api.ts
└── package.json
```

## 📡 API Documentation

### Authentication Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/auth/signup` | User registration |
| `POST` | `/api/auth/login` | User authentication |
| `GET` | `/api/auth/me` | Get current user info |

### Chat Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/chat` | Process chat messages |
| `GET` | `/api/chat/history` | Get chat history |

### Memory Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/memory` | Get user memory |
| `POST` | `/api/memory/search` | Search memory |
| `POST` | `/api/memory/sync` | Synchronize memory |
| `POST` | `/api/memory/update` | Update memory |
| `POST` | `/api/memory/clear` | Clear memory |
| `GET` | `/api/memory/stats` | Memory statistics |
| `GET` | `/api/memory/breakdown` | Memory analysis |
| `GET` | `/api/memory/debug/{user_id}` | Debug memory state |

### System Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/health` | Health check |
| `GET` | `/api/sessions/stats` | Session statistics |

### Example API Usage

```bash
# Register a new user
curl -X POST "http://localhost:8000/api/auth/signup" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "password123",
    "first_name": "John",
    "last_name": "Doe"
  }'

# Login
curl -X POST "http://localhost:8000/api/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "password123"
  }'

# Send a chat message
curl -X POST "http://localhost:8000/api/chat" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "user123",
    "session_id": "sess789",
    "message": "Hello, how are you?"
  }'
```

## 🧠 Memory System

### Dual Memory Architecture

AgnoChat Bot uses a sophisticated dual-memory system:

#### **Zep Memory (Temporal)**
- **Purpose**: Session tracking, conversation flow, entity relationships
- **Storage**: Temporal knowledge graphs
- **Use Cases**: 
  - "My dog's name is Bruno" → creates knowledge graph node
  - Conversation context and flow tracking
  - Entity linking and relationships

#### **Mem0 Memory (Factual)**
- **Purpose**: Long-term fact storage and retrieval
- **Storage**: Fact-based memory with semantic search
- **Use Cases**:
  - "I live in Delhi" → fact: { location: "Delhi" }
  - User preferences and personal information
  - Cross-session knowledge retention

### Memory Operations

```python
# Get memory for a user
memory = client.memory.get(session_id="session123")

# Search memory
results = client.memory.search(
    query="Where do I live?",
    user_id="user123"
)

# Update memory
client.memory.update(
    user_id="user123",
    data={"location": "New York"}
)

# Clear memory
client.memory.clear(user_id="user123")
```

### Memory Analytics

The system provides comprehensive memory analytics:

- **Memory Statistics**: Total memories, Zep vs Mem0 breakdown
- **Memory Health**: System status and performance metrics
- **Memory Breakdown**: Detailed analysis by memory type
- **Session Analytics**: User session patterns and activity

## 🛠️ Development

### Backend Development

1. **Install development dependencies**
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

2. **Run with auto-reload**
   ```bash
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

3. **Access API documentation**
   - Swagger UI: `http://localhost:8000/docs`
   - ReDoc: `http://localhost:8000/redoc`

### Frontend Development

1. **Install dependencies**
   ```bash
   cd agnochat-frontend
   npm install
   ```

2. **Start development server**
   ```bash
   npm start
   ```

3. **Run tests**
   ```bash
   npm test
   ```

### Playground Mode

For development and testing, use the Agno playground:

```bash
cd backend
python playground.py
```

Access the playground at `http://localhost:7777`

## 🚀 Deployment

### Production Deployment

1. **Environment Setup**
   ```bash
   # Set production environment variables
   export DEBUG=false
   export HOST=0.0.0.0
   export PORT=8000
   ```

2. **Database Migration**
   ```bash
   # Run database migrations
   alembic upgrade head
   ```

3. **Start Production Server**
   ```bash
   # Using Gunicorn
   gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
   ```

### Docker Deployment

```dockerfile
# Backend Dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

```bash
# Build and run
docker build -t agnochat-backend .
docker run -p 8000:8000 agnochat-backend
```

## 🤝 Contributing

We welcome contributions! Please follow these steps:

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/amazing-feature
   ```
3. **Make your changes**
4. **Run tests**
   ```bash
   # Backend tests
   cd backend
   pytest
   
   # Frontend tests
   cd agnochat-frontend
   npm test
   ```
5. **Commit your changes**
   ```bash
   git commit -m "Add amazing feature"
   ```
6. **Push to the branch**
   ```bash
   git push origin feature/amazing-feature
   ```
7. **Open a Pull Request**

### Development Guidelines

- Follow PEP 8 for Python code
- Use TypeScript for frontend development
- Write comprehensive tests
- Update documentation for new features
- Follow conventional commit messages

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Agno Framework](https://github.com/agno-agi/agno) - Multi-agent AI framework
- [Zep](https://www.getzep.com/) - Context engineering platform
- [Mem0](https://mem0.ai/) - AI memory layer
- [Google Gemini](https://ai.google.dev/) - Advanced AI model
- [FastAPI](https://fastapi.tiangolo.com/) - Modern web framework
- [React](https://reactjs.org/) - Frontend library

## 📞 Support
---

<div align="center">
  <p>Made with ❤️ by Tushant Gupta</p>
  <p>
    <a href="https://github.com/yourusername/agnochat-bot/stargazers">
      <img src="https://img.shields.io/github/stars/yourusername/agnochat-bot" alt="Stars">
    </a>
    <a href="https://github.com/yourusername/agnochat-bot/network">
      <img src="https://img.shields.io/github/forks/yourusername/agnochat-bot" alt="Forks">
    </a>
    <a href="https://github.com/yourusername/agnochat-bot/issues">
      <img src="https://img.shields.io/github/issues/yourusername/agnochat-bot" alt="Issues">
    </a>
  </p>
</div>












