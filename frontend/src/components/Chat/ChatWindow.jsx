import React, { useState, useEffect, useRef } from 'react';
import ChatInput from './ChatInput';
import Message from './Message';
import './ChatWindow.css';

const ChatWindow = ({ messages, onSendMessage, loading, currentSession }) => {
  const messagesEndRef = useRef(null);
  const [useAgno, setUseAgno] = useState(true);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSendMessage = (message) => {
    onSendMessage(message, useAgno);
  };

  const formatTime = (timestamp) => {
    const date = new Date(timestamp);
    return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  };

  return (
    <div className="chat-window">
      <div className="chat-header">
        <div className="chat-title">
          {currentSession ? currentSession.title : 'New Chat'}
        </div>
        <div className="chat-controls">
          <label className="agno-toggle">
            <input
              type="checkbox"
              checked={useAgno}
              onChange={(e) => setUseAgno(e.target.checked)}
            />
            <span className="toggle-label">Use Agno Framework</span>
          </label>
        </div>
      </div>
      
      <div className="messages-container">
        {messages.length === 0 ? (
          <div className="empty-chat">
            <div className="empty-chat-icon">💬</div>
            <h3>Start a conversation</h3>
            <p>Send a message to begin chatting with your AI assistant</p>
          </div>
        ) : (
          <div className="messages-list">
            {messages.map((message, index) => (
              <Message
                key={index}
                message={message}
                timestamp={formatTime(message.timestamp)}
              />
            ))}
            {loading && (
              <div className="loading-message">
                <div className="typing-indicator">
                  <span></span>
                  <span></span>
                  <span></span>
                </div>
                <span className="loading-text">AI is thinking...</span>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>
        )}
      </div>
      
      <ChatInput onSendMessage={handleSendMessage} loading={loading} />
    </div>
  );
};

export default ChatWindow; 