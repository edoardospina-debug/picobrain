"""Employee service for business logic and orchestration"""
import logging
from typing import Optional, List, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from uuid import UUID
from contextlib import contextmanager

from app.models.core import Person, Employee, Clinic
from app.repositories import PersonRepository, EmployeeRepository
from app.schemas.employee import (
    EmployeeCreateDTO,
    EmployeeCreateResponse,
    EmployeeBulkCreateDTO,
    EmployeeBulkCreateResponse
)
from app.schemas.core import EmployeeResponse, PersonResponse, EmployeeUpdate
from app.validators import EmployeeValidator
from app.core.exceptions import (
    ValidationException,
    EmployeeCreationException,
    DatabaseTransactionException,
    ResourceNotFoundException
)

logger = logging.getLogger(__name__)


class EmployeeService:
    """Service layer for Employee operations"""
    
    def __init__(self, db: Session):
        """
        Initialize Employee service
        
        Args:
            db: Database session
        """
        self.db = db
        self.person_repo = PersonRepository(db)
        self.employee_repo = EmployeeRepository(db)
        self.validator = EmployeeValidator()
    
    @contextmanager
    def transaction(self):
        """
        Context manager for database transactions
        
        Yields control and handles commit/rollback automatically
        """
        try:
            yield
            self.db.commit()
        except Exception as e:
            self.db.rollback()
            logger.error(f"Transaction rolled back: {str(e)}")
            raise
        finally:
            # Ensure session is clean for next operation
            self.db.expire_all()
    
    async def create_employee(self, dto: EmployeeCreateDTO) -> EmployeeCreateResponse:
        """
        Create a new employee with associated person record
        
        This method creates both Person and Employee records in a single transaction,
        ensuring data consistency.
        
        Args:
            dto: Employee creation DTO containing both Person and Employee fields
            
        Returns:
            EmployeeCreateResponse with created employee and person data
            
        Raises:
            ValidationException: If validation fails
            EmployeeCreationException: If creation process fails
            DatabaseTransactionException: If transaction fails
        """
        try:
            # Step 1: Validation phase (before transaction)
            await self.validator.validate_create(dto, self.db)
            
            # Step 2: Generate employee code if not provided
            if not dto.employee_code:
                clinic = self.db.query(Clinic).filter(
                    Clinic.id == dto.primary_clinic_id
                ).first()
                dto.employee_code = self.validator.generate_employee_code(
                    dto.first_name,
                    dto.last_name,
                    clinic.code,
                    self.db
                )
                logger.info(f"Generated employee code: {dto.employee_code}")
            
            # Step 3: Create records in transaction
            with self.transaction():
                # Create Person
                person_data = dto.get_person_fields()
                person = self.person_repo.create(person_data)
                logger.info(f"Created person with ID: {person.id}")
                
                # Create Employee with person_id
                employee_data = dto.get_employee_fields()
                employee_data['person_id'] = person.id
                employee = self.employee_repo.create(employee_data)
                logger.info(f"Created employee with ID: {employee.id}")
                
                # Refresh to get all relationships
                self.db.refresh(person)
                self.db.refresh(employee)
            
            # Step 4: Prepare response
            employee_response = EmployeeResponse.from_orm(employee)
            person_response = PersonResponse.from_orm(person)
            
            return EmployeeCreateResponse(
                employee=employee_response,
                person=person_response,
                message=f"Employee {dto.employee_code} created successfully"
            )
            
        except ValidationException:
            # Re-raise validation exceptions as-is
            raise
        except IntegrityError as e:
            # Handle database constraint violations
            logger.error(f"Integrity error during employee creation: {str(e)}")
            if "unique_email" in str(e) or "email" in str(e):
                raise ValidationException(["Email address already exists"])
            elif "unique_employee_code" in str(e) or "employee_code" in str(e):
                raise ValidationException(["Employee code already exists"])
            else:
                raise DatabaseTransactionException("employee_creation", e)
        except Exception as e:
            # Handle unexpected errors
            logger.error(f"Unexpected error creating employee: {str(e)}")
            raise EmployeeCreationException("unexpected", e)
    
    async def update_employee(
        self,
        employee_id: UUID,
        update_data: EmployeeUpdate
    ) -> EmployeeResponse:
        """
        Update an existing employee
        
        Args:
            employee_id: Employee UUID
            update_data: Fields to update
            
        Returns:
            Updated employee response
            
        Raises:
            ResourceNotFoundException: If employee not found
            ValidationException: If validation fails
        """
        try:
            # Validate update
            update_dict = update_data.dict(exclude_unset=True)
            await self.validator.validate_update(employee_id, update_dict, self.db)
            
            with self.transaction():
                # Update employee
                employee = self.employee_repo.update(employee_id, update_dict)
                if not employee:
                    raise ResourceNotFoundException("Employee", employee_id)
                
                # Refresh to get updated relationships
                self.db.refresh(employee)
            
            return EmployeeResponse.from_orm(employee)
            
        except (ValidationException, ResourceNotFoundException):
            raise
        except Exception as e:
            logger.error(f"Error updating employee {employee_id}: {str(e)}")
            raise DatabaseTransactionException("employee_update", e)
    
    async def get_employee(self, employee_id: UUID) -> Optional[EmployeeResponse]:
        """
        Get employee by ID with person data
        
        Args:
            employee_id: Employee UUID
            
        Returns:
            Employee response with person data or None
        """
        employee = self.employee_repo.get_with_person(employee_id)
        if employee:
            return EmployeeResponse.from_orm(employee)
        return None
    
    async def get_employees(
        self,
        skip: int = 0,
        limit: int = 100,
        clinic_id: Optional[UUID] = None,
        role: Optional[str] = None,
        is_active: Optional[bool] = None
    ) -> List[EmployeeResponse]:
        """
        Get employees with filters
        
        Args:
            skip: Number of records to skip
            limit: Maximum number of records
            clinic_id: Filter by clinic
            role: Filter by role
            is_active: Filter by active status
            
        Returns:
            List of employee responses
        """
        filters = {}
        if clinic_id:
            filters['primary_clinic_id'] = clinic_id
        if role:
            filters['role'] = role
        if is_active is not None:
            filters['is_active'] = is_active
        
        employees = self.employee_repo.get_all_with_person(
            skip=skip,
            limit=limit,
            filters=filters
        )
        
        return [EmployeeResponse.from_orm(emp) for emp in employees]
    
    async def delete_employee(
        self,
        employee_id: UUID,
        soft_delete: bool = True
    ) -> bool:
        """
        Delete an employee
        
        Args:
            employee_id: Employee UUID
            soft_delete: If True, only mark as inactive
            
        Returns:
            True if deleted, False if not found
        """
        try:
            with self.transaction():
                if soft_delete:
                    # Soft delete - mark as inactive
                    employee = self.employee_repo.update(
                        employee_id,
                        {'is_active': False}
                    )
                    return employee is not None
                else:
                    # Hard delete - remove from database
                    return self.employee_repo.delete(employee_id)
        except Exception as e:
            logger.error(f"Error deleting employee {employee_id}: {str(e)}")
            raise DatabaseTransactionException("employee_delete", e)
    
    async def bulk_create_employees(
        self,
        bulk_dto: EmployeeBulkCreateDTO
    ) -> EmployeeBulkCreateResponse:
        """
        Create multiple employees in bulk
        
        Args:
            bulk_dto: Bulk creation DTO
            
        Returns:
            Bulk creation response with successes and failures
        """
        response = EmployeeBulkCreateResponse(
            created=[],
            failed=[],
            total_processed=len(bulk_dto.employees),
            total_created=0,
            total_failed=0
        )
        
        # Validate all first if requested
        if bulk_dto.validate_all_first:
            for idx, employee_dto in enumerate(bulk_dto.employees):
                try:
                    await self.validator.validate_create(employee_dto, self.db)
                except Exception as e:
                    response.failed.append({
                        "index": idx,
                        "employee_code": employee_dto.employee_code,
                        "error": str(e)
                    })
                    if bulk_dto.stop_on_error:
                        response.total_failed = len(response.failed)
                        return response
        
        # Process each employee
        for idx, employee_dto in enumerate(bulk_dto.employees):
            try:
                result = await self.create_employee(employee_dto)
                response.created.append(result)
                response.total_created += 1
            except Exception as e:
                logger.error(f"Failed to create employee at index {idx}: {str(e)}")
                response.failed.append({
                    "index": idx,
                    "employee_code": employee_dto.employee_code,
                    "email": employee_dto.email,
                    "error": str(e)
                })
                response.total_failed += 1
                
                if bulk_dto.stop_on_error:
                    break
        
        return response
    
    async def get_employee_by_code(
        self,
        employee_code: str
    ) -> Optional[EmployeeResponse]:
        """
        Get employee by employee code
        
        Args:
            employee_code: Employee code
            
        Returns:
            Employee response or None
        """
        employee = self.employee_repo.get_by_employee_code(employee_code)
        if employee:
            # Load person data
            employee = self.employee_repo.get_with_person(employee.id)
            return EmployeeResponse.from_orm(employee)
        return None
    
    async def get_medical_staff(
        self,
        clinic_id: Optional[UUID] = None
    ) -> List[EmployeeResponse]:
        """
        Get all medical staff (employees who can perform treatments)
        
        Args:
            clinic_id: Optional clinic filter
            
        Returns:
            List of medical staff employees
        """
        employees = self.employee_repo.get_medical_staff(clinic_id)
        return [EmployeeResponse.from_orm(emp) for emp in employees]