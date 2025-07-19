import React from 'react';
import { BarChart3, TrendingUp, Database, Users, RefreshCw } from 'lucide-react';

interface MemoryStats {
  totalMemories: number;
  zepMemories: number;
  mem0Memories: number;
  activeSessions: number;
  lastUpdated: string;
}

interface MemoryAnalyticsProps {
  stats: MemoryStats;
  isOpen: boolean;
  onToggle: () => void;
  onRefresh?: () => void;
  isLoading?: boolean;
  error?: string | null;
}

const MemoryAnalytics: React.FC<MemoryAnalyticsProps> = ({ 
  stats, 
  isOpen, 
  onToggle, 
  onRefresh,
  isLoading = false,
  error = null 
}) => {
  const metrics = [
    {
      label: 'Total Memories',
      value: stats.totalMemories,
      icon: Database,
      color: 'text-blue-500',
      bgColor: 'bg-blue-50 dark:bg-blue-900/20'
    },
    {
      label: 'Zep Memories',
      value: stats.zepMemories,
      icon: BarChart3,
      color: 'text-green-500',
      bgColor: 'bg-green-50 dark:bg-green-900/20'
    },
    {
      label: 'Mem0 Memories',
      value: stats.mem0Memories,
      icon: TrendingUp,
      color: 'text-purple-500',
      bgColor: 'bg-purple-50 dark:bg-purple-900/20'
    },
    {
      label: 'Active Sessions',
      value: stats.activeSessions,
      icon: Users,
      color: 'text-orange-500',
      bgColor: 'bg-orange-50 dark:bg-orange-900/20'
    }
  ];

  return (
    <div className="border-t border-gray-200 dark:border-gray-700">
      <button
        onClick={onToggle}
        className="w-full flex items-center justify-between p-3 bg-gray-50 dark:bg-gray-800 hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors"
      >
        <div className="flex items-center space-x-2">
          <BarChart3 className="w-4 h-4 text-green-500" />
          <span className="font-medium text-gray-700 dark:text-gray-300">Memory Analytics</span>
        </div>
        <div className="flex items-center space-x-2">
          {isLoading && (
            <div className="w-4 h-4 border-2 border-green-500 border-t-transparent rounded-full animate-spin"></div>
          )}
          <span className="text-xs text-gray-500">Last updated: {stats.lastUpdated}</span>
          {isOpen ? (
            <span className="text-xs bg-green-100 text-green-800 px-2 py-1 rounded-full">Live</span>
          ) : null}
        </div>
      </button>
      
      {isOpen && (
        <div className="p-4 bg-white dark:bg-gray-900 border-t border-gray-200 dark:border-gray-700 max-h-[70vh] overflow-y-auto">
          {/* Refresh Button */}
          <div className="flex justify-between items-center mb-4 flex-shrink-0">
            <h3 className="text-lg font-semibold text-gray-900 dark:text-white">Memory Statistics</h3>
            <button
              onClick={onRefresh}
              disabled={isLoading}
              className="flex items-center space-x-2 px-3 py-2 bg-blue-100 dark:bg-blue-900/20 hover:bg-blue-200 dark:hover:bg-blue-900/40 text-blue-700 dark:text-blue-300 rounded-lg transition-colors duration-200 disabled:opacity-50 disabled:cursor-not-allowed flex-shrink-0"
              title="Refresh memory statistics"
            >
              <RefreshCw className={`w-4 h-4 ${isLoading ? 'animate-spin' : ''}`} />
              <span className="text-sm font-medium">Refresh</span>
            </button>
          </div>
          
          {error && (
            <div className="mb-4 p-3 bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg">
              <p className="text-sm text-red-600 dark:text-red-400">{error}</p>
            </div>
          )}
          
          {isLoading ? (
            <div className="flex items-center justify-center py-8">
              <div className="w-8 h-8 border-2 border-green-500 border-t-transparent rounded-full animate-spin"></div>
              <span className="ml-2 text-sm text-gray-600 dark:text-gray-400">Loading memory statistics...</span>
            </div>
          ) : (
            <>
              {/* Metrics Grid */}
              <div className="grid grid-cols-2 gap-3 mb-6">
                {metrics.map((metric) => {
                  const Icon = metric.icon;
                  return (
                    <div key={metric.label} className={`p-3 rounded-lg ${metric.bgColor} min-h-[80px]`}>
                      <div className="flex items-center justify-between h-full">
                        <div className="flex-1 min-w-0">
                          <p className="text-xs font-medium text-gray-600 dark:text-gray-400 truncate">
                            {metric.label}
                          </p>
                          <p className="text-xl font-bold text-gray-900 dark:text-white mt-1">
                            {metric.value}
                          </p>
                        </div>
                        <div className="flex-shrink-0 ml-2">
                          <Icon className={`w-6 h-6 ${metric.color}`} />
                        </div>
                      </div>
                    </div>
                  );
                })}
              </div>
              
              {/* Memory Usage Chart */}
              <div className="bg-gray-50 dark:bg-gray-800 rounded-lg p-4">
                <h4 className="font-medium text-gray-900 dark:text-white mb-3">Memory Distribution</h4>
                <div className="space-y-3">
                  <div className="flex items-center justify-between">
                    <span className="text-sm text-gray-600 dark:text-gray-400">Zep Memory</span>
                    <div className="flex items-center space-x-2">
                      <div className="w-24 bg-gray-200 dark:bg-gray-700 rounded-full h-2">
                        <div 
                          className="bg-green-500 h-2 rounded-full transition-all duration-300"
                          style={{ width: `${stats.totalMemories > 0 ? (stats.zepMemories / stats.totalMemories) * 100 : 0}%` }}
                        ></div>
                      </div>
                      <span className="text-sm font-medium text-gray-900 dark:text-white">
                        {stats.zepMemories}
                      </span>
                    </div>
                  </div>
                  
                  <div className="flex items-center justify-between">
                    <span className="text-sm text-gray-600 dark:text-gray-400">Mem0 Memory</span>
                    <div className="flex items-center space-x-2">
                      <div className="w-24 bg-gray-200 dark:bg-gray-700 rounded-full h-2">
                        <div 
                          className="bg-purple-500 h-2 rounded-full transition-all duration-300"
                          style={{ width: `${stats.totalMemories > 0 ? (stats.mem0Memories / stats.totalMemories) * 100 : 0}%` }}
                        ></div>
                      </div>
                      <span className="text-sm font-medium text-gray-900 dark:text-white">
                        {stats.mem0Memories}
                      </span>
                    </div>
                  </div>
                </div>
              </div>
              
              {/* Manual Refresh Info */}
              <div className="mt-4 flex items-center space-x-2 text-sm text-gray-600 dark:text-gray-400">
                <div className="w-2 h-2 bg-blue-500 rounded-full"></div>
                <span>Click refresh to update memory statistics</span>
              </div>
            </>
          )}
        </div>
      )}
    </div>
  );
};

export default MemoryAnalytics; 