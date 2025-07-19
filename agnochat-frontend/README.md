# AgnoChat Frontend

A modern, responsive React frontend for the AgnoChat Bot with theme toggling and real-time chat functionality.

## Features

- 🔐 **Authentication**: Login and signup with JWT token management
- 💬 **Real-time Chat**: Interactive chat interface with AgnoChat Bot
- 🌓 **Theme Toggle**: Dark/light mode with persistent preferences
- 📱 **Responsive Design**: Mobile-first design with Tailwind CSS
- 🔒 **Protected Routes**: Authentication guards for secure access
- ⚡ **Modern UI**: Clean, minimalist interface with smooth animations

## Tech Stack

- **Framework**: React 18 with TypeScript
- **Styling**: Tailwind CSS
- **Icons**: Lucide React
- **Routing**: React Router v6
- **HTTP Client**: Axios
- **State Management**: React Context API

## Getting Started

### Prerequisites

- Node.js (v16 or higher)
- npm or yarn
- Backend server running on `http://localhost:8000`

### Installation

1. Clone the repository and navigate to the frontend directory:
   ```bash
   cd agnochat-frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Create environment file:
   ```bash
   echo "REACT_APP_API_URL=http://localhost:8000/api" > .env
   ```

4. Start the development server:
   ```bash
   npm start
   ```

The application will be available at `http://localhost:3000`.

## Project Structure

```
src/
├── components/
│   ├── ChatBubble.tsx      # Chat message component
│   ├── ProtectedRoute.tsx  # Authentication guard
│   └── ThemeToggle.tsx     # Dark/light mode toggle
├── context/
│   └── AuthContext.tsx     # Authentication state management
├── pages/
│   ├── Chat.tsx           # Main chat interface
│   ├── Login.tsx          # Login page
│   └── Signup.tsx         # Signup page
├── services/
│   └── api.ts             # API service layer
├── App.tsx                # Main app component
└── index.tsx              # App entry point
```

## API Integration

The frontend integrates with the AgnoChat Bot backend API:

- **Authentication**: `/api/auth/login`, `/api/auth/signup`, `/api/auth/me`
- **Chat**: `/api/chat` for sending messages
- **Memory**: `/api/memory` for retrieving conversation history

## Features in Detail

### Authentication
- JWT token-based authentication
- Automatic token refresh and validation
- Protected routes with redirect to login
- Persistent login state

### Chat Interface
- Real-time message display
- Typing indicators
- Auto-scroll to latest messages
- Session management
- Error handling with user-friendly messages

### Theme System
- Dark/light mode toggle
- Persistent theme preferences
- System preference detection
- Smooth transitions

### Responsive Design
- Mobile-first approach
- Tablet and desktop optimizations
- Touch-friendly interface
- Adaptive layouts

## Available Scripts

- `npm start` - Start development server
- `npm run build` - Build for production
- `npm test` - Run test suite
- `npm run eject` - Eject from Create React App

## Environment Variables

- `REACT_APP_API_URL` - Backend API URL (default: http://localhost:8000/api)

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is part of the AgnoChat Bot application.
