import { apiRequest } from '@/lib/api';
import { 
  Person, 
  PersonCreate, 
  PersonUpdate,
  Clinic,
  ClinicCreate,
  ClinicUpdate,
  Client,
  ClientCreate,
  ClientUpdate,
  Employee,
  EmployeeCreate,
  EmployeeUpdate,
  User,
  UserCreate,
  UserUpdate,
  PaginatedResponse,
  FilterOptions
} from '@/types/api';

// Helper function to handle API responses
const handleResponse = async <T>(promise: Promise<any>): Promise<T> => {
  try {
    const response = await promise;
    return response;
  } catch (error: any) {
    // If it's a 404, return empty result
    if (error.message?.includes('Not Found')) {
      return { items: [], total: 0, page: 1, page_size: 20, total_pages: 0 } as any;
    }
    throw error;
  }
};

// Person Service
export class PersonService {
  private basePath = '/api/v1/persons';
  
  async getAll(filters?: FilterOptions): Promise<PaginatedResponse<Person>> {
    // For now, return the raw array response wrapped in pagination format
    try {
      const response = await apiRequest.get<Person[] | PaginatedResponse<Person>>(this.basePath, filters);
      
      // Check if response is already paginated
      if (response && typeof response === 'object' && 'items' in response) {
        return response as PaginatedResponse<Person>;
      }
      
      // If it's an array, wrap it in pagination format
      if (Array.isArray(response)) {
        return {
          items: response,
          total: response.length,
          page: 1,
          page_size: response.length,
          total_pages: 1
        };
      }
      
      // Default empty response
      return {
        items: [],
        total: 0,
        page: 1,
        page_size: 20,
        total_pages: 0
      };
    } catch (error) {
      console.error('Error fetching persons:', error);
      return {
        items: [],
        total: 0,
        page: 1,
        page_size: 20,
        total_pages: 0
      };
    }
  }
  
  async getById(id: string): Promise<Person> {
    return apiRequest.get<Person>(`${this.basePath}/${id}`);
  }
  
  async create(data: PersonCreate): Promise<Person> {
    return apiRequest.post<Person>(this.basePath, data);
  }
  
  async update(id: string, data: PersonUpdate): Promise<Person> {
    return apiRequest.put<Person>(`${this.basePath}/${id}`, data);
  }
  
  async delete(id: string): Promise<void> {
    return apiRequest.delete(`${this.basePath}/${id}`);
  }
  
  async search(query: string): Promise<Person[]> {
    return apiRequest.get<Person[]>(`${this.basePath}/search`, { q: query });
  }
}

// Clinic Service
export class ClinicService {
  private basePath = '/api/v1/clinics';
  
  async getAll(filters?: FilterOptions): Promise<PaginatedResponse<Clinic>> {
    try {
      const response = await apiRequest.get<Clinic[] | PaginatedResponse<Clinic>>(this.basePath, filters);
      
      if (response && typeof response === 'object' && 'items' in response) {
        return response as PaginatedResponse<Clinic>;
      }
      
      if (Array.isArray(response)) {
        return {
          items: response,
          total: response.length,
          page: 1,
          page_size: response.length,
          total_pages: 1
        };
      }
      
      return {
        items: [],
        total: 0,
        page: 1,
        page_size: 20,
        total_pages: 0
      };
    } catch (error) {
      console.error('Error fetching clinics:', error);
      return {
        items: [],
        total: 0,
        page: 1,
        page_size: 20,
        total_pages: 0
      };
    }
  }
  
  async getById(id: string): Promise<Clinic> {
    return apiRequest.get<Clinic>(`${this.basePath}/${id}`);
  }
  
  async create(data: ClinicCreate): Promise<Clinic> {
    return apiRequest.post<Clinic>(this.basePath, data);
  }
  
  async update(id: string, data: ClinicUpdate): Promise<Clinic> {
    return apiRequest.put<Clinic>(`${this.basePath}/${id}`, data);
  }
  
  async delete(id: string): Promise<void> {
    return apiRequest.delete(`${this.basePath}/${id}`);
  }
  
  async getActive(): Promise<Clinic[]> {
    return apiRequest.get<Clinic[]>(`${this.basePath}/active`);
  }
}

// Client Service
export class ClientService {
  private basePath = '/api/v1/clients';
  
  async getAll(filters?: FilterOptions): Promise<PaginatedResponse<Client>> {
    try {
      const response = await apiRequest.get<Client[] | PaginatedResponse<Client>>(this.basePath, filters);
      
      if (response && typeof response === 'object' && 'items' in response) {
        return response as PaginatedResponse<Client>;
      }
      
      if (Array.isArray(response)) {
        return {
          items: response,
          total: response.length,
          page: 1,
          page_size: response.length,
          total_pages: 1
        };
      }
      
      return {
        items: [],
        total: 0,
        page: 1,
        page_size: 20,
        total_pages: 0
      };
    } catch (error) {
      console.error('Error fetching clients:', error);
      return {
        items: [],
        total: 0,
        page: 1,
        page_size: 20,
        total_pages: 0
      };
    }
  }
  
  async getById(id: string): Promise<Client> {
    return apiRequest.get<Client>(`${this.basePath}/${id}`);
  }
  
  async create(data: ClientCreate): Promise<Client> {
    return apiRequest.post<Client>(this.basePath, data);
  }
  
  async update(id: string, data: ClientUpdate): Promise<Client> {
    return apiRequest.put<Client>(`${this.basePath}/${id}`, data);
  }
  
  async delete(id: string): Promise<void> {
    return apiRequest.delete(`${this.basePath}/${id}`);
  }
  
  async getByPersonId(personId: string): Promise<Client | null> {
    return apiRequest.get<Client | null>(`${this.basePath}/person/${personId}`);
  }
  
  async getByClinic(clinicId: string): Promise<Client[]> {
    return apiRequest.get<Client[]>(`${this.basePath}/clinic/${clinicId}`);
  }
}

// Employee Service
export class EmployeeService {
  private basePath = '/api/v1/employees';
  
  async getAll(filters?: FilterOptions): Promise<PaginatedResponse<Employee>> {
    try {
      const response = await apiRequest.get<Employee[] | PaginatedResponse<Employee>>(this.basePath, filters);
      
      if (response && typeof response === 'object' && 'items' in response) {
        return response as PaginatedResponse<Employee>;
      }
      
      if (Array.isArray(response)) {
        return {
          items: response,
          total: response.length,
          page: 1,
          page_size: response.length,
          total_pages: 1
        };
      }
      
      return {
        items: [],
        total: 0,
        page: 1,
        page_size: 20,
        total_pages: 0
      };
    } catch (error) {
      console.error('Error fetching employees:', error);
      return {
        items: [],
        total: 0,
        page: 1,
        page_size: 20,
        total_pages: 0
      };
    }
  }
  
  async getById(id: string): Promise<Employee> {
    return apiRequest.get<Employee>(`${this.basePath}/${id}`);
  }
  
  async create(data: EmployeeCreate): Promise<Employee> {
    return apiRequest.post<Employee>(this.basePath, data);
  }
  
  async update(id: string, data: EmployeeUpdate): Promise<Employee> {
    return apiRequest.put<Employee>(`${this.basePath}/${id}`, data);
  }
  
  async delete(id: string): Promise<void> {
    return apiRequest.delete(`${this.basePath}/${id}`);
  }
  
  async getByPersonId(personId: string): Promise<Employee | null> {
    return apiRequest.get<Employee | null>(`${this.basePath}/person/${personId}`);
  }
  
  async getByClinic(clinicId: string): Promise<Employee[]> {
    return apiRequest.get<Employee[]>(`${this.basePath}/clinic/${clinicId}`);
  }
  
  async getByRole(role: string): Promise<Employee[]> {
    return apiRequest.get<Employee[]>(`${this.basePath}/role/${role}`);
  }
  
  async getDoctors(clinicId?: string): Promise<Employee[]> {
    const params = clinicId ? { clinic_id: clinicId } : {};
    return apiRequest.get<Employee[]>(`${this.basePath}/doctors`, params);
  }
}

// User Service
export class UserService {
  private basePath = '/api/v1/users';
  
  async getAll(filters?: FilterOptions): Promise<PaginatedResponse<User>> {
    try {
      const response = await apiRequest.get<User[] | PaginatedResponse<User>>(this.basePath, filters);
      
      if (response && typeof response === 'object' && 'items' in response) {
        return response as PaginatedResponse<User>;
      }
      
      if (Array.isArray(response)) {
        return {
          items: response,
          total: response.length,
          page: 1,
          page_size: response.length,
          total_pages: 1
        };
      }
      
      return {
        items: [],
        total: 0,
        page: 1,
        page_size: 20,
        total_pages: 0
      };
    } catch (error) {
      console.error('Error fetching users:', error);
      return {
        items: [],
        total: 0,
        page: 1,
        page_size: 20,
        total_pages: 0
      };
    }
  }
  
  async getById(id: string): Promise<User> {
    return apiRequest.get<User>(`${this.basePath}/${id}`);
  }
  
  async create(data: UserCreate): Promise<User> {
    return apiRequest.post<User>(this.basePath, data);
  }
  
  async update(id: string, data: UserUpdate): Promise<User> {
    return apiRequest.put<User>(`${this.basePath}/${id}`, data);
  }
  
  async delete(id: string): Promise<void> {
    return apiRequest.delete(`${this.basePath}/${id}`);
  }
  
  async changePassword(id: string, oldPassword: string, newPassword: string): Promise<void> {
    return apiRequest.post(`${this.basePath}/${id}/change-password`, {
      old_password: oldPassword,
      new_password: newPassword,
    });
  }
  
  async resetPassword(id: string, newPassword: string): Promise<void> {
    return apiRequest.post(`${this.basePath}/${id}/reset-password`, {
      password: newPassword,
    });
  }
}

// Export service instances
export const personService = new PersonService();
export const clinicService = new ClinicService();
export const clientService = new ClientService();
export const employeeService = new EmployeeService();
export const userService = new UserService();
