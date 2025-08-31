from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import date, datetime
from uuid import UUID
from enum import Enum
from decimal import Decimal

class GenderType(str, Enum):
    M = "M"
    F = "F"
    O = "O"
    N = "N"

class EmployeeRole(str, Enum):
    doctor = "doctor"
    nurse = "nurse"
    receptionist = "receptionist"
    manager = "manager"
    finance = "finance"
    admin = "admin"

class UserRole(str, Enum):
    admin = "admin"
    manager = "manager"
    staff = "staff"
    medical = "medical"
    finance = "finance"
    readonly = "readonly"

# Person Schemas
class PersonBase(BaseModel):
    first_name: str = Field(..., max_length=100)
    last_name: str = Field(..., max_length=100)
    middle_name: Optional[str] = Field(None, max_length=100)
    email: Optional[EmailStr] = None
    # Split phone fields
    phone_mobile_country_code: Optional[str] = Field(None, max_length=6)
    phone_mobile_number: Optional[str] = Field(None, max_length=20)
    phone_home_country_code: Optional[str] = Field(None, max_length=6)
    phone_home_number: Optional[str] = Field(None, max_length=20)
    dob: Optional[date] = None
    gender: Optional[GenderType] = None
    nationality: Optional[str] = Field(None, max_length=2)  # Country code
    id_type: Optional[str] = Field(None, max_length=20)
    id_number: Optional[str] = None

class PersonCreate(PersonBase):
    pass

class PersonUpdate(BaseModel):
    first_name: Optional[str] = Field(None, max_length=100)
    last_name: Optional[str] = Field(None, max_length=100)
    middle_name: Optional[str] = Field(None, max_length=100)
    email: Optional[EmailStr] = None
    # Split phone fields
    phone_mobile_country_code: Optional[str] = Field(None, max_length=6)
    phone_mobile_number: Optional[str] = Field(None, max_length=20)
    phone_home_country_code: Optional[str] = Field(None, max_length=6)
    phone_home_number: Optional[str] = Field(None, max_length=20)
    dob: Optional[date] = None
    gender: Optional[GenderType] = None
    nationality: Optional[str] = Field(None, max_length=2)
    id_type: Optional[str] = Field(None, max_length=20)
    id_number: Optional[str] = None

class PersonResponse(PersonBase):
    id: UUID
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

# Clinic Schemas
class ClinicBase(BaseModel):
    code: str = Field(..., max_length=10)
    name: str = Field(..., max_length=100)
    functional_currency: Optional[str] = Field(None, max_length=3)
    # Address fields
    address_line_1: Optional[str] = Field(None, max_length=255)
    address_line_2: Optional[str] = Field(None, max_length=255)
    city: Optional[str] = Field(None, max_length=100)
    state_province: Optional[str] = Field(None, max_length=100)
    postal_code: Optional[str] = Field(None, max_length=20)
    country_code: Optional[str] = Field(None, max_length=2)
    # Split phone fields
    phone_country_code: Optional[str] = Field(None, max_length=6)
    phone_number: Optional[str] = Field(None, max_length=20)
    email: Optional[EmailStr] = None
    tax_id: Optional[str] = Field(None, max_length=50)
    is_active: bool = True

class ClinicCreate(ClinicBase):
    pass

class ClinicUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=100)
    functional_currency: Optional[str] = Field(None, max_length=3)
    # Address fields
    address_line_1: Optional[str] = Field(None, max_length=255)
    address_line_2: Optional[str] = Field(None, max_length=255)
    city: Optional[str] = Field(None, max_length=100)
    state_province: Optional[str] = Field(None, max_length=100)
    postal_code: Optional[str] = Field(None, max_length=20)
    country_code: Optional[str] = Field(None, max_length=2)
    # Split phone fields
    phone_country_code: Optional[str] = Field(None, max_length=6)
    phone_number: Optional[str] = Field(None, max_length=20)
    email: Optional[EmailStr] = None
    tax_id: Optional[str] = Field(None, max_length=50)
    is_active: Optional[bool] = None

class ClinicResponse(ClinicBase):
    id: UUID
    created_at: datetime
    updated_at: datetime
    temp_id: Optional[int] = None  # Migration helper field
    
    class Config:
        from_attributes = True

# Client Schemas  
class ClientBase(BaseModel):
    client_code: Optional[str] = Field(None, max_length=20)
    acquisition_date: Optional[date] = None
    preferred_clinic_id: Optional[UUID] = None
    is_active: bool = True

class ClientCreate(ClientBase):
    person_id: UUID

class ClientUpdate(BaseModel):
    client_code: Optional[str] = Field(None, max_length=20)
    acquisition_date: Optional[date] = None
    preferred_clinic_id: Optional[UUID] = None
    is_active: Optional[bool] = None

class ClientResponse(ClientBase):
    id: UUID
    person_id: UUID
    temp_id: Optional[int] = None  # Migration helper field
    person: Optional[PersonResponse] = None
    
    class Config:
        from_attributes = True

# Employee Schemas
class EmployeeBase(BaseModel):
    employee_code: Optional[str] = Field(None, max_length=20)
    primary_clinic_id: UUID
    role: EmployeeRole
    specialization: Optional[str] = Field(None, max_length=100)
    license_number: Optional[str] = Field(None, max_length=50)
    license_expiry: Optional[date] = None
    hire_date: date
    termination_date: Optional[date] = None
    base_salary_minor: Optional[int] = None  # Store in cents/pence
    salary_currency: Optional[str] = Field(None, max_length=3)
    commission_rate: Optional[Decimal] = None
    is_active: bool = True
    can_perform_treatments: bool = False

class EmployeeCreate(EmployeeBase):
    person_id: UUID

class EmployeeUpdate(BaseModel):
    employee_code: Optional[str] = Field(None, max_length=20)
    primary_clinic_id: Optional[UUID] = None
    role: Optional[EmployeeRole] = None
    specialization: Optional[str] = Field(None, max_length=100)
    license_number: Optional[str] = Field(None, max_length=50)
    license_expiry: Optional[date] = None
    hire_date: Optional[date] = None
    termination_date: Optional[date] = None
    base_salary_minor: Optional[int] = None
    salary_currency: Optional[str] = Field(None, max_length=3)
    commission_rate: Optional[Decimal] = None
    is_active: Optional[bool] = None
    can_perform_treatments: Optional[bool] = None

class EmployeeResponse(EmployeeBase):
    id: UUID
    person_id: UUID
    temp_id: Optional[int] = None  # Migration helper field
    created_at: datetime
    updated_at: datetime
    person: Optional[PersonResponse] = None
    
    class Config:
        from_attributes = True

# Utility schemas for phone number handling
class PhoneNumber(BaseModel):
    """Utility schema for handling phone numbers"""
    country_code: str = Field(..., max_length=6, pattern=r'^\+\d{1,5}$')
    number: str = Field(..., max_length=20, pattern=r'^\d{4,20}$')
    
    @property
    def full_number(self) -> str:
        """Get the full formatted phone number"""
        return f"{self.country_code} {self.number}"

class PhoneNumberUpdate(BaseModel):
    """Utility schema for updating phone numbers"""
    country_code: Optional[str] = Field(None, max_length=6, pattern=r'^\+\d{1,5}$')
    number: Optional[str] = Field(None, max_length=20, pattern=r'^\d{4,20}$')
