'use client';

import React, { useEffect, useState } from 'react';
import {
  Form,
  Input,
  Select,
  Switch,
  Button,
  Card,
  Row,
  Col,
  Space,
  Divider,
  message,
  Spin,
} from 'antd';
import {
  SaveOutlined,
  CloseOutlined,
  EnvironmentOutlined,
  PhoneOutlined,
  MailOutlined,
  BankOutlined,
} from '@ant-design/icons';
import { useForm, Controller } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { useRouter } from 'next/navigation';
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import { clinicsApi } from '@/lib/api/endpoints/clinics';
import {
  clinicFormSchema,
  ClinicFormData,
  CURRENCY_CODES,
  COUNTRY_CODES,
} from '@/lib/validators/clinic';
import { Clinic } from '@/types';

const { TextArea } = Input;

interface ClinicFormProps {
  mode: 'create' | 'edit';
  clinicId?: string;
  initialData?: Partial<Clinic>;
}

export default function ClinicForm({ mode, clinicId, initialData }: ClinicFormProps) {
  const router = useRouter();
  const queryClient = useQueryClient();
  const [loading, setLoading] = useState(false);

  // Form setup with react-hook-form
  const {
    control,
    handleSubmit,
    formState: { errors, isDirty },
    reset,
    watch,
    setError,
  } = useForm<ClinicFormData>({
    resolver: zodResolver(clinicFormSchema),
    defaultValues: {
      code: '',
      name: '',
      functional_currency: 'USD',
      is_active: true,
      ...initialData,
    },
  });

  // Fetch clinic data if in edit mode
  const { data: clinic, isLoading: isLoadingClinic } = useQuery({
    queryKey: ['clinic', clinicId],
    queryFn: () => clinicsApi.get(clinicId!),
    enabled: mode === 'edit' && !!clinicId && !initialData,
  });

  // Update form when clinic data is fetched
  useEffect(() => {
    if (clinic) {
      reset(clinic);
    }
  }, [clinic, reset]);

  // Create mutation
  const createMutation = useMutation({
    mutationFn: clinicsApi.create,
    onSuccess: (data) => {
      message.success('Clinic created successfully');
      queryClient.invalidateQueries({ queryKey: ['clinics'] });
      router.push('/clinics');
    },
    onError: (error: any) => {
      const errorMessage = error.response?.data?.detail || 'Failed to create clinic';
      message.error(errorMessage);
      
      // Handle field-specific errors
      if (error.response?.data?.errors) {
        Object.entries(error.response.data.errors).forEach(([field, messages]: [string, any]) => {
          setError(field as keyof ClinicFormData, {
            message: Array.isArray(messages) ? messages[0] : messages,
          });
        });
      }
    },
  });

  // Update mutation
  const updateMutation = useMutation({
    mutationFn: (data: ClinicFormData) => clinicsApi.update(clinicId!, data),
    onSuccess: () => {
      message.success('Clinic updated successfully');
      queryClient.invalidateQueries({ queryKey: ['clinics'] });
      queryClient.invalidateQueries({ queryKey: ['clinic', clinicId] });
      router.push('/clinics');
    },
    onError: (error: any) => {
      const errorMessage = error.response?.data?.detail || 'Failed to update clinic';
      message.error(errorMessage);
      
      // Handle field-specific errors
      if (error.response?.data?.errors) {
        Object.entries(error.response.data.errors).forEach(([field, messages]: [string, any]) => {
          setError(field as keyof ClinicFormData, {
            message: Array.isArray(messages) ? messages[0] : messages,
          });
        });
      }
    },
  });

  // Form submission
  const onSubmit = async (data: ClinicFormData) => {
    setLoading(true);
    try {
      if (mode === 'create') {
        await createMutation.mutateAsync(data);
      } else {
        await updateMutation.mutateAsync(data);
      }
    } finally {
      setLoading(false);
    }
  };

  // Cancel handler
  const handleCancel = () => {
    if (isDirty) {
      if (window.confirm('You have unsaved changes. Are you sure you want to leave?')) {
        router.push('/clinics');
      }
    } else {
      router.push('/clinics');
    }
  };

  // Watch for phone number to validate country code requirement
  const phoneNumber = watch('phone_number');

  if (mode === 'edit' && isLoadingClinic && !initialData) {
    return (
      <div style={{ display: 'flex', justifyContent: 'center', padding: 100 }}>
        <Spin size="large" />
      </div>
    );
  }

  return (
    <Form layout="vertical" onFinish={handleSubmit(onSubmit)}>
      <div style={{ padding: 24 }}>
        {/* Page Header */}
        <div style={{ marginBottom: 24 }}>
          <h2 style={{ margin: 0, fontSize: 24, fontWeight: 600 }}>
            {mode === 'create' ? 'Create New Clinic' : 'Edit Clinic'}
          </h2>
          <p style={{ margin: '8px 0 0', color: '#666' }}>
            {mode === 'create'
              ? 'Add a new clinic to your medical practice network'
              : 'Update clinic information and settings'}
          </p>
        </div>

        {/* Basic Information Card */}
        <Card
          title={
            <span>
              <BankOutlined /> Basic Information
            </span>
          }
          style={{ marginBottom: 24 }}
        >
          <Row gutter={16}>
            <Col xs={24} sm={12} md={8}>
              <Controller
                name="code"
                control={control}
                render={({ field }) => (
                  <Form.Item
                    label="Clinic Code"
                    required
                    validateStatus={errors.code ? 'error' : ''}
                    help={errors.code?.message}
                  >
                    <Input
                      {...field}
                      placeholder="e.g., MAIN-01"
                      disabled={mode === 'edit'}
                      style={{ textTransform: 'uppercase' }}
                    />
                  </Form.Item>
                )}
              />
            </Col>
            <Col xs={24} sm={12} md={8}>
              <Controller
                name="name"
                control={control}
                render={({ field }) => (
                  <Form.Item
                    label="Clinic Name"
                    required
                    validateStatus={errors.name ? 'error' : ''}
                    help={errors.name?.message}
                  >
                    <Input {...field} placeholder="e.g., Main Street Medical Center" />
                  </Form.Item>
                )}
              />
            </Col>
            <Col xs={24} sm={12} md={8}>
              <Controller
                name="functional_currency"
                control={control}
                render={({ field }) => (
                  <Form.Item
                    label="Functional Currency"
                    required
                    validateStatus={errors.functional_currency ? 'error' : ''}
                    help={errors.functional_currency?.message}
                  >
                    <Select {...field} placeholder="Select currency">
                      {CURRENCY_CODES.map((code) => (
                        <Select.Option key={code} value={code}>
                          {code}
                        </Select.Option>
                      ))}
                    </Select>
                  </Form.Item>
                )}
              />
            </Col>
          </Row>

          <Row gutter={16}>
            <Col xs={24} sm={12}>
              <Controller
                name="tax_id"
                control={control}
                render={({ field }) => (
                  <Form.Item
                    label="Tax ID"
                    validateStatus={errors.tax_id ? 'error' : ''}
                    help={errors.tax_id?.message}
                  >
                    <Input {...field} placeholder="e.g., 12-3456789" />
                  </Form.Item>
                )}
              />
            </Col>
            <Col xs={24} sm={12}>
              <Controller
                name="is_active"
                control={control}
                render={({ field }) => (
                  <Form.Item label="Status">
                    <Switch
                      {...field}
                      checked={field.value}
                      checkedChildren="Active"
                      unCheckedChildren="Inactive"
                    />
                  </Form.Item>
                )}
              />
            </Col>
          </Row>
        </Card>

        {/* Address Information Card */}
        <Card
          title={
            <span>
              <EnvironmentOutlined /> Address Information
            </span>
          }
          style={{ marginBottom: 24 }}
        >
          <Row gutter={16}>
            <Col xs={24}>
              <Controller
                name="address_line_1"
                control={control}
                render={({ field }) => (
                  <Form.Item
                    label="Address Line 1"
                    validateStatus={errors.address_line_1 ? 'error' : ''}
                    help={errors.address_line_1?.message}
                  >
                    <Input {...field} placeholder="Street address" />
                  </Form.Item>
                )}
              />
            </Col>
          </Row>

          <Row gutter={16}>
            <Col xs={24}>
              <Controller
                name="address_line_2"
                control={control}
                render={({ field }) => (
                  <Form.Item
                    label="Address Line 2"
                    validateStatus={errors.address_line_2 ? 'error' : ''}
                    help={errors.address_line_2?.message}
                  >
                    <Input {...field} placeholder="Apartment, suite, unit, building, floor, etc." />
                  </Form.Item>
                )}
              />
            </Col>
          </Row>

          <Row gutter={16}>
            <Col xs={24} sm={12} md={6}>
              <Controller
                name="city"
                control={control}
                render={({ field }) => (
                  <Form.Item
                    label="City"
                    validateStatus={errors.city ? 'error' : ''}
                    help={errors.city?.message}
                  >
                    <Input {...field} placeholder="City" />
                  </Form.Item>
                )}
              />
            </Col>
            <Col xs={24} sm={12} md={6}>
              <Controller
                name="state_province"
                control={control}
                render={({ field }) => (
                  <Form.Item
                    label="State/Province"
                    validateStatus={errors.state_province ? 'error' : ''}
                    help={errors.state_province?.message}
                  >
                    <Input {...field} placeholder="State or Province" />
                  </Form.Item>
                )}
              />
            </Col>
            <Col xs={24} sm={12} md={6}>
              <Controller
                name="postal_code"
                control={control}
                render={({ field }) => (
                  <Form.Item
                    label="Postal Code"
                    validateStatus={errors.postal_code ? 'error' : ''}
                    help={errors.postal_code?.message}
                  >
                    <Input {...field} placeholder="Postal/ZIP code" />
                  </Form.Item>
                )}
              />
            </Col>
            <Col xs={24} sm={12} md={6}>
              <Controller
                name="country_code"
                control={control}
                render={({ field }) => (
                  <Form.Item
                    label="Country"
                    validateStatus={errors.country_code ? 'error' : ''}
                    help={errors.country_code?.message}
                  >
                    <Select {...field} placeholder="Select country" allowClear>
                      {COUNTRY_CODES.map((code) => (
                        <Select.Option key={code} value={code}>
                          {code}
                        </Select.Option>
                      ))}
                    </Select>
                  </Form.Item>
                )}
              />
            </Col>
          </Row>
        </Card>

        {/* Contact Information Card */}
        <Card
          title={
            <span>
              <PhoneOutlined /> Contact Information
            </span>
          }
          style={{ marginBottom: 24 }}
        >
          <Row gutter={16}>
            <Col xs={24} sm={8}>
              <Controller
                name="phone_country_code"
                control={control}
                render={({ field }) => (
                  <Form.Item
                    label="Phone Country Code"
                    validateStatus={errors.phone_country_code ? 'error' : ''}
                    help={errors.phone_country_code?.message}
                    required={!!phoneNumber}
                  >
                    <Input {...field} placeholder="e.g., 1" prefix="+" />
                  </Form.Item>
                )}
              />
            </Col>
            <Col xs={24} sm={16}>
              <Controller
                name="phone_number"
                control={control}
                render={({ field }) => (
                  <Form.Item
                    label="Phone Number"
                    validateStatus={errors.phone_number ? 'error' : ''}
                    help={errors.phone_number?.message}
                  >
                    <Input {...field} placeholder="e.g., 555-123-4567" />
                  </Form.Item>
                )}
              />
            </Col>
          </Row>

          <Row gutter={16}>
            <Col xs={24}>
              <Controller
                name="email"
                control={control}
                render={({ field }) => (
                  <Form.Item
                    label="Email Address"
                    validateStatus={errors.email ? 'error' : ''}
                    help={errors.email?.message}
                  >
                    <Input
                      {...field}
                      type="email"
                      prefix={<MailOutlined />}
                      placeholder="clinic@example.com"
                    />
                  </Form.Item>
                )}
              />
            </Col>
          </Row>
        </Card>

        {/* Form Actions */}
        <Card>
          <Space>
            <Button
              type="primary"
              htmlType="submit"
              loading={loading || createMutation.isPending || updateMutation.isPending}
              icon={<SaveOutlined />}
              size="large"
            >
              {mode === 'create' ? 'Create Clinic' : 'Save Changes'}
            </Button>
            <Button
              size="large"
              onClick={handleCancel}
              disabled={loading || createMutation.isPending || updateMutation.isPending}
              icon={<CloseOutlined />}
            >
              Cancel
            </Button>
          </Space>
        </Card>
      </div>
    </Form>
  );
}
