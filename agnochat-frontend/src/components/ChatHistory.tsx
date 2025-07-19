import React, { useState, useEffect } from 'react';
import { MessageSquare, Filter, Send } from 'lucide-react';
import { chatAPI } from '../services/api';

interface ChatHistoryItem {
  id: string;
  user_id: string;
  session_id: string;
  message: string;
  response: string;
  timestamp: string;
  message_type: string;
}

interface ChatHistoryResponse {
  user_id: string;
  total_messages: number;
  sessions: Record<string, ChatHistoryItem[]>;
  last_activity: string;
  history_summary: Record<string, number>;
}

interface ChatHistoryProps {
  user_id: string;
  isOpen: boolean;
  onToggle: () => void;
}

const ChatHistory: React.FC<ChatHistoryProps> = ({ user_id, isOpen, onToggle }) => {
  const [history, setHistory] = useState<ChatHistoryResponse | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [selectedSession, setSelectedSession] = useState<string | null>(null);
  const [limit, setLimit] = useState<number>(50);
  const [messages, setMessages] = useState<ChatHistoryItem[]>([]);
  const [inputMessage, setInputMessage] = useState('');
  const [isTyping, setIsTyping] = useState(false);

  const loadChatHistory = async () => {
    if (!user_id) return;
    
    setIsLoading(true);
    setError(null);
    
    try {
      const response = await chatAPI.getChatHistory(user_id, selectedSession || undefined, limit);
      setHistory(response.data);
      
      // Convert history to chat messages format
      const chatMessages: ChatHistoryItem[] = [];
      Object.entries(response.data.sessions).forEach(([sessionId, sessionMessages]) => {
        if (Array.isArray(sessionMessages)) {
          chatMessages.push(...sessionMessages);
        }
      });
      
      // Sort by timestamp (newest first)
      chatMessages.sort((a, b) => new Date(b.timestamp).getTime() - new Date(a.timestamp).getTime());
      setMessages(chatMessages);
      
      console.log('Chat history loaded:', response.data);
    } catch (err) {
      console.error('Failed to load chat history:', err);
      setError('Failed to load chat history');
    } finally {
      setIsLoading(false);
    }
  };

  const handleSendMessage = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!inputMessage.trim() || !selectedSession) return;

    setIsTyping(true);
    
    try {
      // Add user message to the chat
      const userMessage: ChatHistoryItem = {
        id: Date.now().toString(),
        user_id: user_id,
        session_id: selectedSession,
        message: inputMessage,
        response: '',
        timestamp: new Date().toISOString(),
        message_type: 'user'
      };
      
      setMessages(prev => [userMessage, ...prev]);
      setInputMessage('');
      
      // Simulate AI response (you can replace this with actual API call)
      setTimeout(() => {
        const assistantMessage: ChatHistoryItem = {
          id: (Date.now() + 1).toString(),
          user_id: user_id,
          session_id: selectedSession,
          message: '',
          response: `This is a simulated response to: "${inputMessage}"`,
          timestamp: new Date().toISOString(),
          message_type: 'assistant'
        };
        
        setMessages(prev => [assistantMessage, ...prev]);
        setIsTyping(false);
      }, 1000);
      
    } catch (error) {
      console.error('Failed to send message:', error);
      setIsTyping(false);
    }
  };

  useEffect(() => {
    if (isOpen && user_id) {
      loadChatHistory();
    }
  }, [isOpen, user_id, selectedSession, limit]);

  const formatTimestamp = (timestamp: string) => {
    return new Date(timestamp).toLocaleString();
  };

  const ChatBubble = ({ message, isUser, timestamp }: { message: string; isUser: boolean; timestamp: string }) => (
    <div className={`flex ${isUser ? 'justify-end' : 'justify-start'} mb-4`}>
      <div className={`max-w-xs lg:max-w-md px-4 py-2 rounded-lg ${
        isUser 
          ? 'bg-blue-500 text-white' 
          : 'bg-gray-200 dark:bg-gray-700 text-gray-900 dark:text-white'
      }`}>
        <p className="text-sm">{message}</p>
        <p className={`text-xs mt-1 ${isUser ? 'text-blue-100' : 'text-gray-500 dark:text-gray-400'}`}>
          {formatTimestamp(timestamp)}
        </p>
      </div>
    </div>
  );

  const TypingIndicator = () => (
    <div className="flex justify-start mb-4">
      <div className="bg-gray-200 dark:bg-gray-700 text-gray-900 dark:text-white px-4 py-2 rounded-lg">
        <div className="flex items-center space-x-1">
          <div className="w-2 h-2 bg-gray-500 rounded-full animate-bounce"></div>
          <div className="w-2 h-2 bg-gray-500 rounded-full animate-bounce" style={{ animationDelay: '0.1s' }}></div>
          <div className="w-2 h-2 bg-gray-500 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
        </div>
      </div>
    </div>
  );

  return (
    <div className="border-t border-gray-200 dark:border-gray-700">
      <button
        onClick={onToggle}
        className="w-full flex items-center justify-between p-3 bg-gray-50 dark:bg-gray-800 hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors"
      >
        <div className="flex items-center space-x-2">
          <MessageSquare className="w-4 h-4 text-blue-500" />
          <span className="font-medium text-gray-700 dark:text-gray-300">Chat History</span>
          {history && history.total_messages > 0 ? (
            <span className="text-xs bg-blue-100 text-blue-800 px-2 py-1 rounded-full">
              {history.total_messages} messages
            </span>
          ) : (
            <span className="text-xs bg-gray-100 text-gray-600 px-2 py-1 rounded-full">
              No conversations
            </span>
          )}
        </div>
      </button>
      
      {isOpen && (
        <div className="bg-white dark:bg-gray-900 border-t border-gray-200 dark:border-gray-700 max-h-[70vh] overflow-hidden flex flex-col">
          {/* Session Summary at Top */}
          {selectedSession && history && (
            <div className="p-4 border-b border-gray-200 dark:border-gray-700 bg-gray-50 dark:bg-gray-800">
              <div className="space-y-2">
                <div className="flex items-center justify-between">
                  <h3 className="text-lg font-semibold text-gray-900 dark:text-white">
                    {selectedSession}
                  </h3>
                  <span className="text-sm text-gray-600 dark:text-gray-400">
                    {history.history_summary[selectedSession] || 0} messages
                  </span>
                </div>
                <div className="text-sm text-gray-600 dark:text-gray-400">
                  Last: {formatTimestamp(history.sessions[selectedSession]?.[0]?.timestamp || '')}
                </div>
              </div>
            </div>
          )}

          {/* Main Content Area */}
          <div className="flex-1 flex flex-col overflow-hidden">
            {/* Top Section - Session Selection */}
            <div className="border-b border-gray-200 dark:border-gray-700">
              {/* Controls */}
              <div className="p-3 border-b border-gray-200 dark:border-gray-700">
                <div className="flex items-center space-x-2">
                  <div className="flex-1">
                    <select
                      value={selectedSession || ''}
                      onChange={(e) => setSelectedSession(e.target.value || null)}
                      className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent dark:bg-gray-700 dark:text-white text-sm"
                    >
                      <option value="">
                        {!history || Object.keys(history.sessions).length === 0 
                          ? "No conversations available" 
                          : "Select Session"
                        }
                      </option>
                      {history && Object.keys(history.sessions).map((sessionId) => (
                        <option key={sessionId} value={sessionId}>
                          {sessionId} ({history.history_summary[sessionId]} messages)
                        </option>
                      ))}
                    </select>
                  </div>
                  <div className="w-24">
                    <input
                      type="number"
                      value={limit}
                      onChange={(e) => setLimit(parseInt(e.target.value) || 50)}
                      min="1"
                      max="100"
                      className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent dark:bg-gray-700 dark:text-white text-sm"
                      placeholder="Limit"
                    />
                  </div>
                  <button
                    onClick={loadChatHistory}
                    disabled={isLoading}
                    className="px-3 py-2 bg-blue-500 hover:bg-blue-600 disabled:bg-gray-400 text-white rounded-lg transition-colors"
                  >
                    <Filter className="w-4 h-4" />
                  </button>
                </div>
              </div>

              {/* Session List */}
              <div className="p-3 max-h-32 overflow-y-auto">
                {!history || Object.keys(history.sessions).length === 0 ? (
                  <div className="text-center py-4 text-gray-500 dark:text-gray-400">
                    <p className="text-sm">No conversation sessions found</p>
                  </div>
                ) : (
                  <div className="flex space-x-2">
                    {Object.entries(history.sessions).map(([sessionId, sessionMessages]) => (
                      <div
                        key={sessionId}
                        onClick={() => setSelectedSession(sessionId)}
                        className={`p-3 rounded-lg cursor-pointer transition-colors border min-w-0 flex-shrink-0 ${
                          selectedSession === sessionId
                            ? 'bg-blue-100 dark:bg-blue-900/20 border-blue-200 dark:border-blue-800'
                            : 'bg-gray-50 dark:bg-gray-800 hover:bg-gray-100 dark:hover:bg-gray-700 border-gray-200 dark:border-gray-700'
                        }`}
                      >
                        <div className="text-center">
                          <h4 className="font-medium text-gray-900 dark:text-white text-sm truncate">
                            {sessionId}
                          </h4>
                          <span className="text-xs bg-gray-200 text-gray-700 px-2 py-1 rounded-full">
                            {sessionMessages.length}
                          </span>
                          <p className="text-xs text-gray-500 dark:text-gray-400 mt-1 truncate">
                            Last: {formatTimestamp(sessionMessages[0]?.timestamp || '')}
                          </p>
                        </div>
                      </div>
                    ))}
                  </div>
                )}
              </div>
            </div>

            {/* Bottom Section - Chat Interface */}
            <div className="flex-1 flex flex-col">
              {/* Chat Header */}
              <div className="p-3 border-b border-gray-200 dark:border-gray-700 bg-gray-50 dark:bg-gray-800">
                <div className="flex items-center justify-between">
                  <h3 className="font-medium text-gray-900 dark:text-white">
                    {selectedSession 
                      ? `Session: ${selectedSession}` 
                      : !history || history.total_messages === 0
                        ? 'No conversations available'
                        : 'Select a session to view chat'
                    }
                  </h3>
                  {history && selectedSession && (
                    <span className="text-sm text-gray-500 dark:text-gray-400">
                      {history.history_summary[selectedSession] || 0} messages
                    </span>
                  )}
                </div>
              </div>

              {/* Messages Area */}
              <div className="flex-1 overflow-y-auto p-4 space-y-4">
                {isLoading ? (
                  <div className="flex items-center justify-center py-8">
                    <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-500"></div>
                    <span className="ml-2 text-sm text-gray-500 dark:text-gray-400">Loading chat history...</span>
                  </div>
                ) : error ? (
                  <div className="p-4 bg-red-50 dark:bg-red-900/20 rounded-lg border border-red-200 dark:border-red-800">
                    <div className="flex items-center space-x-2 text-sm text-red-700 dark:text-red-300">
                      <span>❌ {error}</span>
                    </div>
                  </div>
                ) : !history || history.total_messages === 0 ? (
                  <div className="text-center py-12 text-gray-500 dark:text-gray-400">
                    <MessageSquare className="w-16 h-16 mx-auto mb-4 opacity-50" />
                    <h3 className="text-lg font-medium text-gray-700 dark:text-gray-300 mb-2">
                      No Conversations Found
                    </h3>
                    <p className="text-sm max-w-md mx-auto">
                      You haven't had any conversations yet. Start chatting to see your message history here.
                    </p>
                  </div>
                ) : selectedSession ? (
                  <>
                    {messages.length === 0 ? (
                      <div className="text-center py-8 text-gray-500 dark:text-gray-400">
                        <MessageSquare className="w-12 h-12 mx-auto mb-2 opacity-50" />
                        <p>No messages in this session</p>
                      </div>
                    ) : (
                      messages.map((item) => (
                        <ChatBubble
                          key={item.id}
                          message={item.message_type === 'user' ? item.message : item.response}
                          isUser={item.message_type === 'user'}
                          timestamp={item.timestamp}
                        />
                      ))
                    )}
                    {isTyping && <TypingIndicator />}
                  </>
                ) : (
                  <div className="text-center py-8 text-gray-500 dark:text-gray-400">
                    <MessageSquare className="w-12 h-12 mx-auto mb-2 opacity-50" />
                    <p>Select a session from above to view chat history</p>
                  </div>
                )}
              </div>

              {/* Input Area */}
              {selectedSession && (
                <div className="p-4 border-t border-gray-200 dark:border-gray-700">
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
              )}
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default ChatHistory; 