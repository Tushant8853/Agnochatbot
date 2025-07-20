import React, { useState } from 'react';
import { Search, Clock, Brain, Sparkles } from 'lucide-react';

interface SearchResult {
  id: string;
  query: string;
  results: string;
  timestamp: string;
  relevance?: number; // Made optional since we removed hardcoded relevance
}

interface MemorySearchProps {
  onSearch: (query: string) => Promise<SearchResult>;
  recentSearches: SearchResult[];
  isOpen: boolean;
  onToggle: () => void;
  onClearHistory?: () => void;
}

const MemorySearch: React.FC<MemorySearchProps> = ({
  onSearch,
  recentSearches,
  isOpen,
  onToggle,
  onClearHistory
}) => {
  const [searchQuery, setSearchQuery] = useState('');
  const [isSearching, setIsSearching] = useState(false);
  const [searchResults, setSearchResults] = useState<SearchResult | null>(null);
  const [searchHistory, setSearchHistory] = useState<SearchResult[]>(recentSearches);

  const handleSearch = async () => {
    if (!searchQuery.trim()) return;

    setIsSearching(true);
    try {
      const result = await onSearch(searchQuery);
      setSearchResults(result);
      setSearchHistory(prev => [result, ...prev.slice(0, 9)]); // Keep last 10 searches
    } catch (error) {
      console.error('Search failed:', error);
      // Show error message to user
      setSearchResults({
        id: Date.now().toString(),
        query: searchQuery,
        results: `Search failed: ${error instanceof Error ? error.message : 'Unknown error'}`,
        timestamp: new Date().toISOString()
        // Removed hardcoded relevance score
      });
    } finally {
      setIsSearching(false);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter') {
      handleSearch();
    }
  };

  const quickSearches = [
    'My personal information',
    'Recent conversations',
    'Important facts',
    'Preferences',
    'Goals and plans'
  ];

  return (
    <div className="border-t border-gray-200 dark:border-gray-700">
      <button
        onClick={onToggle}
        className="w-full flex items-center justify-between p-3 bg-gray-50 dark:bg-gray-800 hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors"
      >
        <div className="flex items-center space-x-2">
          <Search className="w-4 h-4 text-purple-500" />
          <span className="font-medium text-gray-700 dark:text-gray-300">Memory Search</span>
          <span className="text-xs bg-purple-100 text-purple-800 px-2 py-1 rounded-full">
            {searchHistory.length} searches
          </span>
        </div>
      </button>
      
      {isOpen && (
        <div className="p-4 bg-white dark:bg-gray-900 border-t border-gray-200 dark:border-gray-700">
          {/* Search Input */}
          <div className="flex space-x-2 mb-4">
            <div className="flex-1 relative">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-gray-400" />
              <input
                type="text"
                placeholder="Search your memory..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                onKeyPress={handleKeyPress}
                className="w-full pl-10 pr-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent dark:bg-gray-700 dark:text-white text-sm"
              />
            </div>
            <button
              onClick={handleSearch}
              disabled={isSearching || !searchQuery.trim()}
              className="px-4 py-2 bg-purple-500 hover:bg-purple-600 disabled:bg-gray-400 text-white rounded-lg transition-colors flex items-center space-x-1"
            >
              {isSearching ? (
                <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
              ) : (
                <Search className="w-4 h-4" />
              )}
            </button>
          </div>

          {/* Quick Searches */}
          <div className="mb-4">
            <h4 className="text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Quick Searches</h4>
            <div className="flex flex-wrap gap-2">
              {quickSearches.map((quickSearch) => (
                <button
                  key={quickSearch}
                  onClick={() => {
                    setSearchQuery(quickSearch);
                    setTimeout(() => handleSearch(), 100);
                  }}
                  className="px-3 py-1 bg-gray-100 dark:bg-gray-800 text-gray-700 dark:text-gray-300 rounded-full text-xs hover:bg-gray-200 dark:hover:bg-gray-700 transition-colors"
                >
                  {quickSearch}
                </button>
              ))}
            </div>
          </div>

          {/* Search Results */}
          {searchResults && (
            <div className="mb-4 p-4 bg-purple-50 dark:bg-purple-900/20 rounded-lg border border-purple-200 dark:border-purple-800">
              <div className="flex items-center space-x-2 mb-2">
                <Brain className="w-4 h-4 text-purple-500" />
                <h4 className="font-medium text-purple-800 dark:text-purple-200">Search Results</h4>
                <span className="text-xs bg-purple-100 text-purple-800 px-2 py-1 rounded-full">
                  {searchResults.relevance !== undefined ? `${Math.round(searchResults.relevance * 100)}% relevant` : 'Relevance unknown'}
                </span>
              </div>
              <p className="text-sm text-purple-700 dark:text-purple-300 mb-2">
                Query: "{searchResults.query}"
              </p>
              <div className="text-sm text-purple-700 dark:text-purple-300 bg-white dark:bg-gray-800 p-3 rounded border">
                {searchResults.results}
              </div>
              <div className="flex items-center space-x-2 mt-2 text-xs text-purple-600 dark:text-purple-400">
                <Clock className="w-3 h-3" />
                <span>{new Date(searchResults.timestamp).toLocaleString()}</span>
              </div>
            </div>
          )}

          {/* Search History */}
          {searchHistory.length > 0 && (
            <div>
              <div className="flex items-center justify-between mb-2">
                <h4 className="text-sm font-medium text-gray-700 dark:text-gray-300">Recent Searches</h4>
                {onClearHistory && (
                  <button
                    onClick={onClearHistory}
                    className="text-xs text-red-600 dark:text-red-400 hover:text-red-800 dark:hover:text-red-300"
                  >
                    Clear All
                  </button>
                )}
              </div>
              <div className="space-y-2 max-h-48 overflow-y-auto">
                {searchHistory.map((search, index) => (
                  <div
                    key={index}
                    className="p-3 bg-gray-50 dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700 cursor-pointer hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors"
                    onClick={() => {
                      setSearchQuery(search.query);
                      setTimeout(() => handleSearch(), 100);
                    }}
                  >
                    <div className="flex items-center justify-between mb-1">
                      <h5 className="font-medium text-gray-900 dark:text-white text-sm">
                        {search.query}
                      </h5>
                      <span className="text-xs bg-blue-100 text-blue-800 px-2 py-1 rounded-full">
                        {search.relevance !== undefined ? `${Math.round(search.relevance * 100)}%` : 'Relevance unknown'}
                      </span>
                    </div>
                    <p className="text-xs text-gray-600 dark:text-gray-400 line-clamp-2">
                      {search.results.substring(0, 100)}...
                    </p>
                    <div className="flex items-center space-x-2 mt-2 text-xs text-gray-500 dark:text-gray-400">
                      <Clock className="w-3 h-3" />
                      <span>{new Date(search.timestamp).toLocaleString()}</span>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Search Tips */}
          <div className="mt-4 p-3 bg-blue-50 dark:bg-blue-900/20 rounded-lg">
            <div className="flex items-center space-x-2 text-sm text-blue-700 dark:text-blue-300">
              <Sparkles className="w-4 h-4" />
              <span>Tip: Use specific keywords for better search results</span>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default MemorySearch; 