"""Employee repository for database operations"""
from typing import Optional, List
from sqlalchemy.orm import Session, joinedload
from uuid import UUID
from app.models.core import Employee
from app.repositories.base import BaseRepository


class EmployeeRepository(BaseRepository[Employee]):
    """Repository for Employee entity operations"""
    
    def __init__(self, db: Session):
        """Initialize Employee repository"""
        super().__init__(Employee, db)
    
    def get_with_person(self, id: UUID) -> Optional[Employee]:
        """
        Get employee with person data eagerly loaded
        
        Args:
            id: Employee UUID
            
        Returns:
            Employee instance with person data or None if not found
        """
        return self.db.query(Employee).options(
            joinedload(Employee.person),
            joinedload(Employee.clinic)
        ).filter(Employee.id == id).first()
    
    def get_by_employee_code(self, employee_code: str) -> Optional[Employee]:
        """
        Get employee by employee code
        
        Args:
            employee_code: Employee code to search for
            
        Returns:
            Employee instance or None if not found
        """
        return self.db.query(Employee).filter(
            Employee.employee_code == employee_code
        ).first()
    
    def exists_by_employee_code(self, employee_code: str) -> bool:
        """
        Check if an employee with given code exists
        
        Args:
            employee_code: Employee code to check
            
        Returns:
            True if employee with code exists, False otherwise
        """
        return self.exists(employee_code=employee_code)
    
    def get_by_person_id(self, person_id: UUID) -> Optional[Employee]:
        """
        Get employee by person ID
        
        Args:
            person_id: Person UUID
            
        Returns:
            Employee instance or None if not found
        """
        return self.db.query(Employee).filter(
            Employee.person_id == person_id
        ).first()
    
    def exists_by_person_id(self, person_id: UUID) -> bool:
        """
        Check if a person is already an employee
        
        Args:
            person_id: Person UUID to check
            
        Returns:
            True if person is already an employee, False otherwise
        """
        return self.exists(person_id=person_id)
    
    def get_by_clinic(
        self, 
        clinic_id: UUID, 
        skip: int = 0, 
        limit: int = 100,
        is_active: Optional[bool] = None
    ) -> List[Employee]:
        """
        Get all employees for a specific clinic
        
        Args:
            clinic_id: Clinic UUID
            skip: Number of records to skip
            limit: Maximum number of records to return
            is_active: Filter by active status (optional)
            
        Returns:
            List of Employee instances
        """
        query = self.db.query(Employee).filter(
            Employee.primary_clinic_id == clinic_id
        )
        
        if is_active is not None:
            query = query.filter(Employee.is_active == is_active)
        
        return query.offset(skip).limit(limit).all()
    
    def get_by_role(
        self, 
        role: str, 
        clinic_id: Optional[UUID] = None,
        is_active: bool = True
    ) -> List[Employee]:
        """
        Get employees by role
        
        Args:
            role: Employee role (doctor, nurse, etc.)
            clinic_id: Optional clinic filter
            is_active: Filter by active status
            
        Returns:
            List of Employee instances
        """
        query = self.db.query(Employee).filter(
            Employee.role == role,
            Employee.is_active == is_active
        )
        
        if clinic_id:
            query = query.filter(Employee.primary_clinic_id == clinic_id)
        
        return query.all()
    
    def get_medical_staff(self, clinic_id: Optional[UUID] = None) -> List[Employee]:
        """
        Get employees who can perform treatments (medical staff)
        
        Args:
            clinic_id: Optional clinic filter
            
        Returns:
            List of Employee instances who can perform treatments
        """
        query = self.db.query(Employee).options(
            joinedload(Employee.person),
            joinedload(Employee.clinic)
        ).filter(
            Employee.can_perform_treatments == True,
            Employee.is_active == True
        )
        
        if clinic_id:
            query = query.filter(Employee.primary_clinic_id == clinic_id)
        
        return query.all()
    
    def get_all_with_person(
        self, 
        skip: int = 0, 
        limit: int = 100,
        filters: Optional[dict] = None
    ) -> List[Employee]:
        """
        Get all employees with person data eagerly loaded
        
        Args:
            skip: Number of records to skip
            limit: Maximum number of records to return
            filters: Optional filter dictionary
            
        Returns:
            List of Employee instances with person data
        """
        query = self.db.query(Employee).options(
            joinedload(Employee.person),
            joinedload(Employee.clinic)
        )
        
        if filters:
            for key, value in filters.items():
                if hasattr(Employee, key) and value is not None:
                    query = query.filter(getattr(Employee, key) == value)
        
        return query.offset(skip).limit(limit).all()
