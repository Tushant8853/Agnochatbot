import React from 'react';
import './Message.css';

const Message = ({ message, timestamp }) => {
  const isUser = message.role === 'user';

  return (
    <div className={`message ${isUser ? 'user' : 'assistant'}`}>
      <div className="message-avatar">
        {isUser ? (
          <div className="avatar user-avatar">
            <span>👤</span>
          </div>
        ) : (
          <div className="avatar assistant-avatar">
            <span>🤖</span>
          </div>
        )}
      </div>
      
      <div className="message-content">
        <div className="message-header">
          <span className="message-author">
            {isUser ? 'You' : 'AgnoChat AI'}
          </span>
          <span className="message-time">{timestamp}</span>
        </div>
        
        <div className="message-bubble">
          <div className="message-text">
            {message.content}
          </div>
        </div>
        
        {!isUser && (
          <div className="message-actions">
            <button className="action-btn" title="Copy message">
              📋
            </button>
            <button className="action-btn" title="Like message">
              👍
            </button>
            <button className="action-btn" title="Dislike message">
              👎
            </button>
          </div>
        )}
      </div>
    </div>
  );
};

export default Message; 