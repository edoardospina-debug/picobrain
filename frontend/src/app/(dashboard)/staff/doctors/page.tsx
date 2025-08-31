'use client';

import React, { useState } from 'react';
import { useRouter } from 'next/navigation';
import { Tag, Button, message, Space, Tooltip } from 'antd';
import {
  PhoneOutlined,
  MailOutlined,
  UserOutlined,
  MedicineBoxOutlined,
  SafetyCertificateOutlined,
  DollarOutlined,
  CalendarOutlined,
  CheckCircleOutlined,
  CloseCircleOutlined,
  ExportOutlined,
  IdcardOutlined,
} from '@ant-design/icons';
import DataTable from '@/components/shared/DataTable';
import { doctorsApi } from '@/lib/api/endpoints/employees';
import { Doctor } from '@/types';
import { saveAs } from 'file-saver';
import dayjs from 'dayjs';

export default function DoctorsPage() {
  const router = useRouter();
  const [exporting, setExporting] = useState(false);

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
      render: (_: any, record: Doctor) => (
        <div>
          <div style={{ fontWeight: 500 }}>
            <UserOutlined /> Dr. {record.person?.first_name} {record.person?.last_name}
          </div>
          {record.person?.middle_name && (
            <div style={{ fontSize: 12, color: '#666' }}>
              {record.person.middle_name}
            </div>
          )}
        </div>
      ),
    },
    {
      title: 'Specialization',
      dataIndex: 'specialization',
      key: 'specialization',
      render: (specialization: string) => (
        <Tag icon={<MedicineBoxOutlined />} color="blue">
          {specialization || 'General Practice'}
        </Tag>
      ),
    },
    {
      title: 'License',
      key: 'license',
      render: (_: any, record: Doctor) => (
        <div style={{ fontSize: 13 }}>
          {record.license_number && (
            <div>
              <SafetyCertificateOutlined /> {record.license_number}
            </div>
          )}
          {record.license_expiry && (
            <div style={{ color: dayjs(record.license_expiry).isBefore(dayjs()) ? '#ff4d4f' : '#666' }}>
              Expires: {dayjs(record.license_expiry).format('MM/DD/YYYY')}
            </div>
          )}
        </div>
      ),
    },
    {
      title: 'Contact',
      key: 'contact',
      render: (_: any, record: Doctor) => (
        <div style={{ fontSize: 13 }}>
          {record.person?.email && (
            <div>
              <MailOutlined /> {record.person.email}
            </div>
          )}
          {record.person?.phone_mobile_number && (
            <div>
              <PhoneOutlined /> 
              {record.person.phone_mobile_country_code && `+${record.person.phone_mobile_country_code} `}
              {record.person.phone_mobile_number}
            </div>
          )}
        </div>
      ),
    },
    {
      title: 'Clinic',
      key: 'clinic',
      render: (_: any, record: Doctor) => (
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
      render: (_: any, record: Doctor) => (
        <Space size="small">
          <Tooltip title="View Details">
            <Button
              type="text"
              icon={<IdcardOutlined />}
              onClick={() => router.push(`/staff/doctors/${record.id}`)}
            />
          </Tooltip>
          <Tooltip title="Edit">
            <Button
              type="text"
              icon={<UserOutlined />}
              onClick={() => router.push(`/staff/doctors/${record.id}/edit`)}
            />
          </Tooltip>
        </Space>
      ),
    },
  ];

  // Handle navigation to create page
  const handleCreate = () => {
    router.push('/staff/doctors/new');
  };

  // Handle navigation to edit page
  const handleEdit = (doctor: Doctor) => {
    router.push(`/staff/doctors/${doctor.id}/edit`);
  };

  // Handle delete
  const handleDelete = async (doctor: Doctor) => {
    try {
      await doctorsApi.delete(doctor.id);
      message.success('Doctor deactivated successfully');
      return Promise.resolve();
    } catch (error) {
      console.error('Delete error:', error);
      message.error('Failed to deactivate doctor');
      throw error;
    }
  };

  // Handle export
  const handleExport = async () => {
    try {
      setExporting(true);
      const blob = await doctorsApi.export();
      const filename = `doctors_export_${dayjs().format('YYYYMMDD_HHmmss')}.csv`;
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
      onClick: (doctor: Doctor) => {
        router.push(`/staff/doctors/${doctor.id}`);
      },
    },
    {
      key: 'schedule',
      label: 'View Schedule',
      onClick: (doctor: Doctor) => {
        router.push(`/staff/doctors/${doctor.id}/schedule`);
      },
    },
    {
      key: 'patients',
      label: 'View Patients',
      onClick: (doctor: Doctor) => {
        router.push(`/staff/doctors/${doctor.id}/patients`);
      },
    },
    {
      key: 'deactivate',
      label: 'Deactivate',
      onClick: async (doctor: Doctor) => {
        try {
          await doctorsApi.update(doctor.id, { is_active: false });
          message.success('Doctor deactivated');
        } catch (error) {
          message.error('Failed to deactivate doctor');
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
        message.info(`Exporting ${selectedKeys.length} doctors...`);
        // Implement bulk export logic
      },
    },
    {
      key: 'bulk-deactivate',
      label: 'Deactivate Selected',
      danger: true,
      onClick: (selectedKeys: React.Key[]) => {
        message.warning(`Deactivating ${selectedKeys.length} doctors...`);
        // Implement bulk deactivate logic
      },
    },
  ];

  return (
    <DataTable<Doctor>
      queryKey={['doctors']}
      fetchData={doctorsApi.list}
      columns={columns}
      rowKey="id"
      title="Doctors Management"
      searchPlaceholder="Search by name, code, or specialization..."
      resource="doctors"
      onCreate={handleCreate}
      onEdit={handleEdit}
      onDelete={handleDelete}
      onExport={handleExport}
      customActions={customActions}
      selectable={true}
      bulkActions={bulkActions}
      scroll={{ x: 1400 }}
    />
  );
}
