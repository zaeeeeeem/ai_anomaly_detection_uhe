import React from 'react';
import { AdminSidebar } from './AdminSidebar';
import { Navbar } from '../layout/Navbar';
import './AdminLayout.css';

export const AdminLayout = ({ title, subtitle, actions, children }) => {
  return (
    <div className="admin-layout">
      <AdminSidebar />
      <div className="admin-main">
        <Navbar />
        <div className="admin-content">
          <div className="admin-page-header">
            <div>
              <h1>{title}</h1>
              {subtitle ? <p>{subtitle}</p> : null}
            </div>
            {actions ? <div className="admin-page-actions">{actions}</div> : null}
          </div>
          {children}
        </div>
      </div>
    </div>
  );
};
