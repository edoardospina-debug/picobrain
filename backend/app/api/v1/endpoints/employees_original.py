from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from typing import List, Any, Optional
from uuid import UUID

from app.api import deps
from app.models import Employee, User, Person, Clinic
from app import schemas

router = APIRouter()

@router.get("/", response_model=List[schemas.EmployeeResponse])
def get_employees(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, le=100),
    clinic_id: Optional[UUID] = None,
    role: Optional[schemas.EmployeeRole] = None,
    is_active: Optional[bool] = None,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
) -> Any:
    """Get all employees with optional filters (requires authentication)"""
    query = db.query(Employee)
    
    # Apply filters
    if clinic_id:
        query = query.filter(Employee.primary_clinic_id == clinic_id)
    if role:
        query = query.filter(Employee.role == role)
    if is_active is not None:
        query = query.filter(Employee.is_active == is_active)
    
    employees = query.offset(skip).limit(limit).all()
    return employees

@router.get("/{employee_id}", response_model=schemas.EmployeeResponse)
def get_employee(
    employee_id: UUID, 
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
) -> Any:
    """Get employee by ID (requires authentication)"""
    employee = db.query(Employee).filter(Employee.id == employee_id).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    return employee

@router.post("/", response_model=schemas.EmployeeResponse)
def create_employee(
    employee: schemas.EmployeeCreate, 
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_superuser)
) -> Any:
    """Create new employee (admin only)"""
    # Verify person exists
    person = db.query(Person).filter(Person.id == employee.person_id).first()
    if not person:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Person not found"
        )
    
    # Verify clinic exists
    clinic = db.query(Clinic).filter(Clinic.id == employee.primary_clinic_id).first()
    if not clinic:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Clinic not found"
        )
    
    # Check if person is already an employee
    existing = db.query(Employee).filter(Employee.person_id == employee.person_id).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Person is already registered as an employee"
        )
    
    # Check if employee code is unique if provided
    if employee.employee_code:
        code_exists = db.query(Employee).filter(Employee.employee_code == employee.employee_code).first()
        if code_exists:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Employee code already exists"
            )
    
    db_employee = Employee(**employee.dict())
    db.add(db_employee)
    db.commit()
    db.refresh(db_employee)
    return db_employee

@router.put("/{employee_id}", response_model=schemas.EmployeeResponse)
def update_employee(
    employee_id: UUID,
    employee_update: schemas.EmployeeUpdate,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_superuser)
) -> Any:
    """Update employee (admin only)"""
    employee = db.query(Employee).filter(Employee.id == employee_id).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    
    # If updating clinic, verify it exists
    if employee_update.primary_clinic_id:
        clinic = db.query(Clinic).filter(Clinic.id == employee_update.primary_clinic_id).first()
        if not clinic:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Clinic not found"
            )
    
    # If updating employee code, check uniqueness
    if employee_update.employee_code and employee_update.employee_code != employee.employee_code:
        code_exists = db.query(Employee).filter(Employee.employee_code == employee_update.employee_code).first()
        if code_exists:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Employee code already exists"
            )
    
    for field, value in employee_update.dict(exclude_unset=True).items():
        setattr(employee, field, value)
    
    db.commit()
    db.refresh(employee)
    return employee

@router.delete("/{employee_id}")
def delete_employee(
    employee_id: UUID, 
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_superuser)
) -> Any:
    """Delete employee (admin only)"""
    employee = db.query(Employee).filter(Employee.id == employee_id).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    
    db.delete(employee)
    db.commit()
    return {"message": "Employee deleted successfully"}

@router.get("/clinic/{clinic_id}", response_model=List[schemas.EmployeeResponse])
def get_employees_by_clinic(
    clinic_id: UUID,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, le=100),
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
) -> Any:
    """Get all employees for a specific clinic"""
    # Verify clinic exists
    clinic = db.query(Clinic).filter(Clinic.id == clinic_id).first()
    if not clinic:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Clinic not found"
        )
    
    employees = db.query(Employee).filter(
        Employee.primary_clinic_id == clinic_id
    ).offset(skip).limit(limit).all()
    
    return employees
