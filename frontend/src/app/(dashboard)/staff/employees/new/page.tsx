'use client';

import React, { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { 
  Form, 
  Input, 
  Button, 
  Card, 
  Row, 
  Col, 
  DatePicker, 
  Select, 
  Switch, 
  InputNumber,
  message,
  Space,
  Divider,
  Typography,
  Alert,
  Tooltip
} from 'antd';
import {
  UserOutlined,
  PhoneOutlined,
  MailOutlined,
  IdcardOutlined,
  MedicineBoxOutlined,
  SafetyCertificateOutlined,
  DollarOutlined,
  BankOutlined,
  CalendarOutlined,
  SaveOutlined,
  ArrowLeftOutlined,
  TeamOutlined,
  HeartOutlined,
  CustomerServiceOutlined,
  SettingOutlined,
  InfoCircleOutlined,
} from '@ant-design/icons';
import { employeesApi } from '@/lib/api/endpoints/employees';
import { clinicsApi } from '@/lib/api/endpoints/clinics';
import { EmployeeCreateDTO, EmployeeRole } from '@/types';
import dayjs from 'dayjs';
import { useQuery } from '@tanstack/react-query';

const { Title, Text } = Typography;
const { Option } = Select;
const { TextArea } = Input;

// Role configuration
const roleConfig = {
  doctor: { 
    icon: <MedicineBoxOutlined />, 
    label: 'Doctor',
    requiresLicense: true,
    canPerformTreatments: true,
    specializations: [
      'General Practice', 'Cardiology', 'Dermatology', 'Endocrinology',
      'Gastroenterology', 'Neurology', 'Oncology', 'Ophthalmology',
      'Orthopedics', 'Pediatrics', 'Psychiatry', 'Radiology',
      'Surgery', 'Urology'
    ]
  },
  nurse: { 
    icon: <HeartOutlined />, 
    label: 'Nurse',
    requiresLicense: true,
    canPerformTreatments: true,
    specializations: [
      'General Nursing', 'Emergency Care', 'Pediatric Nursing',
      'Surgical Nursing', 'Critical Care', 'Mental Health',
      'Geriatric Care', 'Oncology Nursing'
    ]
  },
  receptionist: { 
    icon: <CustomerServiceOutlined />, 
    label: 'Receptionist',
    requiresLicense: false,
    canPerformTreatments: false,
    specializations: []
  },
  manager: { 
    icon: <TeamOutlined />, 
    label: 'Manager',
    requiresLicense: false,
    canPerformTreatments: false,
    specializations: []
  },
  finance: { 
    icon: <DollarOutlined />, 
    label: 'Finance',
    requiresLicense: false,
    canPerformTreatments: false,
    specializations: []
  },
  admin: { 
    icon: <SettingOutlined />, 
    label: 'Admin',
    requiresLicense: false,
    canPerformTreatments: false,
    specializations: []
  },
};

export default function NewEmployeePage() {
  const router = useRouter();
  const [form] = Form.useForm();
  const [loading, setLoading] = useState(false);
  const [selectedRole, setSelectedRole] = useState<EmployeeRole | null>(null);

  // Watch for role changes
  const role = Form.useWatch('role', form);

  useEffect(() => {
    if (role && role !== selectedRole) {
      setSelectedRole(role);
      
      // Update can_perform_treatments based on role
      const roleInfo = roleConfig[role as EmployeeRole];
      if (roleInfo) {
        form.setFieldsValue({
          can_perform_treatments: roleInfo.canPerformTreatments
        });
        
        // Clear specialization if role doesn't have specializations
        if (roleInfo.specializations.length === 0) {
          form.setFieldsValue({ specialization: undefined });
        }
        
        // Clear license fields if not required
        if (!roleInfo.requiresLicense) {
          form.setFieldsValue({ 
            license_number: undefined,
            license_expiry: undefined 
          });
        }
      }
    }
  }, [role, selectedRole, form]);

  // Fetch clinics for dropdown
  const { data: clinicsData } = useQuery({
    queryKey: ['clinics-list'],
    queryFn: () => clinicsApi.list({ limit: 100 }),
  });

  const onFinish = async (values: any) => {
    try {
      setLoading(true);
      
      // Transform form values to match EmployeeCreateDTO
      const employeeData: EmployeeCreateDTO = {
        // Person fields
        first_name: values.first_name,
        last_name: values.last_name,
        middle_name: values.middle_name,
        email: values.email,
        phone_mobile_country_code: values.phone_mobile_country_code,
        phone_mobile_number: values.phone_mobile_number,
        phone_home_country_code: values.phone_home_country_code,
        phone_home_number: values.phone_home_number,
        dob: values.dob ? values.dob.format('YYYY-MM-DD') : undefined,
        gender: values.gender,
        nationality: values.nationality,
        id_type: values.id_type,
        id_number: values.id_number,
        
        // Employee fields
        employee_code: values.employee_code,
        primary_clinic_id: values.primary_clinic_id,
        role: values.role,
        specialization: values.specialization,
        license_number: values.license_number,
        license_expiry: values.license_expiry ? values.license_expiry.format('YYYY-MM-DD') : undefined,
        hire_date: values.hire_date.format('YYYY-MM-DD'),
        termination_date: values.termination_date ? values.termination_date.format('YYYY-MM-DD') : undefined,
        base_salary_minor: values.base_salary ? Math.round(values.base_salary * 100) : undefined,
        salary_currency: values.salary_currency || 'USD',
        commission_rate: values.commission_rate,
        is_active: values.is_active !== false,
        can_perform_treatments: values.can_perform_treatments || false,
      };

      const response = await employeesApi.create(employeeData);
      message.success(`Employee ${response.person.first_name} ${response.person.last_name} created successfully!`);
      router.push('/staff/employees');
    } catch (error: any) {
      console.error('Error creating employee:', error);
      if (error.response?.data?.detail) {
        const detail = error.response.data.detail;
        if (typeof detail === 'object' && detail.message) {
          message.error(detail.message);
        } else {
          message.error('Failed to create employee');
        }
      } else {
        message.error('Failed to create employee. Please check all required fields.');
      }
    } finally {
      setLoading(false);
    }
  };

  const handleCancel = () => {
    router.push('/staff/employees');
  };

  // Generate employee code based on role and name
  const generateEmployeeCode = () => {
    const firstName = form.getFieldValue('first_name') || '';
    const lastName = form.getFieldValue('last_name') || '';
    const role = form.getFieldValue('role') || 'EMP';
    
    if (firstName && lastName) {
      const rolePrefix = {
        doctor: 'DR',
        nurse: 'NR',
        receptionist: 'RC',
        manager: 'MG',
        finance: 'FN',
        admin: 'AD',
      }[role] || 'EMP';
      
      const code = `${rolePrefix}${firstName.charAt(0)}${lastName.charAt(0)}${Date.now().toString().slice(-4)}`.toUpperCase();
      form.setFieldValue('employee_code', code);
    }
  };

  const currentRoleConfig = selectedRole ? roleConfig[selectedRole] : null;

  return (
    <div style={{ padding: '24px' }}>
      <div style={{ marginBottom: '24px' }}>
        <Button 
          icon={<ArrowLeftOutlined />} 
          onClick={handleCancel}
          style={{ marginBottom: '16px' }}
        >
          Back to Employees
        </Button>
        <Title level={2}>Add New Employee</Title>
        <Text type="secondary">Create a new employee profile with personal and professional information</Text>
      </div>

      {/* Role Selection Alert */}
      <Alert
        message="Select Employee Role"
        description="Please select the employee role first. The form will adapt based on the selected role."
        type="info"
        showIcon
        icon={<InfoCircleOutlined />}
        style={{ marginBottom: '24px' }}
      />

      <Form
        form={form}
        layout="vertical"
        onFinish={onFinish}
        initialValues={{
          is_active: true,
          salary_currency: 'USD',
          gender: 'M',
          phone_mobile_country_code: '+1',
          phone_home_country_code: '+1',
          can_perform_treatments: false,
        }}
      >
        {/* Role Selection - First Priority */}
        <Card 
          title={<><TeamOutlined /> Employee Role Selection</>}
          style={{ marginBottom: '24px', border: '2px solid #1890ff' }}
        >
          <Form.Item
            name="role"
            label="Employee Role"
            rules={[{ required: true, message: 'Please select employee role' }]}
          >
            <Select 
              placeholder="Select employee role"
              size="large"
              onChange={(value) => {
                setSelectedRole(value);
                generateEmployeeCode();
              }}
            >
              {Object.entries(roleConfig).map(([key, config]) => (
                <Option key={key} value={key}>
                  <Space>
                    {config.icon}
                    {config.label}
                  </Space>
                </Option>
              ))}
            </Select>
          </Form.Item>
          
          {selectedRole && (
            <Alert
              message={`${roleConfig[selectedRole].label} Selected`}
              description={
                <ul style={{ marginBottom: 0, paddingLeft: 20 }}>
                  <li>License Required: {roleConfig[selectedRole].requiresLicense ? 'Yes' : 'No'}</li>
                  <li>Can Perform Treatments: {roleConfig[selectedRole].canPerformTreatments ? 'Yes' : 'No'}</li>
                  {roleConfig[selectedRole].specializations.length > 0 && (
                    <li>Specializations Available: {roleConfig[selectedRole].specializations.length}</li>
                  )}
                </ul>
              }
              type="success"
              showIcon
            />
          )}
        </Card>

        {/* Personal Information Section */}
        <Card 
          title={<><UserOutlined /> Personal Information</>}
          style={{ marginBottom: '24px' }}
        >
          <Row gutter={16}>
            <Col span={8}>
              <Form.Item
                name="first_name"
                label="First Name"
                rules={[{ required: true, message: 'Please enter first name' }]}
              >
                <Input 
                  placeholder="Enter first name" 
                  onChange={generateEmployeeCode}
                />
              </Form.Item>
            </Col>
            <Col span={8}>
              <Form.Item
                name="middle_name"
                label="Middle Name"
              >
                <Input placeholder="Enter middle name (optional)" />
              </Form.Item>
            </Col>
            <Col span={8}>
              <Form.Item
                name="last_name"
                label="Last Name"
                rules={[{ required: true, message: 'Please enter last name' }]}
              >
                <Input 
                  placeholder="Enter last name"
                  onChange={generateEmployeeCode}
                />
              </Form.Item>
            </Col>
          </Row>

          <Row gutter={16}>
            <Col span={8}>
              <Form.Item
                name="email"
                label="Email"
                rules={[
                  { type: 'email', message: 'Please enter a valid email' }
                ]}
              >
                <Input 
                  prefix={<MailOutlined />}
                  placeholder="employee@example.com" 
                />
              </Form.Item>
            </Col>
            <Col span={8}>
              <Form.Item
                name="dob"
                label="Date of Birth"
              >
                <DatePicker 
                  style={{ width: '100%' }}
                  placeholder="Select date of birth"
                  disabledDate={(current) => current && current > dayjs().subtract(18, 'years')}
                />
              </Form.Item>
            </Col>
            <Col span={8}>
              <Form.Item
                name="gender"
                label="Gender"
              >
                <Select placeholder="Select gender">
                  <Option value="M">Male</Option>
                  <Option value="F">Female</Option>
                  <Option value="O">Other</Option>
                  <Option value="N">Prefer not to say</Option>
                </Select>
              </Form.Item>
            </Col>
          </Row>

          <Divider orientation="left">Contact Information</Divider>

          <Row gutter={16}>
            <Col span={3}>
              <Form.Item
                name="phone_mobile_country_code"
                label="Code"
              >
                <Input placeholder="+1" />
              </Form.Item>
            </Col>
            <Col span={9}>
              <Form.Item
                name="phone_mobile_number"
                label="Mobile Phone"
              >
                <Input 
                  prefix={<PhoneOutlined />}
                  placeholder="Enter mobile number" 
                />
              </Form.Item>
            </Col>
            <Col span={3}>
              <Form.Item
                name="phone_home_country_code"
                label="Code"
              >
                <Input placeholder="+1" />
              </Form.Item>
            </Col>
            <Col span={9}>
              <Form.Item
                name="phone_home_number"
                label="Home Phone"
              >
                <Input 
                  prefix={<PhoneOutlined />}
                  placeholder="Enter home number (optional)" 
                />
              </Form.Item>
            </Col>
          </Row>

          <Divider orientation="left">Identification</Divider>

          <Row gutter={16}>
            <Col span={8}>
              <Form.Item
                name="nationality"
                label="Nationality"
              >
                <Select placeholder="Select nationality">
                  <Option value="US">United States</Option>
                  <Option value="CA">Canada</Option>
                  <Option value="GB">United Kingdom</Option>
                  <Option value="AU">Australia</Option>
                  <Option value="IN">India</Option>
                </Select>
              </Form.Item>
            </Col>
            <Col span={8}>
              <Form.Item
                name="id_type"
                label="ID Type"
              >
                <Select placeholder="Select ID type">
                  <Option value="passport">Passport</Option>
                  <Option value="national_id">National ID</Option>
                  <Option value="drivers_license">Driver's License</Option>
                  <Option value="ssn">Social Security Number</Option>
                </Select>
              </Form.Item>
            </Col>
            <Col span={8}>
              <Form.Item
                name="id_number"
                label="ID Number"
              >
                <Input 
                  prefix={<IdcardOutlined />}
                  placeholder="Enter ID number" 
                />
              </Form.Item>
            </Col>
          </Row>
        </Card>

        {/* Professional Information Section */}
        <Card 
          title={
            <>
              {currentRoleConfig?.icon || <TeamOutlined />} Professional Information
            </>
          }
          style={{ marginBottom: '24px' }}
        >
          <Row gutter={16}>
            <Col span={8}>
              <Form.Item
                name="employee_code"
                label="Employee Code"
                tooltip="Auto-generated based on role and name"
              >
                <Input 
                  placeholder="e.g., EMP001" 
                  addonAfter={
                    <Button size="small" onClick={generateEmployeeCode}>
                      Generate
                    </Button>
                  }
                />
              </Form.Item>
            </Col>
            <Col span={8}>
              <Form.Item
                name="primary_clinic_id"
                label="Primary Clinic"
                rules={[{ required: true, message: 'Please select a clinic' }]}
              >
                <Select 
                  placeholder="Select primary clinic"
                  showSearch
                  optionFilterProp="children"
                >
                  {clinicsData?.items.map((clinic) => (
                    <Option key={clinic.id} value={clinic.id}>
                      {clinic.name} ({clinic.code})
                    </Option>
                  ))}
                </Select>
              </Form.Item>
            </Col>
            <Col span={8}>
              <Form.Item
                name="hire_date"
                label="Hire Date"
                rules={[{ required: true, message: 'Please select hire date' }]}
              >
                <DatePicker 
                  style={{ width: '100%' }}
                  placeholder="Select hire date"
                  disabledDate={(current) => current && current > dayjs()}
                />
              </Form.Item>
            </Col>
          </Row>

          <Row gutter={16}>
            {currentRoleConfig && currentRoleConfig.specializations.length > 0 && (
              <Col span={12}>
                <Form.Item
                  name="specialization"
                  label="Specialization"
                  rules={[{ 
                    required: currentRoleConfig.requiresLicense, 
                    message: 'Please select specialization' 
                  }]}
                >
                  <Select placeholder="Select specialization">
                    {currentRoleConfig.specializations.map((spec) => (
                      <Option key={spec} value={spec}>{spec}</Option>
                    ))}
                  </Select>
                </Form.Item>
              </Col>
            )}
            <Col span={6}>
              <Form.Item
                name="termination_date"
                label="Termination Date"
              >
                <DatePicker 
                  style={{ width: '100%' }}
                  placeholder="If applicable"
                />
              </Form.Item>
            </Col>
            <Col span={6}>
              <Form.Item
                name="is_active"
                label="Status"
                valuePropName="checked"
              >
                <Switch checkedChildren="Active" unCheckedChildren="Inactive" defaultChecked />
              </Form.Item>
            </Col>
            {currentRoleConfig && (
              <Col span={6}>
                <Form.Item
                  name="can_perform_treatments"
                  label={
                    <Tooltip title="Whether this employee can perform medical treatments">
                      Can Treat <InfoCircleOutlined />
                    </Tooltip>
                  }
                  valuePropName="checked"
                >
                  <Switch 
                    checkedChildren="Yes" 
                    unCheckedChildren="No"
                    disabled={!currentRoleConfig.canPerformTreatments}
                  />
                </Form.Item>
              </Col>
            )}
          </Row>

          {/* License Information - Only for medical roles */}
          {currentRoleConfig?.requiresLicense && (
            <>
              <Divider orientation="left">License Information</Divider>
              <Row gutter={16}>
                <Col span={12}>
                  <Form.Item
                    name="license_number"
                    label="License Number"
                    rules={[{ required: true, message: 'Please enter license number' }]}
                  >
                    <Input 
                      prefix={<SafetyCertificateOutlined />}
                      placeholder="Enter professional license number" 
                    />
                  </Form.Item>
                </Col>
                <Col span={12}>
                  <Form.Item
                    name="license_expiry"
                    label="License Expiry Date"
                  >
                    <DatePicker 
                      style={{ width: '100%' }}
                      placeholder="Select expiry date"
                      disabledDate={(current) => current && current < dayjs()}
                    />
                  </Form.Item>
                </Col>
              </Row>
            </>
          )}
        </Card>

        {/* Compensation Section */}
        <Card 
          title={<><DollarOutlined /> Compensation Information</>}
          style={{ marginBottom: '24px' }}
        >
          <Row gutter={16}>
            <Col span={8}>
              <Form.Item
                name="base_salary"
                label="Base Salary"
              >
                <InputNumber
                  style={{ width: '100%' }}
                  formatter={value => `$ ${value}`.replace(/\B(?=(\d{3})+(?!\d))/g, ',')}
                  parser={value => value!.replace(/\$\s?|(,*)/g, '')}
                  placeholder="Enter base salary"
                  min={0}
                />
              </Form.Item>
            </Col>
            <Col span={8}>
              <Form.Item
                name="salary_currency"
                label="Currency"
              >
                <Select placeholder="Select currency">
                  <Option value="USD">USD - US Dollar</Option>
                  <Option value="EUR">EUR - Euro</Option>
                  <Option value="GBP">GBP - British Pound</Option>
                  <Option value="CAD">CAD - Canadian Dollar</Option>
                  <Option value="AUD">AUD - Australian Dollar</Option>
                </Select>
              </Form.Item>
            </Col>
            <Col span={8}>
              <Form.Item
                name="commission_rate"
                label="Commission Rate (%)"
              >
                <InputNumber
                  style={{ width: '100%' }}
                  min={0}
                  max={100}
                  formatter={value => `${value}%`}
                  parser={value => value!.replace('%', '')}
                  placeholder="Enter commission rate"
                />
              </Form.Item>
            </Col>
          </Row>
        </Card>

        {/* Form Actions */}
        <Card>
          <Space>
            <Button
              type="primary"
              htmlType="submit"
              loading={loading}
              icon={<SaveOutlined />}
              size="large"
              disabled={!selectedRole}
            >
              Create Employee Profile
            </Button>
            <Button
              onClick={handleCancel}
              size="large"
            >
              Cancel
            </Button>
          </Space>
        </Card>
      </Form>
    </div>
  );
}
