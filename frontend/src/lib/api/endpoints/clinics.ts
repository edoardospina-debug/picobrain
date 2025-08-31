import { api } from '../client';
import { 
  Clinic, 
  ClinicCreateRequest, 
  ClinicUpdateRequest, 
  PaginatedResponse 
} from '@/types';

export const clinicsApi = {
  // Get paginated list of clinics
  list: async (params?: {
    page?: number;
    limit?: number;
    search?: string;
    is_active?: boolean;
    sort_by?: string;
    sort_order?: 'asc' | 'desc';
  }) => {
    console.log('🔍 clinicsApi.list called with params:', params);
    
    // Build query parameters for the backend
    const queryParams = {
      skip: ((params?.page || 1) - 1) * (params?.limit || 20),
      limit: params?.limit || 20,
      ...(params?.search && { search: params.search }),
      ...(params?.is_active !== undefined && { is_active: params.is_active }),
      ...(params?.sort_by && { sort_by: params.sort_by }),
      ...(params?.sort_order && { sort_order: params.sort_order }),
    };
    
    console.log('📤 Sending query params to backend:', queryParams);
    
    // The backend returns an array, but DataTable expects { items, total }
    const response = await api.get<Clinic[]>('/clinics', queryParams);
    
    console.log('📦 Raw response from backend:', response);
    console.log('📊 response.data type:', Array.isArray(response.data) ? 'Array' : typeof response.data);
    console.log('📊 response.data length:', response.data?.length);
    
    // Transform the response to match DataTable's expected format
    const transformedData = {
      items: response.data,
      total: response.data.length, // This is not ideal, but works for now
      // In a proper implementation, the backend should return total count
    };
    
    console.log('✅ Transformed data:', transformedData);
    console.log('✅ Has items?', 'items' in transformedData);
    console.log('✅ Has total?', 'total' in transformedData);
    
    return transformedData;
  },

  // Get single clinic by ID
  get: async (id: string) => {
    const response = await api.get<Clinic>(`/clinics/${id}`);
    return response.data;
  },

  // Create new clinic
  create: async (data: ClinicCreateRequest) => {
    const response = await api.post<Clinic>('/clinics', data);
    return response.data;
  },

  // Update clinic
  update: async (id: string, data: ClinicUpdateRequest) => {
    const response = await api.put<Clinic>(`/clinics/${id}`, data);
    return response.data;
  },

  // Delete clinic (soft delete)
  delete: async (id: string) => {
    const response = await api.delete(`/clinics/${id}`);
    return response.data;
  },

  // Export clinics to CSV
  export: async (params?: {
    search?: string;
    is_active?: boolean;
  }) => {
    const response = await api.get('/clinics/export', {
      ...params,
      responseType: 'blob',
    });
    return response.data;
  },

  // Validate clinic code uniqueness
  validateCode: async (code: string, excludeId?: string) => {
    const response = await api.get<{ is_unique: boolean }>('/clinics/validate-code', {
      code,
      exclude_id: excludeId,
    });
    return response.data;
  },
};
