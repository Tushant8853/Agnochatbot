import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { ChevronDown, ChevronUp, Brain, Search, Plus } from 'lucide-react';
import { useChat } from '../../contexts/ChatContext';
import { apiService } from '../../services/api';
import toast from 'react-hot-toast';

const MemoryPanel: React.FC = () => {
  const { memoryContext, memorySummary } = useChat();
  const [isExpanded, setIsExpanded] = useState(false);
  const [searchQuery, setSearchQuery] = useState('');
  const [searchResults, setSearchResults] = useState<any[]>([]);
  const [isSearching, setIsSearching] = useState(false);
  const [newFact, setNewFact] = useState('');

  const handleSearch = async () => {
    if (!searchQuery.trim()) return;

    setIsSearching(true);
    try {
      const results = await apiService.searchMemory({
        query: searchQuery,
        search_type: 'hybrid'
      });
      setSearchResults(results.results || []);
    } catch (error) {
      toast.error('Failed to search memory');
    } finally {
      setIsSearching(false);
    }
  };

  const handleAddFact = async () => {
    if (!newFact.trim()) return;

    try {
      await apiService.addCustomFact(newFact);
      toast.success('Fact added to memory');
      setNewFact('');
    } catch (error) {
      toast.error('Failed to add fact');
    }
  };

  return (
    <div className="card">
      <div className="p-4">
        <button
          onClick={() => setIsExpanded(!isExpanded)}
          className="flex items-center justify-between w-full text-left"
        >
          <div className="flex items-center space-x-2">
            <Brain className="w-5 h-5 text-primary-600" />
            <span className="font-semibold text-gray-900 dark:text-white">Memory Context</span>
            {memorySummary && (
              <span className="text-xs bg-primary-100 text-primary-800 px-2 py-1 rounded-full">
                {memorySummary.zep_facts_count + memorySummary.mem0_memories_count} items
              </span>
            )}
          </div>
          {isExpanded ? <ChevronUp className="w-5 h-5" /> : <ChevronDown className="w-5 h-5" />}
        </button>

        <AnimatePresence>
          {isExpanded && (
            <motion.div
              initial={{ height: 0, opacity: 0 }}
              animate={{ height: 'auto', opacity: 1 }}
              exit={{ height: 0, opacity: 0 }}
              transition={{ duration: 0.3 }}
              className="mt-4 space-y-4"
            >
              {/* Memory Summary */}
              {memorySummary && (
                <div className="bg-gray-50 dark:bg-dark-700 rounded-lg p-3">
                  <h4 className="font-medium text-gray-900 dark:text-white mb-2">Memory Summary</h4>
                  <div className="grid grid-cols-2 gap-4 text-sm">
                    <div>
                      <span className="text-gray-600 dark:text-gray-400">Zep Facts:</span>
                      <span className="ml-2 font-medium">{memorySummary.zep_facts_count}</span>
                    </div>
                    <div>
                      <span className="text-gray-600 dark:text-gray-400">Mem0 Memories:</span>
                      <span className="ml-2 font-medium">{memorySummary.mem0_memories_count}</span>
                    </div>
                  </div>
                  {memorySummary.key_facts && memorySummary.key_facts.length > 0 && (
                    <div className="mt-3">
                      <span className="text-gray-600 dark:text-gray-400 text-sm">Key Facts:</span>
                      <ul className="mt-1 space-y-1">
                        {memorySummary.key_facts.slice(0, 3).map((fact: string, index: number) => (
                          <li key={index} className="text-sm text-gray-700 dark:text-gray-300">
                            • {fact}
                          </li>
                        ))}
                      </ul>
                    </div>
                  )}
                </div>
              )}

              {/* Active Memory Context */}
              {memoryContext && (
                <div className="bg-blue-50 dark:bg-blue-900/20 rounded-lg p-3">
                  <h4 className="font-medium text-gray-900 dark:text-white mb-2">Active Context</h4>
                  <div className="text-sm text-gray-700 dark:text-gray-300">
                    {memoryContext.agno_memories && memoryContext.agno_memories.length > 0 ? (
                      <div className="space-y-2">
                        {memoryContext.agno_memories.slice(0, 3).map((memory: any, index: number) => (
                          <div key={index} className="bg-white dark:bg-dark-800 rounded p-2">
                            <div className="font-medium text-xs text-gray-500 dark:text-gray-400">
                              Memory {index + 1}
                            </div>
                            <div className="text-sm">{memory.content || memory.text}</div>
                          </div>
                        ))}
                      </div>
                    ) : (
                      <p className="text-gray-500 dark:text-gray-400">No active memories</p>
                    )}
                  </div>
                </div>
              )}

              {/* Memory Search */}
              <div className="space-y-3">
                <h4 className="font-medium text-gray-900 dark:text-white">Search Memory</h4>
                <div className="flex space-x-2">
                  <input
                    type="text"
                    value={searchQuery}
                    onChange={(e) => setSearchQuery(e.target.value)}
                    placeholder="Search memories..."
                    className="input-field flex-1"
                  />
                  <button
                    onClick={handleSearch}
                    disabled={isSearching || !searchQuery.trim()}
                    className="btn-secondary px-3"
                  >
                    {isSearching ? (
                      <div className="w-4 h-4 border-2 border-gray-600 border-t-transparent rounded-full animate-spin"></div>
                    ) : (
                      <Search className="w-4 h-4" />
                    )}
                  </button>
                </div>

                {/* Search Results */}
                {searchResults.length > 0 && (
                  <div className="bg-gray-50 dark:bg-dark-700 rounded-lg p-3">
                    <h5 className="font-medium text-sm mb-2">Search Results</h5>
                    <div className="space-y-2 max-h-40 overflow-y-auto">
                      {searchResults.map((result, index) => (
                        <div key={index} className="bg-white dark:bg-dark-800 rounded p-2 text-sm">
                          <div className="font-medium text-xs text-gray-500 dark:text-gray-400">
                            Score: {result.score?.toFixed(2)}
                          </div>
                          <div>{result.content || result.text}</div>
                        </div>
                      ))}
                    </div>
                  </div>
                )}
              </div>

              {/* Add Custom Fact */}
              <div className="space-y-3">
                <h4 className="font-medium text-gray-900 dark:text-white">Add Custom Fact</h4>
                <div className="flex space-x-2">
                  <input
                    type="text"
                    value={newFact}
                    onChange={(e) => setNewFact(e.target.value)}
                    placeholder="Enter a fact to remember..."
                    className="input-field flex-1"
                  />
                  <button
                    onClick={handleAddFact}
                    disabled={!newFact.trim()}
                    className="btn-secondary px-3"
                  >
                    <Plus className="w-4 h-4" />
                  </button>
                </div>
              </div>
            </motion.div>
          )}
        </AnimatePresence>
      </div>
    </div>
  );
};

export default MemoryPanel; 