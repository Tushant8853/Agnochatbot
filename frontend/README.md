# AgnoChat Frontend

A modern, responsive React.js frontend for the AgnoChat AI assistant with advanced memory capabilities.

## 🚀 Features

- **JWT Authentication**: Secure login/signup with token-based authentication
- **Multi-Session Chat**: Create and manage multiple chat sessions
- **Hybrid Memory System**: View and manage Zep, Mem0, and Agno memories
- **Memory Search**: Search across all memory systems with different search types
- **Memory Management**: Add custom facts and memories to the AI's knowledge base
- **Agno Framework Integration**: Toggle between regular chat and Agno framework
- **Responsive Design**: Works seamlessly on desktop, tablet, and mobile devices
- **Real-time Chat**: Live message exchange with typing indicators
- **Session Persistence**: Chat history and sessions are saved and restored
- **Debug Panel**: Technical information and system status monitoring

## 🛠️ Tech Stack

- **Framework**: React.js 18
- **Routing**: React Router DOM v6
- **HTTP Client**: Axios
- **Styling**: Pure CSS (no UI frameworks)
- **State Management**: React Hooks (useState, useEffect)
- **Authentication**: JWT tokens with localStorage

## 📁 Project Structure

```
src/
├── components/
│   ├── Auth/           # Authentication components
│   ├── Chat/           # Chat interface components
│   │   ├── ChatWindow.jsx
│   │   ├── ChatInput.jsx
│   │   ├── Message.jsx
│   │   └── *.css
│   ├── Sidebar/        # Session management
│   │   ├── Sidebar.jsx
│   │   └── Sidebar.css
│   ├── MemoryPanel/    # Memory system interface
│   │   ├── MemoryPanel.jsx
│   │   ├── MemoryFacts.jsx
│   │   ├── MemorySearch.jsx
│   │   ├── AddMemory.jsx
│   │   ├── MemoryDebug.jsx
│   │   └── *.css
│   ├── Header.jsx      # Main header component
│   └── Header.css
├── pages/
│   ├── Login.jsx       # Login page
│   ├── Signup.jsx      # Signup page
│   ├── Chat.jsx        # Main chat interface
│   └── *.css
├── services/
│   ├── auth.js         # Authentication API calls
│   ├── chat.js         # Chat API calls
│   └── memory.js       # Memory API calls
├── utils/              # Utility functions
├── App.js              # Main app component
├── App.css             # Global styles
├── index.js            # App entry point
└── index.css           # Base styles
```

## 🚀 Getting Started

### Prerequisites

- Node.js 16+ and npm
- Backend server running (see backend README)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd frontend
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Environment Configuration**
   Create a `.env` file in the frontend directory:
   ```env
   REACT_APP_API_URL=http://localhost:8000
   ```

4. **Start the development server**
   ```bash
   npm start
   ```

5. **Open your browser**
   Navigate to `http://localhost:3000`

## 🔧 Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `REACT_APP_API_URL` | Backend API URL | `http://localhost:8000` |

### Backend Integration

The frontend connects to the FastAPI backend with the following endpoints:

- **Authentication**: `/auth/signup`, `/auth/login`
- **Chat**: `/chat`, `/sessions`, `/sessions/{id}/history`
- **Memory**: `/memory/search`, `/memory/summary`, `/memory/facts`
- **Agno**: `/agno/chat`, `/agno/memories`, `/agno/agent`

## 🎨 Features in Detail

### Authentication System
- **Signup**: Create new account with username, email, password
- **Login**: Authenticate with username/password
- **JWT Tokens**: Automatic token management and refresh
- **Protected Routes**: Automatic redirection for unauthenticated users

### Chat Interface
- **Three-Column Layout**: Sidebar, Chat Window, Memory Panel
- **Message Bubbles**: User messages (right-aligned, blue) and AI responses (left-aligned, grey)
- **Real-time Updates**: Messages appear instantly with smooth animations
- **Typing Indicators**: Visual feedback while AI is processing
- **Session Management**: Create new chats and switch between sessions
- **Agno Toggle**: Switch between regular chat and Agno framework

### Memory System
- **Memory Facts**: View summary and key facts from all memory systems
- **Memory Search**: Search across Zep, Mem0, and combined results
- **Add Memories**: Create new facts, preferences, and experiences
- **Debug Panel**: Technical information and system status

### Responsive Design
- **Desktop**: Full three-column layout
- **Tablet**: Adaptive layout with collapsible panels
- **Mobile**: Single-column layout with navigation

## 🎯 Usage Guide

### Getting Started
1. **Sign up** for a new account or **log in** with existing credentials
2. **Create a new chat** session or select an existing one
3. **Start chatting** with the AI assistant
4. **Explore memory features** using the right panel

### Memory Management
1. **View Facts**: Check the "Facts" tab to see your memory summary
2. **Search Memory**: Use the "Search" tab to find specific information
3. **Add Memories**: Use the "Add" tab to create new memories
4. **Debug Info**: Check the "Debug" tab for technical details

### Chat Features
- **Send Messages**: Type and press Enter or click the send button
- **Use Agno**: Toggle the "Use Agno Framework" checkbox for advanced reasoning
- **Session History**: All conversations are automatically saved
- **New Sessions**: Click "New Chat" to start fresh conversations

## 🔒 Security Features

- **JWT Authentication**: Secure token-based authentication
- **Protected Routes**: Automatic redirection for unauthorized access
- **Token Expiry**: Automatic logout on token expiration
- **Input Validation**: Client-side validation for all forms
- **XSS Protection**: Sanitized input handling

## 🚀 Deployment

### Build for Production
```bash
npm run build
```

### Deploy to Vercel
1. Install Vercel CLI: `npm i -g vercel`
2. Deploy: `vercel`

### Deploy to Netlify
1. Build the project: `npm run build`
2. Upload the `build` folder to Netlify

### Environment Variables for Production
Set the following environment variables in your hosting platform:
- `REACT_APP_API_URL`: Your production backend URL

## 🐛 Troubleshooting

### Common Issues

1. **Backend Connection Error**
   - Ensure the backend server is running
   - Check the `REACT_APP_API_URL` environment variable
   - Verify CORS settings on the backend

2. **Authentication Issues**
   - Clear browser localStorage
   - Check JWT token expiration
   - Verify backend authentication endpoints

3. **Memory Panel Not Loading**
   - Check browser console for errors
   - Verify memory API endpoints
   - Ensure proper authentication

### Development Tips

- Use browser developer tools to inspect network requests
- Check the browser console for error messages
- Use the Debug panel to monitor system status
- Test responsive design using browser dev tools

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 🆘 Support

For support and questions:
- Check the browser console for error messages
- Review the Debug panel for system information
- Create an issue in the repository
- Check the backend logs for API errors
