import React from 'react';
import './LoadingSpinner.css';

export const LoadingSpinner = ({ size = 'medium', text }) => {
  return (
    <div className={`spinner-wrapper spinner-${size}`}>
      <div className="spinner" />
      {text && <span className="spinner-text">{text}</span>}
    </div>
  );
};
