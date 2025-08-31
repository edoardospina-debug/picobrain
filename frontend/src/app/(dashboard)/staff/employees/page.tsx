'use client';

import React, { useState } from 'react';
import { useRouter } from 'next/navigation';
import { Tag, Button, message, Space, Tooltip, Badge } from 'antd';
import {
  PhoneOutlined,
  MailOutlined,
  UserOutlined,
  TeamOutlined,
  MedicineBoxOutlined,
  DollarOutlined,
  CalendarOutlined,
  CheckCircleOutlined,
  CloseCircleOutlined,
  ExportOutlined,
  IdcardOutlined,
  HeartOutlined,
  CustomerServiceOutlined,
  BankOutlined,
  SettingOutlined,
  SafetyCertificateOutlined,
} from '@ant-design/icons';
import DataTable from '@/components/shared/DataTable';
import { employeesApi } from '@/lib/api/endpoints/employees';
import { Employee, EmployeeRole } from '@/types';
import { saveAs } from 'file-saver';
import dayjs from 'dayjs';

// Role configuration with colors and icons
const roleConfig: Record<EmployeeRole, { color: string; icon: React.ReactNode; label: string }> = {
  doctor: { color: 'blue', icon: <MedicineBoxOutlined />, label: 'Doctor' },
  nurse: { color: 'green', icon: <HeartOutlined />, label: 'Nurse' },
  receptionist: { color: 'purple', icon: <CustomerServiceOutlined />, label: 'Receptionist' },
  manager: { color: 'orange', icon: <TeamOutlined />, label: 'Manager' },
  finance: { color: 'gold', icon: <DollarOutlined />, label: 'Finance' },
  admin: { color: 'red', icon: <SettingOutlined />, label: 'Admin' },
};

export default function EmployeesPage() {
  const router = useRouter();
  const [exporting, setExporting] = useState(false);
  const [selectedRole, setSelectedRole] = useState<EmployeeRole | undefined>(undefined);

  // Table columns configuration
  const columns = [
    {
      title: 'Code',
      dataIndex: 'employee_code',
      key: 'employee_code',
      width: 100,
      sorter: true,
      fixed: 'left' as const,
      render: (code: string) => (
        <span style={{ fontWeight: 600 }}>{code || 'N/A'}</span>
      ),
    },
    {
      title: 'Name',
      key: 'name',
      sorter: true,
      render: (_: any, record: Employee) => {
        const roleInfo = roleConfig[record.role];
        const isDoctor = record.role === 'doctor';
        return (
          <div>
            <div style={{ fontWeight: 500 }}>
              <UserOutlined /> {isDoctor && 'Dr. '}
              {record.person?.first_name} {record.person?.last_name}
            </div>
            {record.person?.middle_name && (
              <div style={{ fontSize: 12, color: '#666' }}>
                {record.person.middle_name}
              </div>
            )}
          </div>
        );
      },
    },
    {
      title: 'Role',
      dataIndex: 'role',
      key: 'role',
      width: 140,
      filters: Object.entries(roleConfig).map(([key, config]) => ({
        text: config.label,
        value: key,
      })),
      render: (role: EmployeeRole) => {
        const config = roleConfig[role];
        return (
          <Tag icon={config.icon} color={config.color}>
            {config.label}
          </Tag>
        );
      },
    },
    {
      title: 'Specialization',
      dataIndex: 'specialization',
      key: 'specialization',
      render: (specialization: string, record: Employee) => {
        if (!specialization) return '-';
        
        // Only show specialization for medical roles
        if (record.role === 'doctor' || record.role === 'nurse') {
          return (
            <Tag color="cyan">
              {specialization}
            </Tag>
          );
        }
        return specialization;
      },
    },
    {
      title: 'License',
      key: 'license',
      width: 150,
      render: (_: any, record: Employee) => {
        // Only show license for medical staff
        if (record.role !== 'doctor' && record.role !== 'nurse') {
          return '-';
        }
        
        return (
          <div style={{ fontSize: 13 }}>
            {record.license_number && (
              <div>
                <SafetyCertificateOutlined /> {record.license_number}
              </div>
            )}
            {record.license_expiry && (
              <div style={{ 
                color: dayjs(record.license_expiry).isBefore(dayjs()) ? '#ff4d4f' : '#666',
                fontSize: 11 
              }}>
                Exp: {dayjs(record.license_expiry).format('MM/YY')}
              </div>
            )}
          </div>
        );
      },
    },
    {
      title: 'Contact',
      key: 'contact',
      render: (_: any, record: Employee) => (
        <div style={{ fontSize: 13 }}>
          {record.person?.email && (
            <div>
              <MailOutlined /> {record.person.email}
            </div>
          )}
          {record.person?.phone_mobile_number && (
            <div>
              <PhoneOutlined /> 
              {record.person.phone_mobile_country_code || '+1'} 
              {record.person.phone_mobile_number}
            </div>
          )}
        </div>
      ),
    },
    {
      title: 'Clinic',
      key: 'clinic',
      render: (_: any, record: Employee) => (
        <Tag color="cyan">
          {record.clinic?.name || 'N/A'}
        </Tag>
      ),
    },
    {
      title: 'Hire Date',
      dataIndex: 'hire_date',
      key: 'hire_date',
      width: 120,
      sorter: true,
      render: (date: string) => (
        <Space>
          <CalendarOutlined />
          {dayjs(date).format('MM/DD/YYYY')}
        </Space>
      ),
    },
    {
      title: 'Can Treat',
      dataIndex: 'can_perform_treatments',
      key: 'can_perform_treatments',
      width: 100,
      align: 'center' as const,
      render: (canTreat: boolean) => {
        if (canTreat) {
          return <Badge status="success" text="Yes" />;
        }
        return <Badge status="default" text="No" />;
      },
    },
    {
      title: 'Status',
      dataIndex: 'is_active',
      key: 'is_active',
      width: 100,
      align: 'center' as const,
      filters: [
        { text: 'Active', value: true },
        { text: 'Inactive', value: false },
      ],
      render: (isActive: boolean) => (
        <Tag
          icon={isActive ? <CheckCircleOutlined /> : <CloseCircleOutlined />}
          color={isActive ? 'success' : 'default'}
        >
          {isActive ? 'Active' : 'Inactive'}
        </Tag>
      ),
    },
    {
      title: 'Actions',
      key: 'actions',
      width: 150,
      fixed: 'right' as const,
      render: (_: any, record: Employee) => (
        <Space size="small">
          <Tooltip title="View Details">
            <Button
              type="text"
              icon={<IdcardOutlined />}
              onClick={() => router.push(`/staff/employees/${record.id}`)}
            />
          </Tooltip>
          <Tooltip title="Edit">
            <Button
              type="text"
              icon={<UserOutlined />}
              onClick={() => router.push(`/staff/employees/${record.id}/edit`)}
            />
          </Tooltip>
        </Space>
      ),
    },
  ];

  // Handle navigation to create page
  const handleCreate = () => {
    router.push('/staff/employees/new');
  };

  // Handle navigation to edit page
  const handleEdit = (employee: Employee) => {
    router.push(`/staff/employees/${employee.id}/edit`);
  };

  // Handle delete
  const handleDelete = async (employee: Employee) => {
    try {
      await employeesApi.delete(employee.id);
      message.success('Employee deactivated successfully');
      return Promise.resolve();
    } catch (error) {
      console.error('Delete error:', error);
      message.error('Failed to deactivate employee');
      throw error;
    }
  };

  // Handle export
  const handleExport = async () => {
    try {
      setExporting(true);
      const blob = await employeesApi.export({ role: selectedRole });
      const filename = `employees_export_${selectedRole || 'all'}_${dayjs().format('YYYYMMDD_HHmmss')}.csv`;
      saveAs(blob, filename);
      message.success('Export completed successfully');
    } catch (error) {
      console.error('Export error:', error);
      message.error('Failed to export data');
    } finally {
      setExporting(false);
    }
  };

  // Custom actions for each row
  const customActions = [
    {
      key: 'view',
      label: 'View Full Profile',
      onClick: (employee: Employee) => {
        router.push(`/staff/employees/${employee.id}`);
      },
    },
    {
      key: 'person',
      label: 'View Person Details',
      onClick: (employee: Employee) => {
        router.push(`/persons/${employee.person_id}`);
      },
    },
    {
      key: 'schedule',
      label: 'View Schedule',
      onClick: (employee: Employee) => {
        router.push(`/staff/employees/${employee.id}/schedule`);
      },
      hidden: (employee: Employee) => !employee.can_perform_treatments,
    },
    {
      key: 'permissions',
      label: 'Manage Permissions',
      onClick: (employee: Employee) => {
        router.push(`/staff/employees/${employee.id}/permissions`);
      },
    },
    {
      key: 'deactivate',
      label: 'Deactivate',
      onClick: async (employee: Employee) => {
        try {
          await employeesApi.update(employee.id, { is_active: false });
          message.success('Employee deactivated');
        } catch (error) {
          message.error('Failed to deactivate employee');
        }
      },
      danger: true,
    },
  ];

  // Bulk actions
  const bulkActions = [
    {
      key: 'bulk-export',
      label: 'Export Selected',
      icon: <ExportOutlined />,
      onClick: (selectedKeys: React.Key[]) => {
        message.info(`Exporting ${selectedKeys.length} employees...`);
        // Implement bulk export logic
      },
    },
    {
      key: 'bulk-assign-clinic',
      label: 'Assign to Clinic',
      icon: <BankOutlined />,
      onClick: (selectedKeys: React.Key[]) => {
        message.info(`Assigning ${selectedKeys.length} employees to clinic...`);
        // Implement bulk clinic assignment
      },
    },
    {
      key: 'bulk-deactivate',
      label: 'Deactivate Selected',
      danger: true,
      onClick: (selectedKeys: React.Key[]) => {
        message.warning(`Deactivating ${selectedKeys.length} employees...`);
        // Implement bulk deactivate logic
      },
    },
  ];

  // Quick filter buttons
  const quickFilters = (
    <Space style={{ marginBottom: 16 }}>
      <Button
        type={!selectedRole ? 'primary' : 'default'}
        onClick={() => setSelectedRole(undefined)}
      >
        All Employees
      </Button>
      {Object.entries(roleConfig).map(([role, config]) => (
        <Button
          key={role}
          type={selectedRole === role ? 'primary' : 'default'}
          icon={config.icon}
          onClick={() => setSelectedRole(role as EmployeeRole)}
        >
          {config.label}s
        </Button>
      ))}
    </Space>
  );

  return (
    <div>
      {quickFilters}
      <DataTable<Employee>
        queryKey={['employees', selectedRole]}
        fetchData={(params) => employeesApi.list({ ...params, role: selectedRole })}
        columns={columns}
        rowKey="id"
        title="Employees Management"
        searchPlaceholder="Search by name, code, or email..."
        resource="employees"
        onCreate={handleCreate}
        onEdit={handleEdit}
        onDelete={handleDelete}
        onExport={handleExport}
        customActions={customActions}
        selectable={true}
        bulkActions={bulkActions}
        scroll={{ x: 1500 }}
      />
    </div>
  );
}
