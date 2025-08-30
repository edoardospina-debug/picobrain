import { tokenManager } from '@/lib/api';
import { LoginRequest, TokenResponse, AuthUser } from '@/types/api';
import axios from 'axios';

class AuthService {
  private apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

  async login(credentials: LoginRequest): Promise<AuthUser> {
    try {
      // Create form data for OAuth2 password flow
      const formData = new URLSearchParams();
      formData.append('username', credentials.username);
      formData.append('password', credentials.password);
      
      // Login and get token - use axios directly for the login request
      const response = await axios.post<TokenResponse>(
        `${this.apiUrl}/api/v1/auth/login`,
        formData.toString(),
        {
          headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
          },
        }
      );
      
      const tokenResponse = response.data;
      
      // Store token
      tokenManager.setToken(tokenResponse);
      
      // Get current user info
      const user = await this.getCurrentUser();
      
      return user;
    } catch (error: any) {
      tokenManager.clearToken();
      const errorMessage = error.response?.data?.detail || error.message || 'Login failed';
      throw new Error(errorMessage);
    }
  }
  
  async logout(): Promise<void> {
    try {
      const token = tokenManager.getToken();
      if (token) {
        await axios.post(
          `${this.apiUrl}/api/v1/auth/logout`,
          {},
          {
            headers: {
              Authorization: `Bearer ${token}`,
            },
          }
        ).catch(() => {
          // Ignore error if logout endpoint doesn't exist
        });
      }
    } finally {
      // Always clear token
      tokenManager.clearToken();
      
      // Redirect to login
      if (typeof window !== 'undefined') {
        window.location.href = '/login';
      }
    }
  }
  
  async getCurrentUser(): Promise<AuthUser> {
    try {
      const token = tokenManager.getToken();
      if (!token) {
        throw new Error('No token found');
      }
      
      const response = await axios.get<AuthUser>(
        `${this.apiUrl}/api/v1/auth/me`,
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );
      
      return response.data;
    } catch (error) {
      tokenManager.clearToken();
      throw error;
    }
  }
  
  async refreshToken(): Promise<void> {
    try {
      const token = tokenManager.getToken();
      if (!token) {
        throw new Error('No token found');
      }
      
      const response = await axios.post<TokenResponse>(
        `${this.apiUrl}/api/v1/auth/refresh`,
        {},
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );
      
      tokenManager.setToken(response.data);
    } catch (error) {
      tokenManager.clearToken();
      throw error;
    }
  }
  
  isAuthenticated(): boolean {
    return tokenManager.isAuthenticated();
  }
  
  getToken(): string | null {
    return tokenManager.getToken();
  }
}

export const authService = new AuthService();
