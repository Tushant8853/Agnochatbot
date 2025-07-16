import React from 'react';
import './Message.css';

const Message = ({ message, timestamp }) => {
  const isUser = message.role === 'user';

  return (
    <div className={`message ${isUser ? 'user-message' : 'ai-message'}`}>
      <div className="message-content">
        <div className="message-text">
          {message.content}
        </div>
        <div className="message-timestamp">
          {timestamp}
        </div>
      </div>
      <div className="message-avatar">
        {isUser ? '👤' : '🤖'}
      </div>
    </div>
  );
};

export default Message; 