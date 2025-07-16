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

  const formatDate = (timestamp) => {
    const date = new Date(timestamp);
    const today = new Date();
    const yesterday = new Date(today);
    yesterday.setDate(yesterday.getDate() - 1);

    if (date.toDateString() === today.toDateString()) {
      return 'Today';
    } else if (date.toDateString() === yesterday.toDateString()) {
      return 'Yesterday';
    } else {
      return date.toLocaleDateString([], { 
        weekday: 'long', 
        year: 'numeric', 
        month: 'long', 
        day: 'numeric' 
      });
    }
  };

  const groupMessagesByDate = (messages) => {
    const groups = [];
    let currentDate = null;
    let currentGroup = [];

    messages.forEach((message, index) => {
      const messageDate = formatDate(message.timestamp);
      
      if (messageDate !== currentDate) {
        if (currentGroup.length > 0) {
          groups.push({
            date: currentDate,
            messages: currentGroup
          });
        }
        currentDate = messageDate;
        currentGroup = [message];
      } else {
        currentGroup.push(message);
      }
    });

    if (currentGroup.length > 0) {
      groups.push({
        date: currentDate,
        messages: currentGroup
      });
    }

    return groups;
  };

  const messageGroups = groupMessagesByDate(messages);

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
            <span className="toggle-label">Agno Framework</span>
          </label>
        </div>
      </div>
      
      <div className="messages-container">
        {messages.length === 0 ? (
          <div className="empty-chat">
            <div className="empty-chat-icon">🤖</div>
            <h3>Welcome to AgnoChat</h3>
            <p>
              Your intelligent AI assistant powered by advanced reasoning and memory systems. 
              Start a conversation to experience the future of AI chat.
            </p>
            <div className="features">
              <div className="feature-item">
                <span>🧠</span>
                <span>Advanced Reasoning</span>
              </div>
              <div className="feature-item">
                <span>💾</span>
                <span>Memory System</span>
              </div>
              <div className="feature-item">
                <span>🎨</span>
                <span>Theme Support</span>
              </div>
              <div className="feature-item">
                <span>📱</span>
                <span>Responsive</span>
              </div>
            </div>
          </div>
        ) : (
          <div className="messages-list">
            {messageGroups.map((group, groupIndex) => (
              <div key={groupIndex}>
                <div className="date-separator">
                  <span>{group.date}</span>
                </div>
                {group.messages.map((message, index) => (
                  <Message
                    key={`${groupIndex}-${index}`}
                    message={message}
                    timestamp={formatTime(message.timestamp)}
                  />
                ))}
              </div>
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