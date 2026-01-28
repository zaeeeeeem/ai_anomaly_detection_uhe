import React from 'react';
import { Link } from 'react-router-dom';
import './EmptyStates.css';

/**
 * Empty State Components
 * Display when no data is available
 */

export const EmptyState = ({
  icon = '📭',
  title = 'No data available',
  message = 'There is nothing to display at the moment.',
  actionLabel,
  actionHref,
  onAction,
  className = ''
}) => (
  <div className={`empty-state ${className}`}>
    <div className="empty-state-icon">{icon}</div>
    <h3 className="empty-state-title">{title}</h3>
    <p className="empty-state-message">{message}</p>
    {(actionLabel && (actionHref || onAction)) && (
      <div className="empty-state-action">
        {actionHref ? (
          <Link to={actionHref} className="btn btn-primary">
            {actionLabel}
          </Link>
        ) : (
          <button onClick={onAction} className="btn btn-primary">
            {actionLabel}
          </button>
        )}
      </div>
    )}
  </div>
);

/**
 * Empty Interactions List
 */
export const EmptyInteractions = () => (
  <EmptyState
    icon="💬"
    title="No Interactions Found"
    message="There are no interactions to review at the moment. New interactions will appear here as they are flagged."
  />
);

/**
 * Empty Flagged Cases
 */
export const EmptyFlaggedCases = () => (
  <EmptyState
    icon="🎉"
    title="No Flagged Cases"
    message="Great news! There are no flagged cases requiring review. All interactions are within safety parameters."
  />
);

/**
 * Empty Search Results
 */
export const EmptySearchResults = ({ searchTerm }) => (
  <EmptyState
    icon="🔍"
    title="No Results Found"
    message={searchTerm ? `No results found for "${searchTerm}". Try adjusting your search criteria.` : 'No results match your search criteria.'}
  />
);

/**
 * Empty Recent Activity
 */
export const EmptyRecentActivity = () => (
  <EmptyState
    icon="📊"
    title="No Recent Activity"
    message="No recent activity to display. Activity will appear here as users interact with the system."
  />
);

/**
 * Empty Citations
 */
export const EmptyCitations = () => (
  <EmptyState
    icon="📄"
    title="No Citations Available"
    message="No relevant citations were found for this interaction."
  />
);

/**
 * No Review Yet
 */
export const NoReviewYet = () => (
  <div className="empty-state empty-state-pending">
    <div className="empty-state-icon-large">⏳</div>
    <h3 className="empty-state-title">Pending Human Review</h3>
    <p className="empty-state-message">
      This interaction has been flagged and is awaiting expert verification.
    </p>
  </div>
);

/**
 * Generic Empty Table
 */
export const EmptyTable = ({ message = 'No data to display' }) => (
  <EmptyState
    icon="📋"
    title="Empty"
    message={message}
  />
);
