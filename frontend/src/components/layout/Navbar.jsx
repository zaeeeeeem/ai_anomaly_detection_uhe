import React, { useState, useRef, useEffect } from 'react';
import { useAuth } from '../../hooks/useAuth';
import './Navbar.css';

export const Navbar = () => {
  const { user, logout } = useAuth();
  const [dropdownOpen, setDropdownOpen] = useState(false);
  const [searchFocused, setSearchFocused] = useState(false);
  const dropdownRef = useRef(null);

  // Close dropdown when clicking outside
  useEffect(() => {
    const handleClickOutside = (event) => {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target)) {
        setDropdownOpen(false);
      }
    };

    if (dropdownOpen) {
      document.addEventListener('mousedown', handleClickOutside);
      return () => document.removeEventListener('mousedown', handleClickOutside);
    }
  }, [dropdownOpen]);

  return (
    <nav className="navbar">
      {/* Search Section */}
      <div className={`navbar-search ${searchFocused ? 'navbar-search-focused' : ''}`}>
        <svg className="navbar-search-icon" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
          <circle cx="11" cy="11" r="8" />
          <path d="m21 21-4.35-4.35" />
        </svg>
        <input
          type="text"
          className="navbar-search-input"
          placeholder="Search conversations, anomalies..."
          onFocus={() => setSearchFocused(true)}
          onBlur={() => setSearchFocused(false)}
        />
        <kbd className="navbar-search-kbd">⌘K</kbd>
      </div>

      {/* Right Section */}
      <div className="navbar-actions">
        {/* Notifications */}
        <button className="navbar-icon-btn" aria-label="Notifications">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9" />
            <path d="M13.73 21a2 2 0 0 1-3.46 0" />
          </svg>
          <span className="navbar-notification-badge">3</span>
        </button>

        {/* Help */}
        <button className="navbar-icon-btn" aria-label="Help">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <circle cx="12" cy="12" r="10" />
            <path d="M9.09 9a3 3 0 0 1 5.83 1c0 2-3 3-3 3" />
            <line x1="12" y1="17" x2="12.01" y2="17" />
          </svg>
        </button>

        {/* User Menu */}
        <div className="navbar-user-menu" ref={dropdownRef}>
          <button
            className="navbar-user-trigger"
            onClick={() => setDropdownOpen(!dropdownOpen)}
            aria-expanded={dropdownOpen}
            aria-haspopup="true"
          >
            <div className="navbar-user-avatar">
              {(user?.full_name || user?.username || 'U').charAt(0).toUpperCase()}
            </div>
            <div className="navbar-user-info">
              <span className="navbar-user-name">{user?.full_name || user?.username || 'User'}</span>
              <span className="navbar-user-role">
                {user?.is_admin ? 'Administrator' : 'Analyst'}
              </span>
            </div>
            <svg
              className={`navbar-user-chevron ${dropdownOpen ? 'navbar-user-chevron-open' : ''}`}
              width="16"
              height="16"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              strokeWidth="2"
            >
              <polyline points="6 9 12 15 18 9" />
            </svg>
          </button>

          {/* Dropdown Menu */}
          {dropdownOpen && (
            <div className="navbar-dropdown">
              <div className="navbar-dropdown-section">
                <div className="navbar-dropdown-header">
                  <div className="navbar-dropdown-user-avatar">
                    {(user?.full_name || user?.username || 'U').charAt(0).toUpperCase()}
                  </div>
                  <div className="navbar-dropdown-user-info">
                    <div className="navbar-dropdown-user-name">
                      {user?.full_name || user?.username || 'User'}
                    </div>
                    <div className="navbar-dropdown-user-email">
                      {user?.email || 'user@example.com'}
                    </div>
                  </div>
                </div>
              </div>

              <div className="navbar-dropdown-divider" />

              <div className="navbar-dropdown-section">
                <button className="navbar-dropdown-item">
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                    <path d="M19 21v-2a4 4 0 0 0-4-4H9a4 4 0 0 0-4 4v2" />
                    <circle cx="12" cy="7" r="4" />
                  </svg>
                  Profile Settings
                </button>
                <button className="navbar-dropdown-item">
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                    <circle cx="12" cy="12" r="3" />
                    <path d="M12 1v6m0 6v6" />
                    <path d="m4.93 4.93 4.24 4.24m5.66 5.66 4.24 4.24" />
                    <path d="M1 12h6m6 0h6" />
                    <path d="m4.93 19.07 4.24-4.24m5.66-5.66 4.24-4.24" />
                  </svg>
                  Preferences
                </button>
                <button className="navbar-dropdown-item">
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                    <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z" />
                    <polyline points="14 2 14 8 20 8" />
                    <line x1="12" y1="18" x2="12" y2="12" />
                    <line x1="9" y1="15" x2="15" y2="15" />
                  </svg>
                  Documentation
                </button>
              </div>

              <div className="navbar-dropdown-divider" />

              <div className="navbar-dropdown-section">
                <button
                  className="navbar-dropdown-item navbar-dropdown-item-danger"
                  onClick={logout}
                >
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                    <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4" />
                    <polyline points="16 17 21 12 16 7" />
                    <line x1="21" y1="12" x2="9" y2="12" />
                  </svg>
                  Logout
                </button>
              </div>
            </div>
          )}
        </div>
      </div>
    </nav>
  );
};
