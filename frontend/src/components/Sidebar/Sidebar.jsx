import React from 'react';
import './Sidebar.css';

const Sidebar = ({ sessions, currentSession, onSessionSelect, onNewChat }) => {
  const formatDate = (dateString) => {
    const date = new Date(dateString);
    const now = new Date();
    const diffTime = Math.abs(now - date);
    const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
    
    if (diffDays === 1) {
      return 'Today';
    } else if (diffDays === 2) {
      return 'Yesterday';
    } else if (diffDays <= 7) {
      return `${diffDays - 1} days ago`;
    } else {
      return date.toLocaleDateString();
    }
  };

  const truncateTitle = (title, maxLength = 30) => {
    if (title.length <= maxLength) return title;
    return title.substring(0, maxLength) + '...';
  };

  return (
    <div className="sidebar">
      <div className="sidebar-header">
        <h3>Chat Sessions</h3>
        <button 
          className="new-chat-button"
          onClick={onNewChat}
          title="Start New Chat"
        >
          <span className="new-chat-icon">+</span>
          <span className="new-chat-text">New Chat</span>
        </button>
      </div>
      
      <div className="sessions-list">
        {sessions.length === 0 ? (
          <div className="empty-sessions">
            <p>No chat sessions yet</p>
            <p>Start a new conversation!</p>
          </div>
        ) : (
          sessions.map((session) => (
            <div
              key={session.session_id}
              className={`session-item ${currentSession?.session_id === session.session_id ? 'active' : ''}`}
              onClick={() => onSessionSelect(session)}
            >
              <div className="session-content">
                <div className="session-title">
                  {truncateTitle(session.title)}
                </div>
                <div className="session-date">
                  {formatDate(session.created_at)}
                </div>
              </div>
              {currentSession?.session_id === session.session_id && (
                <div className="session-indicator">●</div>
              )}
            </div>
          ))
        )}
      </div>
    </div>
  );
};

export default Sidebar; 