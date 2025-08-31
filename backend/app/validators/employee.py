"""Employee validation logic"""
from typing import List, Optional
from sqlalchemy.orm import Session
from uuid import UUID
from app.schemas.employee import EmployeeCreateDTO
from app.repositories import PersonRepository, EmployeeRepository
from app.models.core import Clinic
from app.core.exceptions import (
    ValidationException,
    DuplicateResourceException,
    PersonAlreadyEmployeeException,
    ResourceNotFoundException
)
import re


class EmployeeValidator:
    """Validator for Employee operations"""
    
    @staticmethod
    async def validate_create(dto: EmployeeCreateDTO, db: Session) -> None:
        """
        Validate employee creation request
        
        Args:
            dto: Employee creation DTO
            db: Database session
            
        Raises:
            ValidationException: If validation fails
            DuplicateResourceException: If duplicate found
            ResourceNotFoundException: If required resource not found
        """
        errors = []
        person_repo = PersonRepository(db)
        employee_repo = EmployeeRepository(db)
        
        # 1. Validate email uniqueness if provided
        if dto.email:
            if person_repo.exists_by_email(dto.email):
                raise DuplicateResourceException("Person", "email", dto.email)
        
        # 2. Validate employee code uniqueness if provided
        if dto.employee_code:
            if employee_repo.exists_by_employee_code(dto.employee_code):
                raise DuplicateResourceException("Employee", "employee_code", dto.employee_code)
        
        # 3. Validate clinic exists
        clinic = db.query(Clinic).filter(Clinic.id == dto.primary_clinic_id).first()
        if not clinic:
            raise ResourceNotFoundException("Clinic", dto.primary_clinic_id)
        
        # 4. Validate clinic is active
        if not clinic.is_active:
            errors.append(f"Clinic {clinic.code} is not active")
        
        # 5. Validate ID number uniqueness if provided
        if dto.id_number and dto.id_type:
            existing_person = person_repo.db.query(person_repo.model).filter(
                person_repo.model.id_number == dto.id_number,
                person_repo.model.id_type == dto.id_type
            ).first()
            if existing_person:
                errors.append(
                    f"Person with {dto.id_type} number {dto.id_number} already exists"
                )
        
        # 6. Validate phone number format
        if dto.phone_mobile_number and dto.phone_mobile_country_code:
            if not EmployeeValidator._validate_phone_format(
                dto.phone_mobile_country_code, 
                dto.phone_mobile_number
            ):
                errors.append("Invalid mobile phone format")
        
        if dto.phone_home_number and dto.phone_home_country_code:
            if not EmployeeValidator._validate_phone_format(
                dto.phone_home_country_code,
                dto.phone_home_number
            ):
                errors.append("Invalid home phone format")
        
        # 7. Validate professional license for medical roles
        if dto.role in ['doctor', 'nurse']:
            if not dto.license_number:
                errors.append(f"License number is required for {dto.role}")
            if not dto.license_expiry:
                errors.append(f"License expiry date is required for {dto.role}")
        
        # 8. Validate salary currency if salary is provided
        if dto.base_salary_minor and not dto.salary_currency:
            errors.append("Salary currency is required when base salary is provided")
        
        # 9. Additional business rules
        if dto.commission_rate and dto.role not in ['doctor', 'manager']:
            errors.append(f"Commission rate not applicable for role: {dto.role}")
        
        # Raise validation exception if any errors found
        if errors:
            raise ValidationException(errors)
    
    @staticmethod
    def _validate_phone_format(country_code: str, number: str) -> bool:
        """
        Validate phone number format
        
        Args:
            country_code: Country code with + prefix
            number: Phone number
            
        Returns:
            True if valid, False otherwise
        """
        # Check country code format
        if not re.match(r'^\+\d{1,5}$', country_code):
            return False
        
        # Check number format (digits only, 4-20 characters)
        if not re.match(r'^\d{4,20}$', number):
            return False
        
        return True
    
    @staticmethod
    async def validate_update(
        employee_id: UUID,
        update_data: dict,
        db: Session
    ) -> None:
        """
        Validate employee update request
        
        Args:
            employee_id: Employee ID being updated
            update_data: Dictionary of fields to update
            db: Database session
            
        Raises:
            ValidationException: If validation fails
            DuplicateResourceException: If duplicate found
            ResourceNotFoundException: If required resource not found
        """
        errors = []
        employee_repo = EmployeeRepository(db)
        
        # Get existing employee
        existing_employee = employee_repo.get(employee_id)
        if not existing_employee:
            raise ResourceNotFoundException("Employee", employee_id)
        
        # Validate employee code uniqueness if being updated
        if 'employee_code' in update_data:
            new_code = update_data['employee_code']
            if new_code and new_code != existing_employee.employee_code:
                if employee_repo.exists_by_employee_code(new_code):
                    raise DuplicateResourceException(
                        "Employee", 
                        "employee_code", 
                        new_code
                    )
        
        # Validate clinic if being updated
        if 'primary_clinic_id' in update_data:
            clinic_id = update_data['primary_clinic_id']
            clinic = db.query(Clinic).filter(Clinic.id == clinic_id).first()
            if not clinic:
                raise ResourceNotFoundException("Clinic", clinic_id)
            if not clinic.is_active:
                errors.append(f"Clinic {clinic.code} is not active")
        
        # Validate termination date if being set
        if 'termination_date' in update_data:
            term_date = update_data['termination_date']
            if term_date and term_date < existing_employee.hire_date:
                errors.append("Termination date cannot be before hire date")
        
        # Validate role change implications
        if 'role' in update_data:
            new_role = update_data['role']
            # Check if losing medical role while having treatments permission
            if (new_role not in ['doctor', 'nurse'] and 
                existing_employee.can_perform_treatments):
                errors.append(
                    f"Cannot change role to {new_role} while employee "
                    "has treatment permissions"
                )
        
        if errors:
            raise ValidationException(errors)
    
    @staticmethod
    async def validate_person_not_employee(
        person_id: UUID,
        db: Session
    ) -> None:
        """
        Validate that a person is not already an employee
        
        Args:
            person_id: Person ID to check
            db: Database session
            
        Raises:
            PersonAlreadyEmployeeException: If person is already an employee
        """
        employee_repo = EmployeeRepository(db)
        if employee_repo.exists_by_person_id(person_id):
            raise PersonAlreadyEmployeeException(str(person_id))
    
    @staticmethod
    def generate_employee_code(
        first_name: str,
        last_name: str,
        clinic_code: str,
        db: Session
    ) -> str:
        """
        Generate a unique employee code
        
        Args:
            first_name: Employee's first name
            last_name: Employee's last name
            clinic_code: Clinic code
            db: Database session
            
        Returns:
            Generated unique employee code
        """
        # Create base code from initials and clinic
        base_code = f"{first_name[0]}{last_name[0]}{clinic_code}".upper()
        
        # Find existing codes with this pattern
        employee_repo = EmployeeRepository(db)
        counter = 1
        employee_code = f"{base_code}{counter:03d}"
        
        while employee_repo.exists_by_employee_code(employee_code):
            counter += 1
            employee_code = f"{base_code}{counter:03d}"
        
        return employee_code