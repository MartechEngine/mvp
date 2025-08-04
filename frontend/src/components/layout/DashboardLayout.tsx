'use client';

import React from 'react';
import Sidebar from './Sidebar';
import AppHeader from './AppHeader';

interface DashboardLayoutProps {
  children: React.ReactNode;
}

const DashboardLayout: React.FC<DashboardLayoutProps> = ({ children }) => {
  return (
    <div className="min-h-screen flex">
      {/* Sidebar - starts from top */}
      <Sidebar />

      <div className="flex-1 flex flex-col">
        {/* Header */}
        <AppHeader />

        {/* Main Content Area */}
        <main className="flex-1 p-6 md:p-8 overflow-y-auto animate-fade-in">
          {children}
        </main>
      </div>
    </div>
  );
};

export default DashboardLayout;
