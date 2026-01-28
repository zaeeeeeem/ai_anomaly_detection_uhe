import React from 'react';
import { Link } from 'react-router-dom';
import './FlaggedItemsList.css';

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

// Mock function - in real app, this would come from the backend
const calculateRiskScore = (interaction) => {
  // For demo purposes, generate a mock risk score
  return Math.floor(Math.random() * 30) + 70; // 70-99
};

const getRiskLevel = (score) => {
  if (score >= 90) return { level: 'Critical', class: 'risk-critical' };
  if (score >= 80) return { level: 'High', class: 'risk-high' };
  if (score >= 70) return { level: 'Medium', class: 'risk-medium' };
  return { level: 'Low', class: 'risk-low' };
};

const getModelIcon = (modelName) => {
  if (!modelName) return 'AI';
  if (modelName.toLowerCase().includes('gpt')) return 'GPT';
  if (modelName.toLowerCase().includes('gemini')) return 'GMN';
  if (modelName.toLowerCase().includes('claude')) return 'CLD';
  return 'AI';
};

export const FlaggedItemsList = ({ interactions, loading }) => {
  if (loading) {
    return (
      <div className="flagged-loading">
        <div className="loading-spinner-flagged"></div>
        <p>Loading flagged interactions...</p>
      </div>
    );
  }

  if (!interactions?.length) {
    return (
      <div className="flagged-empty">
        <svg width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5">
          <path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z" />
          <line x1="12" y1="9" x2="12" y2="13" />
          <line x1="12" y1="17" x2="12.01" y2="17" />
        </svg>
        <h3>All Clear</h3>
        <p>No flagged interactions at the moment. The system is monitoring all conversations.</p>
      </div>
    );
  }

  return (
    <div className="flagged-grid">
      {interactions.map((interaction, index) => {
        const riskScore = calculateRiskScore(interaction);
        const { level, class: riskClass } = getRiskLevel(riskScore);

        return (
          <div
            key={interaction.id}
            className={`flagged-card-modern ${riskClass}`}
            style={{ '--index': index }}
          >
            {/* Alert stripe */}
            <div className="flagged-alert-stripe"></div>

            {/* Header with risk score and timestamp */}
            <div className="flagged-card-header">
              <div className="flagged-risk-indicator">
                <div className="risk-score-badge">
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5">
                    <path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z" />
                    <line x1="12" y1="9" x2="12" y2="13" />
                    <line x1="12" y1="17" x2="12.01" y2="17" />
                  </svg>
                  <span className="risk-score">{riskScore}</span>
                </div>
                <div className="risk-info">
                  <span className="risk-level">{level} Risk</span>
                  <span className="risk-label">Anomaly Score</span>
                </div>
              </div>

              <div className="flagged-meta-info">
                <div className="flagged-timestamp">
                  <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                    <circle cx="12" cy="12" r="10" />
                    <polyline points="12 6 12 12 16 14" />
                  </svg>
                  <span>{formatTimestamp(interaction.timestamp)}</span>
                </div>
                <div className="flagged-model-badge">
                  <span className="model-icon">{getModelIcon(interaction.model_name)}</span>
                  {interaction.model_name || 'Unknown'}
                </div>
              </div>
            </div>

            {/* Message exchange */}
            <div className="flagged-messages">
              {/* User message */}
              <div className="flagged-message user-message-flagged">
                <div className="flagged-message-header">
                  <div className="flagged-message-icon user-icon-flagged">
                    <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                      <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2" />
                      <circle cx="12" cy="7" r="4" />
                    </svg>
                  </div>
                  <span className="flagged-message-label">User Query</span>
                </div>
                <div className="flagged-message-content">{truncate(interaction.prompt, 120)}</div>
              </div>

              {/* Assistant message */}
              <div className="flagged-message assistant-message-flagged">
                <div className="flagged-message-header">
                  <div className="flagged-message-icon assistant-icon-flagged">
                    <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                      <path d="M12 2L2 7l10 5 10-5-10-5z" />
                      <path d="M2 17l10 5 10-5" />
                      <path d="M2 12l10 5 10-5" />
                    </svg>
                  </div>
                  <span className="flagged-message-label">AI Response</span>
                </div>
                <div className="flagged-message-content">{truncate(interaction.response, 120)}</div>
              </div>
            </div>

            {/* Actions */}
            <div className="flagged-actions">
              <Link to={`/admin/interaction/${interaction.id}`} className="flagged-action-secondary">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z" />
                  <circle cx="12" cy="12" r="3" />
                </svg>
                View Details
              </Link>
              <Link to={`/admin/review/${interaction.id}`} className="flagged-action-primary">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z" />
                  <polyline points="14 2 14 8 20 8" />
                  <line x1="16" y1="13" x2="8" y2="13" />
                  <line x1="16" y1="17" x2="8" y2="17" />
                  <polyline points="10 9 9 9 8 9" />
                </svg>
                Review Now
              </Link>
            </div>
          </div>
        );
      })}
    </div>
  );
};
