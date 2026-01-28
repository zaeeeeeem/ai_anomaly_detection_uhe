import React from 'react';
import { useChat } from '../../hooks/useChat';
import './ConversationItem.css';

export const ConversationItem = ({ conversation }) => {
  const { activeConversation, selectConversation, deleteConversation } = useChat();
  const isActive = activeConversation?.id === conversation.id;

  return (
    <div
      className={`conversation-item ${isActive ? 'active' : ''}`}
      onClick={() => selectConversation(conversation)}
      role="button"
      tabIndex={0}
      onKeyDown={(e) => {
        if (e.key === 'Enter') {
          selectConversation(conversation);
        }
      }}
    >
      <div className="conversation-title">{conversation.title}</div>
      <div className="conversation-meta">
        <span>{conversation.model_type}</span>
        <span>•</span>
        <span>{conversation.model_name}</span>
      </div>
      <button
        className="conversation-delete"
        onClick={(e) => {
          e.stopPropagation();
          deleteConversation(conversation.id);
        }}
      >
        Delete
      </button>
    </div>
  );
};
