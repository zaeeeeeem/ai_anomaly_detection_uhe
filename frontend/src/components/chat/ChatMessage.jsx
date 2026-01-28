import React from 'react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import './ChatMessage.css';

export const ChatMessage = ({ message }) => {
  const isUser = message.role === 'user';

  // Format timestamp
  const formatTime = (timestamp) => {
    if (!timestamp) return '';
    const date = new Date(timestamp);
    return date.toLocaleTimeString('en-US', { hour: 'numeric', minute: '2-digit' });
  };

  return (
    <div className={`chat-message ${isUser ? 'chat-message-user' : 'chat-message-assistant'}`}>
      {!isUser && (
        <div className="message-avatar">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <path d="M22 12h-4l-3 9L9 3l-3 9H2" />
          </svg>
        </div>
      )}

      <div className="message-content">
        <div className="message-bubble">
          <ReactMarkdown remarkPlugins={[remarkGfm]}>
            {message.content}
          </ReactMarkdown>
        </div>
        <div className="message-meta">
          <span className="message-role">{isUser ? 'You' : 'MediGuard AI'}</span>
          {message.timestamp && (
            <>
              <span className="message-meta-divider">•</span>
              <span className="message-time">{formatTime(message.timestamp)}</span>
            </>
          )}
        </div>
      </div>

      {isUser && (
        <div className="message-avatar message-avatar-user">
          {message.user_name?.charAt(0).toUpperCase() || 'U'}
        </div>
      )}
    </div>
  );
};
