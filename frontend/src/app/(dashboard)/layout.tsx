'use client';

import React, { useState } from 'react';
import { Layout, Menu, Avatar, Dropdown, Space, Typography, Badge } from 'antd';
import {
  HomeOutlined,
  ShopOutlined,
  TeamOutlined,
  UserOutlined,
  SettingOutlined,
  LogoutOutlined,
  MenuFoldOutlined,
  MenuUnfoldOutlined,
  BellOutlined,
  FileTextOutlined,
  DollarOutlined,
} from '@ant-design/icons';
import { useRouter, usePathname } from 'next/navigation';
import { useAuth } from '@/lib/auth/AuthProvider';
import type { MenuProps } from 'antd';

const { Header, Sider, Content } = Layout;
const { Text } = Typography;

export default function DashboardLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const [collapsed, setCollapsed] = useState(false);
  const router = useRouter();
  const pathname = usePathname();
  const { user, logout, hasPermission } = useAuth();

  // Build menu items based on permissions
  const menuItems: MenuProps['items'] = [
    {
      key: '/clinics',
      icon: <ShopOutlined />,
      label: 'Clinics',
      onClick: () => router.push('/clinics'),
    },
    hasPermission('employees', 'view') && {
      key: '/staff',
      icon: <TeamOutlined />,
      label: 'Staff',
      children: [
        {
          key: '/staff/employees',
          label: 'Employees',
          onClick: () => router.push('/staff/employees'),
        },
        {
          key: '/staff/doctors',
          label: 'Doctors',
          onClick: () => router.push('/staff/doctors'),
        },
      ],
    },
    hasPermission('clients', 'view') && {
      key: '/clients',
      icon: <UserOutlined />,
      label: 'Clients',
      onClick: () => router.push('/clients'),
    },
    hasPermission('users', 'view') && {
      key: '/users',
      icon: <UserOutlined />,
      label: 'Users',
      onClick: () => router.push('/users'),
    },
    // Additional menu items for future modules
    {
      key: 'reports',
      icon: <FileTextOutlined />,
      label: 'Reports',
      children: [
        hasPermission('reports', 'view') && {
          key: '/reports/financial',
          label: 'Financial Reports',
          onClick: () => router.push('/reports/financial'),
        },
        hasPermission('reports', 'view') && {
          key: '/reports/operational',
          label: 'Operational Reports',
          onClick: () => router.push('/reports/operational'),
        },
      ].filter(Boolean),
    },
    hasPermission('settings', 'view') && {
      key: '/settings',
      icon: <SettingOutlined />,
      label: 'Settings',
      onClick: () => router.push('/settings'),
    },
  ].filter(Boolean) as MenuProps['items'];

  const userMenuItems: MenuProps['items'] = [
    {
      key: 'profile',
      icon: <UserOutlined />,
      label: 'Profile',
      onClick: () => router.push('/profile'),
    },
    {
      key: 'settings',
      icon: <SettingOutlined />,
      label: 'Settings',
      onClick: () => router.push('/settings'),
    },
    {
      type: 'divider',
    },
    {
      key: 'logout',
      icon: <LogoutOutlined />,
      label: 'Logout',
      onClick: logout,
    },
  ];

  const getSelectedKeys = () => {
    // Match the current path to menu keys
    if (pathname.startsWith('/staff')) {
      return [pathname];
    }
    return [pathname.split('/').slice(0, 2).join('/')];
  };

  const getOpenKeys = () => {
    // Open parent menu if in submenu
    if (pathname.startsWith('/staff')) {
      return ['/staff'];
    }
    if (pathname.startsWith('/reports')) {
      return ['reports'];
    }
    return [];
  };

  return (
    <Layout style={{ minHeight: '100vh' }}>
      <Sider 
        trigger={null} 
        collapsible 
        collapsed={collapsed}
        theme="light"
        width={250}
        style={{
          borderRight: '1px solid #f0f0f0',
        }}
      >
        <div 
          style={{ 
            height: 64, 
            display: 'flex', 
            alignItems: 'center', 
            justifyContent: 'center',
            borderBottom: '1px solid #f0f0f0',
          }}
        >
          <Typography.Title 
            level={4} 
            style={{ margin: 0, color: '#1890ff' }}
          >
            {collapsed ? 'PB' : 'PicoBrain'}
          </Typography.Title>
        </div>
        <Menu
          theme="light"
          mode="inline"
          selectedKeys={getSelectedKeys()}
          defaultOpenKeys={getOpenKeys()}
          items={menuItems}
          style={{ borderRight: 0 }}
        />
      </Sider>
      <Layout>
        <Header 
          style={{ 
            padding: 0, 
            background: '#fff',
            borderBottom: '1px solid #f0f0f0',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'space-between',
          }}
        >
          <div style={{ display: 'flex', alignItems: 'center' }}>
            {React.createElement(collapsed ? MenuUnfoldOutlined : MenuFoldOutlined, {
              className: 'trigger',
              onClick: () => setCollapsed(!collapsed),
              style: { fontSize: '18px', padding: '0 24px', cursor: 'pointer' },
            })}
          </div>
          
          <div style={{ paddingRight: 24, display: 'flex', alignItems: 'center', gap: 20 }}>
            {/* Notifications */}
            <Badge count={5} size="small">
              <BellOutlined style={{ fontSize: 18, cursor: 'pointer' }} />
            </Badge>
            
            {/* User Menu */}
            <Dropdown menu={{ items: userMenuItems }} placement="bottomRight">
              <Space style={{ cursor: 'pointer' }}>
                <Avatar size="small" icon={<UserOutlined />} />
                <div style={{ display: 'flex', flexDirection: 'column', lineHeight: 1.2 }}>
                  <Text strong style={{ fontSize: 13 }}>
                    {user?.username || 'User'}
                  </Text>
                  <Text type="secondary" style={{ fontSize: 11 }}>
                    {user?.role || 'Role'}
                  </Text>
                </div>
              </Space>
            </Dropdown>
          </div>
        </Header>
        
        <Content
          style={{
            margin: '24px',
            minHeight: 280,
            background: '#fff',
            borderRadius: 8,
            overflow: 'auto',
          }}
        >
          {children}
        </Content>
      </Layout>
    </Layout>
  );
}
