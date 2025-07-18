import axios, { AxiosInstance } from 'axios';

// API Base URL - adjust this based on your backend setup
const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

// Types
export interface User {
  id: string;
  username: string;
  email: string;
  first_name?: string;
  last_name?: string;
}

export interface ChatMessage {
  role: 'user' | 'assistant';
  content: string;
  timestamp: string;
}

export interface ChatSession {
  session_id: string;
  title: string;
  created_at: string;
  is_active: string;
}

export interface ChatRequest {
  message: string;
  session_id?: string;
  use_memory?: boolean;
}

export interface ChatResponse {
  message: string;
  session_id: string;
  memory_context: {
    agno_memories: any[];
    memory_count: number;
    reasoning_steps?: any[];
    tool_calls?: any[];
  };
  timestamp: string;
}

export interface MemorySearchRequest {
  query: string;
  search_type: 'hybrid' | 'temporal' | 'factual';
}

export interface MemorySummary {
  user_id: string;
  zep_facts_count: number;
  mem0_memories_count: number;
  key_facts: string[];
}

export interface AuthResponse {
  access_token: string;
  token_type: string;
  user_id: string;
  username: string;
}

export interface LoginRequest {
  username: string;
  password: string;
}

export interface SignupRequest {
  username: string;
  email: string;
  password: string;
  first_name?: string;
  last_name?: string;
}

class ApiService {
  private api: AxiosInstance;
  private token: string | null = null;

  constructor() {
    this.api = axios.create({
      baseURL: API_BASE_URL,
      headers: {
        'Content-Type': 'application/json',
      },
    });

    // Load token from localStorage
    this.token = localStorage.getItem('token');
    if (this.token) {
      this.setAuthToken(this.token);
    }

    // Add response interceptor for error handling
    this.api.interceptors.response.use(
      (response) => response,
      (error) => {
        if (error.response?.status === 401) {
          this.logout();
        }
        return Promise.reject(error);
      }
    );
  }

  setAuthToken(token: string) {
    this.token = token;
    this.api.defaults.headers.common['Authorization'] = `Bearer ${token}`;
    localStorage.setItem('token', token);
  }

  logout() {
    this.token = null;
    delete this.api.defaults.headers.common['Authorization'];
    localStorage.removeItem('token');
  }

  // Authentication
  async login(credentials: LoginRequest): Promise<AuthResponse> {
    const response = await this.api.post('/auth/login', credentials);
    return response.data;
  }

  async signup(userData: SignupRequest): Promise<AuthResponse> {
    const response = await this.api.post('/auth/signup', userData);
    return response.data;
  }

  // Chat endpoints - using /chat/agno as requested
  async sendMessage(request: ChatRequest): Promise<ChatResponse> {
    const response = await this.api.post('/chat/agno', request);
    return response.data;
  }

  // Session management
  async createSession(sessionData: { session_id?: string; title?: string }): Promise<ChatSession> {
    const response = await this.api.post('/sessions', sessionData);
    return response.data;
  }

  async getSessions(): Promise<ChatSession[]> {
    const response = await this.api.get('/sessions');
    return response.data;
  }

  async getSessionHistory(sessionId: string): Promise<ChatMessage[]> {
    const response = await this.api.get(`/sessions/${sessionId}/history`);
    return response.data;
  }

  // Memory management
  async searchMemory(request: MemorySearchRequest): Promise<any> {
    const response = await this.api.post('/memory/search', request);
    return response.data;
  }

  async getMemorySummary(): Promise<MemorySummary> {
    const response = await this.api.get('/memory/summary');
    return response.data;
  }

  async addCustomFact(fact: string, factType: string = 'custom'): Promise<any> {
    const response = await this.api.post('/memory/facts', null, {
      params: { fact, fact_type: factType }
    });
    return response.data;
  }

  async getMemory(memoryId: string): Promise<any> {
    const response = await this.api.get(`/memory/${memoryId}`);
    return response.data;
  }

  async getMemoryHistory(memoryId: string): Promise<any> {
    const response = await this.api.get(`/memory/${memoryId}/history`);
    return response.data;
  }

  // Agno specific endpoints
  async getAgnoMemories(): Promise<any> {
    const response = await this.api.get('/agno/memories');
    return response.data;
  }

  async addAgnoMemory(memoryData: any): Promise<any> {
    const response = await this.api.post('/agno/memories', memoryData);
    return response.data;
  }

  async clearAgnoAgent(): Promise<any> {
    const response = await this.api.delete('/agno/agent');
    return response.data;
  }

  // Health check
  async healthCheck(): Promise<any> {
    const response = await this.api.get('/health');
    return response.data;
  }

  // Export conversation
  async exportConversation(sessionId: string): Promise<any> {
    const response = await this.api.get(`/sessions/${sessionId}/export`);
    return response.data;
  }
}

export const apiService = new ApiService();
export default apiService; 