'use client';

import { useState, useEffect } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { clientService, personService, clinicService } from '@/services/api.service';
import { Client, ClientCreate, ClientUpdate, Person, Clinic } from '@/types/api';
import { toast } from '@/components/ui/toaster';

export default function ClientsPage() {
  const queryClient = useQueryClient();
  const [searchTerm, setSearchTerm] = useState('');
  const [currentPage, setCurrentPage] = useState(1);
  const [isCreateModalOpen, setIsCreateModalOpen] = useState(false);
  const [isEditModalOpen, setIsEditModalOpen] = useState(false);
  const [selectedClient, setSelectedClient] = useState<Client | null>(null);
  const pageSize = 10;

  // Fetch clients data
  const { data, isLoading, error } = useQuery({
    queryKey: ['clients', currentPage, searchTerm],
    queryFn: () =>
      clientService.getAll({
        page: currentPage,
        page_size: pageSize,
        search: searchTerm,
      }),
  });

  // Fetch persons for dropdown
  const { data: personsData } = useQuery({
    queryKey: ['persons-all'],
    queryFn: () => personService.getAll({ page_size: 1000 }),
  });

  // Fetch clinics for dropdown
  const { data: clinicsData } = useQuery({
    queryKey: ['clinics-all'],
    queryFn: () => clinicService.getAll({ page_size: 1000 }),
  });

  // Create mutation
  const createMutation = useMutation({
    mutationFn: (newClient: ClientCreate) => clientService.create(newClient),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['clients'] });
      toast.success('Client created successfully');
      setIsCreateModalOpen(false);
    },
    onError: (error: any) => {
      toast.error(error.message || 'Failed to create client');
    },
  });

  // Update mutation
  const updateMutation = useMutation({
    mutationFn: ({ id, data }: { id: string; data: ClientUpdate }) =>
      clientService.update(id, data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['clients'] });
      toast.success('Client updated successfully');
      setIsEditModalOpen(false);
      setSelectedClient(null);
    },
    onError: (error: any) => {
      toast.error(error.message || 'Failed to update client');
    },
  });

  // Delete mutation
  const deleteMutation = useMutation({
    mutationFn: (id: string) => clientService.delete(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['clients'] });
      toast.success('Client deleted successfully');
    },
    onError: (error: any) => {
      toast.error(error.message || 'Failed to delete client');
    },
  });

  const handleEdit = (client: Client) => {
    setSelectedClient(client);
    setIsEditModalOpen(true);
  };

  const handleDelete = async (id: string) => {
    if (confirm('Are you sure you want to delete this client?')) {
      deleteMutation.mutate(id);
    }
  };

  const totalPages = data ? Math.ceil(data.total / pageSize) : 0;

  // Get available persons (those who are not already clients)
  const availablePersons = personsData?.items.filter(person => {
    return !data?.items.some(client => client.person_id === person.id);
  }) || [];

  return (
    <div>
      {/* Page Header */}
      <div className="mb-6">
        <h1 className="text-2xl font-bold text-gray-900">Clients Management</h1>
        <p className="text-gray-600 mt-1">
          Manage all clients in the system
        </p>
      </div>

      {/* Actions Bar */}
      <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-4 mb-6">
        <div className="flex flex-col sm:flex-row justify-between items-center gap-4">
          <div className="w-full sm:w-96">
            <input
              type="text"
              placeholder="Search by client code or person name..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="input-field"
            />
          </div>
          <button
            onClick={() => setIsCreateModalOpen(true)}
            className="btn-primary whitespace-nowrap"
            disabled={!availablePersons.length}
          >
            + Add New Client
          </button>
        </div>
        {!availablePersons.length && (
          <p className="text-sm text-gray-500 mt-2">
            All persons are already registered as clients. Add new persons first.
          </p>
        )}
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
                      Client Code
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Person Name
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Email
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Phone
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Preferred Clinic
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
                  {data?.items.map((client) => {
                    const clinic = clinicsData?.items.find(c => c.id === client.preferred_clinic_id);
                    return (
                      <tr key={client.id} className="hover:bg-gray-50">
                        <td className="px-6 py-4 whitespace-nowrap">
                          <div className="text-sm font-medium text-gray-900">
                            {client.client_code || '-'}
                          </div>
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap">
                          <div className="text-sm text-gray-900">
                            {client.person ? 
                              `${client.person.first_name} ${client.person.last_name}` : 
                              'Unknown Person'}
                          </div>
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap">
                          <div className="text-sm text-gray-600">
                            {client.person?.email || '-'}
                          </div>
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap">
                          <div className="text-sm text-gray-600">
                            {client.person?.phone_mobile || '-'}
                          </div>
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap">
                          <div className="text-sm text-gray-600">
                            {clinic?.name || '-'}
                          </div>
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap">
                          <span className={`px-2 inline-flex text-xs leading-5 font-semibold rounded-full ${
                            client.is_active 
                              ? 'bg-green-100 text-green-800' 
                              : 'bg-red-100 text-red-800'
                          }`}>
                            {client.is_active ? 'Active' : 'Inactive'}
                          </span>
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                          <button
                            onClick={() => handleEdit(client)}
                            className="text-primary-600 hover:text-primary-900 mr-3"
                          >
                            Edit
                          </button>
                          <button
                            onClick={() => handleDelete(client.id)}
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

            {/* Empty State */}
            {data?.items.length === 0 && (
              <div className="text-center py-12">
                <p className="text-gray-500">No clients found</p>
              </div>
            )}

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
                  {[...Array(totalPages)].map((_, i) => (
                    <button
                      key={i}
                      onClick={() => setCurrentPage(i + 1)}
                      className={`px-3 py-1 text-sm border rounded-md ${
                        currentPage === i + 1
                          ? 'bg-primary-600 text-white border-primary-600'
                          : 'border-gray-300 hover:bg-gray-50'
                      }`}
                    >
                      {i + 1}
                    </button>
                  ))}
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
        <ClientFormModal
          title="Add New Client"
          persons={availablePersons}
          clinics={clinicsData?.items || []}
          onClose={() => setIsCreateModalOpen(false)}
          onSubmit={(data) => createMutation.mutate(data)}
          isLoading={createMutation.isPending}
        />
      )}

      {/* Edit Modal */}
      {isEditModalOpen && selectedClient && (
        <ClientFormModal
          title="Edit Client"
          client={selectedClient}
          persons={personsData?.items || []}
          clinics={clinicsData?.items || []}
          onClose={() => {
            setIsEditModalOpen(false);
            setSelectedClient(null);
          }}
          onSubmit={(data) =>
            updateMutation.mutate({ id: selectedClient.id, data })
          }
          isLoading={updateMutation.isPending}
        />
      )}
    </div>
  );
}

// Client Form Modal Component
interface ClientFormModalProps {
  title: string;
  client?: Client | null;
  persons: Person[];
  clinics: Clinic[];
  onClose: () => void;
  onSubmit: (data: ClientCreate | ClientUpdate) => void;
  isLoading: boolean;
}

function ClientFormModal({
  title,
  client,
  persons,
  clinics,
  onClose,
  onSubmit,
  isLoading,
}: ClientFormModalProps) {
  const [formData, setFormData] = useState({
    person_id: client?.person_id || '',
    client_code: client?.client_code || '',
    preferred_clinic_id: client?.preferred_clinic_id || '',
    is_active: client?.is_active !== undefined ? client.is_active : true,
  });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    
    // For update, we don't send person_id
    if (client) {
      const { person_id, ...updateData } = formData;
      onSubmit({
        ...updateData,
        preferred_clinic_id: formData.preferred_clinic_id || undefined,
      });
    } else {
      // For create, person_id is required
      onSubmit({
        person_id: formData.person_id,
        client_code: formData.client_code || undefined,
        preferred_clinic_id: formData.preferred_clinic_id || undefined,
      });
    }
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-white rounded-lg p-6 w-full max-w-md">
        <h2 className="text-xl font-semibold mb-4">{title}</h2>
        <form onSubmit={handleSubmit} className="space-y-4">
          {!client && (
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
                disabled={!!client}
              >
                <option value="">Select a person...</option>
                {persons.map((person) => (
                  <option key={person.id} value={person.id}>
                    {person.first_name} {person.last_name}
                    {person.email && ` (${person.email})`}
                  </option>
                ))}
              </select>
            </div>
          )}

          {client && (
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Person
              </label>
              <div className="text-sm text-gray-600 p-2 bg-gray-50 rounded">
                {client.person ? 
                  `${client.person.first_name} ${client.person.last_name}` : 
                  'Unknown Person'}
              </div>
            </div>
          )}

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Client Code
            </label>
            <input
              type="text"
              value={formData.client_code}
              onChange={(e) =>
                setFormData({ ...formData, client_code: e.target.value })
              }
              className="input-field"
              placeholder="Optional unique client identifier"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Preferred Clinic
            </label>
            <select
              value={formData.preferred_clinic_id}
              onChange={(e) =>
                setFormData({ ...formData, preferred_clinic_id: e.target.value })
              }
              className="input-field"
            >
              <option value="">No preference</option>
              {clinics.filter(c => c.is_active).map((clinic) => (
                <option key={clinic.id} value={clinic.id}>
                  {clinic.name} ({clinic.code})
                </option>
              ))}
            </select>
          </div>

          {client && (
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Status
              </label>
              <select
                value={formData.is_active ? 'active' : 'inactive'}
                onChange={(e) =>
                  setFormData({ ...formData, is_active: e.target.value === 'active' })
                }
                className="input-field"
              >
                <option value="active">Active</option>
                <option value="inactive">Inactive</option>
              </select>
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
              disabled={isLoading || (!client && !formData.person_id)}
            >
              {isLoading ? 'Saving...' : 'Save'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
