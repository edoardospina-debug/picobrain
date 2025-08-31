'use client';

import React, { useState } from 'react';
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
  Typography
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
} from '@ant-design/icons';
import { doctorsApi } from '@/lib/api/endpoints/employees';
import { clinicsApi } from '@/lib/api/endpoints/clinics';
import { EmployeeCreateDTO } from '@/types';
import dayjs from 'dayjs';
import { useQuery } from '@tanstack/react-query';

const { Title, Text } = Typography;
const { Option } = Select;
const { TextArea } = Input;

export default function NewDoctorPage() {
  const router = useRouter();
  const [form] = Form.useForm();
  const [loading, setLoading] = useState(false);

  // Fetch clinics for dropdown
  const { data: clinicsData } = useQuery({
    queryKey: ['clinics-list'],
    queryFn: () => clinicsApi.list({ limit: 100 }),
  });

  const onFinish = async (values: any) => {
    try {
      setLoading(true);
      
      // Transform form values to match EmployeeCreateDTO
      const doctorData: EmployeeCreateDTO = {
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
        role: 'doctor', // Always doctor for this form
        specialization: values.specialization,
        license_number: values.license_number,
        license_expiry: values.license_expiry ? values.license_expiry.format('YYYY-MM-DD') : undefined,
        hire_date: values.hire_date.format('YYYY-MM-DD'),
        base_salary_minor: values.base_salary ? Math.round(values.base_salary * 100) : undefined, // Convert to cents
        salary_currency: values.salary_currency || 'USD',
        commission_rate: values.commission_rate,
        is_active: values.is_active !== false, // Default to true
        can_perform_treatments: true, // Doctors can perform treatments
      };

      const response = await doctorsApi.create(doctorData);
      message.success(`Doctor ${response.person.first_name} ${response.person.last_name} created successfully!`);
      router.push('/staff/doctors');
    } catch (error: any) {
      console.error('Error creating doctor:', error);
      if (error.response?.data?.detail) {
        message.error(error.response.data.detail.message || 'Failed to create doctor');
      } else {
        message.error('Failed to create doctor. Please check all required fields.');
      }
    } finally {
      setLoading(false);
    }
  };

  const handleCancel = () => {
    router.push('/staff/doctors');
  };

  // Generate employee code based on name
  const generateEmployeeCode = () => {
    const firstName = form.getFieldValue('first_name') || '';
    const lastName = form.getFieldValue('last_name') || '';
    if (firstName && lastName) {
      const code = `DR${firstName.charAt(0)}${lastName.charAt(0)}${Date.now().toString().slice(-4)}`.toUpperCase();
      form.setFieldValue('employee_code', code);
    }
  };

  return (
    <div style={{ padding: '24px' }}>
      <div style={{ marginBottom: '24px' }}>
        <Button 
          icon={<ArrowLeftOutlined />} 
          onClick={handleCancel}
          style={{ marginBottom: '16px' }}
        >
          Back to Doctors
        </Button>
        <Title level={2}>Add New Doctor</Title>
        <Text type="secondary">Create a new doctor profile with personal and professional information</Text>
      </div>

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
        }}
      >
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
                  placeholder="doctor@example.com" 
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
                  disabledDate={(current) => current && current > dayjs()}
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
                label="Country Code"
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
                label="Country Code"
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
                  {/* Add more countries as needed */}
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
          title={<><MedicineBoxOutlined /> Professional Information</>}
          style={{ marginBottom: '24px' }}
        >
          <Row gutter={16}>
            <Col span={8}>
              <Form.Item
                name="employee_code"
                label="Employee Code"
                tooltip="Auto-generated based on name, or enter custom code"
              >
                <Input 
                  placeholder="e.g., DR001" 
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
            <Col span={12}>
              <Form.Item
                name="specialization"
                label="Specialization"
                rules={[{ required: true, message: 'Please enter specialization' }]}
              >
                <Select placeholder="Select or enter specialization">
                  <Option value="General Practice">General Practice</Option>
                  <Option value="Cardiology">Cardiology</Option>
                  <Option value="Dermatology">Dermatology</Option>
                  <Option value="Endocrinology">Endocrinology</Option>
                  <Option value="Gastroenterology">Gastroenterology</Option>
                  <Option value="Neurology">Neurology</Option>
                  <Option value="Oncology">Oncology</Option>
                  <Option value="Ophthalmology">Ophthalmology</Option>
                  <Option value="Orthopedics">Orthopedics</Option>
                  <Option value="Pediatrics">Pediatrics</Option>
                  <Option value="Psychiatry">Psychiatry</Option>
                  <Option value="Radiology">Radiology</Option>
                  <Option value="Surgery">Surgery</Option>
                  <Option value="Urology">Urology</Option>
                </Select>
              </Form.Item>
            </Col>
            <Col span={12}>
              <Form.Item
                name="is_active"
                label="Status"
                valuePropName="checked"
              >
                <Switch checkedChildren="Active" unCheckedChildren="Inactive" defaultChecked />
              </Form.Item>
            </Col>
          </Row>

          <Divider orientation="left">License Information</Divider>

          <Row gutter={16}>
            <Col span={12}>
              <Form.Item
                name="license_number"
                label="Medical License Number"
                rules={[{ required: true, message: 'Please enter license number' }]}
              >
                <Input 
                  prefix={<SafetyCertificateOutlined />}
                  placeholder="Enter medical license number" 
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
            >
              Create Doctor Profile
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
