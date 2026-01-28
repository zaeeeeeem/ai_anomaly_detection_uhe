import React from 'react';
import { useChat } from '../../hooks/useChat';
import { ConversationItem } from './ConversationItem';
import './ConversationList.css';

export const ConversationList = ({ loading }) => {
  const { conversations } = useChat();

  if (loading) {
    return <div className="conversation-empty">Loading conversations...</div>;
  }

  if (!conversations.length) {
    return <div className="conversation-empty">No conversations yet.</div>;
  }

  return (
    <div className="conversation-list">
      {conversations.map((conversation, index) => (
        <ConversationItem
          key={conversation.id}
          conversation={conversation}
          index={index}
        />
      ))}
    </div>
  );
};
