import React, { useState } from 'react';
import { ChevronDown, ChevronRight, Brain, Database, Network, Info } from 'lucide-react';

interface MemoryData {
  zep_memory: any;
  mem0_memory: any;
  consolidated_memory: string;
}

interface MemoryPanelProps {
  memoryData: MemoryData | null;
  isOpen: boolean;
  onToggle: () => void;
  isLoading?: boolean;
}

const MemoryPanel: React.FC<MemoryPanelProps> = ({ memoryData, isOpen, onToggle, isLoading = false }) => {
  const [activeTab, setActiveTab] = useState<'zep' | 'mem0' | 'consolidated'>('consolidated');

  if (!memoryData) return null;

  const tabs = [
    { id: 'consolidated', label: 'Consolidated', icon: Brain },
    { id: 'zep', label: 'Zep Memory', icon: Network },
    { id: 'mem0', label: 'Mem0 Memory', icon: Database },
  ] as const;

  const renderMemoryContent = () => {
    switch (activeTab) {
      case 'consolidated':
        return (
          <div className="space-y-3">
            <div className="bg-blue-50 dark:bg-blue-900/20 p-3 rounded-lg">
              <h4 className="font-medium text-blue-800 dark:text-blue-200 mb-2">Active Memory Context</h4>
              <p className="text-sm text-blue-700 dark:text-blue-300 break-words overflow-wrap-anywhere">
                {memoryData.consolidated_memory || 'No consolidated memory available'}
              </p>
            </div>
          </div>
        );
      
      case 'zep':
        return (
          <div className="space-y-3">
            <div className="bg-green-50 dark:bg-green-900/20 p-3 rounded-lg">
              <h4 className="font-medium text-green-800 dark:text-green-200 mb-2">Temporal Knowledge Graph</h4>
              <div className="max-h-48 overflow-y-auto">
                <pre className="text-xs text-green-700 dark:text-green-300 whitespace-pre-wrap break-words">
                  {JSON.stringify(memoryData.zep_memory, null, 2)}
                </pre>
              </div>
            </div>
          </div>
        );
      
      case 'mem0':
        return (
          <div className="space-y-3">
            <div className="bg-purple-50 dark:bg-purple-900/20 p-3 rounded-lg">
              <h4 className="font-medium text-purple-800 dark:text-purple-200 mb-2">Fact-Based Memory</h4>
              <div className="max-h-48 overflow-y-auto">
                <pre className="text-xs text-purple-700 dark:text-purple-300 whitespace-pre-wrap break-words">
                  {JSON.stringify(memoryData.mem0_memory, null, 2)}
                </pre>
              </div>
            </div>
          </div>
        );
      
      default:
        return null;
    }
  };

  return (
    <div className="border-t border-gray-200 dark:border-gray-700">
      <button
        onClick={onToggle}
        className="w-full flex items-center justify-between p-3 bg-gray-50 dark:bg-gray-800 hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors"
      >
        <div className="flex items-center space-x-2">
          <Brain className="w-4 h-4 text-blue-500" />
          <span className="font-medium text-gray-700 dark:text-gray-300">Memory Context</span>
        </div>
        {isOpen ? (
          <ChevronDown className="w-4 h-4 text-gray-500" />
        ) : (
          <ChevronRight className="w-4 h-4 text-gray-500" />
        )}
      </button>
      
      {isOpen && (
        <div className="p-3 bg-white dark:bg-gray-900 border-t border-gray-200 dark:border-gray-700 max-h-[70vh] overflow-hidden flex flex-col">
          {/* Tab Navigation */}
          <div className="grid grid-cols-3 gap-1 mb-3 border-b border-gray-200 dark:border-gray-700 flex-shrink-0 pb-1">
            {tabs.map((tab) => {
              const Icon = tab.icon;
              return (
                <button
                  key={tab.id}
                  onClick={() => setActiveTab(tab.id)}
                  className={`flex items-center justify-center space-x-1 px-1 py-2 text-xs font-medium rounded-t-lg transition-colors ${
                    activeTab === tab.id
                      ? 'bg-blue-500 text-white'
                      : 'text-gray-600 dark:text-gray-400 hover:text-gray-800 dark:hover:text-gray-200'
                  }`}
                >
                  <Icon className="w-3 h-3" />
                  <span className="truncate">{tab.label}</span>
                </button>
              );
            })}
          </div>
          
          {/* Memory Content */}
          <div className="flex-1 overflow-y-auto min-h-0">
            {isLoading ? (
              <div className="flex items-center justify-center py-8">
                <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-500"></div>
                <span className="ml-2 text-sm text-gray-500 dark:text-gray-400">Loading memory...</span>
              </div>
            ) : (
              renderMemoryContent()
            )}
          </div>
          
          {/* Memory Info */}
          <div className="mt-3 p-2 bg-gray-50 dark:bg-gray-800 rounded-lg flex-shrink-0">
            <div className="flex items-center space-x-2 text-xs text-gray-600 dark:text-gray-400">
              <Info className="w-3 h-3 flex-shrink-0" />
              <span className="break-words">Memory data is automatically updated with each conversation</span>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default MemoryPanel; 