'use client';

import { useState, useEffect } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { personService } from '@/services/api.service';
import { Person, PersonCreate, PersonUpdate, GenderType } from '@/types/api';
import { toast } from '@/components/ui/toaster';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  Users, 
  UserPlus, 
  Mail, 
  Phone, 
  Calendar, 
  User,
  Download,
  Filter,
  Search,
  MoreVertical,
  Edit,
  Trash2,
  Eye
} from 'lucide-react';
import {
  CRMLayout,
  EnhancedTable,
  EnhancedStatsCard,
  type Column
} from '@/components/enhanced';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Badge } from '@/components/ui/badge';
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from '@/components/ui/dialog';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';

export default function PersonsPage() {
  const queryClient = useQueryClient();
  const [isCreateModalOpen, setIsCreateModalOpen] = useState(false);
  const [isEditModalOpen, setIsEditModalOpen] = useState(false);
  const [selectedPerson, setSelectedPerson] = useState<Person | null>(null);
  const [searchTerm, setSearchTerm] = useState('');

  // Fetch persons data
  const { data, isLoading, error } = useQuery({
    queryKey: ['persons'],
    queryFn: () => personService.getAll(),
  });

  // Calculate statistics
  const stats = {
    total: data?.total || 0,
    active: data?.items.filter(p => p.email).length || 0,
    withPhone: data?.items.filter(p => p.phone_mobile).length || 0,
    withEmail: data?.items.filter(p => p.email).length || 0,
  };

  // Create mutation
  const createMutation = useMutation({
    mutationFn: (newPerson: PersonCreate) => personService.create(newPerson),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['persons'] });
      toast.success('Person created successfully');
      setIsCreateModalOpen(false);
    },
    onError: (error: any) => {
      toast.error(error.message || 'Failed to create person');
    },
  });

  // Update mutation
  const updateMutation = useMutation({
    mutationFn: ({ id, data }: { id: string; data: PersonUpdate }) =>
      personService.update(id, data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['persons'] });
      toast.success('Person updated successfully');
      setIsEditModalOpen(false);
      setSelectedPerson(null);
    },
    onError: (error: any) => {
      toast.error(error.message || 'Failed to update person');
    },
  });

  // Delete mutation
  const deleteMutation = useMutation({
    mutationFn: (id: string) => personService.delete(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['persons'] });
      toast.success('Person deleted successfully');
    },
    onError: (error: any) => {
      toast.error(error.message || 'Failed to delete person');
    },
  });

  const handleRowAction = (action: string, person: Person) => {
    switch (action) {
      case 'view':
        // In future, navigate to detail page
        toast.info(`Viewing ${person.first_name} ${person.last_name}`);
        break;
      case 'edit':
        setSelectedPerson(person);
        setIsEditModalOpen(true);
        break;
      case 'delete':
        if (confirm(`Are you sure you want to delete ${person.first_name} ${person.last_name}?`)) {
          deleteMutation.mutate(person.id);
        }
        break;
    }
  };

  // Define table columns
  const columns: Column<Person>[] = [
    {
      key: 'name',
      header: 'Full Name',
      cell: (person) => (
        <div className="flex items-center gap-3">
          <div className="w-8 h-8 rounded-full bg-[var(--pico-coral-subtle)] flex items-center justify-center">
            <User className="w-4 h-4 text-[var(--pico-coral-primary)]" />
          </div>
          <div>
            <div className="font-medium text-[var(--pico-text-primary)]">
              {person.first_name} {person.last_name}
            </div>
            {person.email && (
              <div className="text-xs text-[var(--pico-text-tertiary)]">
                {person.email}
              </div>
            )}
          </div>
        </div>
      ),
      sortable: true,
      searchable: true,
    },
    {
      key: 'phone_mobile',
      header: 'Phone',
      cell: (person) => person.phone_mobile ? (
        <div className="flex items-center gap-2">
          <Phone className="w-3 h-3 text-[var(--pico-text-tertiary)]" />
          <span>{person.phone_mobile}</span>
        </div>
      ) : (
        <span className="text-[var(--pico-text-tertiary)]">-</span>
      ),
      sortable: true,
      searchable: true,
    },
    {
      key: 'gender',
      header: 'Gender',
      cell: (person) => {
        if (!person.gender) return <span className="text-[var(--pico-text-tertiary)]">-</span>;
        
        const genderMap = {
          [GenderType.M]: { label: 'Male', color: 'bg-blue-100 text-blue-800' },
          [GenderType.F]: { label: 'Female', color: 'bg-pink-100 text-pink-800' },
          [GenderType.O]: { label: 'Other', color: 'bg-purple-100 text-purple-800' },
          [GenderType.N]: { label: 'N/A', color: 'bg-gray-100 text-gray-800' },
        };
        
        const gender = genderMap[person.gender];
        return gender ? (
          <Badge className={gender.color}>
            {gender.label}
          </Badge>
        ) : null;
      },
      sortable: true,
    },
    {
      key: 'dob',
      header: 'Date of Birth',
      cell: (person) => person.dob ? (
        <div className="flex items-center gap-2">
          <Calendar className="w-3 h-3 text-[var(--pico-text-tertiary)]" />
          <span>{new Date(person.dob).toLocaleDateString()}</span>
        </div>
      ) : (
        <span className="text-[var(--pico-text-tertiary)]">-</span>
      ),
      sortable: true,
    },
    {
      key: 'status',
      header: 'Status',
      cell: (person) => {
        const hasCompleteInfo = person.email && person.phone_mobile;
        return (
          <Badge 
            className={hasCompleteInfo 
              ? 'bg-[var(--pico-success-light)] text-[var(--pico-success)] border-[var(--pico-success)]' 
              : 'bg-[var(--pico-warning-light)] text-[var(--pico-warning)] border-[var(--pico-warning)]'
            }
          >
            {hasCompleteInfo ? 'Complete' : 'Incomplete'}
          </Badge>
        );
      },
    },
  ];

  const bulkActions = [
    {
      label: 'Export Selected',
      action: (selected: Person[]) => {
        toast.info(`Exporting ${selected.length} persons`);
      },
    },
    {
      label: 'Delete Selected',
      action: (selected: Person[]) => {
        if (confirm(`Delete ${selected.length} persons?`)) {
          selected.forEach(p => deleteMutation.mutate(p.id));
        }
      },
    },
  ];

  return (
    <CRMLayout
      title="Persons Management"
      description="Manage all persons in your system"
      breadcrumbs={[{ label: 'Persons' }]}
      actions={
        <div className="flex gap-2">
          <Button
            variant="outline"
            onClick={() => toast.info('Export functionality coming soon')}
          >
            <Download className="w-4 h-4 mr-2" />
            Export All
          </Button>
          <Button
            onClick={() => setIsCreateModalOpen(true)}
            className="bg-[var(--pico-coral-primary)] hover:bg-[var(--pico-coral-dark)] text-white"
          >
            <UserPlus className="w-4 h-4 mr-2" />
            Add Person
          </Button>
        </div>
      }
    >
      {/* Statistics Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <EnhancedStatsCard
          title="Total Persons"
          value={stats.total}
          icon={Users}
          change={12}
          trend="up"
          color="primary"
          delay={0}
        />
        <EnhancedStatsCard
          title="With Email"
          value={stats.withEmail}
          icon={Mail}
          format="number"
          color="success"
          delay={0.1}
        />
        <EnhancedStatsCard
          title="With Phone"
          value={stats.withPhone}
          icon={Phone}
          format="number"
          color="success"
          delay={0.2}
        />
        <EnhancedStatsCard
          title="Complete Profiles"
          value={`${Math.round((stats.active / stats.total) * 100) || 0}%`}
          icon={User}
          trend="up"
          change={5}
          color="warning"
          delay={0.3}
        />
      </div>

      {/* Enhanced Data Table */}
      <Card className="bg-white/80 backdrop-blur-md border-[var(--pico-border-light)]">
        <CardHeader>
          <CardTitle>All Persons</CardTitle>
        </CardHeader>
        <CardContent>
          <EnhancedTable
            data={data?.items || []}
            columns={columns}
            loading={isLoading}
            error={error as Error}
            onRowAction={handleRowAction}
            searchable={true}
            filterable={true}
            exportable={true}
            bulkActions={bulkActions}
            emptyState={
              <div className="text-center py-12">
                <Users className="w-12 h-12 text-[var(--pico-text-tertiary)] mx-auto mb-4" />
                <h3 className="text-lg font-medium text-[var(--pico-text-primary)] mb-2">
                  No persons found
                </h3>
                <p className="text-[var(--pico-text-secondary)] mb-4">
                  Get started by adding your first person
                </p>
                <Button
                  onClick={() => setIsCreateModalOpen(true)}
                  className="bg-[var(--pico-coral-primary)] hover:bg-[var(--pico-coral-dark)] text-white"
                >
                  <UserPlus className="w-4 h-4 mr-2" />
                  Add First Person
                </Button>
              </div>
            }
          />
        </CardContent>
      </Card>

      {/* Create Modal */}
      <Dialog open={isCreateModalOpen} onOpenChange={setIsCreateModalOpen}>
        <DialogContent className="sm:max-w-[500px]">
          <DialogHeader>
            <DialogTitle>Add New Person</DialogTitle>
            <DialogDescription>
              Enter the person's information below
            </DialogDescription>
          </DialogHeader>
          <PersonForm
            onSubmit={(data) => createMutation.mutate(data)}
            onCancel={() => setIsCreateModalOpen(false)}
            isLoading={createMutation.isPending}
          />
        </DialogContent>
      </Dialog>

      {/* Edit Modal */}
      <Dialog 
        open={isEditModalOpen} 
        onOpenChange={(open) => {
          setIsEditModalOpen(open);
          if (!open) setSelectedPerson(null);
        }}
      >
        <DialogContent className="sm:max-w-[500px]">
          <DialogHeader>
            <DialogTitle>Edit Person</DialogTitle>
            <DialogDescription>
              Update the person's information below
            </DialogDescription>
          </DialogHeader>
          {selectedPerson && (
            <PersonForm
              person={selectedPerson}
              onSubmit={(data) =>
                updateMutation.mutate({ id: selectedPerson.id, data })
              }
              onCancel={() => {
                setIsEditModalOpen(false);
                setSelectedPerson(null);
              }}
              isLoading={updateMutation.isPending}
            />
          )}
        </DialogContent>
      </Dialog>
    </CRMLayout>
  );
}

// Person Form Component
interface PersonFormProps {
  person?: Person | null;
  onSubmit: (data: PersonCreate | PersonUpdate) => void;
  onCancel: () => void;
  isLoading: boolean;
}

function PersonForm({
  person,
  onSubmit,
  onCancel,
  isLoading,
}: PersonFormProps) {
  const [formData, setFormData] = useState({
    first_name: person?.first_name || '',
    last_name: person?.last_name || '',
    email: person?.email || '',
    phone_mobile: person?.phone_mobile || '',
    dob: person?.dob || '',
    gender: person?.gender || '',
  });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onSubmit(formData);
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <div className="grid grid-cols-2 gap-4">
        <div className="space-y-2">
          <Label htmlFor="first_name">
            First Name <span className="text-[var(--pico-error)]">*</span>
          </Label>
          <Input
            id="first_name"
            type="text"
            value={formData.first_name}
            onChange={(e) =>
              setFormData({ ...formData, first_name: e.target.value })
            }
            placeholder="John"
            required
            className="border-[var(--pico-border-light)] focus:ring-[var(--pico-coral-primary)]"
          />
        </div>

        <div className="space-y-2">
          <Label htmlFor="last_name">
            Last Name <span className="text-[var(--pico-error)]">*</span>
          </Label>
          <Input
            id="last_name"
            type="text"
            value={formData.last_name}
            onChange={(e) =>
              setFormData({ ...formData, last_name: e.target.value })
            }
            placeholder="Doe"
            required
            className="border-[var(--pico-border-light)] focus:ring-[var(--pico-coral-primary)]"
          />
        </div>
      </div>

      <div className="space-y-2">
        <Label htmlFor="email">Email</Label>
        <Input
          id="email"
          type="email"
          value={formData.email}
          onChange={(e) =>
            setFormData({ ...formData, email: e.target.value })
          }
          placeholder="john.doe@example.com"
          className="border-[var(--pico-border-light)] focus:ring-[var(--pico-coral-primary)]"
        />
      </div>

      <div className="space-y-2">
        <Label htmlFor="phone_mobile">Phone</Label>
        <Input
          id="phone_mobile"
          type="tel"
          value={formData.phone_mobile}
          onChange={(e) =>
            setFormData({ ...formData, phone_mobile: e.target.value })
          }
          placeholder="+1 (555) 000-0000"
          className="border-[var(--pico-border-light)] focus:ring-[var(--pico-coral-primary)]"
        />
      </div>

      <div className="grid grid-cols-2 gap-4">
        <div className="space-y-2">
          <Label htmlFor="dob">Date of Birth</Label>
          <Input
            id="dob"
            type="date"
            value={formData.dob}
            onChange={(e) =>
              setFormData({ ...formData, dob: e.target.value })
            }
            className="border-[var(--pico-border-light)] focus:ring-[var(--pico-coral-primary)]"
          />
        </div>

        <div className="space-y-2">
          <Label htmlFor="gender">Gender</Label>
          <Select
            value={formData.gender}
            onValueChange={(value) =>
              setFormData({ ...formData, gender: value })
            }
          >
            <SelectTrigger className="border-[var(--pico-border-light)] focus:ring-[var(--pico-coral-primary)]">
              <SelectValue placeholder="Select gender" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value={GenderType.M}>Male</SelectItem>
              <SelectItem value={GenderType.F}>Female</SelectItem>
              <SelectItem value={GenderType.O}>Other</SelectItem>
              <SelectItem value={GenderType.N}>Prefer not to say</SelectItem>
            </SelectContent>
          </Select>
        </div>
      </div>

      <DialogFooter>
        <Button
          type="button"
          variant="outline"
          onClick={onCancel}
          disabled={isLoading}
        >
          Cancel
        </Button>
        <Button
          type="submit"
          disabled={isLoading}
          className="bg-[var(--pico-coral-primary)] hover:bg-[var(--pico-coral-dark)] text-white"
        >
          {isLoading ? (
            <>
              <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin mr-2"></div>
              Saving...
            </>
          ) : person ? (
            'Update Person'
          ) : (
            'Create Person'
          )}
        </Button>
      </DialogFooter>
    </form>
  );
}
