import React from 'react';
import './Badge.css';

export const Badge = ({
  children,
  variant = 'default',
  size = 'md',
  pulse = false,
  dot = false,
  className = '',
  ...props
}) => {
  const badgeClasses = [
    'badge',
    `badge-${variant}`,
    `badge-${size}`,
    pulse && 'badge-pulse',
    dot && 'badge-dot',
    className
  ].filter(Boolean).join(' ');

  return (
    <span className={badgeClasses} {...props}>
      {dot && <span className={`status-dot status-dot-${variant}`} />}
      {children}
    </span>
  );
};

export const StatusDot = ({ variant = 'default', live = false, className = '', ...props }) => {
  const dotClasses = [
    'status-dot',
    `status-dot-${variant}`,
    live && 'status-dot-live',
    className
  ].filter(Boolean).join(' ');

  return <span className={dotClasses} {...props} />;
};
