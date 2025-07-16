import api from './auth';

export const memoryService = {
  // Search memory
  async searchMemory(query, searchType = 'hybrid') {
    try {
      const response = await api.post('/memory/search', {
        query,
        search_type: searchType
      });
      return { success: true, data: response.data };
    } catch (error) {
      return {
        success: false,
        error: error.response?.data?.detail || 'Failed to search memory'
      };
    }
  },

  // Get memory summary
  async getMemorySummary() {
    try {
      const response = await api.get('/memory/summary');
      return { success: true, data: response.data };
    } catch (error) {
      return {
        success: false,
        error: error.response?.data?.detail || 'Failed to get memory summary'
      };
    }
  },

  // Add custom fact
  async addFact(fact, factType = 'custom') {
    try {
      const response = await api.post('/memory/facts', null, {
        params: { fact, fact_type: factType }
      });
      return { success: true, data: response.data };
    } catch (error) {
      return {
        success: false,
        error: error.response?.data?.detail || 'Failed to add fact'
      };
    }
  },

  // Get Agno memories
  async getAgnoMemories() {
    try {
      const response = await api.get('/agno/memories');
      return { success: true, data: response.data };
    } catch (error) {
      return {
        success: false,
        error: error.response?.data?.detail || 'Failed to get Agno memories'
      };
    }
  },

  // Add Agno memory
  async addAgnoMemory(content, memoryType = 'fact') {
    try {
      const response = await api.post('/agno/memories', {
        content,
        memory_type: memoryType
      });
      return { success: true, data: response.data };
    } catch (error) {
      return {
        success: false,
        error: error.response?.data?.detail || 'Failed to add Agno memory'
      };
    }
  },

  // Clear Agno agent cache
  async clearAgnoAgent() {
    try {
      const response = await api.delete('/agno/agent');
      return { success: true, data: response.data };
    } catch (error) {
      return {
        success: false,
        error: error.response?.data?.detail || 'Failed to clear Agno agent'
      };
    }
  }
}; 