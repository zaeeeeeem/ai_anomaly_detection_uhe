import React from 'react';
import './AuthLayout.css';

export const AuthLayout = ({ title, subtitle, children }) => {
  return (
    <div className="auth-layout">
      {/* Left Panel - Branding */}
      <div className="auth-branding">
        <div className="auth-branding-content">
          {/* Logo */}
          <div className="auth-branding-logo">
            <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <path d="M22 12h-4l-3 9L9 3l-3 9H2" />
            </svg>
            <div className="auth-branding-logo-text">
              <span className="auth-branding-title">MediGuard AI</span>
              <span className="auth-branding-subtitle">Anomaly Detection</span>
            </div>
          </div>

          {/* Hero Section */}
          <div className="auth-branding-hero">
            <h2 className="auth-branding-headline">
              Clinical Intelligence
              <br />
              <span className="auth-branding-gradient">Powered by AI</span>
            </h2>
            <p className="auth-branding-description">
              Advanced anomaly detection for healthcare conversations. Identify potential risks in real-time with machine learning precision.
            </p>
          </div>

          {/* Features */}
          <div className="auth-branding-features">
            <div className="auth-branding-feature">
              <div className="auth-branding-feature-icon">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z" />
                </svg>
              </div>
              <div className="auth-branding-feature-text">
                <div className="auth-branding-feature-title">Real-time Detection</div>
                <div className="auth-branding-feature-desc">Instant anomaly identification</div>
              </div>
            </div>

            <div className="auth-branding-feature">
              <div className="auth-branding-feature-icon">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z" />
                  <polyline points="3.27 6.96 12 12.01 20.73 6.96" />
                  <line x1="12" y1="22.08" x2="12" y2="12" />
                </svg>
              </div>
              <div className="auth-branding-feature-text">
                <div className="auth-branding-feature-title">ML-Powered Analysis</div>
                <div className="auth-branding-feature-desc">Advanced pattern recognition</div>
              </div>
            </div>

            <div className="auth-branding-feature">
              <div className="auth-branding-feature-icon">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z" />
                  <polyline points="9 22 9 12 15 12 15 22" />
                </svg>
              </div>
              <div className="auth-branding-feature-text">
                <div className="auth-branding-feature-title">HIPAA Compliant</div>
                <div className="auth-branding-feature-desc">Enterprise-grade security</div>
              </div>
            </div>
          </div>

          {/* Decorative Elements */}
          <div className="auth-branding-decoration auth-branding-decoration-1"></div>
          <div className="auth-branding-decoration auth-branding-decoration-2"></div>
        </div>
      </div>

      {/* Right Panel - Form */}
      <div className="auth-form-panel">
        <div className="auth-form-container">
          <div className="auth-header">
            <h1 className="auth-title">{title}</h1>
            <p className="auth-subtitle">{subtitle}</p>
          </div>
          <div className="auth-content">{children}</div>
        </div>
      </div>
    </div>
  );
};
