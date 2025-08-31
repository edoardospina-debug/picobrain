"""Enhanced employee schemas with composite creation support"""
from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional, Dict, Any
from datetime import date, datetime
from uuid import UUID
from decimal import Decimal
from app.schemas.core import (
    PersonBase, 
    PersonResponse, 
    EmployeeBase, 
    EmployeeResponse,
    GenderType,
    EmployeeRole
)


class PersonBaseDTO(BaseModel):
    """Base DTO for Person fields - used as a mixin"""
    first_name: str = Field(..., max_length=100, description="Person's first name")
    last_name: str = Field(..., max_length=100, description="Person's last name")
    middle_name: Optional[str] = Field(None, max_length=100, description="Person's middle name")
    email: Optional[EmailStr] = Field(None, description="Email address")
    
    # Split phone fields for mobile
    phone_mobile_country_code: Optional[str] = Field(
        None, 
        max_length=6, 
        pattern=r'^\+\d{1,5}$',
        description="Mobile phone country code (e.g., +1)"
    )
    phone_mobile_number: Optional[str] = Field(
        None, 
        max_length=20,
        pattern=r'^\d{4,20}$',
        description="Mobile phone number"
    )
    
    # Split phone fields for home
    phone_home_country_code: Optional[str] = Field(
        None,
        max_length=6,
        pattern=r'^\+\d{1,5}$',
        description="Home phone country code"
    )
    phone_home_number: Optional[str] = Field(
        None,
        max_length=20,
        pattern=r'^\d{4,20}$',
        description="Home phone number"
    )
    
    # Personal details
    dob: Optional[date] = Field(None, description="Date of birth")
    gender: Optional[GenderType] = Field(None, description="Gender")
    nationality: Optional[str] = Field(
        None, 
        max_length=2,
        pattern=r'^[A-Z]{2}$',
        description="Nationality as 2-letter country code"
    )
    
    # Identification
    id_type: Optional[str] = Field(
        None,
        max_length=20,
        description="Type of ID (passport, national_id, etc.)"
    )
    id_number: Optional[str] = Field(None, description="ID number/value")
    
    @validator('email', pre=True)
    def email_to_lower(cls, v):
        """Convert email to lowercase"""
        return v.lower() if v else v
    
    @validator('phone_mobile_country_code', 'phone_home_country_code', pre=True)
    def format_country_code(cls, v):
        """Ensure country code starts with +"""
        if v and not v.startswith('+'):
            return f'+{v}'
        return v


class EmployeeCreateDTO(PersonBaseDTO):
    """DTO for creating an Employee with Person data"""
    
    # Employee-specific fields
    employee_code: Optional[str] = Field(
        None,
        max_length=20,
        description="Unique employee code (auto-generated if not provided)"
    )
    primary_clinic_id: UUID = Field(..., description="Primary clinic assignment")
    role: EmployeeRole = Field(..., description="Employee role")
    specialization: Optional[str] = Field(
        None,
        max_length=100,
        description="Medical specialization or department"
    )
    
    # Professional licensing
    license_number: Optional[str] = Field(
        None,
        max_length=50,
        description="Professional license number"
    )
    license_expiry: Optional[date] = Field(
        None,
        description="License expiration date"
    )
    
    # Employment dates
    hire_date: date = Field(..., description="Employment start date")
    termination_date: Optional[date] = Field(
        None,
        description="Employment end date (if applicable)"
    )
    
    # Compensation
    base_salary_minor: Optional[int] = Field(
        None,
        ge=0,
        description="Base salary in minor units (cents/pence)"
    )
    salary_currency: Optional[str] = Field(
        None,
        max_length=3,
        pattern=r'^[A-Z]{3}$',
        description="Salary currency code (e.g., USD, EUR)"
    )
    commission_rate: Optional[Decimal] = Field(
        None,
        ge=0,
        le=100,
        description="Commission rate percentage (0-100)"
    )
    
    # Status flags
    is_active: bool = Field(True, description="Whether employee is active")
    can_perform_treatments: bool = Field(
        False,
        description="Whether employee can perform medical treatments"
    )
    
    @validator('termination_date')
    def validate_termination_date(cls, v, values):
        """Ensure termination date is after hire date"""
        if v and 'hire_date' in values and values['hire_date']:
            if v < values['hire_date']:
                raise ValueError("Termination date cannot be before hire date")
        return v
    
    @validator('employee_code', pre=True)
    def clean_employee_code(cls, v):
        """Clean and validate employee code"""
        if v:
            return v.strip().upper()
        return v
    
    @validator('can_perform_treatments')
    def validate_treatment_permission(cls, v, values):
        """Only medical staff can perform treatments"""
        if v and 'role' in values:
            allowed_roles = ['doctor', 'nurse']
            if values['role'] not in allowed_roles:
                raise ValueError(
                    f"Only {', '.join(allowed_roles)} can perform treatments"
                )
        return v
    
    def get_person_fields(self) -> Dict[str, Any]:
        """Extract Person model fields from DTO"""
        person_fields = {
            'first_name': self.first_name,
            'last_name': self.last_name,
            'middle_name': self.middle_name,
            'email': self.email,
            'phone_mobile_country_code': self.phone_mobile_country_code,
            'phone_mobile_number': self.phone_mobile_number,
            'phone_home_country_code': self.phone_home_country_code,
            'phone_home_number': self.phone_home_number,
            'dob': self.dob,
            'gender': self.gender,
            'nationality': self.nationality,
            'id_type': self.id_type,
            'id_number': self.id_number
        }
        # Remove None values
        return {k: v for k, v in person_fields.items() if v is not None}
    
    def get_employee_fields(self) -> Dict[str, Any]:
        """Extract Employee model fields from DTO"""
        employee_fields = {
            'employee_code': self.employee_code,
            'primary_clinic_id': self.primary_clinic_id,
            'role': self.role,
            'specialization': self.specialization,
            'license_number': self.license_number,
            'license_expiry': self.license_expiry,
            'hire_date': self.hire_date,
            'termination_date': self.termination_date,
            'base_salary_minor': self.base_salary_minor,
            'salary_currency': self.salary_currency,
            'commission_rate': self.commission_rate,
            'is_active': self.is_active,
            'can_perform_treatments': self.can_perform_treatments
        }
        # Remove None values except for optional fields that should be stored as null
        return {k: v for k, v in employee_fields.items() if v is not None}


class EmployeeCreateResponse(BaseModel):
    """Response model for successful employee creation"""
    employee: EmployeeResponse
    person: PersonResponse
    message: str = "Employee created successfully"
    
    class Config:
        from_attributes = True


class EmployeeBulkCreateDTO(BaseModel):
    """DTO for bulk employee creation"""
    employees: list[EmployeeCreateDTO] = Field(
        ...,
        min_items=1,
        max_items=100,
        description="List of employees to create (max 100)"
    )
    
    # Options for bulk operation
    stop_on_error: bool = Field(
        False,
        description="Stop processing if any employee fails"
    )
    validate_all_first: bool = Field(
        True,
        description="Validate all employees before creating any"
    )


class EmployeeBulkCreateResponse(BaseModel):
    """Response for bulk employee creation"""
    created: list[EmployeeCreateResponse] = Field(
        default_factory=list,
        description="Successfully created employees"
    )
    failed: list[dict] = Field(
        default_factory=list,
        description="Failed employee creations with error details"
    )
    total_processed: int = Field(..., description="Total number processed")
    total_created: int = Field(..., description="Total successfully created")
    total_failed: int = Field(..., description="Total failed")