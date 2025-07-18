# Agnochat Frontend

A modern, responsive React frontend for the Agnochat AI assistant with memory capabilities.

## Features

### 🎨 Modern UI Design
- Clean, responsive chat interface
- Dark/light theme toggle
- Smooth animations and transitions
- Mobile-responsive design

### ⚡ Real-time Features
- Live typing indicators
- Message status indicators
- Real-time message updates
- Auto-scroll to latest messages

### 🧠 Memory Visualization
- Display active memory context
- Show stored facts and relationships
- Memory debugging panel (collapsible)
- Memory search functionality

### 👤 User Experience
- User authentication (login/signup)
- Session management
- Message history with timestamps
- Export conversation history

### 📊 Advanced Features
- Memory analytics dashboard
- Session management interface
- Memory search functionality
- Custom fact addition

## Tech Stack

- **React 18** with TypeScript
- **Tailwind CSS** for styling
- **Framer Motion** for animations
- **Axios** for API communication
- **React Hot Toast** for notifications
- **Lucide React** for icons
- **Date-fns** for date formatting

## Getting Started

### Prerequisites

- Node.js (v16 or higher)
- npm or yarn
- Backend server running on `http://localhost:8000`

### Installation

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm start
```

The application will open at `http://localhost:3000`

### Environment Variables

Create a `.env` file in the frontend directory:

```env
REACT_APP_API_URL=http://localhost:8000
```

## Project Structure

```
src/
├── components/
│   ├── auth/           # Authentication components
│   ├── chat/           # Chat interface components
│   ├── layout/         # Layout and navigation
│   ├── memory/         # Memory visualization
│   └── sessions/       # Session management
├── contexts/           # React contexts
├── pages/              # Page components
├── services/           # API services
└── utils/              # Utility functions
```

## API Integration

The frontend communicates with the backend using the following endpoints:

- **Authentication**: `/auth/login`, `/auth/signup`
- **Chat**: `/chat/agno` (as requested)
- **Sessions**: `/sessions`
- **Memory**: `/memory/*`, `/agno/memories`

## Key Components

### Authentication
- `LoginForm`: User login with validation
- `SignupForm`: User registration with validation
- `AuthContext`: Authentication state management

### Chat Interface
- `ChatInterface`: Main chat component
- `MessageBubble`: Individual message display
- `TypingIndicator`: Real-time typing indicator
- `ChatInput`: Message input with auto-resize

### Memory Management
- `MemoryPanel`: Memory visualization and search
- Memory context display
- Custom fact addition
- Memory search functionality

### Session Management
- `SessionList`: Chat session list
- Session creation and switching
- Export functionality

## Styling

The application uses Tailwind CSS with custom components:

- **Color Scheme**: Primary blue theme with dark mode support
- **Components**: Pre-built component classes for buttons, inputs, cards
- **Animations**: Framer Motion for smooth transitions
- **Responsive**: Mobile-first design approach

## Development

### Available Scripts

- `npm start`: Start development server
- `npm build`: Build for production
- `npm test`: Run tests
- `npm eject`: Eject from Create React App

### Code Style

- TypeScript for type safety
- Functional components with hooks
- Context API for state management
- Component composition pattern

## Deployment

1. Build the application:
```bash
npm run build
```

2. The `build` folder contains the production-ready files

3. Deploy to your preferred hosting service (Vercel, Netlify, etc.)

## Contributing

1. Follow the existing code style
2. Add TypeScript types for new features
3. Test thoroughly before submitting
4. Update documentation as needed

## License

This project is part of the Agnochat application.
