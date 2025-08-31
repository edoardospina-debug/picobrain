import React, { useState, useEffect, useCallback } from 'react';
import {
  Table,
  Button,
  Input,
  Space,
  Dropdown,
  Modal,
  message,
  Tooltip,
  Tag,
  TableProps,
} from 'antd';
import {
  SearchOutlined,
  PlusOutlined,
  EditOutlined,
  DeleteOutlined,
  ExportOutlined,
  ReloadOutlined,
  FilterOutlined,
  MoreOutlined,
} from '@ant-design/icons';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import type { ColumnsType, TablePaginationConfig } from 'antd/es/table';
import type { FilterValue, SorterResult } from 'antd/es/table/interface';
import { useAuth } from '@/lib/auth/AuthProvider';
import { debounce } from 'lodash';

const { Search } = Input;
const { confirm } = Modal;

export interface DataTableColumn<T> {
  searchable?: boolean;
  exportable?: boolean;
  [key: string]: any; // Allow any column properties from Ant Design
}

export interface DataTableProps<T> {
  // Data fetching
  queryKey: string[];
  fetchData: (params: any) => Promise<{ items: T[]; total: number }>;
  
  // Display
  columns: DataTableColumn<T>[];
  rowKey: string | ((record: T) => string);
  title?: string;
  
  // Features
  searchable?: boolean;
  searchPlaceholder?: string;
  creatable?: boolean;
  editable?: boolean;
  deletable?: boolean;
  exportable?: boolean;
  refreshable?: boolean;
  
  // Permissions
  resource?: string;
  
  // Actions
  onCreate?: () => void;
  onEdit?: (record: T) => void;
  onDelete?: (record: T) => Promise<void>;
  onExport?: () => void;
  
  // Custom actions
  customActions?: Array<{
    key: string;
    label: string;
    icon?: React.ReactNode;
    onClick: (record: T) => void;
    danger?: boolean;
  }>;
  
  // Bulk actions
  selectable?: boolean;
  bulkActions?: Array<{
    key: string;
    label: string;
    icon?: React.ReactNode;
    onClick: (selectedKeys: React.Key[]) => void;
    danger?: boolean;
  }>;
  
  // Table config
  pageSize?: number;
  pageSizeOptions?: string[];
  size?: 'small' | 'middle' | 'large';
  scroll?: { x?: number; y?: number };
}

export default function DataTable<T extends Record<string, any>>({
  queryKey,
  fetchData,
  columns,
  rowKey,
  title,
  searchable = true,
  searchPlaceholder = 'Search...',
  creatable = true,
  editable = true,
  deletable = true,
  exportable = true,
  refreshable = true,
  resource,
  onCreate,
  onEdit,
  onDelete,
  onExport,
  customActions = [],
  selectable = false,
  bulkActions = [],
  pageSize: defaultPageSize = 20,
  pageSizeOptions = ['10', '20', '50', '100'],
  size = 'middle',
  scroll,
}: DataTableProps<T>) {
  const { hasPermission } = useAuth();
  const queryClient = useQueryClient();
  
  // Table state
  const [searchText, setSearchText] = useState('');
  const [pagination, setPagination] = useState<TablePaginationConfig>({
    current: 1,
    pageSize: defaultPageSize,
    showSizeChanger: true,
    pageSizeOptions,
    showTotal: (total, range) => `${range[0]}-${range[1]} of ${total} items`,
  });
  const [filters, setFilters] = useState<Record<string, FilterValue | null>>({});
  const [sorter, setSorter] = useState<SorterResult<T> | SorterResult<T>[]>({});
  const [selectedRowKeys, setSelectedRowKeys] = useState<React.Key[]>([]);
  
  // Fetch data
  const { data, isLoading, refetch, isRefetching } = useQuery({
    queryKey: [...queryKey, pagination, searchText, filters, sorter],
    queryFn: () => {
      const params: any = {
        page: pagination.current,
        limit: pagination.pageSize,
      };
      
      if (searchText) {
        params.search = searchText;
      }
      
      // Add filters
      Object.entries(filters).forEach(([key, value]) => {
        if (value) {
          params[key] = value;
        }
      });
      
      // Add sorting
      if (!Array.isArray(sorter) && sorter.field) {
        params.sort_by = sorter.field;
        params.sort_order = sorter.order === 'descend' ? 'desc' : 'asc';
      }
      
      return fetchData(params);
    },
    staleTime: 5 * 60 * 1000, // 5 minutes
  });
  
  // Delete mutation
  const deleteMutation = useMutation({
    mutationFn: onDelete || (() => Promise.resolve()),
    onSuccess: () => {
      message.success('Deleted successfully');
      queryClient.invalidateQueries({ queryKey });
    },
    onError: () => {
      message.error('Failed to delete');
    },
  });
  
  // Debounced search
  const debouncedSearch = useCallback(
    debounce((value: string) => {
      setSearchText(value);
      setPagination(prev => ({ ...prev, current: 1 }));
    }, 500),
    []
  );
  
  // Handle table change
  const handleTableChange: TableProps<T>['onChange'] = (
    newPagination,
    newFilters,
    newSorter
  ) => {
    setPagination(newPagination);
    setFilters(newFilters);
    setSorter(newSorter as SorterResult<T>);
  };
  
  // Handle delete
  const handleDelete = (record: T) => {
    confirm({
      title: 'Are you sure you want to delete this item?',
      content: 'This action cannot be undone.',
      okText: 'Yes, delete',
      okType: 'danger',
      cancelText: 'Cancel',
      onOk: () => deleteMutation.mutate(record),
    });
  };
  
  // Build action column
  const actionColumn: ColumnsType<T>[0] = {
    title: 'Actions',
    key: 'actions',
    fixed: 'right',
    width: 100,
    render: (_, record) => {
      const items = [];
      
      if (editable && onEdit && (!resource || hasPermission(resource, 'edit'))) {
        items.push({
          key: 'edit',
          label: 'Edit',
          icon: <EditOutlined />,
          onClick: () => onEdit(record),
        });
      }
      
      // Add custom actions
      customActions.forEach(action => {
        items.push({
          key: action.key,
          label: action.label,
          icon: action.icon,
          onClick: () => action.onClick(record),
          danger: action.danger,
        });
      });
      
      if (deletable && onDelete && (!resource || hasPermission(resource, 'delete'))) {
        items.push({
          key: 'delete',
          label: 'Delete',
          icon: <DeleteOutlined />,
          danger: true,
          onClick: () => handleDelete(record),
        });
      }
      
      if (items.length === 0) return null;
      
      if (items.length === 1) {
        const item = items[0];
        return (
          <Button
            type="text"
            size="small"
            icon={item.icon}
            danger={item.danger}
            onClick={item.onClick}
          >
            {item.label}
          </Button>
        );
      }
      
      return (
        <Dropdown
          menu={{ items }}
          trigger={['click']}
        >
          <Button type="text" size="small" icon={<MoreOutlined />} />
        </Dropdown>
      );
    },
  };
  
  // Final columns with actions
  const finalColumns = [...columns];
  if ((editable && onEdit) || (deletable && onDelete) || customActions.length > 0) {
    finalColumns.push(actionColumn);
  }
  
  // Row selection config
  const rowSelection = selectable
    ? {
        selectedRowKeys,
        onChange: (keys: React.Key[]) => setSelectedRowKeys(keys),
      }
    : undefined;
  
  return (
    <div style={{ padding: 24 }}>
      {/* Header */}
      <div style={{ marginBottom: 16, display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <div style={{ display: 'flex', gap: 16, alignItems: 'center' }}>
          {title && (
            <h2 style={{ margin: 0, fontSize: 20, fontWeight: 600 }}>{title}</h2>
          )}
          {searchable && (
            <Search
              placeholder={searchPlaceholder}
              allowClear
              style={{ width: 300 }}
              onChange={(e) => debouncedSearch(e.target.value)}
              loading={isLoading}
            />
          )}
        </div>
        
        <Space>
          {/* Bulk actions */}
          {selectedRowKeys.length > 0 && bulkActions.length > 0 && (
            <Dropdown
              menu={{
                items: bulkActions.map(action => ({
                  key: action.key,
                  label: action.label,
                  icon: action.icon,
                  danger: action.danger,
                  onClick: () => action.onClick(selectedRowKeys),
                })),
              }}
            >
              <Button icon={<MoreOutlined />}>
                Bulk Actions ({selectedRowKeys.length})
              </Button>
            </Dropdown>
          )}
          
          {refreshable && (
            <Tooltip title="Refresh">
              <Button
                icon={<ReloadOutlined />}
                onClick={() => refetch()}
                loading={isRefetching}
              />
            </Tooltip>
          )}
          
          {exportable && onExport && (!resource || hasPermission(resource, 'export')) && (
            <Button icon={<ExportOutlined />} onClick={onExport}>
              Export
            </Button>
          )}
          
          {creatable && onCreate && (!resource || hasPermission(resource, 'create')) && (
            <Button type="primary" icon={<PlusOutlined />} onClick={onCreate}>
              Add New
            </Button>
          )}
        </Space>
      </div>
      
      {/* Table */}
      <Table<T>
        columns={finalColumns}
        dataSource={data?.items || []}
        rowKey={rowKey}
        pagination={{
          ...pagination,
          total: data?.total || 0,
        }}
        loading={isLoading}
        onChange={handleTableChange}
        rowSelection={rowSelection}
        size={size}
        scroll={scroll}
      />
    </div>
  );
}
