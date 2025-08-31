'use client';

import React, { createContext, useContext, useState, useEffect, useCallback } from 'react';
import { useRouter } from 'next/navigation';
import { message } from 'antd';
import { api } from '@/lib/api/client';
import { tokenManager } from '@/lib/api/client';
import axios from 'axios';
import { User, LoginRequest, LoginResponse } from '@/types';

interface AuthContextType {
  user: User | null;
  isLoading: boolean;
  isAuthenticated: boolean;
  login: (credentials: LoginRequest) => Promise<void>;
  logout: () => Promise<void>;
  checkAuth: () => Promise<void>;
  hasPermission: (resource: string, action: string) => boolean;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

// Permission matrix (will be replaced by dynamic permissions from backend)
const PERMISSION_MATRIX: Record<string, Record<string, string[]>> = {
  clinics: {
    view: ['admin', 'manager', 'staff', 'medical', 'finance', 'readonly'],
    create: ['admin', 'manager'],
    edit: ['admin', 'manager'],
    delete: ['admin'],
    export: ['admin', 'manager', 'finance'],
  },
  employees: {
    view: ['admin', 'manager', 'staff', 'finance', 'readonly'],
    create: ['admin', 'manager'],
    edit: ['admin', 'manager'],
    delete: ['admin'],
    export: ['admin', 'manager', 'finance'],
  },
  clients: {
    view: ['admin', 'manager', 'staff', 'medical', 'readonly'],
    create: ['admin', 'manager', 'staff', 'medical'],
    edit: ['admin', 'manager', 'staff', 'medical'],
    delete: ['admin'],
    export: ['admin', 'manager', 'medical'],
  },
  users: {
    view: ['admin', 'manager'],
    create: ['admin'],
    edit: ['admin'],
    delete: ['admin'],
    export: ['admin'],
  },
};

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const router = useRouter();

  const checkAuth = useCallback(async () => {
    try {
      setIsLoading(true);
      const response = await api.get<User>('/auth/me');
      setUser(response.data);
    } catch (error) {
      console.error('Auth check failed:', error);
      setUser(null);
      // Don't redirect here, let the route protection handle it
    } finally {
      setIsLoading(false);
    }
  }, []);

  const login = useCallback(async (credentials: LoginRequest) => {
    try {
      // The OAuth2PasswordRequestForm expects form data, not JSON
      const formData = new URLSearchParams();
      formData.append('username', credentials.username);
      formData.append('password', credentials.password);
      
      const response = await axios.post<LoginResponse>(
        'http://localhost:8000/api/v1/auth/login',
        formData,
        {
          headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
          },
        }
      );
      
      const { access_token, user } = response.data;
      
      // Store the token
      tokenManager.setTokens(access_token);
      
      // Set the user
      setUser(user);
      
      // Success message
      message.success('Login successful!');
      
      // Redirect to dashboard
      router.push('/clinics');
    } catch (error: any) {
      console.error('Login failed:', error);
      const errorMessage = error.response?.data?.detail || 'Invalid username or password';
      message.error(errorMessage);
      throw error;
    }
  }, [router]);

  const logout = useCallback(async () => {
    try {
      await api.post('/auth/logout');
    } catch (error) {
      console.error('Logout error:', error);
    } finally {
      // Clear tokens and user state regardless
      tokenManager.clearTokens();
      setUser(null);
      message.success('Logged out successfully');
      router.push('/login');
    }
  }, [router]);

  const hasPermission = useCallback((resource: string, action: string): boolean => {
    if (!user) return false;
    if (user.is_superuser) return true; // Superuser has all permissions
    
    const allowedRoles = PERMISSION_MATRIX[resource]?.[action];
    if (!allowedRoles) return false;
    
    return allowedRoles.includes(user.role);
  }, [user]);

  // Check authentication on mount
  useEffect(() => {
    const token = tokenManager.getAccessToken();
    if (token) {
      checkAuth();
    } else {
      setIsLoading(false);
    }
  }, [checkAuth]);

  const value: AuthContextType = {
    user,
    isLoading,
    isAuthenticated: !!user,
    login,
    logout,
    checkAuth,
    hasPermission,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
}

// HOC for protected routes
export function withAuth<P extends object>(
  Component: React.ComponentType<P>,
  requiredPermission?: { resource: string; action: string }
) {
  return function ProtectedComponent(props: P) {
    const { isAuthenticated, isLoading, hasPermission } = useAuth();
    const router = useRouter();

    useEffect(() => {
      if (!isLoading && !isAuthenticated) {
        router.push('/login');
      } else if (
        !isLoading &&
        isAuthenticated &&
        requiredPermission &&
        !hasPermission(requiredPermission.resource, requiredPermission.action)
      ) {
        message.error('You do not have permission to access this page');
        router.push('/');
      }
    }, [isLoading, isAuthenticated, router]);

    if (isLoading) {
      return <div>Loading...</div>;
    }

    if (!isAuthenticated) {
      return null;
    }

    if (
      requiredPermission &&
      !hasPermission(requiredPermission.resource, requiredPermission.action)
    ) {
      return null;
    }

    return <Component {...props} />;
  };
}
