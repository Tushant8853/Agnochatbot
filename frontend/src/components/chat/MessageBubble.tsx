import React from 'react';
import { motion } from 'framer-motion';
import { format } from 'date-fns';
import { ChatMessage } from '../../services/api';

interface MessageBubbleProps {
  message: ChatMessage;
  isLast: boolean;
}

const MessageBubble: React.FC<MessageBubbleProps> = ({ message, isLast }) => {
  const isUser = message.role === 'user';
  const timestamp = new Date(message.timestamp);

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.3 }}
      className={`flex ${isUser ? 'justify-end' : 'justify-start'} mb-4`}
    >
      <div className={`message-bubble ${isUser ? 'message-user' : 'message-assistant'}`}>
        <div className="whitespace-pre-wrap break-words">{message.content}</div>
        <div className={`text-xs mt-2 ${isUser ? 'text-blue-100' : 'text-gray-500 dark:text-gray-400'}`}>
          {format(timestamp, 'HH:mm')}
        </div>
      </div>
    </motion.div>
  );
};

export default MessageBubble; 