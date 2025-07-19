import React from 'react';
import MessageStatusComponent, { MessageStatus as StatusType } from './MessageStatus';

interface ChatBubbleProps {
  message: string;
  isUser: boolean;
  timestamp: string;
  status?: StatusType;
  showStatus?: boolean;
}

const ChatBubble: React.FC<ChatBubbleProps> = ({ 
  message, 
  isUser, 
  timestamp, 
  status = 'sent',
  showStatus = false 
}) => {
  return (
    <div className={`flex ${isUser ? 'justify-end' : 'justify-start'} mb-4 group message-bubble`}>
      <div
        className={`max-w-xs lg:max-w-md px-4 py-2 rounded-lg transition-all-smooth hover:shadow-md ${
          isUser
            ? 'bg-blue-500 text-white rounded-br-none hover:bg-blue-600'
            : 'bg-gray-200 dark:bg-gray-700 text-gray-900 dark:text-gray-100 rounded-bl-none hover:bg-gray-300 dark:hover:bg-gray-600'
        }`}
      >
        <p className="text-sm whitespace-pre-wrap leading-relaxed">{message}</p>
        <div className="flex items-center justify-between mt-2">
          <p
            className={`text-xs ${
              isUser ? 'text-blue-100' : 'text-gray-500 dark:text-gray-400'
            }`}
          >
            {timestamp}
          </p>
          {isUser && showStatus && (
            <MessageStatusComponent status={status} />
          )}
        </div>
      </div>
    </div>
  );
};

export default ChatBubble; 