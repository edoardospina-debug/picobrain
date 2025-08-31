'use client';

import React, { useState } from 'react';
import { useRouter } from 'next/navigation';
import { Tag, Button, message } from 'antd';
import {
  PhoneOutlined,
  MailOutlined,
  EnvironmentOutlined,
  CheckCircleOutlined,
  CloseCircleOutlined,
  ExportOutlined,
} from '@ant-design/icons';
import DataTable from '@/components/shared/DataTable';
import { clinicsApi } from '@/lib/api/endpoints/clinics';
import { Clinic } from '@/types';
import { saveAs } from 'file-saver';
import dayjs from 'dayjs';

export default function ClinicsPage() {
  const router = useRouter();
  const [exporting, setExporting] = useState(false);

  // Table columns configuration
  const columns = [
    {
      title: 'Code',
      dataIndex: 'code',
      key: 'code',
      width: 100,
      sorter: true,
      fixed: 'left' as const,
      render: (code: string) => (
        <span style={{ fontWeight: 600 }}>{code}</span>
      ),
    },
    {
      title: 'Name',
      dataIndex: 'name',
      key: 'name',
      sorter: true,
      render: (name: string, record: Clinic) => (
        <div>
          <div style={{ fontWeight: 500 }}>{name}</div>
          {record.tax_id && (
            <div style={{ fontSize: 12, color: '#666' }}>
              Tax ID: {record.tax_id}
            </div>
          )}
        </div>
      ),
    },
    {
      title: 'Location',
      key: 'location',
      render: (_: any, record: Clinic) => (
        <div style={{ fontSize: 13 }}>
          {record.city && (
            <div>
              <EnvironmentOutlined /> {record.city}
              {record.state_province && `, ${record.state_province}`}
            </div>
          )}
          {record.country_code && (
            <div style={{ color: '#666' }}>{record.country_code}</div>
          )}
        </div>
      ),
    },
    {
      title: 'Contact',
      key: 'contact',
      render: (_: any, record: Clinic) => (
        <div style={{ fontSize: 13 }}>
          {record.phone_number && (
            <div>
              <PhoneOutlined /> {record.phone_country_code && `+${record.phone_country_code} `}
              {record.phone_number}
            </div>
          )}
          {record.email && (
            <div>
              <MailOutlined /> {record.email}
            </div>
          )}
        </div>
      ),
    },
    {
      title: 'Currency',
      dataIndex: 'functional_currency',
      key: 'functional_currency',
      width: 100,
      align: 'center' as const,
      render: (currency: string) => (
        <Tag color="blue">{currency}</Tag>
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
      title: 'Created',
      dataIndex: 'created_at',
      key: 'created_at',
      width: 150,
      sorter: true,
      render: (date: string) => dayjs(date).format('MM/DD/YYYY'),
    },
  ];

  // Handle navigation to create page
  const handleCreate = () => {
    router.push('/clinics/new');
  };

  // Handle navigation to edit page
  const handleEdit = (clinic: Clinic) => {
    router.push(`/clinics/${clinic.id}`);
  };

  // Handle delete
  const handleDelete = async (clinic: Clinic) => {
    try {
      await clinicsApi.delete(clinic.id);
      return Promise.resolve();
    } catch (error) {
      console.error('Delete error:', error);
      throw error;
    }
  };

  // Handle export
  const handleExport = async () => {
    try {
      setExporting(true);
      const blob = await clinicsApi.export();
      const filename = `clinics_export_${dayjs().format('YYYYMMDD_HHmmss')}.csv`;
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
      label: 'View Details',
      onClick: (clinic: Clinic) => {
        router.push(`/clinics/${clinic.id}/view`);
      },
    },
    {
      key: 'deactivate',
      label: 'Deactivate',
      onClick: async (clinic: Clinic) => {
        try {
          await clinicsApi.update(clinic.id, { is_active: false });
          message.success('Clinic deactivated');
        } catch (error) {
          message.error('Failed to deactivate clinic');
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
        message.info(`Exporting ${selectedKeys.length} clinics...`);
        // Implement bulk export logic
      },
    },
    {
      key: 'bulk-deactivate',
      label: 'Deactivate Selected',
      danger: true,
      onClick: (selectedKeys: React.Key[]) => {
        message.warning(`Deactivating ${selectedKeys.length} clinics...`);
        // Implement bulk deactivate logic
      },
    },
  ];

  return (
    <DataTable<Clinic>
      queryKey={['clinics']}
      fetchData={clinicsApi.list}
      columns={columns}
      rowKey="id"
      title="Clinics Management"
      searchPlaceholder="Search by name or code..."
      resource="clinics"
      onCreate={handleCreate}
      onEdit={handleEdit}
      onDelete={handleDelete}
      onExport={handleExport}
      customActions={customActions}
      selectable={true}
      bulkActions={bulkActions}
      scroll={{ x: 1200 }}
    />
  );
}
