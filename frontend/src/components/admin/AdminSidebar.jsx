import React from 'react';
import { NavLink } from 'react-router-dom';
import './AdminSidebar.css';

export const AdminSidebar = () => {
  return (
    <aside className="admin-sidebar">
      <div className="admin-sidebar-header">
        <div className="admin-sidebar-logo">
          <div className="admin-sidebar-logo-icon">
            <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
              <path d="M22 12h-4l-3 9L9 3l-3 9H2" />
            </svg>
          </div>
          <div className="admin-sidebar-logo-text">
            <span className="admin-sidebar-title">MediGuard AI</span>
            <span className="admin-sidebar-subtitle">Anomaly Detection</span>
          </div>
        </div>
      </div>
      <nav className="admin-nav">
        <NavLink
          to="/admin/home"
          className={({ isActive }) =>
            `admin-nav-link ${isActive ? 'active' : ''}`
          }
        >
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
            <path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z" />
            <polyline points="9 22 9 12 15 12 15 22" />
          </svg>
          <span>Admin Home</span>
        </NavLink>
        <NavLink
          to="/admin/all-interactions"
          className={({ isActive }) =>
            `admin-nav-link ${isActive ? 'active' : ''}`
          }
        >
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
            <path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z" />
            <polyline points="3.27 6.96 12 12.01 20.73 6.96" />
            <line x1="12" y1="22.08" x2="12" y2="12" />
          </svg>
          <span>All Interactions</span>
        </NavLink>
        <NavLink
          to="/admin/customer-interactions"
          className={({ isActive }) =>
            `admin-nav-link ${isActive ? 'active' : ''}`
          }
        >
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
            <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2" />
            <circle cx="9" cy="7" r="4" />
            <path d="M23 21v-2a4 4 0 0 0-3-3.87" />
            <path d="M16 3.13a4 4 0 0 1 0 7.75" />
          </svg>
          <span>Customer Interactions</span>
        </NavLink>
        <NavLink
          to="/admin/flagged-review"
          className={({ isActive }) =>
            `admin-nav-link ${isActive ? 'active' : ''}`
          }
        >
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
            <path d="M4 15s1-1 4-1 5 2 8 2 4-1 4-1V3s-1 1-4 1-5-2-8-2-4 1-4 1z" />
            <line x1="4" y1="22" x2="4" y2="15" />
          </svg>
          <span>Flagged Review</span>
        </NavLink>
      </nav>
      <div className="admin-sidebar-footer">
        <div className="admin-sidebar-badge">
          <span className="pulse" />
          Monitoring live
        </div>
      </div>
    </aside>
  );
};
