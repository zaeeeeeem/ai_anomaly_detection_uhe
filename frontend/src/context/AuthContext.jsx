import React, { createContext, useEffect, useState } from 'react';
import { authService } from '../services/authService';

export const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  useEffect(() => {
    const bootstrap = async () => {
      const token = localStorage.getItem('access_token');
      if (!token) {
        setLoading(false);
        return;
      }

      try {
        const me = await authService.getCurrentUser();
        setUser(me);
        setIsAuthenticated(true);
      } catch (error) {
        authService.logout();
        setUser(null);
        setIsAuthenticated(false);
      } finally {
        setLoading(false);
      }
    };

    bootstrap();
  }, []);

  const login = async (credentials) => {
    try {
      const token = await authService.login(credentials);
      localStorage.setItem('access_token', token.access_token);
      const me = await authService.getCurrentUser();
      setUser(me);
      setIsAuthenticated(true);
      return { success: true, role: me?.role };
    } catch (error) {
      const message = error?.response?.data?.detail || 'Login failed';
      return { success: false, error: message };
    }
  };

  const signup = async (data) => {
    try {
      await authService.signup(data);
      return { success: true };
    } catch (error) {
      const message = error?.response?.data?.detail || 'Signup failed';
      return { success: false, error: message };
    }
  };

  const logout = () => {
    authService.logout();
    setUser(null);
    setIsAuthenticated(false);
  };

  return (
    <AuthContext.Provider
      value={{
        user,
        loading,
        isAuthenticated,
        login,
        signup,
        logout,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
};
