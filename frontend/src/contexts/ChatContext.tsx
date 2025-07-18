import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import { apiService, ChatMessage, ChatSession, ChatRequest, ChatResponse } from '../services/api';

interface ChatContextType {
  // Current session
  currentSession: ChatSession | null;
  sessions: ChatSession[];
  
  // Messages
  messages: ChatMessage[];
  isLoading: boolean;
  isTyping: boolean;
  
  // Memory
  memoryContext: any;
  memorySummary: any;
  
  // Actions
  sendMessage: (message: string) => Promise<void>;
  createNewSession: () => Promise<void>;
  loadSession: (sessionId: string) => Promise<void>;
  loadSessions: () => Promise<void>;
  clearMessages: () => void;
  setTyping: (typing: boolean) => void;
}

const ChatContext = createContext<ChatContextType | undefined>(undefined);

export const useChat = () => {
  const context = useContext(ChatContext);
  if (context === undefined) {
    throw new Error('useChat must be used within a ChatProvider');
  }
  return context;
};

interface ChatProviderProps {
  children: ReactNode;
}

export const ChatProvider: React.FC<ChatProviderProps> = ({ children }) => {
  const [currentSession, setCurrentSession] = useState<ChatSession | null>(null);
  const [sessions, setSessions] = useState<ChatSession[]>([]);
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [isTyping, setIsTyping] = useState(false);
  const [memoryContext, setMemoryContext] = useState<any>(null);
  const [memorySummary, setMemorySummary] = useState<any>(null);

  // Load sessions on mount
  useEffect(() => {
    loadSessions();
  }, []);

  const loadSessions = async () => {
    try {
      const sessionsData = await apiService.getSessions();
      setSessions(sessionsData);
    } catch (error) {
      console.error('Failed to load sessions:', error);
    }
  };

  const createNewSession = async () => {
    try {
      const newSession = await apiService.createSession({
        title: `New Chat ${new Date().toLocaleTimeString()}`
      });
      
      setCurrentSession(newSession);
      setMessages([]);
      setMemoryContext(null);
      
      // Add to sessions list
      setSessions(prev => [newSession, ...prev]);
    } catch (error) {
      console.error('Failed to create session:', error);
    }
  };

  const loadSession = async (sessionId: string) => {
    try {
      setIsLoading(true);
      
      // Find session in sessions list
      const session = sessions.find(s => s.session_id === sessionId);
      if (session) {
        setCurrentSession(session);
      }
      
      // Load messages
      const sessionMessages = await apiService.getSessionHistory(sessionId);
      setMessages(sessionMessages);
      
      // Load memory summary
      try {
        const summary = await apiService.getMemorySummary();
        setMemorySummary(summary);
      } catch (error) {
        console.error('Failed to load memory summary:', error);
      }
      
    } catch (error) {
      console.error('Failed to load session:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const sendMessage = async (message: string) => {
    if (!message.trim()) return;

    const userMessage: ChatMessage = {
      role: 'user',
      content: message,
      timestamp: new Date().toISOString(),
    };

    // Add user message immediately
    setMessages(prev => [...prev, userMessage]);
    setIsTyping(true);

    try {
      const request: ChatRequest = {
        message,
        session_id: currentSession?.session_id,
        use_memory: true,
      };

      const response: ChatResponse = await apiService.sendMessage(request);

      // Add assistant response
      const assistantMessage: ChatMessage = {
        role: 'assistant',
        content: response.message,
        timestamp: response.timestamp,
      };

      setMessages(prev => [...prev, assistantMessage]);
      setMemoryContext(response.memory_context);

      // Update current session if it's new
      if (!currentSession && response.session_id) {
        const newSession: ChatSession = {
          session_id: response.session_id,
          title: `Chat ${new Date().toLocaleTimeString()}`,
          created_at: new Date().toISOString(),
          is_active: 'active',
        };
        setCurrentSession(newSession);
        setSessions(prev => [newSession, ...prev]);
      }

    } catch (error) {
      console.error('Failed to send message:', error);
      
      // Add error message
      const errorMessage: ChatMessage = {
        role: 'assistant',
        content: 'Sorry, I encountered an error. Please try again.',
        timestamp: new Date().toISOString(),
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsTyping(false);
    }
  };

  const clearMessages = () => {
    setMessages([]);
    setMemoryContext(null);
  };

  const setTyping = (typing: boolean) => {
    setIsTyping(typing);
  };

  const value: ChatContextType = {
    currentSession,
    sessions,
    messages,
    isLoading,
    isTyping,
    memoryContext,
    memorySummary,
    sendMessage,
    createNewSession,
    loadSession,
    loadSessions,
    clearMessages,
    setTyping,
  };

  return (
    <ChatContext.Provider value={value}>
      {children}
    </ChatContext.Provider>
  );
}; 