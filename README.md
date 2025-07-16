# 🤖 AgnoChat Bot

A full-stack AI chatbot platform with advanced reasoning capabilities, hybrid memory systems, and a modern responsive interface. Built with FastAPI, React, Google Gemini, and the Agno Framework.

![AgnoChat Bot](https://img.shields.io/badge/AgnoChat-Bot-blue?style=for-the-badge&logo=robot)
![React](https://img.shields.io/badge/React-18.0.0-blue?style=for-the-badge&logo=react)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104.0-green?style=for-the-badge&logo=fastapi)
![Python](https://img.shields.io/badge/Python-3.9+-blue?style=for-the-badge&logo=python)

## ✨ Features

### 🧠 Advanced AI Capabilities
- **Agno Framework Integration**: Advanced reasoning and orchestration
- **Google Gemini LLM**: State-of-the-art language model
- **Multi-session Chat**: Persistent conversations across sessions
- **Context-Aware Responses**: Intelligent memory-based conversations

### 🗄️ Hybrid Memory System
- **Zep Memory**: Temporal and graph-based memory for relationships
- **Mem0 Memory**: Factual and semantic memory for long-term storage
- **Intelligent Routing**: Automatic memory system selection
- **Memory Visualization**: Real-time memory statistics and debugging

### 🎨 Modern UI/UX
- **Theme System**: Light and dark mode support
- **Responsive Design**: Mobile-first approach
- **Real-time Updates**: Live chat with typing indicators
- **Memory Panel**: Interactive memory management interface

### 🔐 Security & Authentication
- **JWT Authentication**: Secure token-based auth
- **Protected Routes**: Role-based access control
- **Environment Security**: Secure API key management
- **CSRF Protection**: Cross-site request forgery prevention

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

- **Node.js** (v16 or higher)
- **Python** (3.9 or higher)
- **PostgreSQL** (for production)
- **Git**

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
cp env.example .env
```

### 3. Frontend Setup

```bash
# Navigate to frontend directory
cd ../frontend

# Install dependencies
npm install

# Set up environment variables
cp env.example .env
```

### 4. Environment Configuration

#### Backend (.env)
```env
# Database
DATABASE_URL=postgresql://username:password@localhost:5432/agnochat

# JWT
JWT_SECRET=your-super-secret-jwt-key
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Google Gemini
GEMINI_API_KEY=your-gemini-api-key
GEMINI_MODEL_ID=gemini-pro

# Zep Memory
ZEP_API_URL=https://api.zep.ai
ZEP_API_KEY=your-zep-api-key

# Mem0 Memory
MEM0_API_KEY=your-mem0-api-key
MEM0_BASE_URL=https://api.mem0.ai

# Agno Framework
AGNO_API_KEY=your-agno-api-key
```

#### Frontend (.env)
```env
REACT_APP_API_URL=http://localhost:8000
REACT_APP_WS_URL=ws://localhost:8000/ws
```

### 5. Database Setup

```bash
# Create PostgreSQL database
createdb agnochat

# Run migrations (if using Alembic)
alembic upgrade head
```

### 6. Start the Application

#### Backend
```bash
cd backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

#### Frontend
```bash
cd frontend
npm start
```

The application will be available at:
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

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
- View memory statistics and summaries
- See Zep and Mem0 memory counts
- Access Agno reasoning memories

#### Search Tab
- Search across all memory systems
- Filter by memory type
- View relevance scores

#### Add Tab
- Manually add new memories
- Choose memory type and content
- See example memory formats

#### Debug Tab
- Monitor memory system status
- View debugging information
- Test memory connections

### 4. Theme System

- **Toggle Theme**: Click the theme button in the header
- **Persistent Preference**: Your theme choice is saved
- **Smooth Transitions**: Seamless switching between light and dark modes

## 🛠️ Development

### Project Structure

```
Agnochatbot/
├── backend/
│   ├── agno_agent/          # Agno framework integration
│   ├── auth/               # Authentication system
│   ├── memory/             # Memory system implementations
│   ├── services/           # Business logic services
│   ├── utils/              # Utility functions
│   ├── main.py             # FastAPI application
│   └── requirements.txt    # Python dependencies
├── frontend/
│   ├── src/
│   │   ├── components/     # React components
│   │   │   ├── Auth/       # Authentication components
│   │   │   ├── Chat/       # Chat interface
│   │   │   ├── MemoryPanel/# Memory management
│   │   │   └── Sidebar/    # Session management
│   │   ├── pages/          # Page components
│   │   ├── services/       # API services
│   │   └── utils/          # Utility functions
│   ├── public/             # Static assets
│   └── package.json        # Node.js dependencies
└── README.md
```

### Key Technologies

#### Backend
- **FastAPI**: Modern Python web framework
- **Agno Framework**: AI reasoning and orchestration
- **Google Gemini**: Large language model
- **Zep**: Temporal and graph memory
- **Mem0**: Factual and semantic memory
- **PostgreSQL**: Primary database
- **JWT**: Authentication tokens

#### Frontend
- **React 18**: UI framework
- **CSS3**: Styling with CSS variables
- **Context API**: State management
- **Fetch API**: HTTP requests
- **LocalStorage**: Client-side persistence

### Development Commands

```bash
# Backend development
cd backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Frontend development
cd frontend
npm start

# Run tests
cd backend && python -m pytest
cd frontend && npm test

# Build for production
cd frontend && npm run build
```

## 🚀 Deployment

### Railway Deployment

1. **Connect Repository**: Link your GitHub repository to Railway
2. **Environment Variables**: Set all required environment variables
3. **Database**: Use Railway's PostgreSQL service
4. **Build Commands**: Railway will auto-detect and build the application

### Environment Variables for Production

```env
# Production settings
DATABASE_URL=postgresql://...
JWT_SECRET=your-production-secret
GEMINI_API_KEY=your-gemini-key
ZEP_API_KEY=your-zep-key
MEM0_API_KEY=your-mem0-key
AGNO_API_KEY=your-agno-key

# Frontend
REACT_APP_API_URL=https://your-backend.railway.app
```

## 🔧 Configuration

### Memory System Configuration

#### Zep Memory
```python
# Configure Zep for temporal memory
ZEP_CONFIG = {
    "api_url": "https://api.zep.ai",
    "api_key": os.getenv("ZEP_API_KEY"),
    "session_ttl": 3600,  # 1 hour
    "max_memories": 100
}
```

#### Mem0 Memory
```python
# Configure Mem0 for semantic memory
MEM0_CONFIG = {
    "api_key": os.getenv("MEM0_API_KEY"),
    "base_url": "https://api.mem0.ai",
    "embedding_model": "text-embedding-ada-002",
    "max_results": 10
}
```

### Theme Configuration

```css
/* Light theme variables */
:root {
  --bg-primary: #ffffff;
  --bg-secondary: #f8fafc;
  --text-primary: #1e293b;
  --text-secondary: #64748b;
  --primary-color: #0ea5e9;
}

/* Dark theme variables */
[data-theme="dark"] {
  --bg-primary: #0f172a;
  --bg-secondary: #1e293b;
  --text-primary: #f1f5f9;
  --text-secondary: #94a3b8;
  --primary-color: #38bdf8;
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
cd frontend
npm test
```

### API Testing
```bash
# Test authentication
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com", "password": "password"}'

# Test chat endpoint
curl -X POST http://localhost:8000/chat \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello, how are you?", "session_id": "test-session"}'
```

## 🤝 Contributing

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/amazing-feature`)
3. **Commit** your changes (`git commit -m 'Add amazing feature'`)
4. **Push** to the branch (`git push origin feature/amazing-feature`)
5. **Open** a Pull Request

### Development Guidelines

- Follow PEP 8 for Python code
- Use ESLint and Prettier for JavaScript
- Write tests for new features
- Update documentation for API changes
- Use conventional commit messages

## 📝 API Documentation

### Authentication Endpoints

```http
POST /auth/signup
POST /auth/login
POST /auth/refresh
GET /auth/me
```

### Chat Endpoints

```http
POST /chat
GET /chat/sessions
DELETE /chat/sessions/{session_id}
```

### Memory Endpoints

```http
GET /memory/facts
POST /memory/search
POST /memory/add
GET /memory/debug
```

Full API documentation available at: `http://localhost:8000/docs`

## 🐛 Troubleshooting

### Common Issues

#### Backend Issues
```bash
# Database connection error
# Solution: Check DATABASE_URL and PostgreSQL service

# API key errors
# Solution: Verify all API keys in .env file

# Memory system errors
# Solution: Check Zep and Mem0 API connectivity
```

#### Frontend Issues
```bash
# Build errors
npm run build

# Dependency issues
rm -rf node_modules package-lock.json
npm install

# Theme not working
# Check browser console for CSS variable errors
```

#### Memory System Issues
```bash
# Zep connection issues
# Check ZEP_API_URL and ZEP_API_KEY

# Mem0 connection issues
# Check MEM0_API_KEY and network connectivity

# Memory routing issues
# Check hybrid_memory.py configuration
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Agno Framework** for advanced AI reasoning
- **Google Gemini** for language model capabilities
- **Zep** for temporal memory management
- **Mem0** for semantic memory storage
- **FastAPI** for the robust backend framework
- **React** for the modern frontend framework


---

**Made with ❤️ by the AgnoChat Team** 