import React from 'react';
import './MemoryFacts.css';

const MemoryFacts = ({ summary, agnoMemories }) => {
  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString();
  };

  return (
    <div className="memory-facts">
      {summary && (
        <div className="memory-summary">
          <h4>Memory Summary</h4>
          <div className="summary-stats">
            <div className="stat-item">
              <span className="stat-label">Zep Facts:</span>
              <span className="stat-value">{summary.zep_facts_count || 0}</span>
            </div>
            <div className="stat-item">
              <span className="stat-label">Mem0 Memories:</span>
              <span className="stat-value">{summary.mem0_memories_count || 0}</span>
            </div>
          </div>
          
          {summary.key_facts && summary.key_facts.length > 0 && (
            <div className="key-facts">
              <h5>Key Facts</h5>
              <ul className="facts-list">
                {summary.key_facts.map((fact, index) => (
                  <li key={index} className="fact-item">
                    {fact}
                  </li>
                ))}
              </ul>
            </div>
          )}
        </div>
      )}

      <div className="agno-memories">
        <h4>Agno Memories</h4>
        {agnoMemories && agnoMemories.length > 0 ? (
          <div className="memories-list">
            {agnoMemories.map((memory, index) => (
              <div key={index} className="memory-item">
                <div className="memory-content">
                  {memory.content || memory.text || 'Memory content'}
                </div>
                <div className="memory-meta">
                  <span className="memory-type">
                    {memory.memory_type || memory.type || 'fact'}
                  </span>
                  {memory.created_at && (
                    <span className="memory-date">
                      {formatDate(memory.created_at)}
                    </span>
                  )}
                </div>
              </div>
            ))}
          </div>
        ) : (
          <div className="empty-memories">
            <p>No Agno memories yet</p>
            <p>Add some memories to get started!</p>
          </div>
        )}
      </div>
    </div>
  );
};

export default MemoryFacts; 