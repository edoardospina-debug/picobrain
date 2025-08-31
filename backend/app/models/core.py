from sqlalchemy import Column, String, Boolean, Date, DateTime, ForeignKey, CHAR, Integer, Text, BigInteger, Numeric
from sqlalchemy.dialects.postgresql import UUID, ENUM
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base
import uuid

class Person(Base):
    __tablename__ = "persons"
    
    # Primary fields
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    middle_name = Column(String(100))  # NEW: Additional name field
    
    # Contact fields
    email = Column(String(255), unique=True)
    phone_mobile_country_code = Column(String(6))  # Split phone field
    phone_mobile_number = Column(String(20))  # Split phone field
    phone_home_country_code = Column(String(6))  # Split phone field
    phone_home_number = Column(String(20))  # Split phone field
    
    # Personal details
    dob = Column(Date)
    gender = Column(ENUM('M', 'F', 'O', 'N', name='gender_type'))
    nationality = Column(String(2))  # NEW: Country code for nationality
    
    # Identification
    id_type = Column(String(20))  # NEW: Type of ID (passport, national ID, etc.)
    id_number = Column(Text)  # NEW: ID number/value
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())  # NEW
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())  # NEW
    
    # Relationships
    client = relationship("Client", back_populates="person", uselist=False)
    employee = relationship("Employee", back_populates="person", uselist=False)
    user = relationship("User", back_populates="person", uselist=False)

class Clinic(Base):
    __tablename__ = "clinics"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    code = Column(String(10), nullable=False, unique=True)
    name = Column(String(100), nullable=False)
    functional_currency = Column(CHAR(3))
    
    # Address fields
    address_line_1 = Column(String(255))
    address_line_2 = Column(String(255))
    city = Column(String(100))
    state_province = Column(String(100))
    postal_code = Column(String(20))
    country_code = Column(CHAR(2))
    
    # Contact fields
    phone_country_code = Column(String(6))  # Split phone field
    phone_number = Column(String(20))  # Split phone field
    email = Column(String(255))
    
    # Business fields
    tax_id = Column(String(50))
    is_active = Column(Boolean, default=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Migration helper field
    temp_id = Column(Integer)  # Temporary field for migration mapping
    
    # Relationships
    employees = relationship("Employee", back_populates="clinic")
    clients = relationship("Client", back_populates="preferred_clinic")

class Client(Base):
    __tablename__ = "clients"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    person_id = Column(UUID(as_uuid=True), ForeignKey("persons.id"), nullable=False)
    client_code = Column(String(20), unique=True)
    acquisition_date = Column(Date)
    preferred_clinic_id = Column(UUID(as_uuid=True), ForeignKey("clinics.id"))
    is_active = Column(Boolean, default=True)
    temp_id = Column(Integer)  # Temporary field for migration
    
    # Relationships
    person = relationship("Person", back_populates="client")
    preferred_clinic = relationship("Clinic", back_populates="clients")

class Employee(Base):
    __tablename__ = "employees"
    
    # Primary fields
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    person_id = Column(UUID(as_uuid=True), ForeignKey("persons.id"), nullable=False)
    employee_code = Column(String(20), unique=True)
    primary_clinic_id = Column(UUID(as_uuid=True), ForeignKey("clinics.id"), nullable=False)
    
    # Role and specialization
    role = Column(ENUM('doctor', 'nurse', 'receptionist', 'manager', 'finance', 'admin', name='employee_role'), nullable=False)
    specialization = Column(String(100))  # NEW: Medical specialization or department
    
    # Professional licensing
    license_number = Column(String(50))
    license_expiry = Column(Date)  # NEW: License expiration date
    
    # Employment dates
    hire_date = Column(Date, nullable=False)  # NEW: Employment start date
    termination_date = Column(Date)  # NEW: Employment end date
    
    # Compensation
    base_salary_minor = Column(BigInteger)  # NEW: Salary in minor units (cents/pence)
    salary_currency = Column(CHAR(3), ForeignKey("currencies.currency_code"))  # NEW: Currency code
    commission_rate = Column(Numeric)  # NEW: Commission percentage
    
    # Status flags
    is_active = Column(Boolean, default=True)
    can_perform_treatments = Column(Boolean, default=False)
    
    # Migration field
    temp_id = Column(Integer)  # Temporary field for migration
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())  # NEW
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())  # NEW
    
    # Relationships
    person = relationship("Person", back_populates="employee")
    clinic = relationship("Clinic", back_populates="employees")

class User(Base):
    __tablename__ = "users"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    person_id = Column(UUID(as_uuid=True), ForeignKey("persons.id"), nullable=False)
    username = Column(String(50), nullable=False, unique=True)
    password_hash = Column(String(255), nullable=False)
    role = Column(ENUM('admin', 'manager', 'staff', 'medical', 'finance', 'readonly', name='user_role'), nullable=False)
    is_active = Column(Boolean, default=True)
    
    # Relationships
    person = relationship("Person", back_populates="user")