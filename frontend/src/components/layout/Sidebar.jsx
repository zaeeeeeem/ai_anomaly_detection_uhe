import React, { useEffect } from 'react';
import { useAuth } from '../../hooks/useAuth';
import { useChat } from '../../hooks/useChat';
import { ConversationList } from '../conversations/ConversationList';
import { NewConversationButton } from '../conversations/NewConversationButton';
import './Sidebar.css';

export const Sidebar = () => {
  const { user } = useAuth();
  const { loadConversations, loading } = useChat();

  useEffect(() => {
    loadConversations();
  }, [loadConversations]);

  return (
    <aside className="sidebar">
      {/* Logo Section */}
      <div className="sidebar-logo">
        <div className="sidebar-logo-icon">
          <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
            <path d="M22 12h-4l-3 9L9 3l-3 9H2" />
          </svg>
        </div>
        <div className="sidebar-logo-text">
          <span className="sidebar-logo-title">MediGuard AI</span>
          <span className="sidebar-logo-subtitle">Anomaly Detection</span>
        </div>
      </div>

      {/* Header with New Conversation */}
      <div className="sidebar-header">
        <h2 className="sidebar-title">Conversations</h2>
        <NewConversationButton />
      </div>

      {/* Conversations List */}
      <div className="sidebar-content">
        <ConversationList loading={loading} />
      </div>

      {/* User Profile Section */}
      {user && (
        <div className="sidebar-footer">
          <div className="sidebar-user">
            <div className="sidebar-user-avatar">
              {user.full_name ? user.full_name[0].toUpperCase() : user.email[0].toUpperCase()}
            </div>
            <div className="sidebar-user-info">
              <div className="sidebar-user-name">{user.full_name || 'User'}</div>
              <div className="sidebar-user-email">{user.email}</div>
            </div>
          </div>
        </div>
      )}
    </aside>
  );
};
