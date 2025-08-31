// User and Authentication Types
export interface User {
  id: string;
  username: string;
  email: string;
  is_active: boolean;
  is_superuser: boolean;
  role: UserRole;
  created_at: string;
  updated_at: string;
  person?: Person;
}

export type UserRole = 'admin' | 'manager' | 'staff' | 'medical' | 'finance' | 'readonly';

export interface LoginRequest {
  username: string;
  password: string;
}

export interface LoginResponse {
  access_token: string;
  refresh_token?: string;
  token_type: string;
  user: User;
}

// Clinic Types
export interface Clinic {
  id: string;
  code: string;
  name: string;
  functional_currency: string;
  address_line_1?: string;
  address_line_2?: string;
  city?: string;
  state_province?: string;
  postal_code?: string;
  country_code?: string;
  phone_country_code?: string;
  phone_number?: string;
  email?: string;
  tax_id?: string;
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

export interface ClinicCreateRequest {
  code: string;
  name: string;
  functional_currency: string;
  address_line_1?: string;
  address_line_2?: string;
  city?: string;
  state_province?: string;
  postal_code?: string;
  country_code?: string;
  phone_country_code?: string;
  phone_number?: string;
  email?: string;
  tax_id?: string;
  is_active?: boolean;
}

export interface ClinicUpdateRequest extends Partial<ClinicCreateRequest> {}

// Person Types
export interface Person {
  id: string;
  first_name: string;
  last_name: string;
  middle_name?: string;
  email?: string;
  phone_mobile_country_code?: string;
  phone_mobile_number?: string;
  phone_home_country_code?: string;
  phone_home_number?: string;
  dob?: string;
  gender?: 'M' | 'F' | 'O' | 'N';
  nationality?: string;
  id_type?: string;
  id_number?: string;
  created_at: string;
  updated_at: string;
}

// Employee Types
export type EmployeeRole = 'doctor' | 'nurse' | 'receptionist' | 'manager' | 'finance' | 'admin';

export interface Employee {
  id: string;
  person_id: string;
  employee_code?: string;
  primary_clinic_id: string;
  role: EmployeeRole;
  specialization?: string;
  license_number?: string;
  license_expiry?: string;
  hire_date: string;
  termination_date?: string;
  base_salary_minor?: number;
  salary_currency?: string;
  commission_rate?: number;
  is_active: boolean;
  can_perform_treatments: boolean;
  created_at: string;
  updated_at: string;
  person?: Person;
  clinic?: Clinic;
}

// Doctor-specific interface (extends Employee)
export interface Doctor extends Employee {
  role: 'doctor';
  specialization: string;
  license_number: string;
  license_expiry?: string;
}

// Composite creation DTOs
export interface EmployeeCreateDTO {
  // Person fields
  first_name: string;
  last_name: string;
  middle_name?: string;
  email?: string;
  phone_mobile_country_code?: string;
  phone_mobile_number?: string;
  phone_home_country_code?: string;
  phone_home_number?: string;
  dob?: string;
  gender?: 'M' | 'F' | 'O' | 'N';
  nationality?: string;
  id_type?: string;
  id_number?: string;
  
  // Employee fields
  employee_code?: string;
  primary_clinic_id: string;
  role: EmployeeRole;
  specialization?: string;
  license_number?: string;
  license_expiry?: string;
  hire_date: string;
  termination_date?: string;
  base_salary_minor?: number;
  salary_currency?: string;
  commission_rate?: number;
  is_active?: boolean;
  can_perform_treatments?: boolean;
}

export interface EmployeeCreateResponse {
  person: Person;
  employee: Employee;
  message: string;
}

export interface EmployeeUpdateRequest {
  employee_code?: string;
  primary_clinic_id?: string;
  role?: EmployeeRole;
  specialization?: string;
  license_number?: string;
  license_expiry?: string;
  hire_date?: string;
  termination_date?: string;
  base_salary_minor?: number;
  salary_currency?: string;
  commission_rate?: number;
  is_active?: boolean;
  can_perform_treatments?: boolean;
}

// Client Types
export interface Client {
  id: string;
  person_id: string;
  client_code: string;
  registration_date: string;
  insurance_provider?: string;
  insurance_policy_number?: string;
  emergency_contact_name?: string;
  emergency_contact_phone?: string;
  notes?: string;
  is_active: boolean;
  clinic_id?: string;
  created_at: string;
  updated_at: string;
  person?: Person;
  clinic?: Clinic;
}

// Common Types
export interface PaginatedResponse<T> {
  items: T[];
  total: number;
  page: number;
  limit: number;
  pages: number;
}

export interface ApiError {
  detail: string;
  status_code?: number;
  errors?: Record<string, string[]>;
}

export interface AuditLog {
  entity_type: string;
  entity_id: string;
  action: 'create' | 'update' | 'delete';
  user_id: string;
  timestamp: string;
  changes?: Record<string, any>;
  ip_address?: string;
  user_agent?: string;
}

// Form Types
export interface FormSection {
  title: string;
  fields: string[];
  columns?: 1 | 2 | 3;
  collapsible?: boolean;
  defaultCollapsed?: boolean;
}

// Table Types
export interface TableColumn<T> {
  key: keyof T | string;
  title: string;
  dataIndex?: string | string[];
  width?: number | string;
  fixed?: 'left' | 'right';
  sorter?: boolean;
  filters?: Array<{ text: string; value: any }>;
  render?: (value: any, record: T) => React.ReactNode;
}

export interface TableAction<T> {
  key: string;
  label: string;
  icon?: React.ReactNode;
  onClick: (record: T) => void;
  hidden?: (record: T) => boolean;
  danger?: boolean;
}

// Permission Types
export interface Permission {
  resource: string;
  action: string;
  role: UserRole;
  allowed: boolean;
}

export interface PermissionCheck {
  resource: string;
  action: 'view' | 'create' | 'edit' | 'delete' | 'export';
}
