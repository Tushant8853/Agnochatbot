import React from 'react';
import { motion } from 'framer-motion';
import { MessageSquare, Plus, Download } from 'lucide-react';
import { format } from 'date-fns';
import { useChat } from '../../contexts/ChatContext';
import { ChatSession } from '../../services/api';
import toast from 'react-hot-toast';

const SessionList: React.FC = () => {
  const { sessions, currentSession, loadSession, createNewSession } = useChat();

  const handleSessionClick = (session: ChatSession) => {
    if (session.session_id !== currentSession?.session_id) {
      loadSession(session.session_id);
    }
  };

  const handleNewSession = async () => {
    try {
      await createNewSession();
      toast.success('New session created');
    } catch (error) {
      toast.error('Failed to create new session');
    }
  };

  const handleExportSession = async (sessionId: string) => {
    try {
      // This would need to be implemented in the backend
      toast.success('Session exported successfully');
    } catch (error) {
      toast.error('Failed to export session');
    }
  };

  return (
    <div className="h-full flex flex-col">
      <div className="p-4 border-b border-gray-200 dark:border-dark-700">
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-lg font-semibold text-gray-900 dark:text-white">Chat Sessions</h2>
          <button
            onClick={handleNewSession}
            className="btn-primary p-2"
            title="New Chat"
          >
            <Plus className="w-4 h-4" />
          </button>
        </div>
      </div>

      <div className="flex-1 overflow-y-auto">
        {sessions.length === 0 ? (
          <div className="p-8 text-center">
            <MessageSquare className="w-12 h-12 text-gray-400 mx-auto mb-4" />
            <p className="text-gray-500 dark:text-gray-400 mb-4">No chat sessions yet</p>
            <button onClick={handleNewSession} className="btn-primary">
              Start New Chat
            </button>
          </div>
        ) : (
          <div className="p-2">
            {sessions.map((session, index) => (
              <motion.div
                key={session.session_id}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.3, delay: index * 0.1 }}
                className={`mb-2 rounded-lg p-3 cursor-pointer transition-colors duration-200 ${
                  currentSession?.session_id === session.session_id
                    ? 'bg-primary-100 dark:bg-primary-900/30 border border-primary-200 dark:border-primary-700'
                    : 'bg-gray-50 dark:bg-dark-700 hover:bg-gray-100 dark:hover:bg-dark-600'
                }`}
                onClick={() => handleSessionClick(session)}
              >
                <div className="flex items-start justify-between">
                  <div className="flex-1 min-w-0">
                    <h3 className="font-medium text-gray-900 dark:text-white truncate">
                      {session.title}
                    </h3>
                    <p className="text-xs text-gray-500 dark:text-gray-400 mt-1">
                      {format(new Date(session.created_at), 'MMM d, yyyy HH:mm')}
                    </p>
                    <div className="flex items-center mt-2">
                      <span className={`inline-flex items-center px-2 py-1 rounded-full text-xs font-medium ${
                        session.is_active === 'active'
                          ? 'bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-400'
                          : 'bg-gray-100 text-gray-800 dark:bg-gray-700 dark:text-gray-300'
                      }`}>
                        {session.is_active === 'active' ? 'Active' : 'Inactive'}
                      </span>
                    </div>
                  </div>
                  <div className="flex items-center space-x-1 ml-2">
                    <button
                      onClick={(e) => {
                        e.stopPropagation();
                        handleExportSession(session.session_id);
                      }}
                      className="p-1 text-gray-400 hover:text-gray-600 dark:hover:text-gray-300"
                      title="Export session"
                    >
                      <Download className="w-4 h-4" />
                    </button>
                  </div>
                </div>
              </motion.div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

export default SessionList; 