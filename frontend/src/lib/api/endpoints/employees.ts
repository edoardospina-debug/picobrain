import { api } from '../client';
import { 
  Employee, 
  Doctor,
  EmployeeCreateDTO, 
  EmployeeUpdateRequest, 
  EmployeeCreateResponse 
} from '@/types';

export const employeesApi = {
  // Get paginated list of employees
  list: async (params?: {
    page?: number;
    limit?: number;
    clinic_id?: string;
    role?: string;
    is_active?: boolean;
    sort_by?: string;
    sort_order?: 'asc' | 'desc';
  }) => {
    const queryParams = {
      skip: ((params?.page || 1) - 1) * (params?.limit || 20),
      limit: params?.limit || 20,
      ...(params?.clinic_id && { clinic_id: params.clinic_id }),
      ...(params?.role && { role: params.role }),
      ...(params?.is_active !== undefined && { is_active: params.is_active }),
      ...(params?.sort_by && { sort_by: params.sort_by }),
      ...(params?.sort_order && { sort_order: params.sort_order }),
    };
    
    // The backend returns an array
    const response = await api.get<Employee[]>('/employees', queryParams);
    
    // Transform to match DataTable's expected format
    return {
      items: response.data,
      total: response.data.length,
    };
  },

  // Get employees by role (convenience method for doctors, nurses, etc.)
  listByRole: async (role: string, params?: {
    page?: number;
    limit?: number;
    clinic_id?: string;
    is_active?: boolean;
  }) => {
    return employeesApi.list({ ...params, role });
  },

  // Get all doctors (convenience method)
  listDoctors: async (params?: {
    page?: number;
    limit?: number;
    clinic_id?: string;
    is_active?: boolean;
  }) => {
    const result = await employeesApi.list({ ...params, role: 'doctor' });
    // Type assertion to Doctor[]
    return {
      items: result.items as Doctor[],
      total: result.total,
    };
  },

  // Get single employee by ID
  get: async (id: string) => {
    const response = await api.get<Employee>(`/employees/${id}`);
    return response.data;
  },

  // Get employee by code
  getByCode: async (code: string) => {
    const response = await api.get<Employee>(`/employees/code/${code}`);
    return response.data;
  },

  // Get medical staff
  getMedicalStaff: async (clinic_id?: string) => {
    const params = clinic_id ? { clinic_id } : {};
    const response = await api.get<Employee[]>('/employees/medical-staff', params);
    return response.data;
  },

  // Create new employee with person (composite creation)
  create: async (data: EmployeeCreateDTO) => {
    const response = await api.post<EmployeeCreateResponse>('/employees/', data);
    return response.data;
  },

  // Update employee (only employee fields, not person fields)
  update: async (id: string, data: EmployeeUpdateRequest) => {
    const response = await api.put<Employee>(`/employees/${id}`, data);
    return response.data;
  },

  // Delete employee (soft delete by default)
  delete: async (id: string, softDelete: boolean = true) => {
    const response = await api.delete(`/employees/${id}`, {
      params: { soft_delete: softDelete }
    });
    return response.data;
  },

  // Export employees to CSV
  export: async (params?: {
    role?: string;
    clinic_id?: string;
    is_active?: boolean;
  }) => {
    const response = await api.get('/employees/export', {
      ...params,
      responseType: 'blob',
    });
    return response.data;
  },

  // Validate employee code uniqueness
  validateCode: async (code: string, excludeId?: string) => {
    const response = await api.get<{ is_unique: boolean }>('/employees/validate-code', {
      code,
      exclude_id: excludeId,
    });
    return response.data;
  },

  // Get employees by clinic
  getByClinic: async (clinicId: string, params?: {
    skip?: number;
    limit?: number;
    is_active?: boolean;
  }) => {
    const response = await api.get<Employee[]>(`/employees/clinic/${clinicId}`, params);
    return response.data;
  },
};

// Convenience export for doctors-specific operations
export const doctorsApi = {
  list: employeesApi.listDoctors,
  
  create: async (data: EmployeeCreateDTO) => {
    // Ensure role is set to doctor
    return employeesApi.create({
      ...data,
      role: 'doctor',
      can_perform_treatments: true, // Doctors can perform treatments
    });
  },
  
  update: employeesApi.update,
  delete: employeesApi.delete,
  get: employeesApi.get,
  getByCode: employeesApi.getByCode,
  
  export: async (params?: {
    clinic_id?: string;
    is_active?: boolean;
  }) => {
    return employeesApi.export({ ...params, role: 'doctor' });
  },
};
