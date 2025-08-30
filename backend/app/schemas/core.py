from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import date
from uuid import UUID
from enum import Enum

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

# Person Schemas
class PersonBase(BaseModel):
    first_name: str = Field(..., max_length=100)
    last_name: str = Field(..., max_length=100)
    email: Optional[EmailStr] = None
    phone_mobile: Optional[str] = Field(None, max_length=50)
    dob: Optional[date] = None
    gender: Optional[GenderType] = None

class PersonCreate(PersonBase):
    pass

class PersonUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone_mobile: Optional[str] = None
    dob: Optional[date] = None
    gender: Optional[GenderType] = None

class PersonResponse(PersonBase):
    id: UUID
    
    class Config:
        from_attributes = True

# Clinic Schemas
class ClinicBase(BaseModel):
    code: str = Field(..., max_length=10)
    name: str = Field(..., max_length=100)
    functional_currency: str = Field(..., max_length=3)
    city: Optional[str] = Field(None, max_length=100)
    country_code: Optional[str] = Field(None, max_length=2)

class ClinicCreate(ClinicBase):
    pass

class ClinicUpdate(BaseModel):
    name: Optional[str] = None
    functional_currency: Optional[str] = None
    city: Optional[str] = None
    country_code: Optional[str] = None
    is_active: Optional[bool] = None

class ClinicResponse(ClinicBase):
    id: UUID
    is_active: bool
    
    class Config:
        from_attributes = True

# Client Schemas  
class ClientBase(BaseModel):
    client_code: Optional[str] = None
    preferred_clinic_id: Optional[UUID] = None

class ClientCreate(ClientBase):
    person_id: UUID

class ClientUpdate(BaseModel):
    client_code: Optional[str] = None
    preferred_clinic_id: Optional[UUID] = None
    is_active: Optional[bool] = None

class ClientResponse(ClientBase):
    id: UUID
    person_id: UUID
    acquisition_date: Optional[date]
    is_active: bool
    person: Optional[PersonResponse] = None
    
    class Config:
        from_attributes = True

# Employee Schemas
class EmployeeBase(BaseModel):
    employee_code: Optional[str] = None
    primary_clinic_id: UUID
    role: EmployeeRole
    license_number: Optional[str] = None
    can_perform_treatments: bool = False

class EmployeeCreate(EmployeeBase):
    person_id: UUID

class EmployeeUpdate(BaseModel):
    employee_code: Optional[str] = None
    primary_clinic_id: Optional[UUID] = None
    role: Optional[EmployeeRole] = None
    license_number: Optional[str] = None
    can_perform_treatments: Optional[bool] = None
    is_active: Optional[bool] = None

class EmployeeResponse(EmployeeBase):
    id: UUID
    person_id: UUID
    is_active: bool
    person: Optional[PersonResponse] = None
    
    class Config:
        from_attributes = True