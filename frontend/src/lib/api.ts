import axios, { AxiosInstance, AxiosError } from 'axios';
import { TokenResponse } from '@/types/api';

// Create axios instance
const api: AxiosInstance = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000',
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Token management
const TOKEN_KEY = 'picobrain_access_token';
const TOKEN_EXPIRY_KEY = 'picobrain_token_expiry';

export const tokenManager = {
  getToken: (): string | null => {
    if (typeof window === 'undefined') return null;
    const token = localStorage.getItem(TOKEN_KEY);
    const expiry = localStorage.getItem(TOKEN_EXPIRY_KEY);
    
    // Check if token is expired
    if (token && expiry) {
      const expiryTime = parseInt(expiry, 10);
      if (Date.now() > expiryTime) {
        tokenManager.clearToken();
        return null;
      }
    }
    
    return token;
  },
  
  setToken: (tokenData: TokenResponse): void => {
    if (typeof window === 'undefined') return;
    
    localStorage.setItem(TOKEN_KEY, tokenData.access_token);
    
    // Set expiry time (default to 24 hours if not provided)
    const expiresIn = tokenData.expires_in || 86400; // 24 hours in seconds
    const expiryTime = Date.now() + (expiresIn * 1000);
    localStorage.setItem(TOKEN_EXPIRY_KEY, expiryTime.toString());
  },
  
  clearToken: (): void => {
    if (typeof window === 'undefined') return;
    localStorage.removeItem(TOKEN_KEY);
    localStorage.removeItem(TOKEN_EXPIRY_KEY);
  },
  
  isAuthenticated: (): boolean => {
    return !!tokenManager.getToken();
  },
};

// Request interceptor to add auth token
api.interceptors.request.use(
  (config) => {
    const token = tokenManager.getToken();
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor to handle errors
api.interceptors.response.use(
  (response) => {
    return response;
  },
  async (error: AxiosError) => {
    const originalRequest = error.config as any;
    
    // Handle 401 Unauthorized
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;
      
      // Clear token and redirect to login
      tokenManager.clearToken();
      
      // Only redirect if we're in the browser
      if (typeof window !== 'undefined' && window.location.pathname !== '/login') {
        window.location.href = '/login';
      }
    }
    
    // Handle network errors
    if (!error.response) {
      console.error('Network error:', error.message);
      throw new Error('Network error. Please check your connection.');
    }
    
    // Handle other errors
    const errorMessage = (error.response?.data as any)?.detail || 
                        error.message || 
                        'An unexpected error occurred';
    
    throw new Error(errorMessage);
  }
);

export default api;

// Utility function for handling API errors
export const handleApiError = (error: any): string => {
  if (error.response?.data?.detail) {
    return error.response.data.detail;
  }
  if (error.message) {
    return error.message;
  }
  return 'An unexpected error occurred';
};

// Generic API request functions
export const apiRequest = {
  get: <T>(url: string, params?: any) => 
    api.get<T>(url, { params }).then(res => res.data),
  
  post: <T>(url: string, data?: any) => 
    api.post<T>(url, data).then(res => res.data),
  
  put: <T>(url: string, data?: any) => 
    api.put<T>(url, data).then(res => res.data),
  
  patch: <T>(url: string, data?: any) => 
    api.patch<T>(url, data).then(res => res.data),
  
  delete: <T>(url: string) => 
    api.delete<T>(url).then(res => res.data),
};
