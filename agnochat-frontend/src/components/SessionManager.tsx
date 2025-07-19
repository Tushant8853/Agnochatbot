import React, { useState } from 'react';
import { Clock, Plus, Trash2, Copy, Download, Calendar, MessageSquare, X } from 'lucide-react';

interface Session {
  id: string;
  name: string;
  createdAt: string;
  lastActivity: string;
  messageCount: number;
  isActive: boolean;
}

interface SessionManagerProps {
  sessions: Session[];
  currentSessionId: string;
  onSessionSelect: (sessionId: string) => void;
  onSessionCreate: () => void;
  onSessionDelete: (sessionId: string) => void;
  onSessionExport: (sessionId: string) => void;
  isOpen: boolean;
  onToggle: () => void;
  showSessionCreated?: boolean;
  showSessionSwitched?: boolean;
}

const SessionManager: React.FC<SessionManagerProps> = ({
  sessions,
  currentSessionId,
  onSessionSelect,
  onSessionCreate,
  onSessionDelete,
  onSessionExport,
  isOpen,
  onToggle,
  showSessionCreated = false,
  showSessionSwitched = false
}) => {
  const [searchTerm, setSearchTerm] = useState('');

  const filteredSessions = sessions.filter(session =>
    session.name.toLowerCase().includes(searchTerm.toLowerCase())
  );

  console.log('SessionManager - All sessions:', sessions);
  console.log('SessionManager - Filtered sessions:', filteredSessions);
  console.log('SessionManager - Current session ID:', currentSessionId);

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  return (
    <div className="border-t border-gray-200 dark:border-gray-700">
      <button
        onClick={onToggle}
        className="w-full flex items-center justify-between p-3 bg-gray-50 dark:bg-gray-800 hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors"
      >
        <div className="flex items-center space-x-2">
          <Clock className="w-4 h-4 text-orange-500" />
          <span className="font-medium text-gray-700 dark:text-gray-300">Session Manager</span>
          <span className="text-xs bg-blue-100 text-blue-800 px-2 py-1 rounded-full">
            {sessions.length} sessions
          </span>
        </div>
        <button
          onClick={onToggle}
          className="p-1 rounded-lg hover:bg-gray-200 dark:hover:bg-gray-700 transition-colors"
          title="Close Session Manager"
        >
          <X className="w-4 h-4 text-gray-500" />
        </button>
      </button>
      
      {isOpen && (
        <div className="p-4 bg-white dark:bg-gray-900 border-t border-gray-200 dark:border-gray-700">
          {/* Debug Info (only in development) */}
          {process.env.NODE_ENV === 'development' && (
            <div className="mb-4 p-3 bg-gray-50 dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg">
              <div className="text-xs text-gray-600 dark:text-gray-400">
                <p><strong>Debug Info:</strong></p>
                <p>Total sessions: {sessions.length}</p>
                <p>Filtered sessions: {filteredSessions.length}</p>
                <p>Current session ID: {currentSessionId}</p>
                <p>Session names: {sessions.map(s => s.name).join(', ')}</p>
              </div>
            </div>
          )}

          {/* Success Messages */}
          {showSessionCreated && (
            <div className="mb-4 p-3 bg-green-50 dark:bg-green-900/20 border border-green-200 dark:border-green-800 rounded-lg">
              <div className="flex items-center space-x-2 text-sm text-green-700 dark:text-green-300">
                <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>
                <span>New session created successfully!</span>
              </div>
            </div>
          )}
          
          {showSessionSwitched && (
            <div className="mb-4 p-3 bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-800 rounded-lg">
              <div className="flex items-center space-x-2 text-sm text-blue-700 dark:text-blue-300">
                <div className="w-2 h-2 bg-blue-500 rounded-full animate-pulse"></div>
                <span>Session switched successfully!</span>
              </div>
            </div>
          )}

          {/* Search and Create */}
          <div className="flex space-x-2 mb-4">
            <input
              type="text"
              placeholder="Search sessions..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="flex-1 px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent dark:bg-gray-700 dark:text-white text-sm"
            />
            <button
              onClick={onSessionCreate}
              className="px-3 py-2 bg-blue-500 hover:bg-blue-600 text-white rounded-lg transition-colors flex items-center space-x-1 shadow-sm"
              title="Create new session (Ctrl+N)"
            >
              <Plus className="w-4 h-4" />
              <span className="text-sm font-medium">New</span>
            </button>
          </div>
          
          {/* Sessions List */}
          <div className="space-y-2 max-h-64 overflow-y-auto">
            {sessions.length === 0 ? (
              <div className="text-center py-8 text-gray-500 dark:text-gray-400">
                <MessageSquare className="w-8 h-8 mx-auto mb-2 opacity-50" />
                <p>No sessions available</p>
                <p className="text-xs mt-1">Click "New" to create your first session</p>
              </div>
            ) : filteredSessions.length === 0 ? (
              <div className="text-center py-8 text-gray-500 dark:text-gray-400">
                <MessageSquare className="w-8 h-8 mx-auto mb-2 opacity-50" />
                <p>No sessions match your search</p>
              </div>
            ) : (
              filteredSessions.map((session) => (
                <div
                  key={session.id}
                  className={`p-3 rounded-lg border transition-all duration-200 cursor-pointer ${
                    session.id === currentSessionId
                      ? 'border-blue-500 bg-blue-50 dark:bg-blue-900/20'
                      : 'border-gray-200 dark:border-gray-700 hover:border-gray-300 dark:hover:border-gray-600'
                  } ${showSessionCreated && session.id === currentSessionId ? 'animate-bounce-in' : ''} ${
                    showSessionSwitched && session.id === currentSessionId ? 'animate-bounce-in' : ''
                  }`}
                >
                  <div className="flex items-center justify-between">
                                         <div 
                       className="flex-1 cursor-pointer"
                       onClick={() => onSessionSelect(session.id)}
                       title={session.id === currentSessionId ? 'Current session' : `Switch to ${session.name}`}
                     >
                                             <div className="flex items-center space-x-2">
                         <h4 className={`font-medium text-sm ${
                           session.id === currentSessionId 
                             ? 'text-blue-600 dark:text-blue-400' 
                             : 'text-gray-900 dark:text-white'
                         }`}>
                           {session.name}
                         </h4>
                         {session.id === currentSessionId && (
                           <span className="text-xs bg-blue-100 text-blue-800 px-2 py-1 rounded-full font-medium">
                             Active
                           </span>
                         )}
                         {session.isActive && session.id !== currentSessionId && (
                           <span className="w-2 h-2 bg-green-500 rounded-full"></span>
                         )}
                       </div>
                      <div className="flex items-center space-x-4 mt-1 text-xs text-gray-500 dark:text-gray-400">
                        <div className="flex items-center space-x-1">
                          <Calendar className="w-3 h-3" />
                          <span>{formatDate(session.createdAt)}</span>
                        </div>
                        <div className="flex items-center space-x-1">
                          <MessageSquare className="w-3 h-3" />
                          <span>{session.messageCount} messages</span>
                        </div>
                      </div>
                    </div>
                    
                    <div className="flex items-center space-x-1">
                      <button
                        onClick={() => onSessionExport(session.id)}
                        className="p-1 text-gray-400 hover:text-blue-500 transition-colors"
                        title="Export session"
                      >
                        <Download className="w-4 h-4" />
                      </button>
                      {session.id !== currentSessionId && (
                        <button
                          onClick={() => onSessionDelete(session.id)}
                          className="p-1 text-gray-400 hover:text-red-500 transition-colors"
                          title="Delete session"
                        >
                          <Trash2 className="w-4 h-4" />
                        </button>
                      )}
                    </div>
                  </div>
                </div>
              ))
            )}
          </div>
          
          {/* Session Stats */}
          <div className="mt-4 pt-4 border-t border-gray-200 dark:border-gray-700">
            <div className="grid grid-cols-2 gap-4 text-sm">
              <div className="text-center">
                <p className="text-gray-500 dark:text-gray-400">Total Sessions</p>
                <p className="font-semibold text-gray-900 dark:text-white">{sessions.length}</p>
              </div>
              <div className="text-center">
                <p className="text-gray-500 dark:text-gray-400">Active Sessions</p>
                <p className="font-semibold text-green-600 dark:text-green-400">
                  {sessions.filter(s => s.isActive).length}
                </p>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default SessionManager; 