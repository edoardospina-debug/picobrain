import axios, { AxiosError, InternalAxiosRequestConfig } from 'axios';
import { message } from 'antd';

// Create axios instance
const apiClient = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1',
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
  withCredentials: true, // Send cookies with requests
});

// Token management with localStorage persistence
class TokenManager {
  private static instance: TokenManager;
  private refreshTimer: NodeJS.Timeout | null = null;
  private readonly TOKEN_KEY = 'picobrain_access_token';

  private constructor() {
    // Load token from localStorage on initialization
    if (typeof window !== 'undefined') {
      const stored = localStorage.getItem(this.TOKEN_KEY);
      if (stored) {
        this.scheduleRefresh();
      }
    }
  }

  static getInstance(): TokenManager {
    if (!TokenManager.instance) {
      TokenManager.instance = new TokenManager();
    }
    return TokenManager.instance;
  }

  setTokens(accessToken: string) {
    if (typeof window !== 'undefined') {
      localStorage.setItem(this.TOKEN_KEY, accessToken);
      this.scheduleRefresh();
    }
  }

  getAccessToken(): string | null {
    if (typeof window !== 'undefined') {
      return localStorage.getItem(this.TOKEN_KEY);
    }
    return null;
  }

  clearTokens() {
    if (typeof window !== 'undefined') {
      localStorage.removeItem(this.TOKEN_KEY);
    }
    if (this.refreshTimer) {
      clearTimeout(this.refreshTimer);
      this.refreshTimer = null;
    }
  }

  private scheduleRefresh() {
    // Schedule token refresh 5 minutes before expiry
    // Assuming token expires in 30 minutes
    const refreshIn = 25 * 60 * 1000; // 25 minutes
    
    if (this.refreshTimer) {
      clearTimeout(this.refreshTimer);
    }
    
    this.refreshTimer = setTimeout(async () => {
      try {
        const response = await apiClient.post('/auth/refresh');
        if (response.data.access_token) {
          this.setTokens(response.data.access_token);
        }
      } catch (error) {
        console.error('Token refresh failed:', error);
        this.clearTokens();
        window.location.href = '/login';
      }
    }, refreshIn);
  }
}

export const tokenManager = TokenManager.getInstance();

// Request interceptor
apiClient.interceptors.request.use(
  (config: InternalAxiosRequestConfig) => {
    const token = tokenManager.getAccessToken();
    if (token && config.headers) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor
apiClient.interceptors.response.use(
  (response) => response,
  async (error: AxiosError) => {
    const originalRequest = error.config as InternalAxiosRequestConfig & { _retry?: boolean };
    
    // Handle 401 Unauthorized
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;
      
      try {
        // Try to refresh the token
        const response = await apiClient.post('/auth/refresh');
        if (response.data.access_token) {
          tokenManager.setTokens(response.data.access_token);
          // Retry the original request
          return apiClient(originalRequest);
        }
      } catch (refreshError) {
        // Refresh failed, redirect to login
        tokenManager.clearTokens();
        message.error('Session expired. Please login again.');
        window.location.href = '/login';
        return Promise.reject(refreshError);
      }
    }
    
    // Handle other errors
    if (error.response?.status === 403) {
      message.error('You do not have permission to perform this action');
    } else if (error.response?.status === 404) {
      message.error('Resource not found');
    } else if (error.response?.status === 500) {
      message.error('Server error. Please try again later.');
    } else if (error.message === 'Network Error') {
      message.error('Network error. Please check your connection.');
    }
    
    return Promise.reject(error);
  }
);

// Helper functions for common HTTP methods
export const api = {
  get: <T = any>(url: string, params?: any) => 
    apiClient.get<T>(url, { params }),
  
  post: <T = any>(url: string, data?: any) => 
    apiClient.post<T>(url, data),
  
  put: <T = any>(url: string, data?: any) => 
    apiClient.put<T>(url, data),
  
  patch: <T = any>(url: string, data?: any) => 
    apiClient.patch<T>(url, data),
  
  delete: <T = any>(url: string) => 
    apiClient.delete<T>(url),
};

export default apiClient;
