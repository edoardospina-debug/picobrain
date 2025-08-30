'use client';

import { useState, useEffect } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { employeeService, personService, clinicService } from '@/services/api.service';
import { Employee, EmployeeCreate, EmployeeUpdate, EmployeeRole, Person, Clinic } from '@/types/api';
import { toast } from '@/components/ui/toaster';

export default function EmployeesPage() {
  const queryClient = useQueryClient();
  const [searchTerm, setSearchTerm] = useState('');
  const [currentPage, setCurrentPage] = useState(1);
  const [isCreateModalOpen, setIsCreateModalOpen] = useState(false);
  const [isEditModalOpen, setIsEditModalOpen] = useState(false);
  const [selectedEmployee, setSelectedEmployee] = useState<Employee | null>(null);
  const [filterClinic, setFilterClinic] = useState<string>('');
  const [filterRole, setFilterRole] = useState<string>('');
  const pageSize = 10;

  // Fetch employees data
  const { data, isLoading, error } = useQuery({
    queryKey: ['employees', currentPage, searchTerm, filterClinic, filterRole],
    queryFn: () =>
      employeeService.getAll({
        page: currentPage,
        page_size: pageSize,
        search: searchTerm,
        clinic_id: filterClinic || undefined,
        role: filterRole || undefined,
      }),
  });

  // Fetch clinics for dropdown
  const { data: clinics } = useQuery({
    queryKey: ['clinics-list'],
    queryFn: () => clinicService.getAll(),
  });

  // Fetch persons for dropdown (when creating new employee)
  const { data: persons } = useQuery({
    queryKey: ['persons-list'],
    queryFn: () => personService.getAll(),
  });

  // Create mutation
  const createMutation = useMutation({
    mutationFn: (newEmployee: EmployeeCreate) => employeeService.create(newEmployee),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['employees'] });
      toast.success('Employee created successfully');
      setIsCreateModalOpen(false);
    },
    onError: (error: any) => {
      toast.error(error.message || 'Failed to create employee');
    },
  });

  // Update mutation
  const updateMutation = useMutation({
    mutationFn: ({ id, data }: { id: string; data: EmployeeUpdate }) =>
      employeeService.update(id, data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['employees'] });
      toast.success('Employee updated successfully');
      setIsEditModalOpen(false);
      setSelectedEmployee(null);
    },
    onError: (error: any) => {
      toast.error(error.message || 'Failed to update employee');
    },
  });

  // Delete mutation
  const deleteMutation = useMutation({
    mutationFn: (id: string) => employeeService.delete(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['employees'] });
      toast.success('Employee deleted successfully');
    },
    onError: (error: any) => {
      toast.error(error.message || 'Failed to delete employee');
    },
  });

  const handleEdit = (employee: Employee) => {
    setSelectedEmployee(employee);
    setIsEditModalOpen(true);
  };

  const handleDelete = async (id: string) => {
    if (confirm('Are you sure you want to delete this employee?')) {
      deleteMutation.mutate(id);
    }
  };

  const totalPages = data ? Math.ceil(data.total / pageSize) : 0;

  const getRoleDisplay = (role: string) => {
    return role.charAt(0).toUpperCase() + role.slice(1);
  };

  return (
    <div>
      {/* Page Header */}
      <div className="mb-6">
        <h1 className="text-2xl font-bold text-gray-900">Employees Management</h1>
        <p className="text-gray-600 mt-1">
          Manage all employees in the system
        </p>
      </div>

      {/* Actions Bar */}
      <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-4 mb-6">
        <div className="flex flex-col gap-4">
          <div className="flex flex-col sm:flex-row justify-between items-center gap-4">
            <div className="w-full sm:w-96">
              <input
                type="text"
                placeholder="Search by name or employee code..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="input-field"
              />
            </div>
            <button
              onClick={() => setIsCreateModalOpen(true)}
              className="btn-primary whitespace-nowrap"
            >
              + Add New Employee
            </button>
          </div>
          
          {/* Filters */}
          <div className="flex flex-col sm:flex-row gap-4">
            <div className="flex-1">
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Filter by Clinic
              </label>
              <select
                value={filterClinic}
                onChange={(e) => setFilterClinic(e.target.value)}
                className="input-field"
              >
                <option value="">All Clinics</option>
                {clinics?.items.map((clinic) => (
                  <option key={clinic.id} value={clinic.id}>
                    {clinic.name}
                  </option>
                ))}
              </select>
            </div>
            
            <div className="flex-1">
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Filter by Role
              </label>
              <select
                value={filterRole}
                onChange={(e) => setFilterRole(e.target.value)}
                className="input-field"
              >
                <option value="">All Roles</option>
                {Object.values(EmployeeRole).map((role) => (
                  <option key={role} value={role}>
                    {getRoleDisplay(role)}
                  </option>
                ))}
              </select>
            </div>
          </div>
        </div>
      </div>

      {/* Data Table */}
      <div className="bg-white rounded-lg shadow-sm border border-gray-200 overflow-hidden">
        {isLoading ? (
          <div className="flex justify-center items-center h-64">
            <div className="spinner"></div>
          </div>
        ) : error ? (
          <div className="text-center py-8 text-red-600">
            Error loading data. Please try again.
          </div>
        ) : (
          <>
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead className="bg-gray-50 border-b border-gray-200">
                  <tr>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Employee Code
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Name
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Role
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Clinic
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      License #
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Can Treat
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Status
                    </th>
                    <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Actions
                    </th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-gray-200">
                  {data?.items.map((employee) => {
                    const clinic = clinics?.items.find(c => c.id === employee.primary_clinic_id);
                    return (
                      <tr key={employee.id} className="hover:bg-gray-50">
                        <td className="px-6 py-4 whitespace-nowrap">
                          <div className="text-sm font-medium text-gray-900">
                            {employee.employee_code || '-'}
                          </div>
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap">
                          <div className="text-sm text-gray-900">
                            {employee.person ? 
                              `${employee.person.first_name} ${employee.person.last_name}` : 
                              'N/A'}
                          </div>
                          {employee.person?.email && (
                            <div className="text-xs text-gray-500">
                              {employee.person.email}
                            </div>
                          )}
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap">
                          <div className="text-sm text-gray-900">
                            {getRoleDisplay(employee.role)}
                          </div>
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap">
                          <div className="text-sm text-gray-600">
                            {clinic?.name || '-'}
                          </div>
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap">
                          <div className="text-sm text-gray-600">
                            {employee.license_number || '-'}
                          </div>
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap">
                          <span
                            className={`px-2 inline-flex text-xs leading-5 font-semibold rounded-full ${
                              employee.can_perform_treatments
                                ? 'bg-blue-100 text-blue-800'
                                : 'bg-gray-100 text-gray-800'
                            }`}
                          >
                            {employee.can_perform_treatments ? 'Yes' : 'No'}
                          </span>
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap">
                          <span
                            className={`px-2 inline-flex text-xs leading-5 font-semibold rounded-full ${
                              employee.is_active
                                ? 'bg-green-100 text-green-800'
                                : 'bg-red-100 text-red-800'
                            }`}
                          >
                            {employee.is_active ? 'Active' : 'Inactive'}
                          </span>
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                          <button
                            onClick={() => handleEdit(employee)}
                            className="text-primary-600 hover:text-primary-900 mr-3"
                          >
                            Edit
                          </button>
                          <button
                            onClick={() => handleDelete(employee.id)}
                            className="text-red-600 hover:text-red-900"
                          >
                            Delete
                          </button>
                        </td>
                      </tr>
                    );
                  })}
                </tbody>
              </table>
            </div>

            {/* Pagination */}
            {totalPages > 1 && (
              <div className="px-6 py-3 border-t border-gray-200 flex items-center justify-between">
                <div className="text-sm text-gray-700">
                  Showing {(currentPage - 1) * pageSize + 1} to{' '}
                  {Math.min(currentPage * pageSize, data?.total || 0)} of{' '}
                  {data?.total || 0} results
                </div>
                <div className="flex space-x-2">
                  <button
                    onClick={() => setCurrentPage(currentPage - 1)}
                    disabled={currentPage === 1}
                    className="px-3 py-1 text-sm border border-gray-300 rounded-md hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
                  >
                    Previous
                  </button>
                  {[...Array(Math.min(5, totalPages))].map((_, i) => {
                    const pageNum = i + 1;
                    if (pageNum <= totalPages) {
                      return (
                        <button
                          key={i}
                          onClick={() => setCurrentPage(pageNum)}
                          className={`px-3 py-1 text-sm border rounded-md ${
                            currentPage === pageNum
                              ? 'bg-primary-600 text-white border-primary-600'
                              : 'border-gray-300 hover:bg-gray-50'
                          }`}
                        >
                          {pageNum}
                        </button>
                      );
                    }
                    return null;
                  })}
                  <button
                    onClick={() => setCurrentPage(currentPage + 1)}
                    disabled={currentPage === totalPages}
                    className="px-3 py-1 text-sm border border-gray-300 rounded-md hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
                  >
                    Next
                  </button>
                </div>
              </div>
            )}
          </>
        )}
      </div>

      {/* Create Modal */}
      {isCreateModalOpen && (
        <EmployeeFormModal
          title="Add New Employee"
          persons={persons?.items || []}
          clinics={clinics?.items || []}
          onClose={() => setIsCreateModalOpen(false)}
          onSubmit={(data) => createMutation.mutate(data)}
          isLoading={createMutation.isPending}
        />
      )}

      {/* Edit Modal */}
      {isEditModalOpen && selectedEmployee && (
        <EmployeeFormModal
          title="Edit Employee"
          employee={selectedEmployee}
          persons={persons?.items || []}
          clinics={clinics?.items || []}
          onClose={() => {
            setIsEditModalOpen(false);
            setSelectedEmployee(null);
          }}
          onSubmit={(data) =>
            updateMutation.mutate({ id: selectedEmployee.id, data })
          }
          isLoading={updateMutation.isPending}
        />
      )}
    </div>
  );
}

// Employee Form Modal Component
interface EmployeeFormModalProps {
  title: string;
  employee?: Employee | null;
  persons: Person[];
  clinics: Clinic[];
  onClose: () => void;
  onSubmit: (data: EmployeeCreate | EmployeeUpdate) => void;
  isLoading: boolean;
}

function EmployeeFormModal({
  title,
  employee,
  persons,
  clinics,
  onClose,
  onSubmit,
  isLoading,
}: EmployeeFormModalProps) {
  const [formData, setFormData] = useState({
    person_id: employee?.person_id || '',
    employee_code: employee?.employee_code || '',
    primary_clinic_id: employee?.primary_clinic_id || '',
    role: employee?.role || EmployeeRole.DOCTOR,
    license_number: employee?.license_number || '',
    can_perform_treatments: employee?.can_perform_treatments || false,
    is_active: employee?.is_active ?? true,
  });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    
    // For update, don't send person_id
    if (employee) {
      const { person_id, ...updateData } = formData;
      onSubmit(updateData);
    } else {
      onSubmit(formData);
    }
  };

  const getRoleDisplay = (role: string) => {
    return role.charAt(0).toUpperCase() + role.slice(1);
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-white rounded-lg p-6 w-full max-w-md max-h-[90vh] overflow-y-auto">
        <h2 className="text-xl font-semibold mb-4">{title}</h2>
        <form onSubmit={handleSubmit} className="space-y-4">
          {!employee && (
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Person *
              </label>
              <select
                required
                value={formData.person_id}
                onChange={(e) =>
                  setFormData({ ...formData, person_id: e.target.value })
                }
                className="input-field"
              >
                <option value="">Select a person...</option>
                {persons.map((person) => (
                  <option key={person.id} value={person.id}>
                    {person.first_name} {person.last_name}
                    {person.email && ` (${person.email})`}
                  </option>
                ))}
              </select>
              {!employee && (
                <p className="text-xs text-gray-500 mt-1">
                  Person cannot be changed after creation
                </p>
              )}
            </div>
          )}

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Employee Code
            </label>
            <input
              type="text"
              maxLength={20}
              value={formData.employee_code}
              onChange={(e) =>
                setFormData({ ...formData, employee_code: e.target.value.toUpperCase() })
              }
              className="input-field"
              placeholder="e.g., EMP001"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Primary Clinic *
            </label>
            <select
              required
              value={formData.primary_clinic_id}
              onChange={(e) =>
                setFormData({ ...formData, primary_clinic_id: e.target.value })
              }
              className="input-field"
            >
              <option value="">Select a clinic...</option>
              {clinics.map((clinic) => (
                <option key={clinic.id} value={clinic.id}>
                  {clinic.name} ({clinic.code})
                </option>
              ))}
            </select>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Role *
            </label>
            <select
              required
              value={formData.role}
              onChange={(e) =>
                setFormData({ ...formData, role: e.target.value as EmployeeRole })
              }
              className="input-field"
            >
              {Object.values(EmployeeRole).map((role) => (
                <option key={role} value={role}>
                  {getRoleDisplay(role)}
                </option>
              ))}
            </select>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              License Number
            </label>
            <input
              type="text"
              maxLength={50}
              value={formData.license_number}
              onChange={(e) =>
                setFormData({ ...formData, license_number: e.target.value })
              }
              className="input-field"
              placeholder="e.g., MD123456"
            />
          </div>

          <div>
            <label className="flex items-center space-x-2">
              <input
                type="checkbox"
                checked={formData.can_perform_treatments}
                onChange={(e) =>
                  setFormData({ ...formData, can_perform_treatments: e.target.checked })
                }
                className="rounded"
              />
              <span className="text-sm font-medium text-gray-700">
                Can Perform Treatments
              </span>
            </label>
          </div>

          {employee && (
            <div>
              <label className="flex items-center space-x-2">
                <input
                  type="checkbox"
                  checked={formData.is_active}
                  onChange={(e) =>
                    setFormData({ ...formData, is_active: e.target.checked })
                  }
                  className="rounded"
                />
                <span className="text-sm font-medium text-gray-700">
                  Is Active
                </span>
              </label>
            </div>
          )}

          <div className="flex justify-end space-x-3 pt-4">
            <button
              type="button"
              onClick={onClose}
              className="btn-secondary"
              disabled={isLoading}
            >
              Cancel
            </button>
            <button
              type="submit"
              className="btn-primary"
              disabled={isLoading}
            >
              {isLoading ? 'Saving...' : 'Save'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
