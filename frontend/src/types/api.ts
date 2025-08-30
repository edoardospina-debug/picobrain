// API Types matching the FastAPI backend schemas

// Enums
export enum GenderType {
  M = 'M',
  F = 'F',
  O = 'O',
  N = 'N',
}

export enum EmployeeRole {
  DOCTOR = 'doctor',
  NURSE = 'nurse',
  RECEPTIONIST = 'receptionist',
  MANAGER = 'manager',
  FINANCE = 'finance',
  ADMIN = 'admin',
}

export enum UserRole {
  ADMIN = 'admin',
  USER = 'user',
  VIEWER = 'viewer',
}

// Base Interfaces
export interface Person {
  id: string;
  first_name: string;
  last_name: string;
  email?: string | null;
  phone_mobile?: string | null;
  dob?: string | null;
  gender?: GenderType | null;
}

export interface PersonCreate {
  first_name: string;
  last_name: string;
  email?: string | null;
  phone_mobile?: string | null;
  dob?: string | null;
  gender?: GenderType | null;
}

export interface PersonUpdate {
  first_name?: string;
  last_name?: string;
  email?: string | null;
  phone_mobile?: string | null;
  dob?: string | null;
  gender?: GenderType | null;
}

// Clinic Types
export interface Clinic {
  id: string;
  code: string;
  name: string;
  functional_currency: string;
  city?: string | null;
  country_code?: string | null;
  is_active: boolean;
}

export interface ClinicCreate {
  code: string;
  name: string;
  functional_currency: string;
  city?: string | null;
  country_code?: string | null;
}

export interface ClinicUpdate {
  name?: string;
  functional_currency?: string;
  city?: string | null;
  country_code?: string | null;
  is_active?: boolean;
}

// Client Types
export interface Client {
  id: string;
  person_id: string;
  client_code?: string | null;
  preferred_clinic_id?: string | null;
  acquisition_date?: string | null;
  is_active: boolean;
  person?: Person | null;
}

export interface ClientCreate {
  person_id: string;
  client_code?: string | null;
  preferred_clinic_id?: string | null;
}

export interface ClientUpdate {
  client_code?: string | null;
  preferred_clinic_id?: string | null;
  is_active?: boolean;
}

// Employee Types
export interface Employee {
  id: string;
  person_id: string;
  employee_code?: string | null;
  primary_clinic_id: string;
  role: EmployeeRole;
  license_number?: string | null;
  can_perform_treatments: boolean;
  is_active: boolean;
  person?: Person | null;
}

export interface EmployeeCreate {
  person_id: string;
  employee_code?: string | null;
  primary_clinic_id: string;
  role: EmployeeRole;
  license_number?: string | null;
  can_perform_treatments?: boolean;
}

export interface EmployeeUpdate {
  employee_code?: string | null;
  primary_clinic_id?: string;
  role?: EmployeeRole;
  license_number?: string | null;
  can_perform_treatments?: boolean;
  is_active?: boolean;
}

// User Types
export interface User {
  id: string;
  username: string;
  role: string;
  is_active: boolean;
  person_id?: string | null;
  person?: Person | null;
}

export interface UserCreate {
  username: string;
  password: string;
  role?: string;
  is_active?: boolean;
  person_id?: string | null;
}

export interface UserUpdate {
  username?: string;
  password?: string;
  role?: string;
  is_active?: boolean;
  person_id?: string | null;
}

// Authentication Types
export interface LoginRequest {
  username: string;
  password: string;
}

export interface TokenResponse {
  access_token: string;
  refresh_token?: string;
  token_type: string;
  expires_in?: number;
  user?: {
    id: string;
    username: string;
    role: string;
    person_id?: string | null;
  };
}

export interface AuthUser {
  id: string;
  username: string;
  role: string;
  person?: Person | null;
}

// API Response Types
export interface ApiResponse<T> {
  data: T;
  message?: string;
  success: boolean;
}

export interface PaginatedResponse<T> {
  items: T[];
  total: number;
  page: number;
  page_size: number;
  total_pages: number;
}

export interface ApiError {
  detail: string;
  status_code?: number;
  field?: string;
}

// Form State Types
export interface FormState {
  isSubmitting: boolean;
  isValid: boolean;
  errors: Record<string, string>;
}

// Table Column Configuration
export interface TableColumn<T> {
  key: keyof T | string;
  label: string;
  sortable?: boolean;
  width?: string;
  render?: (value: any, row: T) => React.ReactNode;
}

// Filter Types
export interface FilterOptions {
  search?: string;
  status?: 'active' | 'inactive' | 'all';
  role?: string;
  clinic_id?: string;
  date_from?: string;
  date_to?: string;
  page?: number;
  page_size?: number;
  sort_by?: string;
  sort_order?: 'asc' | 'desc';
}
