import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import axios from 'axios';
import { authAPI } from '../services/api';

interface User {
  user_id: string;
  email: string;
  first_name?: string;
  last_name?: string;
  username?: string;
}

interface AuthContextType {
  user: User | null;
  token: string | null;
  login: (email: string, password: string) => Promise<void>;
  signup: (userData: {
    email: string;
    password: string;
    first_name?: string;
    last_name?: string;
  }) => Promise<void>;
  logout: () => void;
  loading: boolean;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

interface AuthProviderProps {
  children: ReactNode;
}

export const AuthProvider: React.FC<AuthProviderProps> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);
  const [token, setToken] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const initializeAuth = async () => {
      const storedToken = localStorage.getItem('token');
      const storedUser = localStorage.getItem('user');

      if (storedToken && storedUser) {
        try {
          setToken(storedToken);
          setUser(JSON.parse(storedUser));
          
          // Verify token is still valid
          const response = await authAPI.getCurrentUser();
          setUser(response.data);
          localStorage.setItem('user', JSON.stringify(response.data));
        } catch (error) {
          // Token is invalid, clear storage
          localStorage.removeItem('token');
          localStorage.removeItem('user');
          setToken(null);
          setUser(null);
        }
      }
      setLoading(false);
    };

    initializeAuth();
  }, []);

  const login = async (email: string, password: string) => {
    try {
      const response = await authAPI.login({ email, password });
      const { access_token } = response.data;
      
      // Set token first
      setToken(access_token);
      localStorage.setItem('token', access_token);
      
      // Create a temporary axios instance with the token for immediate use
      const tempApi = axios.create({
        baseURL: process.env.REACT_APP_API_URL || 'http://localhost:8000/api',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${access_token}`,
        },
      });
      
      // Get user info with the temporary instance
      const userResponse = await tempApi.get('/auth/me');
      
      setUser(userResponse.data);
      localStorage.setItem('user', JSON.stringify(userResponse.data));
    } catch (error) {
      throw error;
    }
  };

  const signup = async (userData: {
    email: string;
    password: string;
    first_name?: string;
    last_name?: string;
  }) => {
    try {
      const response = await authAPI.signup(userData);
      const { access_token } = response.data;
      
      // Set token first
      setToken(access_token);
      localStorage.setItem('token', access_token);
      
      // Create a temporary axios instance with the token for immediate use
      const tempApi = axios.create({
        baseURL: process.env.REACT_APP_API_URL || 'http://localhost:8000/api',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${access_token}`,
        },
      });
      
      // Get user info with the temporary instance
      const userResponse = await tempApi.get('/auth/me');
      
      setUser(userResponse.data);
      localStorage.setItem('user', JSON.stringify(userResponse.data));
    } catch (error) {
      throw error;
    }
  };

  const logout = () => {
    setToken(null);
    setUser(null);
    localStorage.removeItem('token');
    localStorage.removeItem('user');
  };

  const value: AuthContextType = {
    user,
    token,
    login,
    signup,
    logout,
    loading,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}; 