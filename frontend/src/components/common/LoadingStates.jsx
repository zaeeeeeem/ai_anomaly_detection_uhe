import React from 'react';
import './LoadingStates.css';

/**
 * Skeleton Loader Components
 * Provides shimmer animation while content is loading
 * Note: .skeleton classes are defined in animations.css (imported globally)
 */

export const SkeletonText = ({ width = '100%', height = '1em', className = '' }) => (
  <div 
    className={`skeleton skeleton-text ${className}`}
    style={{ width, height }}
  />
);

export const SkeletonHeading = ({ width = '60%', className = '' }) => (
  <div 
    className={`skeleton skeleton-heading ${className}`}
    style={{ width }}
  />
);

export const SkeletonAvatar = ({ size = 40, className = '' }) => (
  <div 
    className={`skeleton skeleton-avatar ${className}`}
    style={{ width: `${size}px`, height: `${size}px` }}
  />
);

export const SkeletonButton = ({ width = '120px', height = '40px', className = '' }) => (
  <div 
    className={`skeleton skeleton-button ${className}`}
    style={{ width, height }}
  />
);

export const SkeletonCard = ({ height = '200px', className = '' }) => (
  <div 
    className={`skeleton skeleton-card ${className}`}
    style={{ height }}
  />
);

/**
 * Admin Stats Grid Skeleton
 * Loading state for dashboard statistics
 */
export const StatsGridSkeleton = () => (
  <div className="admin-stats-grid">
    {[1, 2, 3, 4].map(i => (
      <div key={i} className="admin-stat-card">
        <SkeletonText width="60%" height="14px" />
        <SkeletonText width="80%" height="36px" style={{ marginTop: '8px' }} />
        <SkeletonText width="40%" height="14px" style={{ marginTop: '8px' }} />
      </div>
    ))}
  </div>
);

/**
 * Interaction Detail Skeleton
 * Loading state for 5-level interaction view
 */
export const InteractionDetailSkeleton = () => (
  <div className="interaction-detail">
    <div className="interaction-detail-header">
      <SkeletonHeading width="200px" />
      <SkeletonText width="150px" height="20px" />
    </div>
    {[1, 2, 3, 4, 5].map(level => (
      <div key={level} className="level-section">
        <div className="level-header">
          <SkeletonAvatar size={32} />
          <div style={{ flex: 1 }}>
            <SkeletonText width="40%" height="18px" />
            <SkeletonText width="60%" height="14px" style={{ marginTop: '4px' }} />
          </div>
        </div>
        <div className="level-content">
          <SkeletonText width="100%" height="100px" />
        </div>
      </div>
    ))}
  </div>
);

/**
 * Generic Spinner
 * Use for inline loading states
 */
export const Spinner = ({ size = 'md', className = '' }) => {
  const sizeMap = {
    sm: '16px',
    md: '24px',
    lg: '32px',
    xl: '48px'
  };

  return (
    <div className={`spinner spinner-${size} ${className}`}>
      <svg
        className="spinner-svg"
        width={sizeMap[size]}
        height={sizeMap[size]}
        viewBox="0 0 24 24"
        xmlns="http://www.w3.org/2000/svg"
      >
        <circle
          className="spinner-circle"
          cx="12"
          cy="12"
          r="10"
          stroke="currentColor"
          strokeWidth="2"
          fill="none"
          strokeLinecap="round"
        />
      </svg>
    </div>
  );
};

/**
 * Loading Overlay
 * Full-screen loading state
 */
export const LoadingOverlay = ({ message = 'Loading...' }) => (
  <div className="loading-overlay">
    <div className="loading-overlay-content">
      <Spinner size="xl" />
      <p className="loading-overlay-message">{message}</p>
    </div>
  </div>
);

/**
 * Section Loader
 * Inline section loading state
 */
export const SectionLoader = ({ message = 'Loading...' }) => (
  <div className="section-loader">
    <Spinner size="lg" />
    <p className="section-loader-message">{message}</p>
  </div>
);
