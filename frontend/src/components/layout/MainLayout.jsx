import React from 'react';
import { Navbar } from './Navbar';
import { Sidebar } from './Sidebar';
import './MainLayout.css';

export const MainLayout = ({ children }) => {
  return (
    <div className="app-layout">
      <Sidebar />
      <Navbar />
      <main className="app-content">
        <div className="scroll-area">
          {children}
        </div>
      </main>
    </div>
  );
};
