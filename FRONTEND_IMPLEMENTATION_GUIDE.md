# PicoBrain Frontend Development Guide - Phase 3

## Environment Configuration Files

### 1. Create `.env.local`
```env
NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1
NEXT_PUBLIC_APP_NAME=PicoBrain Healthcare System
NEXT_PUBLIC_APP_VERSION=1.0.0
```

### 2. Create `src/lib/config.ts`
```typescript
export const config = {
  apiUrl: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1',
  appName: process.env.NEXT_PUBLIC_APP_NAME || 'PicoBrain',
  appVersion: process.env.NEXT_PUBLIC_APP_VERSION || '1.0.0',
  tokenKey: 'picobrain_access_token',
  refreshTokenKey: 'picobrain_refresh_token',
  userKey: 'picobrain_user',
};
```

### 3. Create `src/types/index.ts`
```typescript
// API Response Types
export interface ApiResponse<T> {
  data?: T;
  error?: string;
  message?: string;
}

// Auth Types
export interface LoginRequest {
  username: string;
  password: string;
}

export interface LoginResponse {
  access_token: string;
  refresh_token: string;
  token_type: string;
  user: {
    id: string;
    username: string;
    role: string;
    person_id?: string;
  };
}

export interface User {
  id: string;
  username: string;
  role: 'admin' | 'manager' | 'staff' | 'medical' | 'finance' | 'readonly';
  is_active: boolean;
  person_id?: string;
  person?: Person;
}

// Person Types
export interface Person {
  id: string;
  first_name: string;
  last_name: string;
  email?: string;
  phone_mobile?: string;
  dob?: string;
  gender?: 'M' | 'F' | 'O' | 'N';
}

export interface PersonCreate {
  first_name: string;
  last_name: string;
  email?: string;
  phone_mobile?: string;
  dob?: string;
  gender?: 'M' | 'F' | 'O' | 'N';
}

// Clinic Types
export interface Clinic {
  id: string;
  code: string;
  name: string;
  functional_currency: string;
  city?: string;
  country_code?: string;
  is_active: boolean;
}

export interface ClinicCreate {
  code: string;
  name: string;
  functional_currency: string;
  city?: string;
  country_code?: string;
}
```

## API Integration Layer

### 4. Create `src/lib/api/client.ts`
```typescript
import axios, { AxiosError, AxiosInstance } from 'axios';
import { config } from '@/lib/config';
import { authStore } from '@/lib/stores/authStore';
import toast from 'react-hot-toast';

class ApiClient {
  private client: AxiosInstance;
  private isRefreshing = false;
  private refreshSubscribers: ((token: string) => void)[] = [];

  constructor() {
    this.client = axios.create({
      baseURL: config.apiUrl,
      headers: {
        'Content-Type': 'application/json',
      },
    });

    this.setupInterceptors();
  }

  private setupInterceptors() {
    // Request interceptor to add token
    this.client.interceptors.request.use(
      (config) => {
        const token = authStore.getState().accessToken;
        if (token) {
          config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
      },
      (error) => Promise.reject(error)
    );

    // Response interceptor for token refresh
    this.client.interceptors.response.use(
      (response) => response,
      async (error: AxiosError) => {
        const originalRequest = error.config as any;

        if (error.response?.status === 401 && !originalRequest._retry) {
          if (!this.isRefreshing) {
            this.isRefreshing = true;
            originalRequest._retry = true;

            try {
              const refreshToken = authStore.getState().refreshToken;
              if (!refreshToken) {
                throw new Error('No refresh token');
              }

              const response = await axios.post(`${config.apiUrl}/auth/refresh`, {
                refresh_token: refreshToken,
              });

              const { access_token } = response.data;
              authStore.getState().setTokens(access_token, refreshToken);

              this.isRefreshing = false;
              this.onRefreshed(access_token);
              this.refreshSubscribers = [];

              return this.client(originalRequest);
            } catch (refreshError) {
              this.isRefreshing = false;
              authStore.getState().logout();
              window.location.href = '/login';
              return Promise.reject(refreshError);
            }
          }

          return new Promise((resolve) => {
            this.subscribeTokenRefresh((token: string) => {
              originalRequest.headers.Authorization = `Bearer ${token}`;
              resolve(this.client(originalRequest));
            });
          });
        }

        // Show error toast for other errors
        if (error.response?.status === 403) {
          toast.error('You do not have permission to perform this action');
        } else if (error.response?.status === 500) {
          toast.error('Server error. Please try again later.');
        }

        return Promise.reject(error);
      }
    );
  }

  private subscribeTokenRefresh(cb: (token: string) => void) {
    this.refreshSubscribers.push(cb);
  }

  private onRefreshed(token: string) {
    this.refreshSubscribers.forEach((cb) => cb(token));
  }

  get instance() {
    return this.client;
  }
}

export const apiClient = new ApiClient().instance;
```

### 5. Create `src/lib/api/auth.ts`
```typescript
import { apiClient } from './client';
import { LoginRequest, LoginResponse, User } from '@/types';

export const authApi = {
  login: async (credentials: LoginRequest): Promise<LoginResponse> => {
    const formData = new URLSearchParams();
    formData.append('username', credentials.username);
    formData.append('password', credentials.password);

    const response = await apiClient.post('/auth/login', formData, {
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
    });
    return response.data;
  },

  me: async (): Promise<User> => {
    const response = await apiClient.get('/auth/me');
    return response.data;
  },

  logout: async (): Promise<void> => {
    await apiClient.post('/auth/logout');
  },

  refresh: async (refreshToken: string): Promise<{ access_token: string }> => {
    const response = await apiClient.post('/auth/refresh', {
      refresh_token: refreshToken,
    });
    return response.data;
  },
};
```

### 6. Create `src/lib/api/persons.ts`
```typescript
import { apiClient } from './client';
import { Person, PersonCreate } from '@/types';

export const personsApi = {
  list: async (skip = 0, limit = 100): Promise<Person[]> => {
    const response = await apiClient.get('/persons/', {
      params: { skip, limit },
    });
    return response.data;
  },

  get: async (id: string): Promise<Person> => {
    const response = await apiClient.get(`/persons/${id}`);
    return response.data;
  },

  create: async (data: PersonCreate): Promise<Person> => {
    const response = await apiClient.post('/persons/', data);
    return response.data;
  },

  update: async (id: string, data: Partial<PersonCreate>): Promise<Person> => {
    const response = await apiClient.put(`/persons/${id}`, data);
    return response.data;
  },

  delete: async (id: string): Promise<void> => {
    await apiClient.delete(`/persons/${id}`);
  },
};
```

## State Management

### 7. Create `src/lib/stores/authStore.ts`
```typescript
import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import Cookies from 'js-cookie';
import { config } from '@/lib/config';
import { User } from '@/types';

interface AuthState {
  user: User | null;
  accessToken: string | null;
  refreshToken: string | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  setUser: (user: User | null) => void;
  setTokens: (accessToken: string, refreshToken: string) => void;
  logout: () => void;
  setLoading: (loading: boolean) => void;
}

export const authStore = create<AuthState>()(
  persist(
    (set) => ({
      user: null,
      accessToken: null,
      refreshToken: null,
      isAuthenticated: false,
      isLoading: true,

      setUser: (user) => {
        set({ user, isAuthenticated: !!user });
      },

      setTokens: (accessToken, refreshToken) => {
        Cookies.set(config.tokenKey, accessToken, { expires: 7 });
        Cookies.set(config.refreshTokenKey, refreshToken, { expires: 30 });
        set({ accessToken, refreshToken, isAuthenticated: true });
      },

      logout: () => {
        Cookies.remove(config.tokenKey);
        Cookies.remove(config.refreshTokenKey);
        set({
          user: null,
          accessToken: null,
          refreshToken: null,
          isAuthenticated: false,
        });
      },

      setLoading: (loading) => set({ isLoading: loading }),
    }),
    {
      name: 'auth-storage',
      partialize: (state) => ({
        user: state.user,
        isAuthenticated: state.isAuthenticated,
      }),
    }
  )
);
```

## Authentication Components

### 8. Create `src/components/auth/LoginForm.tsx`
```typescript
'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import * as z from 'zod';
import toast from 'react-hot-toast';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card';
import { authApi } from '@/lib/api/auth';
import { authStore } from '@/lib/stores/authStore';

const loginSchema = z.object({
  username: z.string().email('Invalid email address'),
  password: z.string().min(1, 'Password is required'),
});

type LoginFormData = z.infer<typeof loginSchema>;

export function LoginForm() {
  const router = useRouter();
  const [isLoading, setIsLoading] = useState(false);
  const { setUser, setTokens } = authStore();

  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<LoginFormData>({
    resolver: zodResolver(loginSchema),
    defaultValues: {
      username: '',
      password: '',
    },
  });

  const onSubmit = async (data: LoginFormData) => {
    setIsLoading(true);
    try {
      const response = await authApi.login(data);
      setTokens(response.access_token, response.refresh_token);
      
      // Fetch user details
      const user = await authApi.me();
      setUser(user);
      
      toast.success('Login successful!');
      router.push('/dashboard');
    } catch (error: any) {
      toast.error(error.response?.data?.detail || 'Login failed');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <Card className="w-full max-w-md">
      <CardHeader>
        <CardTitle className="text-2xl text-center">
          PicoBrain Healthcare System
        </CardTitle>
      </CardHeader>
      <CardContent>
        <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
          <div className="space-y-2">
            <Label htmlFor="username">Email</Label>
            <Input
              id="username"
              type="email"
              placeholder="admin@picobrain.com"
              {...register('username')}
              disabled={isLoading}
            />
            {errors.username && (
              <p className="text-sm text-red-500">{errors.username.message}</p>
            )}
          </div>

          <div className="space-y-2">
            <Label htmlFor="password">Password</Label>
            <Input
              id="password"
              type="password"
              placeholder="Enter your password"
              {...register('password')}
              disabled={isLoading}
            />
            {errors.password && (
              <p className="text-sm text-red-500">{errors.password.message}</p>
            )}
          </div>

          <Button type="submit" className="w-full" disabled={isLoading}>
            {isLoading ? 'Logging in...' : 'Login'}
          </Button>
        </form>
      </CardContent>
    </Card>
  );
}
```

### 9. Create `src/middleware.ts`
```typescript
import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';

export function middleware(request: NextRequest) {
  const token = request.cookies.get('picobrain_access_token');
  const isAuthPage = request.nextUrl.pathname.startsWith('/login');
  const isPublicPage = request.nextUrl.pathname === '/';

  if (!token && !isAuthPage && !isPublicPage) {
    return NextResponse.redirect(new URL('/login', request.url));
  }

  if (token && isAuthPage) {
    return NextResponse.redirect(new URL('/dashboard', request.url));
  }

  return NextResponse.next();
}

export const config = {
  matcher: ['/((?!api|_next/static|_next/image|favicon.ico).*)'],
};
```

## Page Components

### 10. Create `src/app/(auth)/login/page.tsx`
```typescript
import { LoginForm } from '@/components/auth/LoginForm';

export default function LoginPage() {
  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50">
      <LoginForm />
    </div>
  );
}
```

### 11. Create `src/app/(dashboard)/layout.tsx`
```typescript
'use client';

import { useEffect } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import { Button } from '@/components/ui/button';
import { authStore } from '@/lib/stores/authStore';
import { authApi } from '@/lib/api/auth';
import toast from 'react-hot-toast';

export default function DashboardLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const router = useRouter();
  const { user, logout, isAuthenticated } = authStore();

  const handleLogout = async () => {
    try {
      await authApi.logout();
      logout();
      router.push('/login');
      toast.success('Logged out successfully');
    } catch (error) {
      logout();
      router.push('/login');
    }
  };

  useEffect(() => {
    if (!isAuthenticated) {
      router.push('/login');
    }
  }, [isAuthenticated, router]);

  if (!isAuthenticated) return null;

  return (
    <div className="min-h-screen bg-gray-50">
      <nav className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-16">
            <div className="flex">
              <div className="flex-shrink-0 flex items-center">
                <h1 className="text-xl font-semibold">PicoBrain</h1>
              </div>
              <div className="hidden sm:ml-6 sm:flex sm:space-x-8">
                <Link
                  href="/dashboard"
                  className="inline-flex items-center px-1 pt-1 text-sm font-medium"
                >
                  Dashboard
                </Link>
                <Link
                  href="/persons"
                  className="inline-flex items-center px-1 pt-1 text-sm font-medium"
                >
                  Persons
                </Link>
                <Link
                  href="/clinics"
                  className="inline-flex items-center px-1 pt-1 text-sm font-medium"
                >
                  Clinics
                </Link>
                {user?.role === 'admin' && (
                  <Link
                    href="/users"
                    className="inline-flex items-center px-1 pt-1 text-sm font-medium"
                  >
                    Users
                  </Link>
                )}
              </div>
            </div>
            <div className="flex items-center space-x-4">
              <span className="text-sm text-gray-500">
                {user?.username}
              </span>
              <Button onClick={handleLogout} variant="outline" size="sm">
                Logout
              </Button>
            </div>
          </div>
        </div>
      </nav>
      <main className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
        {children}
      </main>
    </div>
  );
}
```

### 12. Create `src/app/(dashboard)/dashboard/page.tsx`
```typescript
'use client';

import { useEffect, useState } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { personsApi } from '@/lib/api/persons';
import { clinicsApi } from '@/lib/api/clinics';
import { authStore } from '@/lib/stores/authStore';

export default function DashboardPage() {
  const { user } = authStore();
  const [stats, setStats] = useState({
    persons: 0,
    clinics: 0,
    users: 0,
  });

  useEffect(() => {
    const fetchStats = async () => {
      try {
        const [persons, clinics] = await Promise.all([
          personsApi.list(0, 1),
          clinicsApi.list(0, 1),
        ]);
        setStats({
          persons: persons.length,
          clinics: clinics.length,
          users: 0, // Will be fetched if admin
        });
      } catch (error) {
        console.error('Failed to fetch stats:', error);
      }
    };
    fetchStats();
  }, []);

  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-bold">Dashboard</h1>
      <p className="text-gray-600">Welcome back, {user?.username}!</p>
      
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <Card>
          <CardHeader>
            <CardTitle>Total Persons</CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-3xl font-bold">{stats.persons}</p>
          </CardContent>
        </Card>
        
        <Card>
          <CardHeader>
            <CardTitle>Total Clinics</CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-3xl font-bold">{stats.clinics}</p>
          </CardContent>
        </Card>
        
        {user?.role === 'admin' && (
          <Card>
            <CardHeader>
              <CardTitle>Total Users</CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-3xl font-bold">{stats.users}</p>
            </CardContent>
          </Card>
        )}
      </div>
    </div>
  );
}
```
