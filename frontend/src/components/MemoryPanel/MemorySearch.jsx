import React, { useState } from 'react';
import './MemorySearch.css';

const MemorySearch = ({ onSearch, searchResults }) => {
  const [query, setQuery] = useState('');
  const [searchType, setSearchType] = useState('hybrid');

  const handleSearch = (e) => {
    e.preventDefault();
    if (query.trim()) {
      onSearch(query.trim(), searchType);
    }
  };

  const renderSearchResults = () => {
    if (!searchResults || Object.keys(searchResults).length === 0) {
      return null;
    }

    return (
      <div className="search-results">
        <h4>Search Results</h4>
        
        {searchResults.zep_results && searchResults.zep_results.length > 0 && (
          <div className="result-section">
            <h5>Zep Results</h5>
            {searchResults.zep_results.map((result, index) => (
              <div key={index} className="result-item">
                <div className="result-content">{result.fact || result.content}</div>
                <div className="result-score">Score: {result.score?.toFixed(2) || 'N/A'}</div>
              </div>
            ))}
          </div>
        )}

        {searchResults.mem0_results && searchResults.mem0_results.length > 0 && (
          <div className="result-section">
            <h5>Mem0 Results</h5>
            {searchResults.mem0_results.map((result, index) => (
              <div key={index} className="result-item">
                <div className="result-content">{result.content || result.text}</div>
                <div className="result-score">Score: {result.score?.toFixed(2) || 'N/A'}</div>
              </div>
            ))}
          </div>
        )}

        {searchResults.combined_results && searchResults.combined_results.length > 0 && (
          <div className="result-section">
            <h5>Combined Results</h5>
            {searchResults.combined_results.map((result, index) => (
              <div key={index} className="result-item">
                <div className="result-content">{result.content || result.fact || result.text}</div>
                <div className="result-meta">
                  <span className="result-source">{result.source || 'Unknown'}</span>
                  <span className="result-score">Score: {result.score?.toFixed(2) || 'N/A'}</span>
                </div>
              </div>
            ))}
          </div>
        )}

        {(!searchResults.zep_results || searchResults.zep_results.length === 0) &&
         (!searchResults.mem0_results || searchResults.mem0_results.length === 0) &&
         (!searchResults.combined_results || searchResults.combined_results.length === 0) && (
          <div className="no-results">
            <p>No results found for "{query}"</p>
          </div>
        )}
      </div>
    );
  };

  return (
    <div className="memory-search">
      <form onSubmit={handleSearch} className="search-form">
        <div className="search-input-group">
          <input
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Search your memories..."
            className="search-input"
          />
          <select
            value={searchType}
            onChange={(e) => setSearchType(e.target.value)}
            className="search-type-select"
          >
            <option value="hybrid">Hybrid</option>
            <option value="temporal">Temporal</option>
            <option value="factual">Factual</option>
          </select>
        </div>
        <button type="submit" className="search-button" disabled={!query.trim()}>
          Search
        </button>
      </form>

      {renderSearchResults()}
    </div>
  );
};

export default MemorySearch; 