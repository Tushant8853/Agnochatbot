import React, { useState, useEffect } from 'react';
import { authService } from '../services/auth';
import { chatService } from '../services/chat';
import { memoryService } from '../services/memory';
import Header from '../components/Header';
import Sidebar from '../components/Sidebar/Sidebar';
import ChatWindow from '../components/Chat/ChatWindow';
import MemoryPanel from '../components/MemoryPanel/MemoryPanel';
import './Chat.css';

const Chat = () => {
  const [currentSession, setCurrentSession] = useState(null);
  const [sessions, setSessions] = useState([]);
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);
  const [memoryData, setMemoryData] = useState({
    summary: null,
    agnoMemories: [],
    searchResults: []
  });
  const [showMemoryPanel, setShowMemoryPanel] = useState(true);

  const currentUser = authService.getCurrentUser();

  // Load sessions on component mount
  useEffect(() => {
    loadSessions();
    loadMemoryData();
  }, []);

  // Load or create initial session
  useEffect(() => {
    if (sessions.length > 0 && !currentSession) {
      setCurrentSession(sessions[0]);
    } else if (sessions.length === 0 && !currentSession) {
      createNewSession();
    }
  }, [sessions, currentSession]);

  // Load messages when session changes
  useEffect(() => {
    if (currentSession) {
      loadSessionHistory(currentSession.session_id);
    }
  }, [currentSession]);

  const loadSessions = async () => {
    try {
      const result = await chatService.getSessions();
      if (result.success) {
        setSessions(result.data);
      }
    } catch (error) {
      console.error('Failed to load sessions:', error);
    }
  };

  const loadMemoryData = async () => {
    try {
      const [summaryResult, agnoResult] = await Promise.all([
        memoryService.getMemorySummary(),
        memoryService.getAgnoMemories()
      ]);

      setMemoryData({
        summary: summaryResult.success ? summaryResult.data : null,
        agnoMemories: agnoResult.success ? agnoResult.data.memories : [],
        searchResults: []
      });
    } catch (error) {
      console.error('Failed to load memory data:', error);
    }
  };

  const createNewSession = () => {
    const newSessionId = chatService.generateSessionId();
    const newSession = {
      session_id: newSessionId,
      title: `New Chat ${new Date().toLocaleTimeString()}`,
      created_at: new Date().toISOString(),
      is_active: 'active'
    };
    
    setCurrentSession(newSession);
    setSessions(prev => [newSession, ...prev]);
    setMessages([]);
    localStorage.setItem('currentSessionId', newSessionId);
  };

  const loadSessionHistory = async (sessionId) => {
    try {
      const result = await chatService.getSessionHistory(sessionId);
      if (result.success) {
        setMessages(result.data);
      }
    } catch (error) {
      console.error('Failed to load session history:', error);
    }
  };

  const handleSendMessage = async (message, useAgno = false) => {
    if (!message.trim() || !currentSession) return;

    const newMessage = {
      role: 'user',
      content: message,
      timestamp: new Date().toISOString()
    };

    setMessages(prev => [...prev, newMessage]);
    setLoading(true);

    try {
      const result = useAgno 
        ? await chatService.sendAgnoMessage(message, currentSession.session_id)
        : await chatService.sendMessage(message, currentSession.session_id);

      if (result.success) {
        const aiMessage = {
          role: 'assistant',
          content: result.data.message || result.data.agno_response,
          timestamp: new Date().toISOString()
        };
        setMessages(prev => [...prev, aiMessage]);
        
        // Reload sessions to get updated titles
        loadSessions();
      } else {
        // Add error message
        const errorMessage = {
          role: 'assistant',
          content: 'Sorry, I encountered an error. Please try again.',
          timestamp: new Date().toISOString()
        };
        setMessages(prev => [...prev, errorMessage]);
      }
    } catch (error) {
      console.error('Failed to send message:', error);
      const errorMessage = {
        role: 'assistant',
        content: 'Sorry, I encountered an error. Please try again.',
        timestamp: new Date().toISOString()
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setLoading(false);
    }
  };

  const handleSessionSelect = (session) => {
    setCurrentSession(session);
    localStorage.setItem('currentSessionId', session.session_id);
  };

  const handleLogout = () => {
    authService.logout();
    window.location.reload();
  };

  const handleMemorySearch = async (query) => {
    try {
      const result = await memoryService.searchMemory(query);
      if (result.success) {
        setMemoryData(prev => ({
          ...prev,
          searchResults: result.data
        }));
      }
    } catch (error) {
      console.error('Failed to search memory:', error);
    }
  };

  const handleAddMemory = async (content, type = 'fact') => {
    try {
      const result = await memoryService.addAgnoMemory(content, type);
      if (result.success) {
        loadMemoryData(); // Reload memory data
      }
    } catch (error) {
      console.error('Failed to add memory:', error);
    }
  };

  return (
    <div className="chat-container">
      <Header 
        user={currentUser}
        onLogout={handleLogout}
        onToggleMemoryPanel={() => setShowMemoryPanel(!showMemoryPanel)}
        showMemoryPanel={showMemoryPanel}
      />
      
      <div className="chat-main">
        <Sidebar
          sessions={sessions}
          currentSession={currentSession}
          onSessionSelect={handleSessionSelect}
          onNewChat={createNewSession}
        />
        
        <ChatWindow
          messages={messages}
          onSendMessage={handleSendMessage}
          loading={loading}
          currentSession={currentSession}
        />
        
        {showMemoryPanel && (
          <MemoryPanel
            memoryData={memoryData}
            onSearch={handleMemorySearch}
            onAddMemory={handleAddMemory}
            currentUser={currentUser}
            currentSession={currentSession}
          />
        )}
      </div>
    </div>
  );
};

export default Chat; 