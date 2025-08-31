'use client';

import React, { useState } from 'react';
import { Card, Button, Form, Input, Alert, Space, Typography, message, Divider } from 'antd';
import { UserOutlined, LockOutlined, CheckCircleOutlined, CloseCircleOutlined } from '@ant-design/icons';
import axios from 'axios';

const { Title, Text, Paragraph } = Typography;

export default function AuthDebugPage() {
  const [loading, setLoading] = useState(false);
  const [token, setToken] = useState<string | null>(null);
  const [user, setUser] = useState<any>(null);
  const [error, setError] = useState<string | null>(null);
  const [apiResponse, setApiResponse] = useState<any>(null);
  
  // Test direct login
  const testDirectLogin = async (values: { username: string; password: string }) => {
    setLoading(true);
    setError(null);
    setApiResponse(null);
    
    try {
      console.log('Testing direct login with:', values);
      
      // Prepare form data (OAuth2 requires form-encoded data)
      const formData = new URLSearchParams();
      formData.append('username', values.username);
      formData.append('password', values.password);
      
      console.log('Form data:', formData.toString());
      
      const response = await axios.post(
        'http://localhost:8000/api/v1/auth/login',
        formData,
        {
          headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
          },
        }
      );
      
      console.log('Login response:', response.data);
      
      setApiResponse(response.data);
      
      if (response.data.access_token) {
        setToken(response.data.access_token);
        setUser(response.data.user);
        
        // Store in localStorage
        localStorage.setItem('picobrain_access_token', response.data.access_token);
        
        message.success('Login successful! Token saved to localStorage.');
      }
    } catch (err: any) {
      console.error('Login error:', err);
      const errorMessage = err.response?.data?.detail || err.message || 'Login failed';
      setError(errorMessage);
      setApiResponse(err.response?.data);
      message.error(errorMessage);
    } finally {
      setLoading(false);
    }
  };
  
  // Test /auth/me endpoint
  const testAuthMe = async () => {
    setLoading(true);
    setError(null);
    
    try {
      const storedToken = localStorage.getItem('picobrain_access_token');
      if (!storedToken) {
        throw new Error('No token found in localStorage');
      }
      
      const response = await axios.get('http://localhost:8000/api/v1/auth/me', {
        headers: {
          'Authorization': `Bearer ${storedToken}`,
        },
      });
      
      console.log('/auth/me response:', response.data);
      setUser(response.data);
      message.success('User data fetched successfully');
    } catch (err: any) {
      console.error('Auth check error:', err);
      const errorMessage = err.response?.data?.detail || err.message || 'Auth check failed';
      setError(errorMessage);
      message.error(errorMessage);
    } finally {
      setLoading(false);
    }
  };
  
  // Test backend health
  const testBackendHealth = async () => {
    setLoading(true);
    setError(null);
    
    try {
      const response = await axios.get('http://localhost:8000/health');
      console.log('Health check:', response.data);
      message.success('Backend is healthy!');
      setApiResponse(response.data);
    } catch (err: any) {
      console.error('Health check error:', err);
      setError('Backend is not reachable. Make sure it\'s running on port 8000.');
      message.error('Backend not reachable');
    } finally {
      setLoading(false);
    }
  };
  
  // Clear stored data
  const clearAuth = () => {
    localStorage.removeItem('picobrain_access_token');
    setToken(null);
    setUser(null);
    setApiResponse(null);
    message.info('Cleared authentication data');
  };
  
  // Check stored token
  React.useEffect(() => {
    const storedToken = localStorage.getItem('picobrain_access_token');
    if (storedToken) {
      setToken(storedToken);
    }
  }, []);
  
  return (
    <div style={{ padding: 24, maxWidth: 1200, margin: '0 auto' }}>
      <Title level={2}>Authentication Debug Page</Title>
      <Paragraph>
        Use this page to debug authentication issues. Test the login flow step by step.
      </Paragraph>
      
      {/* Backend Status */}
      <Card title="1. Backend Health Check" style={{ marginBottom: 16 }}>
        <Space direction="vertical" style={{ width: '100%' }}>
          <Text>First, verify the backend is running and accessible.</Text>
          <Button onClick={testBackendHealth} loading={loading}>
            Test Backend Health
          </Button>
        </Space>
      </Card>
      
      {/* Current Auth Status */}
      <Card title="2. Current Authentication Status" style={{ marginBottom: 16 }}>
        <Space direction="vertical" style={{ width: '100%' }}>
          {token ? (
            <Alert
              message="Token Found"
              description={
                <div>
                  <div>Token: {token.substring(0, 30)}...</div>
                  <div style={{ marginTop: 8 }}>
                    <Button size="small" onClick={testAuthMe}>
                      Test /auth/me Endpoint
                    </Button>
                  </div>
                </div>
              }
              type="success"
              icon={<CheckCircleOutlined />}
            />
          ) : (
            <Alert
              message="No Token Found"
              description="No authentication token in localStorage"
              type="warning"
              icon={<CloseCircleOutlined />}
            />
          )}
          
          {user && (
            <Alert
              message="User Data"
              description={
                <pre style={{ fontSize: 12 }}>
                  {JSON.stringify(user, null, 2)}
                </pre>
              }
              type="info"
            />
          )}
          
          <Button danger onClick={clearAuth} disabled={!token}>
            Clear Authentication Data
          </Button>
        </Space>
      </Card>
      
      {/* Login Test */}
      <Card title="3. Test Login" style={{ marginBottom: 16 }}>
        <Form
          layout="vertical"
          onFinish={testDirectLogin}
          initialValues={{
            username: 'admin@picobrain.com',
            password: 'admin123',
          }}
        >
          <Form.Item
            label="Username"
            name="username"
            rules={[{ required: true }]}
          >
            <Input prefix={<UserOutlined />} placeholder="admin@picobrain.com" />
          </Form.Item>
          
          <Form.Item
            label="Password"
            name="password"
            rules={[{ required: true }]}
          >
            <Input.Password prefix={<LockOutlined />} placeholder="admin123" />
          </Form.Item>
          
          <Form.Item>
            <Button type="primary" htmlType="submit" loading={loading} block>
              Test Login
            </Button>
          </Form.Item>
        </Form>
        
        <Divider />
        
        <Alert
          message="Test Credentials"
          description={
            <Space direction="vertical">
              <Text>Admin: admin@picobrain.com / admin123</Text>
              <Text>Manager: manager@picobrain.com / manager123</Text>
              <Text>Staff: staff@picobrain.com / staff123</Text>
            </Space>
          }
          type="info"
        />
      </Card>
      
      {/* API Response */}
      {apiResponse && (
        <Card title="API Response" style={{ marginBottom: 16 }}>
          <pre style={{ maxHeight: 400, overflow: 'auto' }}>
            {JSON.stringify(apiResponse, null, 2)}
          </pre>
        </Card>
      )}
      
      {/* Error Display */}
      {error && (
        <Alert
          message="Error"
          description={error}
          type="error"
          showIcon
          closable
          onClose={() => setError(null)}
          style={{ marginBottom: 16 }}
        />
      )}
      
      {/* Debug Instructions */}
      <Card title="Debug Instructions">
        <ol>
          <li>First, click "Test Backend Health" to ensure the backend is running</li>
          <li>If no token is found, use the login form to authenticate</li>
          <li>After successful login, test the /auth/me endpoint</li>
          <li>Check the browser console (F12) for detailed logs</li>
          <li>Check the Network tab to see actual API requests and responses</li>
        </ol>
        
        <Divider />
        
        <Title level={4}>Common Issues:</Title>
        <ul>
          <li><strong>CORS Error:</strong> Backend needs to allow http://localhost:3000</li>
          <li><strong>Connection Refused:</strong> Backend not running or wrong port</li>
          <li><strong>401 Unauthorized:</strong> Token expired or invalid</li>
          <li><strong>Invalid Credentials:</strong> Wrong username/password format</li>
        </ul>
      </Card>
    </div>
  );
}
