import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api';

// Create axios instance
const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add request interceptor to include auth token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Add response interceptor to handle auth errors
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token');
      localStorage.removeItem('user');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

// Auth API
export const authAPI = {
  signup: (userData: {
    email: string;
    password: string;
    first_name?: string;
    last_name?: string;
  }) => api.post('/auth/signup', userData),
  
  login: (credentials: { email: string; password: string }) =>
    api.post('/auth/login', credentials),
  
  getCurrentUser: () => api.get('/auth/me'),
};

// Chat API
export const chatAPI = {
  sendMessage: (messageData: {
    user_id: string;
    session_id: string;
    message: string;
  }) => api.post('/chat', messageData),
  
  getMemory: (user_id: string, session_id?: string) =>
    api.get('/memory', { params: { user_id, session_id } }),
  
  searchMemory: (user_id: string, query: string) =>
    api.post('/memory/search', {}, { params: { user_id, query } }),
  
  // New endpoints for real memory analytics
  getMemoryStats: (user_id: string) =>
    api.get('/memory/stats', { params: { user_id } }),
  
  getSessionStats: (user_id: string) =>
    api.get('/sessions/stats', { params: { user_id } }),
  
  getMemoryBreakdown: (user_id: string) =>
    api.get('/memory/breakdown', { params: { user_id } }),
  
  // Chat history endpoint
  getChatHistory: (user_id: string, session_id?: string, limit?: number) =>
    api.get('/chat/history', { params: { user_id, session_id, limit } }),
  
  // Memory update and sync endpoints
  syncMemory: (user_id: string) =>
    api.post('/memory/sync', {}, { params: { user_id } }),
  
  updateMemory: (user_id: string, updateData: any) =>
    api.post('/memory/update', updateData, { params: { user_id } }),
  
  clearMemory: (user_id: string) =>
    api.post('/memory/clear', {}, { params: { user_id } }),
};

// Memory Analytics API
export const memoryAPI = {
  getStats: (user_id: string) => api.get('/memory/stats', { params: { user_id } }),
  getSessionStats: (user_id: string) => api.get('/sessions/stats', { params: { user_id } }),
  getMemoryBreakdown: (user_id: string) => api.get('/memory/breakdown', { params: { user_id } }),
};

// Health check
export const healthAPI = {
  check: () => api.get('/health'),
};

export default api; 