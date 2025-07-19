# 🤖 AgnoChat Bot

A full-stack AI chatbot platform with advanced reasoning capabilities, hybrid memory systems, and a modern responsive interface. Built with FastAPI, React, Google Gemini, and the Agno Framework.

[![React](https://img.shields.io/badge/React-19.1.0-blue.svg)](https://reactjs.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104.1-green.svg)](https://fastapi.tiangolo.com/)
[![Agno](https://img.shields.io/badge/Agno-1.6.0-purple.svg)](https://agno.ai/)
[![Gemini](https://img.shields.io/badge/Gemini-2.0--Flash-orange.svg)](https://ai.google.dev/gemini)

## 🎬 Demo

Watch AgnoChat Bot in action! See the advanced AI reasoning, memory systems, and modern UI features.

**🎥 Watch Demo Video** (Coming Soon)

_Experience the future of AI chat with advanced reasoning, hybrid memory systems, and a beautiful responsive interface._

## ✨ Features

### 🧠 Advanced AI Capabilities

* **Agno Framework Integration**: Advanced reasoning and orchestration
* **Google Gemini LLM**: State-of-the-art language model (Gemini 2.0 Flash)
* **Multi-session Chat**: Persistent conversations across sessions
* **Context-Aware Responses**: Intelligent memory-based conversations

### 🗄️ Hybrid Memory System

* **Zep Memory**: Temporal and graph-based memory for relationships
* **Mem0 Memory**: Factual and semantic memory for long-term storage
* **Intelligent Routing**: Automatic memory system selection
* **Memory Visualization**: Real-time memory statistics and debugging

### 🎨 Modern UI/UX

* **Theme System**: Light and dark mode support
* **Responsive Design**: Mobile-first approach
* **Real-time Updates**: Live chat with typing indicators
* **Memory Panel**: Interactive memory management interface
* **Chat History**: Complete conversation history with session management

### 🔐 Security & Authentication

* **JWT Authentication**: Secure token-based auth
* **Protected Routes**: Role-based access control
* **Environment Security**: Secure API key management
* **CSRF Protection**: Cross-site request forgery prevention

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   React Frontend│    │  FastAPI Backend│    │   Memory Systems│
│                 │    │                 │    │                 │
│ • Chat Interface│◄──►│ • Agno Agent    │◄──►│ • Zep (Temporal)│
│ • Memory Panel  │    │ • Gemini LLM    │    │ • Mem0 (Semantic)│
│ • Theme System  │    │ • JWT Auth      │    │ • Hybrid Router │
│ • Responsive UI │    │ • API Routes    │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 🚀 Quick Start

### Prerequisites

* **Node.js** (v16 or higher)
* **Python** (3.9 or higher)
* **PostgreSQL** (for production)
* **Git**
* **API Keys** for:  
   * Google Gemini  
   * ZEP Memory  
   * MEM0 Memory

### 1. Clone the Repository

```bash
git clone https://github.com/Tushant8853/Agnochatbot.git
cd Agnochatbot
```

### 2. Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your API keys
```

### 3. Frontend Setup

```bash
# Navigate to frontend directory
cd agnochat-frontend

# Install dependencies
npm install

# Set up environment variables
cp .env.example .env
# Edit .env with your backend API URL
```

### 4. Environment Variables

#### Backend (.env)
Create a `.env` file in the `backend` directory with the following variables:

```bash
# Database Configuration
DATABASE_URL=postgresql://username:password@localhost:5432/agnochat_db

# API Keys - Get these from respective services
GEMINI_API_KEY=your-gemini-api-key-here
ZEP_API_KEY=your-zep-api-key-here
MEM0_API_KEY=your-mem0-api-key-here

# JWT Configuration
SECRET_KEY=your-secure-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Server Configuration
HOST=0.0.0.0
PORT=8000
DEBUG=true

# Memory System Configuration (Optional)
ZEP_BASE_URL=https://api.getzep.com
MEM0_BASE_URL=https://api.mem0.ai

# CORS Configuration
ALLOWED_ORIGINS=["http://localhost:3000"]
```

**Required API Keys:**
- **Google Gemini**: Get your API key from [Google AI Studio](https://ai.google.dev/)
- **Zep Memory**: Get your API key from [Zep AI](https://zep.ai/)
- **Mem0 Memory**: Get your API key from [Mem0 AI](https://mem0.ai/)

#### Frontend (.env)
Create a `.env` file in the `agnochat-frontend` directory:

```bash
REACT_APP_API_URL=http://localhost:8000/api
```

### 5. Run the Application

#### Backend
```bash
cd backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

#### Frontend
```bash
cd agnochat-frontend
npm start
```

The application will be available at:

* **Frontend**: http://localhost:3000
* **Backend API**: http://localhost:8000
* **API Documentation**: http://localhost:8000/docs

## 📖 Usage Guide

### 1. Authentication

1. **Sign Up**: Create a new account with email and password
2. **Login**: Use your credentials to access the chat interface
3. **Session Management**: Your session persists across browser reloads

### 2. Chat Interface

1. **Start Chatting**: Type your message and press Enter
2. **Memory Context**: The AI remembers previous conversations
3. **Agno Reasoning**: Advanced reasoning capabilities for complex queries
4. **Session Management**: Create and switch between different chat sessions

### 3. Memory Panel

#### Facts Tab
* View memory statistics and summaries
* See Zep and Mem0 memory counts
* Access Agno reasoning memories

#### Search Tab
* Search across all memory systems
* Filter by memory type
* View relevance scores

#### Add Tab
* Manually add new memories
* Choose memory type and content
* See example memory formats

#### Debug Tab
* Monitor memory system status
* View debugging information
* Test memory connections

### 4. Chat History

* **View Conversations**: Browse through past chat sessions
* **Session Management**: Organize conversations by session
* **Search History**: Find specific conversations or topics
* **Export Data**: Download conversation history

### 5. Theme System

* **Toggle Theme**: Click the theme button in the header
* **Persistent Preference**: Your theme choice is saved
* **Smooth Transitions**: Seamless switching between light and dark modes

## 🛠️ Development

### Project Structure

```
Agnochatbot/
├── backend/
│   ├── agno_chatbot/          # Agno framework integration
│   │   ├── agents/            # AI agents (chatbot, memory, research)
│   │   ├── api/               # FastAPI routes
│   │   ├── config/            # Configuration settings
│   │   └── utils/             # Utility functions
│   ├── main.py                # FastAPI application entry point
│   └── requirements.txt       # Python dependencies
├── agnochat-frontend/
│   ├── src/
│   │   ├── components/        # React components
│   │   │   ├── ChatBubble.tsx # Individual message display
│   │   │   ├── ChatHistory.tsx# Conversation history
│   │   │   ├── MemoryPanel.tsx# Memory management
│   │   │   └── ...            # Other components
│   │   ├── pages/             # Page components
│   │   ├── services/          # API services
│   │   └── context/           # React context providers
│   ├── public/                # Static assets
│   └── package.json           # Node.js dependencies
├── README.md                  # Main project documentation
├── TECHNICAL_REPORT.md        # Technical implementation details
└── .gitignore                 # Git ignore rules
```

### Key Technologies

#### Backend
* **FastAPI**: Modern Python web framework
* **Agno Framework**: AI reasoning and orchestration
* **Google Gemini**: Large language model
* **Zep**: Temporal and graph memory
* **Mem0**: Factual and semantic memory
* **PostgreSQL**: Primary database
* **JWT**: Authentication tokens

#### Frontend
* **React 19**: UI framework
* **TypeScript**: Type safety
* **Tailwind CSS**: Utility-first styling
* **Context API**: State management
* **Axios**: HTTP requests
* **LocalStorage**: Client-side persistence

### Development Commands

```bash
# Backend development
cd backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Frontend development
cd agnochat-frontend
npm start

# Run tests
cd backend && python -m pytest
cd agnochat-frontend && npm test

# Build for production
cd agnochat-frontend && npm run build
```

## 🚀 Deployment

### Railway Deployment

1. **Connect Repository**: Link your GitHub repository to Railway
2. **Environment Variables**: Set all required environment variables
3. **Database**: Use Railway's PostgreSQL service
4. **Build Commands**: Railway will auto-detect and build the application

### Environment Variables for Production

```bash
# Production settings
DATABASE_URL=postgresql://...
JWT_SECRET=your-production-secret
GEMINI_API_KEY=your-gemini-key
ZEP_API_KEY=your-zep-key
MEM0_API_KEY=your-mem0-key

# Frontend
REACT_APP_API_URL=https://your-backend.railway.app
```

## 🔧 Configuration

### Memory System Configuration

#### Zep Memory
```python
ZEP_CONFIG = {
    "api_url": "https://api.zep.ai",
    "api_key": os.getenv("ZEP_API_KEY"),
    "session_ttl": 3600,  # 1 hour
    "max_memories": 100
}
```

#### Mem0 Memory
```python
MEM0_CONFIG = {
    "api_key": os.getenv("MEM0_API_KEY"),
    "base_url": "https://api.mem0.ai",
    "embedding_model": "text-embedding-ada-002",
    "max_results": 10
}
```

## 🧪 Testing

### Backend Tests
```bash
cd backend
python -m pytest tests/ -v
```

### Frontend Tests
```bash
cd agnochat-frontend
npm test
```

### API Testing
```bash
# Test authentication
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com", "password": "password"}'

# Test chat endpoint
curl -X POST http://localhost:8000/api/chat \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello, how are you?", "session_id": "test-session"}'
```

## 📝 API Documentation

### Authentication Endpoints
- `POST /api/auth/signup` - User registration
- `POST /api/auth/login` - User authentication
- `GET /api/auth/me` - Get current user info

### Chat Endpoints
- `POST /api/chat` - Send chat message
- `GET /api/chat/history` - Get chat history

### Memory Endpoints
- `GET /api/memory` - Get memory data
- `POST /api/memory/search` - Search memory
- `GET /api/memory/stats` - Get memory statistics
- `GET /api/memory/breakdown` - Get memory breakdown

Full API documentation available at: `http://localhost:8000/docs`

## 🤝 Contributing

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/amazing-feature`)
3. **Commit** your changes (`git commit -m 'Add amazing feature'`)
4. **Push** to the branch (`git push origin feature/amazing-feature`)
5. **Open** a Pull Request

### Development Guidelines
* Follow PEP 8 for Python code
* Use ESLint and Prettier for JavaScript
* Write tests for new features
* Update documentation for API changes
* Use conventional commit messages

## 🐛 Troubleshooting

### Common Issues

#### Backend Issues
* **Database connection error**: Check DATABASE_URL and PostgreSQL service
* **API key errors**: Verify all API keys in .env file
* **Memory system errors**: Check Zep and Mem0 API connectivity

#### Frontend Issues
* **Build errors**: Run `npm run build` to check for issues
* **Dependency issues**: Delete node_modules and reinstall
* **Theme not working**: Check browser console for CSS variable errors

#### Memory System Issues
* **Zep connection issues**: Check ZEP_API_URL and ZEP_API_KEY
* **Mem0 connection issues**: Check MEM0_API_KEY and network connectivity
* **Memory routing issues**: Check hybrid memory configuration

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

* **Agno Framework** for advanced AI reasoning
* **Google Gemini** for language model capabilities
* **Zep** for temporal memory management
* **Mem0** for semantic memory storage
* **FastAPI** for the robust backend framework
* **React** for the modern frontend framework

---

**Made with ❤️ by Tushant Gupta**

## 📊 Project Statistics

* **Backend**: 1,200+ lines of Python code
* **Frontend**: 2,500+ lines of TypeScript code
* **Memory Systems**: Zep + Mem0 hybrid architecture
* **AI Model**: Google Gemini 2.0 Flash
* **Framework**: Agno 1.6.0
* **Database**: PostgreSQL with SQLAlchemy ORM
* **Authentication**: JWT with bcrypt hashing
* **UI Framework**: React 19 with Tailwind CSS
* **Deployment**: Railway-ready configuration 