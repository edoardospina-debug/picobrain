"""Enhanced Employee API endpoints with composite creation"""
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from typing import List, Any, Optional
from uuid import UUID
import logging

from app.api import deps
from app.models import User
from app.schemas.employee import (
    EmployeeCreateDTO,
    EmployeeCreateResponse,
    EmployeeBulkCreateDTO,
    EmployeeBulkCreateResponse
)
from app.schemas.core import EmployeeResponse, EmployeeUpdate, EmployeeRole
from app.services import EmployeeService
from app.core.exceptions import (
    ValidationException,
    DuplicateResourceException,
    ResourceNotFoundException,
    EmployeeCreationException,
    DatabaseTransactionException
)

router = APIRouter()
logger = logging.getLogger(__name__)


def get_employee_service(db: Session = Depends(deps.get_db)) -> EmployeeService:
    """Dependency to get employee service instance"""
    return EmployeeService(db)


@router.post("/", response_model=EmployeeCreateResponse, status_code=status.HTTP_201_CREATED)
async def create_employee_with_person(
    employee_dto: EmployeeCreateDTO,
    service: EmployeeService = Depends(get_employee_service),
    current_user: User = Depends(deps.get_current_active_superuser)
) -> Any:
    """
    Create a new employee with associated person record.
    
    This endpoint creates both Person and Employee records in a single transaction.
    If the person already exists (based on email), it will return an error.
    
    **Required fields:**
    - first_name, last_name (Person)
    - primary_clinic_id, role, hire_date (Employee)
    
    **Optional fields:**
    - email, phone numbers, DOB, etc. (Person)
    - employee_code (auto-generated if not provided)
    - salary, license info, etc. (Employee)
    
    **Access:** Admin only
    """
    try:
        result = await service.create_employee(employee_dto)
        logger.info(
            f"Employee {result.employee.employee_code} created by user {current_user.username}"
        )
        return result
    except ValidationException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"message": "Validation failed", "errors": e.errors}
        )
    except DuplicateResourceException as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={"message": e.message, "details": e.details}
        )
    except ResourceNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"message": e.message, "details": e.details}
        )
    except EmployeeCreationException as e:
        logger.error(f"Employee creation failed: {e.message}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"message": "Failed to create employee", "error": str(e.original_error)}
        )
    except Exception as e:
        logger.error(f"Unexpected error in create_employee: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred"
        )


@router.post("/bulk", response_model=EmployeeBulkCreateResponse, status_code=status.HTTP_201_CREATED)
async def bulk_create_employees(
    bulk_dto: EmployeeBulkCreateDTO,
    service: EmployeeService = Depends(get_employee_service),
    current_user: User = Depends(deps.get_current_active_superuser)
) -> Any:
    """
    Create multiple employees in bulk.
    
    This endpoint allows creation of up to 100 employees at once.
    Each employee will have their associated Person record created.
    
    **Options:**
    - stop_on_error: Stop processing if any employee fails
    - validate_all_first: Validate all employees before creating any
    
    **Access:** Admin only
    """
    try:
        result = await service.bulk_create_employees(bulk_dto)
        logger.info(
            f"Bulk creation by {current_user.username}: "
            f"{result.total_created} created, {result.total_failed} failed"
        )
        return result
    except Exception as e:
        logger.error(f"Bulk creation error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Bulk creation failed"
        )


@router.get("/", response_model=List[EmployeeResponse])
async def get_employees(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, le=100, description="Maximum number of records to return"),
    clinic_id: Optional[UUID] = Query(None, description="Filter by clinic ID"),
    role: Optional[EmployeeRole] = Query(None, description="Filter by role"),
    is_active: Optional[bool] = Query(None, description="Filter by active status"),
    service: EmployeeService = Depends(get_employee_service),
    current_user: User = Depends(deps.get_current_user)
) -> Any:
    """
    Get all employees with optional filters.
    
    Returns employees with their associated person data.
    
    **Filters:**
    - clinic_id: Filter by primary clinic
    - role: Filter by employee role
    - is_active: Filter by active status
    
    **Access:** Requires authentication
    """
    try:
        employees = await service.get_employees(
            skip=skip,
            limit=limit,
            clinic_id=clinic_id,
            role=role,
            is_active=is_active
        )
        return employees
    except Exception as e:
        logger.error(f"Error fetching employees: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch employees"
        )


@router.get("/code/{employee_code}", response_model=EmployeeResponse)
async def get_employee_by_code(
    employee_code: str,
    service: EmployeeService = Depends(get_employee_service),
    current_user: User = Depends(deps.get_current_user)
) -> Any:
    """
    Get employee by employee code.
    
    Returns employee with associated person data.
    
    **Access:** Requires authentication
    """
    employee = await service.get_employee_by_code(employee_code.upper())
    if not employee:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Employee with code '{employee_code}' not found"
        )
    return employee


@router.get("/medical-staff", response_model=List[EmployeeResponse])
async def get_medical_staff(
    clinic_id: Optional[UUID] = Query(None, description="Filter by clinic ID"),
    service: EmployeeService = Depends(get_employee_service),
    current_user: User = Depends(deps.get_current_user)
) -> Any:
    """
    Get all medical staff (employees who can perform treatments).
    
    Returns only active employees with treatment permissions.
    
    **Access:** Requires authentication
    """
    try:
        staff = await service.get_medical_staff(clinic_id)
        return staff
    except Exception as e:
        logger.error(f"Error fetching medical staff: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch medical staff"
        )


@router.get("/{employee_id}", response_model=EmployeeResponse)
async def get_employee(
    employee_id: UUID,
    service: EmployeeService = Depends(get_employee_service),
    current_user: User = Depends(deps.get_current_user)
) -> Any:
    """
    Get employee by ID.
    
    Returns employee with associated person data.
    
    **Access:** Requires authentication
    """
    employee = await service.get_employee(employee_id)
    if not employee:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Employee not found"
        )
    return employee


@router.put("/{employee_id}", response_model=EmployeeResponse)
async def update_employee(
    employee_id: UUID,
    employee_update: EmployeeUpdate,
    service: EmployeeService = Depends(get_employee_service),
    current_user: User = Depends(deps.get_current_active_superuser)
) -> Any:
    """
    Update an employee.
    
    Only updates Employee fields, not Person fields.
    To update Person fields, use the /persons endpoint.
    
    **Access:** Admin only
    """
    try:
        updated_employee = await service.update_employee(employee_id, employee_update)
        logger.info(f"Employee {employee_id} updated by {current_user.username}")
        return updated_employee
    except ResourceNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.message
        )
    except ValidationException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"message": "Validation failed", "errors": e.errors}
        )
    except Exception as e:
        logger.error(f"Error updating employee {employee_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update employee"
        )


@router.delete("/{employee_id}")
async def delete_employee(
    employee_id: UUID,
    soft_delete: bool = Query(True, description="Soft delete (deactivate) vs hard delete"),
    service: EmployeeService = Depends(get_employee_service),
    current_user: User = Depends(deps.get_current_active_superuser)
) -> Any:
    """
    Delete an employee.
    
    **Options:**
    - soft_delete=true: Mark employee as inactive (default)
    - soft_delete=false: Permanently delete employee record
    
    Note: This does not delete the associated Person record.
    
    **Access:** Admin only
    """
    try:
        deleted = await service.delete_employee(employee_id, soft_delete)
        if not deleted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Employee not found"
            )
        
        action = "deactivated" if soft_delete else "deleted"
        logger.info(f"Employee {employee_id} {action} by {current_user.username}")
        
        return {
            "message": f"Employee {action} successfully",
            "employee_id": str(employee_id),
            "soft_delete": soft_delete
        }
    except Exception as e:
        logger.error(f"Error deleting employee {employee_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete employee"
        )


@router.get("/clinic/{clinic_id}", response_model=List[EmployeeResponse])
async def get_employees_by_clinic(
    clinic_id: UUID,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, le=100),
    is_active: Optional[bool] = Query(None, description="Filter by active status"),
    service: EmployeeService = Depends(get_employee_service),
    current_user: User = Depends(deps.get_current_user)
) -> Any:
    """
    Get all employees for a specific clinic.
    
    Returns employees with their associated person data.
    
    **Access:** Requires authentication
    """
    try:
        employees = await service.get_employees(
            skip=skip,
            limit=limit,
            clinic_id=clinic_id,
            is_active=is_active
        )
        return employees
    except Exception as e:
        logger.error(f"Error fetching clinic employees: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch clinic employees"
        )