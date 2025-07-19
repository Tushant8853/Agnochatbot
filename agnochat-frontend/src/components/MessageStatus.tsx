import React from 'react';
import { Check, CheckCheck, Clock, AlertCircle } from 'lucide-react';

export type MessageStatus = 'sending' | 'sent' | 'delivered' | 'read' | 'error';

interface MessageStatusProps {
  status: MessageStatus;
  timestamp?: string;
}

const MessageStatusComponent: React.FC<MessageStatusProps> = ({ status, timestamp }) => {
  const getStatusIcon = () => {
    switch (status) {
      case 'sending':
        return <Clock className="w-3 h-3 text-gray-400 animate-pulse" />;
      case 'sent':
        return <Check className="w-3 h-3 text-gray-400" />;
      case 'delivered':
        return <CheckCheck className="w-3 h-3 text-blue-400" />;
      case 'read':
        return <CheckCheck className="w-3 h-3 text-green-400" />;
      case 'error':
        return <AlertCircle className="w-3 h-3 text-red-400" />;
      default:
        return null;
    }
  };

  const getStatusText = () => {
    switch (status) {
      case 'sending':
        return 'Sending...';
      case 'sent':
        return 'Sent';
      case 'delivered':
        return 'Delivered';
      case 'read':
        return 'Read';
      case 'error':
        return 'Failed';
      default:
        return '';
    }
  };

  return (
    <div className="flex items-center space-x-1 text-xs">
      {getStatusIcon()}
      <span className={`text-xs ${
        status === 'error' ? 'text-red-400' : 
        status === 'read' ? 'text-green-400' : 
        status === 'delivered' ? 'text-blue-400' : 
        'text-gray-400'
      }`}>
        {getStatusText()}
      </span>
      {timestamp && (
        <span className="text-gray-400 ml-1">• {timestamp}</span>
      )}
    </div>
  );
};

export default MessageStatusComponent; 