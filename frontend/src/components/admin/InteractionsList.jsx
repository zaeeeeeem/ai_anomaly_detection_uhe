import React from 'react';
import { Link } from 'react-router-dom';
import './InteractionsList.css';

const formatTimestamp = (timestamp) => {
  if (!timestamp) return '—';
  const date = new Date(timestamp);
  if (Number.isNaN(date.getTime())) return timestamp;

  const now = new Date();
  const diff = now - date;
  const minutes = Math.floor(diff / 60000);
  const hours = Math.floor(minutes / 60);
  const days = Math.floor(hours / 24);

  if (minutes < 1) return 'Just now';
  if (minutes < 60) return `${minutes}m ago`;
  if (hours < 24) return `${hours}h ago`;
  if (days < 7) return `${days}d ago`;

  return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' });
};

const formatTime = (timestamp) => {
  if (!timestamp) return '—';
  const date = new Date(timestamp);
  if (Number.isNaN(date.getTime())) return timestamp;
  return date.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' });
};

const truncate = (text, max = 100) => {
  if (!text) return '—';
  return text.length > max ? `${text.slice(0, max)}…` : text;
};

const getModelIcon = (modelName) => {
  if (!modelName) return 'AI';
  if (modelName.toLowerCase().includes('gpt')) return 'GPT';
  if (modelName.toLowerCase().includes('gemini')) return 'GMN';
  if (modelName.toLowerCase().includes('claude')) return 'CLD';
  return 'AI';
};

export const InteractionsList = ({ interactions, loading, emptyMessage }) => {
  if (loading) {
    return (
      <div className="interactions-loading">
        <div className="loading-spinner"></div>
        <p>Loading interactions...</p>
      </div>
    );
  }

  if (!interactions?.length) {
    return (
      <div className="interactions-empty">
        <svg width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5">
          <path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z" />
          <polyline points="3.27 6.96 12 12.01 20.73 6.96" />
          <line x1="12" y1="22.08" x2="12" y2="12" />
        </svg>
        <h3>No Interactions</h3>
        <p>{emptyMessage || 'No interactions found.'}</p>
      </div>
    );
  }

  return (
    <div className="interactions-grid">
      {interactions.map((interaction, index) => (
        <Link
          key={interaction.id}
          to={`/admin/interaction/${interaction.id}`}
          className="interaction-card-modern"
          style={{ '--index': index }}
        >
          {/* Header with timestamp and model */}
          <div className="interaction-card-top">
            <div className="interaction-timestamp">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <circle cx="12" cy="12" r="10" />
                <polyline points="12 6 12 12 16 14" />
              </svg>
              <span>{formatTimestamp(interaction.timestamp)}</span>
              <span className="interaction-time-detail">{formatTime(interaction.timestamp)}</span>
            </div>
            <div className="interaction-model-badge">
              <span className="model-icon">{getModelIcon(interaction.model_name)}</span>
              <span className="model-name">{interaction.model_name || 'Unknown'}</span>
            </div>
          </div>

          {/* Message exchange */}
          <div className="interaction-messages">
            {/* User message */}
            <div className="message-block user-message">
              <div className="message-header">
                <div className="message-icon user-icon">
                  <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                    <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2" />
                    <circle cx="12" cy="7" r="4" />
                  </svg>
                </div>
                <span className="message-label">User</span>
              </div>
              <div className="message-content">{truncate(interaction.prompt, 120)}</div>
            </div>

            {/* Assistant message */}
            <div className="message-block assistant-message">
              <div className="message-header">
                <div className="message-icon assistant-icon">
                  <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                    <path d="M12 2L2 7l10 5 10-5-10-5z" />
                    <path d="M2 17l10 5 10-5" />
                    <path d="M2 12l10 5 10-5" />
                  </svg>
                </div>
                <span className="message-label">Assistant</span>
              </div>
              <div className="message-content">{truncate(interaction.response, 120)}</div>
            </div>
          </div>

          {/* Footer with action hint */}
          <div className="interaction-card-footer">
            <span className="view-details-hint">
              Click to view full details
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <line x1="5" y1="12" x2="19" y2="12" />
                <polyline points="12 5 19 12 12 19" />
              </svg>
            </span>
          </div>
        </Link>
      ))}
    </div>
  );
};
