import React from 'react';
import './MemoryDebug.css';

const MemoryDebug = ({ currentUser, currentSession, memoryData }) => {
  const formatDate = (dateString) => {
    if (!dateString) return 'N/A';
    return new Date(dateString).toLocaleString();
  };

  return (
    <div className="memory-debug">
      <h4>Debug Information</h4>
      <p className="debug-description">
        Technical information about your memory system and current session.
      </p>

      <div className="debug-sections">
        <div className="debug-section">
          <h5>User Information</h5>
          <div className="debug-item">
            <span className="debug-label">User ID:</span>
            <span className="debug-value">{currentUser?.id || 'N/A'}</span>
          </div>
          <div className="debug-item">
            <span className="debug-label">Username:</span>
            <span className="debug-value">{currentUser?.username || 'N/A'}</span>
          </div>
        </div>

        <div className="debug-section">
          <h5>Session Information</h5>
          <div className="debug-item">
            <span className="debug-label">Session ID:</span>
            <span className="debug-value">{currentSession?.session_id || 'N/A'}</span>
          </div>
          <div className="debug-item">
            <span className="debug-label">Session Title:</span>
            <span className="debug-value">{currentSession?.title || 'N/A'}</span>
          </div>
          <div className="debug-item">
            <span className="debug-label">Created:</span>
            <span className="debug-value">{formatDate(currentSession?.created_at)}</span>
          </div>
          <div className="debug-item">
            <span className="debug-label">Status:</span>
            <span className="debug-value">{currentSession?.is_active || 'N/A'}</span>
          </div>
        </div>

        <div className="debug-section">
          <h5>Memory Statistics</h5>
          <div className="debug-item">
            <span className="debug-label">Zep Facts:</span>
            <span className="debug-value">{memoryData.summary?.zep_facts_count || 0}</span>
          </div>
          <div className="debug-item">
            <span className="debug-label">Mem0 Memories:</span>
            <span className="debug-value">{memoryData.summary?.mem0_memories_count || 0}</span>
          </div>
          <div className="debug-item">
            <span className="debug-label">Agno Memories:</span>
            <span className="debug-value">{memoryData.agnoMemories?.length || 0}</span>
          </div>
          <div className="debug-item">
            <span className="debug-label">Search Results:</span>
            <span className="debug-value">
              {memoryData.searchResults && Object.keys(memoryData.searchResults).length > 0 
                ? 'Available' 
                : 'None'
              }
            </span>
          </div>
        </div>

        <div className="debug-section">
          <h5>System Status</h5>
          <div className="debug-item">
            <span className="debug-label">Memory Panel:</span>
            <span className="debug-value status-active">Active</span>
          </div>
          <div className="debug-item">
            <span className="debug-label">API Connection:</span>
            <span className="debug-value status-active">Connected</span>
          </div>
          <div className="debug-item">
            <span className="debug-label">Last Updated:</span>
            <span className="debug-value">{formatDate(new Date().toISOString())}</span>
          </div>
        </div>
      </div>

      <div className="debug-actions">
        <button className="debug-button" onClick={() => window.location.reload()}>
          Refresh Data
        </button>
        <button className="debug-button" onClick={() => console.log('Memory Data:', memoryData)}>
          Log to Console
        </button>
      </div>
    </div>
  );
};

export default MemoryDebug; 