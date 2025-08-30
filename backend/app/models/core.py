from sqlalchemy import Column, String, Boolean, Date, ForeignKey, CHAR
from sqlalchemy.dialects.postgresql import UUID, ENUM
from sqlalchemy.orm import relationship
from app.database import Base
import uuid

class Person(Base):
    __tablename__ = "persons"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    email = Column(String(255), unique=True)
    phone_mobile = Column(String(50))
    dob = Column(Date)
    gender = Column(ENUM('M', 'F', 'O', 'N', name='gender_type'))
    
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
    city = Column(String(100))
    country_code = Column(CHAR(2))
    is_active = Column(Boolean, default=True)
    
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
    
    # Relationships
    person = relationship("Person", back_populates="client")
    preferred_clinic = relationship("Clinic", back_populates="clients")

class Employee(Base):
    __tablename__ = "employees"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    person_id = Column(UUID(as_uuid=True), ForeignKey("persons.id"), nullable=False)
    employee_code = Column(String(20), unique=True)
    primary_clinic_id = Column(UUID(as_uuid=True), ForeignKey("clinics.id"), nullable=False)
    role = Column(ENUM('doctor', 'nurse', 'receptionist', 'manager', 'finance', 'admin', name='employee_role'), nullable=False)
    license_number = Column(String(50))
    is_active = Column(Boolean, default=True)
    can_perform_treatments = Column(Boolean, default=False)
    
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