"""Repository layer for data access"""
from app.repositories.person import PersonRepository
from app.repositories.employee import EmployeeRepository

__all__ = ["PersonRepository", "EmployeeRepository"]
