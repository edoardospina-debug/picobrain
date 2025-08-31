'use client';

import React, { useEffect, useState } from 'react';
import { Button, Card, message, Space, Tag, Alert, Spin } from 'antd';
import { ReloadOutlined, CheckCircleOutlined, CloseCircleOutlined } from '@ant-design/icons';

export default function EmployeeDebugPage() {
  const [loading, setLoading] = useState(false);
  const [data, setData] = useState<any>(null);
  const [error, setError] = useState<string | null>(null);
  const [token, setToken] = useState<string | null>(null);
  const [apiResponse, setApiResponse] = useState<any>(null);
  
  // Check token on mount
  useEffect(() => {
    const storedToken = localStorage.getItem('picobrain_access_token');
    setToken(storedToken);
  }, []);
  
  // Test direct API call
  const testDirectApi = async () => {
    setLoading(true);
    setError(null);
    setData(null);
    
    try {
      const storedToken = localStorage.getItem('picobrain_access_token');
      
      if (!storedToken) {
        throw new Error('No access token found. Please login first.');
      }
      
      console.log('Making API request with token:', storedToken.substring(0, 20) + '...');
      
      const response = await fetch('http://localhost:8000/api/v1/employees?skip=0&limit=10', {
        method: 'GET',
        headers: {
          'Authorization': `Bearer ${storedToken}`,
          'Content-Type': 'application/json',
        },
      });
      
      console.log('Response status:', response.status);
      console.log('Response headers:', response.headers);
      
      if (!response.ok) {
        const errorText = await response.text();
        throw new Error(`API Error (${response.status}): ${errorText}`);
      }
      
      const data = await response.json();
      console.log('API Response:', data);
      
      setData(data);
      setApiResponse({
        status: response.status,
        statusText: response.statusText,
        dataLength: Array.isArray(data) ? data.length : 0,
        sampleData: Array.isArray(data) && data.length > 0 ? data[0] : null,
      });
      
      message.success(`Successfully fetched ${Array.isArray(data) ? data.length : 0} employees`);
    } catch (err: any) {
      console.error('API Error:', err);
      setError(err.message);
      message.error(err.message);
    } finally {
      setLoading(false);
    }
  };
  
  // Test using the employeesApi service
  const testEmployeesApi = async () => {
    setLoading(true);
    setError(null);
    setData(null);
    
    try {
      const { employeesApi } = await import('@/lib/api/endpoints/employees');
      
      console.log('Testing employeesApi.list()...');
      const result = await employeesApi.list({ page: 1, limit: 10 });
      
      console.log('employeesApi result:', result);
      
      setData(result.items);
      setApiResponse({
        items: result.items?.length || 0,
        total: result.total,
        sampleData: result.items?.[0] || null,
      });
      
      message.success(`Successfully fetched ${result.items?.length || 0} employees via API service`);
    } catch (err: any) {
      console.error('Service Error:', err);
      setError(err.message);
      message.error(err.message);
    } finally {
      setLoading(false);
    }
  };
  
  // Login test
  const testLogin = async () => {
    setLoading(true);
    setError(null);
    
    try {
      const formData = new URLSearchParams();
      formData.append('username', 'admin@picobrain.com');
      formData.append('password', 'admin123');
      
      const response = await fetch('http://localhost:8000/api/v1/auth/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: formData,
      });
      
      if (!response.ok) {
        throw new Error(`Login failed: ${response.status}`);
      }
      
      const data = await response.json();
      console.log('Login response:', data);
      
      if (data.access_token) {
        localStorage.setItem('picobrain_access_token', data.access_token);
        setToken(data.access_token);
        message.success('Login successful! Token saved.');
      }
    } catch (err: any) {
      console.error('Login Error:', err);
      setError(err.message);
      message.error(err.message);
    } finally {
      setLoading(false);
    }
  };
  
  return (
    <div style={{ padding: 24 }}>
      <h1>Employee API Debug Page</h1>
      
      {/* Token Status */}
      <Card title="Authentication Status" style={{ marginBottom: 16 }}>
        {token ? (
          <Alert
            message="Token Found"
            description={`Token: ${token.substring(0, 30)}...`}
            type="success"
            icon={<CheckCircleOutlined />}
          />
        ) : (
          <Alert
            message="No Token Found"
            description="You need to login first to access the API"
            type="error"
            icon={<CloseCircleOutlined />}
            action={
              <Button size="small" danger onClick={testLogin}>
                Login as Admin
              </Button>
            }
          />
        )}
      </Card>
      
      {/* Test Actions */}
      <Card title="API Tests" style={{ marginBottom: 16 }}>
        <Space>
          <Button 
            type="primary" 
            icon={<ReloadOutlined />} 
            onClick={testDirectApi}
            loading={loading}
            disabled={!token}
          >
            Test Direct API Call
          </Button>
          
          <Button 
            icon={<ReloadOutlined />} 
            onClick={testEmployeesApi}
            loading={loading}
            disabled={!token}
          >
            Test via employeesApi Service
          </Button>
          
          {!token && (
            <Button 
              type="primary"
              danger
              onClick={testLogin}
              loading={loading}
            >
              Login First
            </Button>
          )}
        </Space>
      </Card>
      
      {/* Loading State */}
      {loading && (
        <Card style={{ marginBottom: 16 }}>
          <Spin tip="Loading..." />
        </Card>
      )}
      
      {/* Error Display */}
      {error && (
        <Alert
          message="Error"
          description={error}
          type="error"
          showIcon
          style={{ marginBottom: 16 }}
        />
      )}
      
      {/* API Response */}
      {apiResponse && (
        <Card title="API Response Info" style={{ marginBottom: 16 }}>
          <pre>{JSON.stringify(apiResponse, null, 2)}</pre>
        </Card>
      )}
      
      {/* Data Display */}
      {data && (
        <Card title={`Employee Data (${Array.isArray(data) ? data.length : 0} records)`}>
          <div style={{ maxHeight: 600, overflow: 'auto' }}>
            {Array.isArray(data) && data.length > 0 ? (
              data.map((emp: any) => (
                <Card key={emp.id} size="small" style={{ marginBottom: 8 }}>
                  <div>
                    <strong>Code:</strong> {emp.employee_code} |{' '}
                    <strong>Role:</strong> <Tag>{emp.role}</Tag> |{' '}
                    <strong>Name:</strong> {emp.person?.first_name} {emp.person?.last_name} |{' '}
                    <strong>Email:</strong> {emp.person?.email || 'N/A'}
                  </div>
                </Card>
              ))
            ) : (
              <Alert message="No data returned" type="warning" />
            )}
          </div>
        </Card>
      )}
      
      {/* Console Instructions */}
      <Card title="Debug Instructions" style={{ marginTop: 16 }}>
        <ol>
          <li>Open browser console (F12)</li>
          <li>Click "Login First" if no token is present</li>
          <li>Click "Test Direct API Call" to test raw fetch</li>
          <li>Click "Test via employeesApi Service" to test the service layer</li>
          <li>Check console for detailed logs</li>
          <li>Check Network tab to see actual API requests</li>
        </ol>
      </Card>
    </div>
  );
}
