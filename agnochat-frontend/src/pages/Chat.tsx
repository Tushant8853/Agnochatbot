import React, { useState, useEffect, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import { Send, Search, BarChart3, LogOut, MessageSquare } from 'lucide-react';
import { useAuth } from '../context/AuthContext';
import { chatAPI } from '../services/api';
import ChatBubble from '../components/ChatBubble';
import TypingIndicator from '../components/TypingIndicator';
import MemorySearch from '../components/MemorySearch';
import MemoryAnalytics from '../components/MemoryAnalytics';
import MemoryPanel from '../components/MemoryPanel';
import ChatHistory from '../components/ChatHistory';
import ThemeToggle from '../components/ThemeToggle';
import { MessageStatus } from '../components/MessageStatus';

interface Message {
  id: string;
  message: string;
  isUser: boolean;
  timestamp: string;
  status?: MessageStatus;
}

interface MemoryData {
  zep_memory: any;
  mem0_memory: any;
  consolidated_memory: string;
}

interface SearchResult {
  id: string;
  query: string;
  results: string;
  timestamp: string;
  relevance?: number; // Made optional since we removed hardcoded relevance
}

const Chat: React.FC = () => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [inputMessage, setInputMessage] = useState('');
  const [isTyping, setIsTyping] = useState(false);
  const [memoryData, setMemoryData] = useState<MemoryData | null>(null);
  const [isLoadingMemory, setIsLoadingMemory] = useState(false);
  
  // Panel states
  const [isMemoryPanelOpen, setIsMemoryPanelOpen] = useState(false);
  const [isAnalyticsOpen, setIsAnalyticsOpen] = useState(false);
  const [isSearchOpen, setIsSearchOpen] = useState(false);
  const [isChatHistoryOpen, setIsChatHistoryOpen] = useState(false);
  
  // Memory analytics state
  const [memoryStats, setMemoryStats] = useState({
    totalMemories: 0,
    zepMemories: 0,
    mem0Memories: 0,
    activeSessions: 1, // Default to 1 since we removed session management
    lastUpdated: new Date().toLocaleTimeString()
  });
  const [isLoadingMemoryStats, setIsLoadingMemoryStats] = useState(false);
  const [memoryStatsError, setMemoryStatsError] = useState<string | null>(null);
  
  const messagesEndRef = useRef<HTMLDivElement>(null);
  
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  useEffect(() => {
    if (!user) {
      navigate('/login');
      return;
    }
    
    // Load memory data
    loadMemoryData();
  }, [user, navigate]);

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  // Keyboard shortcuts
  useEffect(() => {
    const handleKeyDown = (event: KeyboardEvent) => {
      // Removed session manager specific shortcuts
    };

    document.addEventListener('keydown', handleKeyDown);
    return () => document.removeEventListener('keydown', handleKeyDown);
  }, []);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const loadMemoryData = async () => {
    if (!user) return;
    
    setIsLoadingMemory(true);
    try {
      const response = await chatAPI.getMemory(user.user_id, 'default_session'); // Use default session ID
      setMemoryData(response.data);
      
      // Remove auto-refresh of memory stats
    } catch (error) {
      console.error('Error loading memory data:', error);
    } finally {
      setIsLoadingMemory(false);
    }
  };

  const handleSendMessage = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!inputMessage.trim() || !user) return;

    const userMessage: Message = {
      id: Date.now().toString(),
      message: inputMessage,
      isUser: true,
      timestamp: new Date().toLocaleTimeString(),
      status: 'sending'
    };

    setMessages(prev => [...prev, userMessage]);
    setInputMessage('');
    setIsTyping(true);

    try {
      const response = await chatAPI.sendMessage({
        user_id: user.user_id,
        session_id: 'default_session', // Use default session ID
        message: inputMessage,
      });

      // Update user message status
      setMessages(prev => prev.map(msg => 
        msg.id === userMessage.id ? { ...msg, status: 'delivered' as MessageStatus } : msg
      ));

      const aiMessage: Message = {
        id: (Date.now() + 1).toString(),
        message: response.data.response,
        isUser: false,
        timestamp: new Date().toLocaleTimeString(),
      };

      setMessages(prev => [...prev, aiMessage]);
      
      // Stop typing indicator immediately after receiving response
      setIsTyping(false);
      
      // Reload memory data only (remove memory stats refresh)
      Promise.all([
        loadMemoryData()
      ]).catch(error => {
        console.error('Error updating memory data:', error);
      });
    } catch (error) {
      console.error('Error sending message:', error);
      
      // Update user message status to error
      setMessages(prev => prev.map(msg => 
        msg.id === userMessage.id ? { ...msg, status: 'error' as MessageStatus } : msg
      ));
      
      const errorMessage: Message = {
        id: (Date.now() + 1).toString(),
        message: 'Sorry, I encountered an error. Please try again.',
        isUser: false,
        timestamp: new Date().toLocaleTimeString(),
      };
      setMessages(prev => [...prev, errorMessage]);
      
      // Stop typing indicator on error
      setIsTyping(false);
    }
  };

  const handleMemorySearch = async (query: string): Promise<SearchResult> => {
    if (!user) throw new Error('User not authenticated');
    
    try {
      const response = await chatAPI.searchMemory(user.user_id, query);
      return {
        id: Date.now().toString(),
        query,
        results: response.data.results,
        timestamp: new Date().toISOString()
        // Removed hardcoded relevance score
      };
    } catch (error) {
      console.error('Memory search failed:', error);
      throw new Error('Memory search failed. Please try again.');
    }
  };

  // Removed handleSessionCreate, handleSessionSelect, handleSessionDelete, handleSessionExport

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  // Fetch real memory statistics from API
  const fetchMemoryStats = async () => {
    if (!user) return;
    
    setIsLoadingMemoryStats(true);
    setMemoryStatsError(null);
    
    try {
      // Fetch memory statistics from API
      const memoryStatsResponse = await chatAPI.getMemoryStats(user.user_id);
      const sessionStatsResponse = await chatAPI.getSessionStats(user.user_id);
      
      const memoryData = memoryStatsResponse.data;
      const sessionData = sessionStatsResponse.data;
      
      const newStats = {
        totalMemories: memoryData.total_memories || 0,
        zepMemories: memoryData.zep_memories || 0,
        mem0Memories: memoryData.mem0_memories || 0,
        activeSessions: sessionData.active_sessions || 1,
        lastUpdated: new Date().toLocaleTimeString()
      };
      
      setMemoryStats(newStats);
      console.log('Real memory stats fetched:', newStats);
      
    } catch (error) {
      console.error('Error fetching memory stats:', error);
      setMemoryStatsError('Failed to load memory statistics');
      
      // Fallback to calculated stats
      const fallbackStats = {
        totalMemories: 1, // Default to 1 memory
        zepMemories: 1,
        mem0Memories: 0,
        activeSessions: 1, // Default to 1 since we removed session management
        lastUpdated: new Date().toLocaleTimeString()
      };
      setMemoryStats(fallbackStats);
    } finally {
      setIsLoadingMemoryStats(false);
    }
  };

  // Remove auto-fetch of memory stats - now only manual refresh
  // useEffect(() => {
  //   if (user) {
  //     fetchMemoryStats();
  //   }
  // }, [user]);

  if (!user) {
    return null;
  }

  return (
    <div className="h-screen bg-gray-50 dark:bg-gray-900 flex flex-col">
      {/* Header */}
      <div className="bg-white dark:bg-gray-800 border-b border-gray-200 dark:border-gray-700 px-4 py-3 flex justify-between items-center">
        <div className="flex items-center space-x-3">
          <h1 className="text-xl font-semibold text-gray-900 dark:text-white">
            AgnoChat Bot
          </h1>
          <div className="flex items-center space-x-2">
            <span className="text-sm text-gray-500 dark:text-gray-400">
              Welcome, {user.first_name || user.email}
            </span>
            {/* Removed session count display */}
          </div>
        </div>
        <div className="flex items-center space-x-2">
          {/* Feature Buttons */}
          <button
            onClick={() => setIsSearchOpen(!isSearchOpen)}
            className="p-2 rounded-lg bg-purple-100 dark:bg-purple-900/20 hover:bg-purple-200 dark:hover:bg-purple-900/40 transition-colors duration-200"
            title="Memory Search"
          >
            <Search className="w-5 h-5 text-purple-600 dark:text-purple-400" />
          </button>
          <button
            onClick={() => setIsAnalyticsOpen(!isAnalyticsOpen)}
            className="p-2 rounded-lg bg-green-100 dark:bg-green-900/20 hover:bg-green-200 dark:hover:bg-green-900/40 transition-colors duration-200"
            title="Memory Analytics"
          >
            <BarChart3 className="w-5 h-5 text-green-600 dark:text-green-400" />
          </button>
          <button
            onClick={() => setIsChatHistoryOpen(!isChatHistoryOpen)}
            className="p-2 rounded-lg bg-blue-100 dark:bg-blue-900/20 hover:bg-blue-200 dark:hover:bg-blue-900/40 transition-colors duration-200"
            title="Chat History"
          >
            <MessageSquare className="w-5 h-5 text-blue-600 dark:text-blue-400" />
          </button>
          <ThemeToggle />
          <button
            onClick={handleLogout}
            className="p-2 rounded-lg bg-red-100 dark:bg-red-900/20 hover:bg-red-200 dark:hover:bg-red-900/40 transition-colors duration-200"
            aria-label="Logout"
          >
            <LogOut className="w-5 h-5 text-red-600 dark:text-red-400" />
          </button>
        </div>
      </div>

      {/* Main Content */}
      <div className="flex-1 flex overflow-hidden">
        {/* Chat Area */}
        <div className="flex-1 flex flex-col">
          {/* Messages */}
          <div className="flex-1 overflow-y-auto p-4 space-y-4 custom-scrollbar">
            {messages.length === 0 && (
              <div className="text-center text-gray-500 dark:text-gray-400 mt-8">
                <p>Start a conversation with AgnoChat Bot!</p>
                <p className="text-sm mt-2">Ask me anything and I'll help you out.</p>
                {/* Removed session display */}
              </div>
            )}
            
            {messages.map((message) => (
              <ChatBubble
                key={message.id}
                message={message.message}
                isUser={message.isUser}
                timestamp={message.timestamp}
                status={message.status}
                showStatus={message.isUser}
              />
            ))}
            
            <TypingIndicator isTyping={isTyping} />
            
            <div ref={messagesEndRef} />
          </div>

          {/* Input */}
          <div className="bg-white dark:bg-gray-800 border-t border-gray-200 dark:border-gray-700 p-4">
            <form onSubmit={handleSendMessage} className="flex space-x-2">
              <input
                type="text"
                value={inputMessage}
                onChange={(e) => setInputMessage(e.target.value)}
                placeholder="Type your message..."
                disabled={isTyping}
                className="flex-1 px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent dark:bg-gray-700 dark:text-white disabled:opacity-50"
              />
              <button
                type="submit"
                disabled={!inputMessage.trim() || isTyping}
                className="px-4 py-2 bg-blue-600 hover:bg-blue-700 disabled:bg-gray-400 dark:bg-blue-500 dark:hover:bg-blue-600 text-white rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 disabled:cursor-not-allowed transition-colors duration-200"
              >
                <Send className="w-5 h-5" />
              </button>
            </form>
          </div>
        </div>

        {/* Sidebar Panels */}
        <div className="w-96 bg-white dark:bg-gray-800 border-l border-gray-200 dark:border-gray-700 overflow-y-auto custom-scrollbar">
          {/* Memory Search */}
          <MemorySearch
            onSearch={handleMemorySearch}
            recentSearches={[]} // Removed searchHistory as it's no longer used
            isOpen={isSearchOpen}
            onToggle={() => setIsSearchOpen(!isSearchOpen)}
          />

          {/* Memory Analytics */}
          <MemoryAnalytics
            stats={memoryStats}
            isOpen={isAnalyticsOpen}
            onToggle={() => setIsAnalyticsOpen(!isAnalyticsOpen)}
            isLoading={isLoadingMemoryStats}
            error={memoryStatsError}
            onRefresh={fetchMemoryStats} // Pass the fetch function to the component
          />

          {/* Memory Panel */}
          <MemoryPanel
            memoryData={memoryData}
            isOpen={isMemoryPanelOpen}
            onToggle={() => setIsMemoryPanelOpen(!isMemoryPanelOpen)}
            isLoading={isLoadingMemory}
          />

          {/* Chat History */}
          <ChatHistory
            user_id={user.user_id}
            isOpen={isChatHistoryOpen}
            onToggle={() => setIsChatHistoryOpen(!isChatHistoryOpen)}
          />
        </div>
      </div>
    </div>
  );
};

export default Chat; 