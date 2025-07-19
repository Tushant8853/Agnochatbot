import React from 'react';

interface TypingIndicatorProps {
  isTyping: boolean;
  message?: string;
}

const TypingIndicator: React.FC<TypingIndicatorProps> = ({ isTyping, message = "AgnoChat is typing..." }) => {
  if (!isTyping) return null;

  return (
    <div className="flex justify-start mb-4 animate-slide-in-up">
      <div className="bg-gray-200 dark:bg-gray-700 text-gray-900 dark:text-gray-100 rounded-lg rounded-bl-none px-4 py-3 max-w-xs">
        <div className="flex items-center space-x-2">
          <div className="flex space-x-1">
            <div className="w-2 h-2 bg-gray-500 rounded-full animate-bounce typing-pulse"></div>
            <div className="w-2 h-2 bg-gray-500 rounded-full animate-bounce typing-pulse" style={{ animationDelay: '0.1s' }}></div>
            <div className="w-2 h-2 bg-gray-500 rounded-full animate-bounce typing-pulse" style={{ animationDelay: '0.2s' }}></div>
          </div>
          <span className="text-xs text-gray-500 dark:text-gray-400">{message}</span>
        </div>
      </div>
    </div>
  );
};

export default TypingIndicator; 