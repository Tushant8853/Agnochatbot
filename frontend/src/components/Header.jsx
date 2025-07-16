import React from 'react';
import './Header.css';
import { useTheme } from '../ThemeContext';

const Header = ({ user, onLogout, onToggleMemoryPanel, showMemoryPanel }) => {
  const { theme, toggleTheme } = useTheme();
  return (
    <header className="header">
      <div className="header-left">
        <h1 className="header-title">AgnoChat</h1>
        <span className="header-subtitle">AI Assistant with Memory</span>
      </div>
      
      <div className="header-center">
        <div className="session-info">
          {user && (
            <span className="user-info">
              Welcome, {user.username}
            </span>
          )}
        </div>
      </div>
      
      <div className="header-right">
        <button 
          className="header-button memory-toggle"
          onClick={onToggleMemoryPanel}
          title={showMemoryPanel ? 'Hide Memory Panel' : 'Show Memory Panel'}
        >
          {showMemoryPanel ? '🧠' : '🧠'}
          <span className="button-text">
            {showMemoryPanel ? 'Hide Memory' : 'Show Memory'}
          </span>
        </button>

        <button
          className="header-button theme-toggle"
          onClick={toggleTheme}
          title={theme === 'dark' ? 'Switch to Light Mode' : 'Switch to Dark Mode'}
        >
          {theme === 'dark' ? '🌙' : '☀️'}
          <span className="button-text">
            {theme === 'dark' ? 'Dark' : 'Light'} Mode
          </span>
        </button>
        
        <button 
          className="header-button logout-button"
          onClick={onLogout}
          title="Logout"
        >
          <span className="button-text">Logout</span>
          <span className="logout-icon">🚪</span>
        </button>
      </div>
    </header>
  );
};

export default Header; 