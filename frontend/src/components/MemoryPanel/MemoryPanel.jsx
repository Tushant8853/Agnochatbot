import React, { useState } from 'react';
import MemorySearch from './MemorySearch';
import MemoryFacts from './MemoryFacts';
import AddMemory from './AddMemory';
import MemoryDebug from './MemoryDebug';
import './MemoryPanel.css';

const MemoryPanel = ({ memoryData, onSearch, onAddMemory, currentUser, currentSession }) => {
  const [activeTab, setActiveTab] = useState('facts');

  const tabs = [
    { id: 'facts', label: 'Facts', icon: '📋' },
    { id: 'search', label: 'Search', icon: '🔍' },
    { id: 'add', label: 'Add', icon: '➕' },
    { id: 'debug', label: 'Debug', icon: '🐛' }
  ];

  return (
    <div className="memory-panel">
      <div className="memory-header">
        <h3>Memory System</h3>
        <div className="memory-tabs">
          {tabs.map((tab) => (
            <button
              key={tab.id}
              className={`memory-tab ${activeTab === tab.id ? 'active' : ''}`}
              onClick={() => setActiveTab(tab.id)}
              title={tab.label}
            >
              <span className="tab-icon">{tab.icon}</span>
              <span className="tab-label">{tab.label}</span>
            </button>
          ))}
        </div>
      </div>

      <div className="memory-content">
        {activeTab === 'facts' && (
          <MemoryFacts 
            summary={memoryData.summary}
            agnoMemories={memoryData.agnoMemories}
          />
        )}
        
        {activeTab === 'search' && (
          <MemorySearch 
            onSearch={onSearch}
            searchResults={memoryData.searchResults}
          />
        )}
        
        {activeTab === 'add' && (
          <AddMemory onAddMemory={onAddMemory} />
        )}
        
        {activeTab === 'debug' && (
          <MemoryDebug 
            currentUser={currentUser}
            currentSession={currentSession}
            memoryData={memoryData}
          />
        )}
      </div>
    </div>
  );
};

export default MemoryPanel; 