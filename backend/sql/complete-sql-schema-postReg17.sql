-- =============================================
-- CLINIC MANAGEMENT SYSTEM - POSTGRESQL 17+ SCHEMA WITH UUID
-- Version: 3.1-PG-UUID
-- Database: PostgreSQL 17+
-- =============================================

-- Enable required extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";
CREATE EXTENSION IF NOT EXISTS "btree_gin"; -- Better UUID indexing

-- =============================================
-- SECTION 0: CUSTOM TYPES (PostgreSQL ENUMs)
-- =============================================

-- Drop types if they exist (for clean deployment)
DROP TYPE IF EXISTS gender_type CASCADE;
DROP TYPE IF EXISTS address_type CASCADE;
DROP TYPE IF EXISTS employee_role CASCADE;
DROP TYPE IF EXISTS user_role CASCADE;
DROP TYPE IF EXISTS appointment_status CASCADE;
DROP TYPE IF EXISTS practitioner_role CASCADE;
DROP TYPE IF EXISTS package_status CASCADE;
DROP TYPE IF EXISTS invoice_status CASCADE;
DROP TYPE IF EXISTS payment_method CASCADE;
DROP TYPE IF EXISTS payment_status CASCADE;
DROP TYPE IF EXISTS transaction_type CASCADE;
DROP TYPE IF EXISTS ledger_transaction_type CASCADE;
DROP TYPE IF EXISTS rate_type CASCADE;
DROP TYPE IF EXISTS photo_type CASCADE;
DROP TYPE IF EXISTS item_type CASCADE;
DROP TYPE IF EXISTS refund_method CASCADE;
DROP TYPE IF EXISTS refund_status CASCADE;
DROP TYPE IF EXISTS po_status CASCADE;
DROP TYPE IF EXISTS receipt_type CASCADE;
DROP TYPE IF EXISTS consumption_type CASCADE;
DROP TYPE IF EXISTS provider_type CASCADE;
DROP TYPE IF EXISTS provider_transaction_type CASCADE;
DROP TYPE IF EXISTS reconciliation_status CASCADE;
DROP TYPE IF EXISTS batch_status CASCADE;
DROP TYPE IF EXISTS match_type CASCADE;
DROP TYPE IF EXISTS resolution_status CASCADE;
DROP TYPE IF EXISTS correction_status CASCADE;
DROP TYPE IF EXISTS import_type CASCADE;
DROP TYPE IF EXISTS import_status CASCADE;
DROP TYPE IF EXISTS audit_operation CASCADE;
DROP TYPE IF EXISTS consent_type CASCADE;

-- Create all ENUM types
CREATE TYPE gender_type AS ENUM ('M', 'F', 'O', 'N');
CREATE TYPE address_type AS ENUM ('home', 'work', 'billing', 'other');
CREATE TYPE employee_role AS ENUM ('doctor', 'nurse', 'receptionist', 'manager', 'finance', 'admin');
CREATE TYPE user_role AS ENUM ('admin', 'manager', 'staff', 'medical', 'finance', 'readonly');
CREATE TYPE appointment_status AS ENUM ('scheduled', 'confirmed', 'arrived', 'in_progress', 'completed', 'cancelled', 'no_show');
CREATE TYPE practitioner_role AS ENUM ('primary', 'assistant', 'support', 'observer');
CREATE TYPE package_status AS ENUM ('active', 'completed', 'expired', 'transferred', 'refunded');
CREATE TYPE invoice_status AS ENUM ('draft', 'issued', 'paid', 'partial', 'overdue', 'cancelled');
CREATE TYPE payment_method AS ENUM ('cash', 'card', 'bank_transfer', 'check', 'alipay', 'wechat', 'other');
CREATE TYPE payment_status AS ENUM ('pending', 'completed', 'failed', 'refunded');
CREATE TYPE transaction_type AS ENUM ('payment', 'refund', 'chargeback', 'adjustment');
CREATE TYPE ledger_transaction_type AS ENUM ('invoice', 'payment', 'credit', 'debit', 'refund', 'adjustment');
CREATE TYPE rate_type AS ENUM ('AVERAGE', 'CLOSING');
CREATE TYPE photo_type AS ENUM ('before', 'after', 'progress');
CREATE TYPE item_type AS ENUM ('treatment', 'package', 'product', 'other');
CREATE TYPE refund_method AS ENUM ('cash', 'card', 'bank_transfer', 'check');
CREATE TYPE refund_status AS ENUM ('pending', 'completed', 'failed');
CREATE TYPE po_status AS ENUM ('draft', 'sent', 'partial', 'received', 'cancelled');
CREATE TYPE receipt_type AS ENUM ('purchase', 'transfer', 'adjustment', 'return');
CREATE TYPE consumption_type AS ENUM ('treatment', 'sale', 'waste', 'adjustment', 'transfer');
CREATE TYPE provider_type AS ENUM ('card_processor', 'bank_transfer', 'digital_wallet');
CREATE TYPE provider_transaction_type AS ENUM ('payment', 'refund', 'chargeback', 'adjustment');
CREATE TYPE reconciliation_status AS ENUM ('unmatched', 'matched', 'disputed', 'ignored');
CREATE TYPE batch_status AS ENUM ('in_progress', 'completed', 'reviewed');
CREATE TYPE match_type AS ENUM ('exact', 'fuzzy', 'manual', 'unmatched');
CREATE TYPE resolution_status AS ENUM ('pending', 'accepted', 'corrected', 'disputed');
CREATE TYPE correction_status AS ENUM ('pending', 'approved', 'rejected', 'applied');
CREATE TYPE import_type AS ENUM ('manual_csv', 'api_sync', 'manual_entry');
CREATE TYPE import_status AS ENUM ('pending', 'processing', 'completed', 'failed');
CREATE TYPE audit_operation AS ENUM ('INSERT', 'UPDATE', 'DELETE');
CREATE TYPE consent_type AS ENUM ('marketing', 'photos', 'data_processing', 'third_party');

-- =============================================
-- SECTION 1: FOUNDATIONAL TABLES
-- =============================================

-- Currency management
CREATE TABLE currencies (
    currency_code CHAR(3) PRIMARY KEY,
    currency_name VARCHAR(100) NOT NULL,
    minor_units INT NOT NULL,
    decimal_places INT NOT NULL,
    symbol VARCHAR(10),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

-- Monthly consolidation rates
CREATE TABLE consolidation_rates (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    from_currency CHAR(3) NOT NULL REFERENCES currencies(currency_code),
    to_currency CHAR(3) NOT NULL DEFAULT 'EUR' REFERENCES currencies(currency_code),
    rate DECIMAL(12,6) NOT NULL,
    rate_month DATE NOT NULL,
    rate_type rate_type NOT NULL,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT uk_rate UNIQUE (from_currency, to_currency, rate_month, rate_type)
);

-- Clinic locations
CREATE TABLE clinics (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    code VARCHAR(10) NOT NULL UNIQUE,
    name VARCHAR(100) NOT NULL,
    functional_currency CHAR(3) NOT NULL REFERENCES currencies(currency_code),
    address_line_1 VARCHAR(255),
    address_line_2 VARCHAR(255),
    city VARCHAR(100),
    state_province VARCHAR(100),
    postal_code VARCHAR(20),
    country_code CHAR(2),
    phone VARCHAR(50),
    email VARCHAR(255),
    tax_id VARCHAR(50),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

-- =============================================
-- SECTION 2: PERSON MANAGEMENT (CORE ENTITY)
-- =============================================

-- Central person entity
CREATE TABLE persons (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    middle_name VARCHAR(100),
    email VARCHAR(255) UNIQUE,
    phone_mobile VARCHAR(50),
    phone_home VARCHAR(50),
    dob DATE,
    gender gender_type,
    nationality VARCHAR(2),
    id_type VARCHAR(20),
    id_number TEXT, -- Will be encrypted at application layer
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

-- Person addresses
CREATE TABLE person_addresses (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    person_id UUID NOT NULL REFERENCES persons(id) ON DELETE CASCADE,
    address_type address_type DEFAULT 'home',
    address_line_1 VARCHAR(255) NOT NULL,
    address_line_2 VARCHAR(255),
    city VARCHAR(100),
    state_province VARCHAR(100),
    postal_code VARCHAR(20),
    country_code CHAR(2),
    is_primary BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

-- =============================================
-- SECTION 3: ROLES (CLIENTS, EMPLOYEES, USERS)
-- =============================================

-- Clients
CREATE TABLE clients (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    person_id UUID NOT NULL UNIQUE REFERENCES persons(id),
    client_code VARCHAR(20) UNIQUE,
    acquisition_date DATE DEFAULT CURRENT_DATE,
    acquisition_source VARCHAR(50),
    acquisition_detail VARCHAR(255),
    preferred_clinic_id UUID REFERENCES clinics(id),
    preferred_language CHAR(2) DEFAULT 'EN',
    consent_marketing BOOLEAN DEFAULT FALSE,
    consent_photos BOOLEAN DEFAULT FALSE,
    notes TEXT,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

-- Employees
CREATE TABLE employees (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    person_id UUID NOT NULL UNIQUE REFERENCES persons(id),
    employee_code VARCHAR(20) UNIQUE,
    primary_clinic_id UUID NOT NULL REFERENCES clinics(id),
    role employee_role NOT NULL,
    specialization VARCHAR(100),
    license_number VARCHAR(50),
    license_expiry DATE,
    hire_date DATE NOT NULL,
    termination_date DATE,
    base_salary_minor BIGINT,
    salary_currency CHAR(3) REFERENCES currencies(currency_code),
    commission_rate DECIMAL(5,2),
    is_active BOOLEAN DEFAULT TRUE,
    can_perform_treatments BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

-- Employee clinic assignments
CREATE TABLE employee_clinics (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    employee_id UUID NOT NULL REFERENCES employees(id),
    clinic_id UUID NOT NULL REFERENCES clinics(id),
    start_date DATE NOT NULL,
    end_date DATE,
    work_schedule JSONB,
    is_primary BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT uk_employee_clinic UNIQUE (employee_id, clinic_id)
);

-- System users
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    person_id UUID NOT NULL UNIQUE REFERENCES persons(id),
    username VARCHAR(50) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    role user_role NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    must_change_password BOOLEAN DEFAULT FALSE,
    last_login TIMESTAMPTZ,
    failed_login_attempts INT DEFAULT 0,
    locked_until TIMESTAMPTZ,
    mfa_secret TEXT, -- Will be encrypted at application layer
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

-- =============================================
-- SECTION 4: TREATMENTS AND PACKAGES
-- =============================================

-- Global treatment catalog
CREATE TABLE treatments (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    code VARCHAR(20) NOT NULL UNIQUE,
    name VARCHAR(100) NOT NULL,
    category VARCHAR(50),
    subcategory VARCHAR(50),
    duration_minutes INT DEFAULT 60,
    description TEXT,
    contraindications TEXT,
    is_package_eligible BOOLEAN DEFAULT TRUE,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

-- Clinic-specific treatment pricing
CREATE TABLE clinic_treatments (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    clinic_id UUID NOT NULL REFERENCES clinics(id),
    treatment_id UUID NOT NULL REFERENCES treatments(id),
    price_minor BIGINT NOT NULL,
    currency_code CHAR(3) NOT NULL REFERENCES currencies(currency_code),
    min_price_minor BIGINT,
    max_discount_percent DECIMAL(5,2) DEFAULT 0,
    is_available BOOLEAN DEFAULT TRUE,
    requires_consultation BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT uk_clinic_treatment UNIQUE (clinic_id, treatment_id)
);

-- Package templates
CREATE TABLE packages (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    code VARCHAR(20) NOT NULL UNIQUE,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    total_sessions INT NOT NULL,
    validity_months INT DEFAULT 12,
    is_transferable BOOLEAN DEFAULT FALSE,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

-- Package treatments mapping
CREATE TABLE package_treatments (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    package_id UUID NOT NULL REFERENCES packages(id),
    treatment_id UUID NOT NULL REFERENCES treatments(id),
    sessions_included INT NOT NULL,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT uk_package_treatment UNIQUE (package_id, treatment_id)
);

-- Clinic-specific package pricing
CREATE TABLE clinic_packages (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    clinic_id UUID NOT NULL REFERENCES clinics(id),
    package_id UUID NOT NULL REFERENCES packages(id),
    price_minor BIGINT NOT NULL,
    currency_code CHAR(3) NOT NULL REFERENCES currencies(currency_code),
    is_available BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT uk_clinic_package UNIQUE (clinic_id, package_id)
);

-- =============================================
-- SECTION 5: APPOINTMENTS AND SCHEDULING
-- =============================================

-- Appointments
CREATE TABLE appointments (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    client_id UUID NOT NULL REFERENCES clients(id),
    clinic_id UUID NOT NULL REFERENCES clinics(id),
    primary_practitioner_id UUID NOT NULL REFERENCES employees(id),
    appointment_date DATE NOT NULL,
    start_time TIME NOT NULL,
    end_time TIME NOT NULL,
    status appointment_status DEFAULT 'scheduled',
    cancellation_reason VARCHAR(255),
    notes TEXT,
    created_by UUID REFERENCES users(id),
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

-- Multiple practitioners per appointment
CREATE TABLE appointment_practitioners (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    appointment_id UUID NOT NULL REFERENCES appointments(id) ON DELETE CASCADE,
    employee_id UUID NOT NULL REFERENCES employees(id),
    role practitioner_role DEFAULT 'primary',
    joined_at TIME,
    left_at TIME,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT uk_appointment_practitioner UNIQUE (appointment_id, employee_id)
);

-- Treatments performed
CREATE TABLE appointment_treatments (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    appointment_id UUID NOT NULL REFERENCES appointments(id) ON DELETE CASCADE,
    clinic_treatment_id UUID REFERENCES clinic_treatments(id),
    custom_treatment_name VARCHAR(100),
    performed_by_id UUID NOT NULL REFERENCES employees(id),
    quantity INT DEFAULT 1,
    actual_price_minor BIGINT NOT NULL,
    currency_code CHAR(3) NOT NULL REFERENCES currencies(currency_code),
    discount_percent DECIMAL(5,2) DEFAULT 0,
    discount_reason VARCHAR(100),
    package_deduction_id UUID,
    doctor_commission_rate DECIMAL(5,2),
    notes TEXT,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

-- =============================================
-- SECTION 6: CLIENT PACKAGES
-- =============================================

-- Client packages
CREATE TABLE client_packages (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    client_id UUID NOT NULL REFERENCES clients(id),
    clinic_package_id UUID NOT NULL REFERENCES clinic_packages(id),
    purchase_date DATE NOT NULL,
    expiry_date DATE NOT NULL,
    total_sessions INT NOT NULL,
    sessions_used INT DEFAULT 0,
    sessions_remaining INT GENERATED ALWAYS AS (total_sessions - sessions_used) STORED,
    purchase_price_minor BIGINT NOT NULL,
    currency_code CHAR(3) NOT NULL REFERENCES currencies(currency_code),
    status package_status DEFAULT 'active',
    invoice_id UUID,
    notes TEXT,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

-- Package usage
CREATE TABLE package_usage (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    client_package_id UUID NOT NULL REFERENCES client_packages(id),
    appointment_treatment_id UUID REFERENCES appointment_treatments(id),
    usage_date DATE NOT NULL,
    sessions_deducted INT NOT NULL DEFAULT 1,
    performed_by_id UUID REFERENCES employees(id),
    notes TEXT,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

-- Package transfers
CREATE TABLE package_transfers (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    source_package_id UUID NOT NULL REFERENCES client_packages(id),
    from_client_id UUID NOT NULL REFERENCES clients(id),
    to_client_id UUID NOT NULL REFERENCES clients(id),
    new_package_id UUID REFERENCES client_packages(id),
    sessions_transferred INT NOT NULL,
    transfer_date DATE NOT NULL,
    transfer_reason VARCHAR(255),
    authorized_by UUID NOT NULL REFERENCES employees(id),
    authorization_notes TEXT,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

-- =============================================
-- SECTION 7: MEDICAL COMPLIANCE
-- =============================================

-- Medical questionnaires
CREATE TABLE medical_questionnaires (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    client_id UUID NOT NULL REFERENCES clients(id),
    questionnaire_version VARCHAR(20) NOT NULL,
    completed_date TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    expiry_date TIMESTAMPTZ GENERATED ALWAYS AS 
        (completed_date + INTERVAL '18 months') STORED,
    pdf_url TEXT,
    responses JSONB, -- Encrypt sensitive parts at application layer
    medical_conditions TEXT,
    allergies TEXT,
    current_medications TEXT,
    is_current BOOLEAN DEFAULT TRUE,
    reviewed_by_id UUID REFERENCES employees(id),
    reviewed_date TIMESTAMPTZ,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

-- Client photos
CREATE TABLE client_photos (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    client_id UUID NOT NULL REFERENCES clients(id),
    appointment_id UUID REFERENCES appointments(id),
    photo_type photo_type NOT NULL,
    photo_url TEXT NOT NULL,
    thumbnail_url TEXT,
    body_area VARCHAR(50),
    angle VARCHAR(20),
    treatment_series_id VARCHAR(50),
    taken_date DATE NOT NULL,
    taken_by_id UUID REFERENCES employees(id),
    notes TEXT,
    is_visible BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

-- =============================================
-- SECTION 8: FINANCIAL SYSTEM
-- =============================================

-- Invoices
CREATE TABLE invoices (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    invoice_number VARCHAR(50) NOT NULL UNIQUE,
    client_id UUID NOT NULL REFERENCES clients(id),
    clinic_id UUID NOT NULL REFERENCES clinics(id),
    invoice_date DATE NOT NULL,
    due_date DATE,
    subtotal_minor BIGINT NOT NULL,
    tax_amount_minor BIGINT DEFAULT 0,
    discount_amount_minor BIGINT DEFAULT 0,
    total_minor BIGINT NOT NULL,
    currency_code CHAR(3) NOT NULL REFERENCES currencies(currency_code),
    status invoice_status DEFAULT 'draft',
    payment_terms VARCHAR(50),
    notes TEXT,
    created_by UUID REFERENCES users(id),
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

-- Invoice lines
CREATE TABLE invoice_lines (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    invoice_id UUID NOT NULL REFERENCES invoices(id) ON DELETE CASCADE,
    line_number INT NOT NULL,
    item_type item_type NOT NULL,
    item_id UUID,
    description VARCHAR(255) NOT NULL,
    quantity DECIMAL(10,3) DEFAULT 1,
    unit_price_minor BIGINT NOT NULL,
    subtotal_minor BIGINT NOT NULL,
    tax_rate DECIMAL(5,2) DEFAULT 0,
    tax_amount_minor BIGINT DEFAULT 0,
    total_minor BIGINT NOT NULL,
    appointment_id UUID REFERENCES appointments(id),
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT uk_invoice_line UNIQUE (invoice_id, line_number)
);

-- Payments
CREATE TABLE payments (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    payment_number VARCHAR(50) UNIQUE,
    client_id UUID NOT NULL REFERENCES clients(id),
    clinic_id UUID NOT NULL REFERENCES clinics(id),
    invoice_id UUID REFERENCES invoices(id),
    payment_date TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    payment_method payment_method NOT NULL,
    payment_provider VARCHAR(50),
    amount_minor_units BIGINT NOT NULL,
    currency_code CHAR(3) NOT NULL REFERENCES currencies(currency_code),
    reference_number VARCHAR(100),
    card_last_four VARCHAR(4),
    status payment_status DEFAULT 'completed',
    notes TEXT,
    recorded_by UUID REFERENCES users(id),
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

-- Payment allocations
CREATE TABLE payment_allocations (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    payment_id UUID NOT NULL REFERENCES payments(id) ON DELETE CASCADE,
    invoice_id UUID NOT NULL REFERENCES invoices(id),
    allocated_amount_minor BIGINT NOT NULL,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT uk_payment_invoice UNIQUE (payment_id, invoice_id)
);

-- Customer ledger
CREATE TABLE customer_ledger (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    client_id UUID NOT NULL REFERENCES clients(id),
    transaction_date TIMESTAMPTZ NOT NULL,
    transaction_type ledger_transaction_type NOT NULL,
    reference_type VARCHAR(50),
    reference_id UUID,
    description VARCHAR(255),
    debit_minor BIGINT DEFAULT 0,
    credit_minor BIGINT DEFAULT 0,
    balance_minor BIGINT NOT NULL,
    currency_code CHAR(3) NOT NULL REFERENCES currencies(currency_code),
    created_by UUID REFERENCES users(id),
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

-- Refunds
CREATE TABLE refunds (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    payment_id UUID NOT NULL REFERENCES payments(id),
    refund_date DATE NOT NULL,
    amount_minor BIGINT NOT NULL,
    currency_code CHAR(3) NOT NULL REFERENCES currencies(currency_code),
    refund_method refund_method NOT NULL,
    reason VARCHAR(255),
    reference_number VARCHAR(100),
    status refund_status DEFAULT 'completed',
    approved_by UUID REFERENCES employees(id),
    processed_by UUID REFERENCES users(id),
    notes TEXT,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

-- =============================================
-- SECTION 9: INVENTORY MANAGEMENT
-- =============================================

-- Products
CREATE TABLE products (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    sku VARCHAR(50) NOT NULL UNIQUE,
    name VARCHAR(100) NOT NULL,
    category VARCHAR(50),
    brand VARCHAR(50),
    description TEXT,
    unit_of_measure VARCHAR(20) DEFAULT 'unit',
    is_consumable BOOLEAN DEFAULT TRUE,
    is_for_sale BOOLEAN DEFAULT TRUE,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

-- Suppliers
CREATE TABLE suppliers (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    code VARCHAR(20) NOT NULL UNIQUE,
    name VARCHAR(100) NOT NULL,
    contact_name VARCHAR(100),
    email VARCHAR(255),
    phone VARCHAR(50),
    website VARCHAR(255),
    address TEXT,
    payment_terms VARCHAR(50),
    currency_code CHAR(3) REFERENCES currencies(currency_code),
    tax_id VARCHAR(50),
    is_active BOOLEAN DEFAULT TRUE,
    notes TEXT,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

-- Clinic products
CREATE TABLE clinic_products (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    clinic_id UUID NOT NULL REFERENCES clinics(id),
    product_id UUID NOT NULL REFERENCES products(id),
    supplier_id UUID REFERENCES suppliers(id),
    reorder_point DECIMAL(10,3),
    reorder_quantity DECIMAL(10,3),
    max_stock DECIMAL(10,3),
    retail_price_minor BIGINT,
    currency_code CHAR(3) NOT NULL REFERENCES currencies(currency_code),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT uk_clinic_product UNIQUE (clinic_id, product_id)
);

-- Inventory summary
CREATE TABLE inventory_summary (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    clinic_product_id UUID NOT NULL UNIQUE REFERENCES clinic_products(id),
    quantity_on_hand DECIMAL(10,3) NOT NULL DEFAULT 0,
    average_cost_minor BIGINT NOT NULL DEFAULT 0,
    currency_code CHAR(3) NOT NULL REFERENCES currencies(currency_code),
    last_counted_date DATE,
    last_counted_quantity DECIMAL(10,3),
    last_received_date DATE,
    last_consumed_date DATE,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

-- Purchase orders
CREATE TABLE purchase_orders (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    po_number VARCHAR(50) NOT NULL UNIQUE,
    clinic_id UUID NOT NULL REFERENCES clinics(id),
    supplier_id UUID NOT NULL REFERENCES suppliers(id),
    order_date DATE NOT NULL,
    expected_delivery DATE,
    status po_status DEFAULT 'draft',
    subtotal_minor BIGINT NOT NULL,
    tax_amount_minor BIGINT DEFAULT 0,
    shipping_minor BIGINT DEFAULT 0,
    total_minor BIGINT NOT NULL,
    currency_code CHAR(3) NOT NULL REFERENCES currencies(currency_code),
    notes TEXT,
    created_by UUID REFERENCES users(id),
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

-- Purchase order lines
CREATE TABLE purchase_order_lines (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    purchase_order_id UUID NOT NULL REFERENCES purchase_orders(id) ON DELETE CASCADE,
    clinic_product_id UUID NOT NULL REFERENCES clinic_products(id),
    quantity_ordered DECIMAL(10,3) NOT NULL,
    unit_cost_minor BIGINT NOT NULL,
    total_cost_minor BIGINT NOT NULL,
    quantity_received DECIMAL(10,3) DEFAULT 0,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

-- Inventory receipts
CREATE TABLE inventory_receipts (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    receipt_number VARCHAR(50) NOT NULL UNIQUE,
    purchase_order_id UUID REFERENCES purchase_orders(id),
    clinic_id UUID NOT NULL REFERENCES clinics(id),
    receipt_date DATE NOT NULL,
    receipt_type receipt_type DEFAULT 'purchase',
    supplier_invoice_number VARCHAR(50),
    total_items INT DEFAULT 0,
    total_value_minor BIGINT DEFAULT 0,
    currency_code CHAR(3) NOT NULL REFERENCES currencies(currency_code),
    notes TEXT,
    received_by UUID REFERENCES users(id),
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

-- Receipt lines
CREATE TABLE inventory_receipt_lines (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    receipt_id UUID NOT NULL REFERENCES inventory_receipts(id) ON DELETE CASCADE,
    clinic_product_id UUID NOT NULL REFERENCES clinic_products(id),
    quantity_received DECIMAL(10,3) NOT NULL,
    unit_cost_minor BIGINT NOT NULL,
    total_cost_minor BIGINT NOT NULL,
    expiry_date DATE,
    lot_number VARCHAR(50),
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

-- Inventory consumption
CREATE TABLE inventory_consumption (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    clinic_product_id UUID NOT NULL REFERENCES clinic_products(id),
    consumption_date DATE NOT NULL,
    consumption_type consumption_type NOT NULL,
    reference_type VARCHAR(50),
    reference_id UUID,
    quantity_consumed DECIMAL(10,3) NOT NULL,
    unit_cost_minor BIGINT NOT NULL,
    total_cost_minor BIGINT NOT NULL,
    notes TEXT,
    created_by UUID REFERENCES users(id),
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

-- Treatment products
CREATE TABLE treatment_products (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    clinic_treatment_id UUID NOT NULL REFERENCES clinic_treatments(id),
    clinic_product_id UUID NOT NULL REFERENCES clinic_products(id),
    standard_quantity DECIMAL(10,3) NOT NULL,
    is_optional BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT uk_treatment_product UNIQUE (clinic_treatment_id, clinic_product_id)
);

-- =============================================
-- SECTION 10: PAYMENT RECONCILIATION
-- =============================================

-- Payment providers
CREATE TABLE payment_providers (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    provider_name VARCHAR(100) NOT NULL UNIQUE,
    provider_type provider_type NOT NULL,
    api_enabled BOOLEAN DEFAULT FALSE,
    api_endpoint TEXT,
    field_mapping JSONB,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

-- Clinic payment providers
CREATE TABLE clinic_payment_providers (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    clinic_id UUID NOT NULL REFERENCES clinics(id),
    payment_provider_id UUID NOT NULL REFERENCES payment_providers(id),
    payment_types JSONB,
    merchant_account_id VARCHAR(100),
    credentials_encrypted TEXT, -- Encrypt at application layer
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT uk_clinic_provider UNIQUE (clinic_id, payment_provider_id)
);

-- Provider transactions
CREATE TABLE provider_transactions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    clinic_payment_provider_id UUID NOT NULL REFERENCES clinic_payment_providers(id),
    provider_transaction_id VARCHAR(255) NOT NULL,
    transaction_date TIMESTAMPTZ NOT NULL,
    settlement_date TIMESTAMPTZ,
    amount_minor BIGINT NOT NULL,
    currency_code CHAR(3) NOT NULL,
    transaction_type provider_transaction_type NOT NULL,
    status VARCHAR(50),
    card_last_four VARCHAR(4),
    customer_identifier TEXT,
    raw_data JSONB NOT NULL,
    import_batch_id UUID,
    reconciliation_status reconciliation_status DEFAULT 'unmatched',
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT uk_provider_transaction UNIQUE (clinic_payment_provider_id, provider_transaction_id)
);

-- Reconciliation batches
CREATE TABLE reconciliation_batches (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    clinic_id UUID NOT NULL REFERENCES clinics(id),
    batch_date DATE NOT NULL,
    reconciled_by UUID REFERENCES employees(id),
    period_start TIMESTAMPTZ NOT NULL,
    period_end TIMESTAMPTZ NOT NULL,
    status batch_status DEFAULT 'in_progress',
    system_payment_count INT DEFAULT 0,
    provider_payment_count INT DEFAULT 0,
    matched_count INT DEFAULT 0,
    unmatched_system_count INT DEFAULT 0,
    unmatched_provider_count INT DEFAULT 0,
    discrepancy_count INT DEFAULT 0,
    notes TEXT,
    completed_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

-- Payment reconciliations
CREATE TABLE payment_reconciliations (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    reconciliation_batch_id UUID NOT NULL REFERENCES reconciliation_batches(id),
    payment_id UUID NOT NULL REFERENCES payments(id),
    provider_transaction_id UUID REFERENCES provider_transactions(id),
    match_type match_type NOT NULL,
    match_confidence DECIMAL(3,2),
    match_criteria JSONB,
    discrepancy_type VARCHAR(50),
    discrepancy_details JSONB,
    resolution_status resolution_status DEFAULT 'pending',
    resolved_by UUID REFERENCES employees(id),
    resolved_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT uk_payment_provider UNIQUE (payment_id, provider_transaction_id)
);

-- Payment corrections
CREATE TABLE payment_corrections (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    payment_id UUID NOT NULL REFERENCES payments(id),
    reconciliation_id UUID REFERENCES payment_reconciliations(id),
    field_name VARCHAR(50) NOT NULL,
    old_value TEXT,
    new_value TEXT,
    correction_reason VARCHAR(255),
    corrected_by UUID NOT NULL REFERENCES employees(id),
    corrected_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    requires_approval BOOLEAN DEFAULT FALSE,
    approval_threshold_minor BIGINT DEFAULT 10000,
    approved_by UUID REFERENCES employees(id),
    approved_at TIMESTAMPTZ,
    approval_notes TEXT,
    correction_status correction_status DEFAULT 'pending'
);

-- Provider data imports
CREATE TABLE provider_data_imports (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    clinic_payment_provider_id UUID NOT NULL REFERENCES clinic_payment_providers(id),
    import_type import_type NOT NULL,
    file_name VARCHAR(255),
    imported_by UUID REFERENCES users(id),
    period_start DATE,
    period_end DATE,
    records_imported INT DEFAULT 0,
    records_failed INT DEFAULT 0,
    error_log JSONB,
    status import_status DEFAULT 'pending',
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMPTZ
);

-- =============================================
-- SECTION 11: AUDIT AND COMPLIANCE
-- =============================================

-- Audit log
CREATE TABLE audit_log (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    table_name VARCHAR(50) NOT NULL,
    record_id UUID NOT NULL,
    operation audit_operation NOT NULL,
    field_changes JSONB,
    user_id UUID REFERENCES users(id),
    ip_address INET,
    user_agent VARCHAR(255),
    timestamp TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

-- GDPR consents
CREATE TABLE gdpr_consents (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    person_id UUID NOT NULL REFERENCES persons(id),
    consent_type consent_type NOT NULL,
    consent_given BOOLEAN DEFAULT FALSE,
    consent_date TIMESTAMPTZ,
    consent_method VARCHAR(50),
    consent_version VARCHAR(20),
    ip_address INET,
    withdrawn_date TIMESTAMPTZ,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT uk_person_consent UNIQUE (person_id, consent_type)
);

-- =============================================
-- TRIGGERS FOR updated_at
-- =============================================

CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Create triggers for all tables with updated_at
CREATE TRIGGER update_clinics_updated_at BEFORE UPDATE ON clinics
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_persons_updated_at BEFORE UPDATE ON persons
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_clients_updated_at BEFORE UPDATE ON clients
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_employees_updated_at BEFORE UPDATE ON employees
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_users_updated_at BEFORE UPDATE ON users
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_treatments_updated_at BEFORE UPDATE ON treatments
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_clinic_treatments_updated_at BEFORE UPDATE ON clinic_treatments
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_packages_updated_at BEFORE UPDATE ON packages
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_clinic_packages_updated_at BEFORE UPDATE ON clinic_packages
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_appointments_updated_at BEFORE UPDATE ON appointments
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_client_packages_updated_at BEFORE UPDATE ON client_packages
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_invoices_updated_at BEFORE UPDATE ON invoices
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_payments_updated_at BEFORE UPDATE ON payments
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_products_updated_at BEFORE UPDATE ON products
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_suppliers_updated_at BEFORE UPDATE ON suppliers
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_clinic_products_updated_at BEFORE UPDATE ON clinic_products
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_inventory_summary_updated_at BEFORE UPDATE ON inventory_summary
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_purchase_orders_updated_at BEFORE UPDATE ON purchase_orders
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- =============================================
-- OPTIMIZED INDEXES FOR UUID PERFORMANCE
-- =============================================

-- Person indexes
CREATE INDEX idx_persons_email ON persons(email);
CREATE INDEX idx_persons_phone ON persons(phone_mobile);
CREATE INDEX idx_person_addresses_person ON person_addresses(person_id);

-- Client indexes
CREATE INDEX idx_clients_person ON clients(person_id);
CREATE INDEX idx_clients_acquisition ON clients(acquisition_date, acquisition_source);
CREATE INDEX idx_clients_clinic ON clients(preferred_clinic_id);

-- Employee indexes
CREATE INDEX idx_employees_person ON employees(person_id);
CREATE INDEX idx_employees_clinic ON employees(primary_clinic_id);
CREATE INDEX idx_employees_active ON employees(is_active, can_perform_treatments);
CREATE INDEX idx_employee_clinics_employee ON employee_clinics(employee_id);
CREATE INDEX idx_employee_clinics_clinic ON employee_clinics(clinic_id);

-- User indexes
CREATE INDEX idx_users_person ON users(person_id);
CREATE INDEX idx_users_username ON users(username);
CREATE INDEX idx_users_active ON users(is_active);

-- Treatment indexes
CREATE INDEX idx_treatments_category ON treatments(category, subcategory);
CREATE INDEX idx_treatments_active ON treatments(is_active);
CREATE INDEX idx_clinic_treatments_clinic ON clinic_treatments(clinic_id);
CREATE INDEX idx_clinic_treatments_treatment ON clinic_treatments(treatment_id);
CREATE INDEX idx_clinic_treatments_available ON clinic_treatments(clinic_id, is_available);

-- Package indexes
CREATE INDEX idx_packages_active ON packages(is_active);
CREATE INDEX idx_clinic_packages_clinic ON clinic_packages(clinic_id);
CREATE INDEX idx_clinic_packages_package ON clinic_packages(package_id);
CREATE INDEX idx_clinic_packages_available ON clinic_packages(clinic_id, is_available);

-- Appointment indexes
CREATE INDEX idx_appointments_date_clinic ON appointments(appointment_date, clinic_id);
CREATE INDEX idx_appointments_client ON appointments(client_id);
CREATE INDEX idx_appointments_practitioner ON appointments(primary_practitioner_id);
CREATE INDEX idx_appointments_status ON appointments(status, appointment_date);
CREATE INDEX idx_appointment_practitioners_appointment ON appointment_practitioners(appointment_id);
CREATE INDEX idx_appointment_practitioners_employee ON appointment_practitioners(employee_id);
CREATE INDEX idx_appointment_treatments_appointment ON appointment_treatments(appointment_id);
CREATE INDEX idx_appointment_treatments_performer ON appointment_treatments(performed_by_id);

-- Client package indexes
CREATE INDEX idx_client_packages_client ON client_packages(client_id, status);
CREATE INDEX idx_client_packages_expiry ON client_packages(expiry_date, status);
CREATE INDEX idx_package_usage_package ON package_usage(client_package_id);
CREATE INDEX idx_package_usage_date ON package_usage(usage_date);
CREATE INDEX idx_package_transfers_from ON package_transfers(from_client_id);
CREATE INDEX idx_package_transfers_to ON package_transfers(to_client_id);
CREATE INDEX idx_package_transfers_date ON package_transfers(transfer_date);

-- Medical indexes
CREATE INDEX idx_medical_quest_client ON medical_questionnaires(client_id, is_current);
CREATE INDEX idx_medical_quest_expiry ON medical_questionnaires(expiry_date) WHERE is_current = TRUE;
CREATE INDEX idx_client_photos_client ON client_photos(client_id);
CREATE INDEX idx_client_photos_series ON client_photos(treatment_series_id);
CREATE INDEX idx_client_photos_date ON client_photos(taken_date);

-- Financial indexes
CREATE INDEX idx_invoices_client ON invoices(client_id);
CREATE INDEX idx_invoices_clinic ON invoices(clinic_id);
CREATE INDEX idx_invoices_date ON invoices(invoice_date);
CREATE INDEX idx_invoices_status ON invoices(status);
CREATE INDEX idx_invoice_lines_invoice ON invoice_lines(invoice_id);
CREATE INDEX idx_payments_client ON payments(client_id);
CREATE INDEX idx_payments_clinic ON payments(clinic_id);
CREATE INDEX idx_payments_date ON payments(payment_date);
CREATE INDEX idx_payments_invoice ON payments(invoice_id);
CREATE INDEX idx_payments_reference ON payments(reference_number);
CREATE INDEX idx_customer_ledger_client ON customer_ledger(client_id, transaction_date);
CREATE INDEX idx_refunds_payment ON refunds(payment_id);

-- Inventory indexes
CREATE INDEX idx_clinic_products_clinic ON clinic_products(clinic_id);
CREATE INDEX idx_clinic_products_product ON clinic_products(product_id);
CREATE INDEX idx_purchase_orders_clinic ON purchase_orders(clinic_id);
CREATE INDEX idx_purchase_orders_supplier ON purchase_orders(supplier_id);
CREATE INDEX idx_inventory_consumption_product ON inventory_consumption(clinic_product_id);
CREATE INDEX idx_inventory_consumption_date ON inventory_consumption(consumption_date);

-- Reconciliation indexes
CREATE INDEX idx_provider_trans_reconciliation ON provider_transactions(reconciliation_status, transaction_date);
CREATE INDEX idx_provider_trans_matching ON provider_transactions(transaction_date, amount_minor, currency_code);
CREATE INDEX idx_payment_recons_batch ON payment_reconciliations(reconciliation_batch_id);
CREATE INDEX idx_payment_recons_payment ON payment_reconciliations(payment_id);
CREATE INDEX idx_payment_corrections_payment ON payment_corrections(payment_id);
CREATE INDEX idx_provider_imports_clinic_provider ON provider_data_imports(clinic_payment_provider_id);

-- Audit indexes
CREATE INDEX idx_audit_table ON audit_log(table_name, record_id);
CREATE INDEX idx_audit_timestamp ON audit_log(timestamp);
CREATE INDEX idx_audit_user ON audit_log(user_id);
CREATE INDEX idx_gdpr_person ON gdpr_consents(person_id);

-- =============================================
-- HELPER FUNCTIONS
-- =============================================

-- Convert to minor units
CREATE OR REPLACE FUNCTION to_minor_units(
    amount DECIMAL(10,2),
    p_currency_code CHAR(3)
) RETURNS BIGINT AS $$
DECLARE
    v_minor_units INT;
BEGIN
    SELECT minor_units INTO v_minor_units 
    FROM currencies 
    WHERE currency_code = p_currency_code;
    
    IF v_minor_units IS NULL THEN
        RAISE EXCEPTION 'Currency % not found', p_currency_code;
    END IF;
    
    RETURN CAST(amount * v_minor_units AS BIGINT);
END;
$$ LANGUAGE plpgsql IMMUTABLE;

-- Convert from minor units
CREATE OR REPLACE FUNCTION from_minor_units(
    p_minor_units BIGINT,
    p_currency_code CHAR(3)
) RETURNS DECIMAL(10,2) AS $$
DECLARE
    v_minor_units INT;
BEGIN
    SELECT minor_units INTO v_minor_units 
    FROM currencies 
    WHERE currency_code = p_currency_code;
    
    IF v_minor_units IS NULL THEN
        RAISE EXCEPTION 'Currency % not found', p_currency_code;
    END IF;
    
    RETURN p_minor_units::DECIMAL / v_minor_units;
END;
$$ LANGUAGE plpgsql IMMUTABLE;

-- Format currency
CREATE OR REPLACE FUNCTION format_currency(
    p_amount_minor BIGINT,
    p_currency_code CHAR(3)
) RETURNS VARCHAR(50) AS $$
DECLARE
    v_symbol VARCHAR(10);
    v_decimal_places INT;
    v_amount DECIMAL(10,2);
BEGIN
    SELECT symbol, decimal_places 
    INTO v_symbol, v_decimal_places 
    FROM currencies 
    WHERE currency_code = p_currency_code;
    
    IF v_symbol IS NULL THEN
        RAISE EXCEPTION 'Currency % not found', p_currency_code;
    END IF;
    
    v_amount := from_minor_units(p_amount_minor, p_currency_code);
    
    RETURN CONCAT(v_symbol, TO_CHAR(v_amount, 'FM999,999,990.00'));
END;
$$ LANGUAGE plpgsql IMMUTABLE;

-- Calculate average cost for inventory
CREATE OR REPLACE FUNCTION calculate_average_cost(
    current_qty DECIMAL(10,3),
    current_cost_minor BIGINT,
    new_qty DECIMAL(10,3),
    new_cost_minor BIGINT
) RETURNS BIGINT AS $$
BEGIN
    IF (current_qty + new_qty) = 0 THEN
        RETURN 0;
    END IF;
    
    RETURN CAST(
        ((current_qty * current_cost_minor) + (new_qty * new_cost_minor)) / 
        (current_qty + new_qty) 
        AS BIGINT
    );
END;
$$ LANGUAGE plpgsql IMMUTABLE;

-- =============================================
-- INITIAL DATA
-- =============================================

-- Insert currencies
INSERT INTO currencies (currency_code, currency_name, minor_units, decimal_places, symbol) VALUES
('EUR', 'Euro', 100, 2, '€'),
('GBP', 'British Pound', 100, 2, '£'),
('USD', 'US Dollar', 100, 2, '$'),
('CAD', 'Canadian Dollar', 100, 2, 'C$')
ON CONFLICT (currency_code) DO NOTHING;

-- Insert sample clinics (using predetermined UUIDs for consistency)
INSERT INTO clinics (id, code, name, functional_currency, city, country_code) VALUES
('a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11', 'LON', 'London Clinic', 'GBP', 'London', 'GB'),
('a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a12', 'MIL', 'Milan Clinic', 'EUR', 'Milan', 'IT'),
('a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a13', 'NYC', 'New York Clinic', 'USD', 'New York', 'US'),
('a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a14', 'LAX', 'Los Angeles Clinic', 'USD', 'Los Angeles', 'US'),
('a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a15', 'VAN', 'Vancouver Clinic', 'CAD', 'Vancouver', 'CA')
ON CONFLICT (code) DO NOTHING;

-- Insert payment providers (using generated UUIDs)
INSERT INTO payment_providers (provider_name, provider_type) VALUES
('Stripe', 'card_processor'),
('Chase merchant', 'card_processor'),
('Barclaycard merchant', 'card_processor'),
('Unicredit merchant', 'card_processor'),
('SquareUp', 'card_processor'),
('SumUp', 'card_processor'),
('Pockyt', 'digital_wallet'),
('AlphaPay', 'digital_wallet'),
('Globepay', 'digital_wallet'),
('Atoa', 'digital_wallet'),
('Chase Bank bank account', 'bank_transfer'),
('Lloyds Bank bank account', 'bank_transfer'),
('Unicredit bank account', 'bank_transfer'),
('TD Bank bank account', 'bank_transfer')
ON CONFLICT (provider_name) DO NOTHING;

-- =============================================
-- END OF SCHEMA
-- =============================================