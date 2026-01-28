import React from 'react';
import './ErrorStates.css';

/**
 * Error State Components
 * Display when errors occur
 */

export const ErrorState = ({
  icon = '⚠️',
  title = 'Something went wrong',
  message = 'An unexpected error occurred. Please try again.',
  onRetry,
  retryLabel = 'Try Again',
  className = ''
}) => (
  <div className={`error-state ${className}`}>
    <div className="error-state-icon">{icon}</div>
    <h3 className="error-state-title">{title}</h3>
    <p className="error-state-message">{message}</p>
    {onRetry && (
      <button onClick={onRetry} className="btn btn-primary btn-md error-state-button">
        {retryLabel}
      </button>
    )}
  </div>
);

/**
 * Error Banner
 * Inline error notification
 */
export const ErrorBanner = ({ message, onDismiss, className = '' }) => (
  <div className={`error-banner ${className}`}>
    <div className="error-banner-content">
      <span className="error-banner-icon">⚠️</span>
      <span className="error-banner-message">{message}</span>
    </div>
    {onDismiss && (
      <button onClick={onDismiss} className="error-banner-close" aria-label="Dismiss">
        ✕
      </button>
    )}
  </div>
);

/**
 * API Error
 */
export const ApiError = ({ error, onRetry }) => {
  let message = 'Failed to load data. Please check your connection and try again.';
  
  if (error?.message) {
    message = error.message;
  } else if (error?.status === 404) {
    message = 'The requested resource was not found.';
  } else if (error?.status === 403) {
    message = 'You do not have permission to access this resource.';
  } else if (error?.status === 500) {
    message = 'Server error. Please try again later.';
  }

  return (
    <ErrorState
      icon="🔌"
      title="Connection Error"
      message={message}
      onRetry={onRetry}
    />
  );
};

/**
 * Not Found Error
 */
export const NotFoundError = ({ resourceName = 'Page', onGoBack }) => (
  <ErrorState
    icon="🔍"
    title={`${resourceName} Not Found`}
    message={`The ${resourceName.toLowerCase()} you're looking for doesn't exist or has been removed.`}
    onRetry={onGoBack}
    retryLabel="Go Back"
  />
);

/**
 * Permission Denied
 */
export const PermissionDenied = () => (
  <ErrorState
    icon="🔒"
    title="Access Denied"
    message="You don't have permission to access this resource. Please contact your administrator."
  />
);

/**
 * Network Error
 */
export const NetworkError = ({ onRetry }) => (
  <ErrorState
    icon="📡"
    title="Network Error"
    message="Unable to connect to the server. Please check your internet connection and try again."
    onRetry={onRetry}
  />
);

/**
 * Form Error Summary
 */
export const FormErrorSummary = ({ errors = [], className = '' }) => {
  if (!errors || errors.length === 0) return null;

  return (
    <div className={`form-error-summary ${className}`}>
      <div className="form-error-icon">⚠️</div>
      <div className="form-error-content">
        <h4 className="form-error-title">Please fix the following errors:</h4>
        <ul className="form-error-list">
          {errors.map((error, index) => (
            <li key={index}>{error}</li>
          ))}
        </ul>
      </div>
    </div>
  );
};

/**
 * Validation Error
 */
export const ValidationError = ({ message }) => (
  <div className="validation-error">
    <span className="validation-error-icon">✕</span>
    <span className="validation-error-message">{message}</span>
  </div>
);
