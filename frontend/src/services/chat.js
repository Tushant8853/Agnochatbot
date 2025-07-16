import api from './auth';

export const chatService = {
  // Send a chat message
  async sendMessage(message, sessionId = null, useMemory = true) {
    try {
      const response = await api.post('/chat', {
        message,
        session_id: sessionId,
        use_memory: useMemory
      });
      return { success: true, data: response.data };
    } catch (error) {
      return {
        success: false,
        error: error.response?.data?.detail || 'Failed to send message'
      };
    }
  },

  // Get all user sessions
  async getSessions() {
    try {
      const response = await api.get('/sessions');
      return { success: true, data: response.data };
    } catch (error) {
      return {
        success: false,
        error: error.response?.data?.detail || 'Failed to get sessions'
      };
    }
  },

  // Get chat history for a specific session
  async getSessionHistory(sessionId) {
    try {
      const response = await api.get(`/sessions/${sessionId}/history`);
      return { success: true, data: response.data };
    } catch (error) {
      return {
        success: false,
        error: error.response?.data?.detail || 'Failed to get session history'
      };
    }
  },

  // Send message using Agno framework
  async sendAgnoMessage(message, sessionId = null) {
    try {
      const response = await api.post('/agno/chat', {
        message,
        session_id: sessionId
      });
      return { success: true, data: response.data };
    } catch (error) {
      return {
        success: false,
        error: error.response?.data?.detail || 'Failed to send Agno message'
      };
    }
  },

  // Generate new session ID
  generateSessionId() {
    return 'session_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
  }
}; 