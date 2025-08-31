"""Custom exceptions for the application"""
from typing import List, Optional, Any


class BaseApplicationException(Exception):
    """Base exception for all application exceptions"""
    
    def __init__(self, message: str, code: str = None, details: Any = None):
        self.message = message
        self.code = code
        self.details = details
        super().__init__(self.message)


class ValidationException(BaseApplicationException):
    """Exception raised for validation errors"""
    
    def __init__(self, errors: List[str]):
        self.errors = errors
        super().__init__(
            message="Validation failed",
            code="VALIDATION_ERROR",
            details={"errors": errors}
        )


class DuplicateResourceException(BaseApplicationException):
    """Exception raised when trying to create a duplicate resource"""
    
    def __init__(self, resource: str, field: str, value: Any):
        super().__init__(
            message=f"{resource} with {field}='{value}' already exists",
            code="DUPLICATE_RESOURCE",
            details={"resource": resource, "field": field, "value": value}
        )


class ResourceNotFoundException(BaseApplicationException):
    """Exception raised when a resource is not found"""
    
    def __init__(self, resource: str, id: Any):
        super().__init__(
            message=f"{resource} with id='{id}' not found",
            code="RESOURCE_NOT_FOUND",
            details={"resource": resource, "id": str(id)}
        )


class EmployeeCreationException(BaseApplicationException):
    """Exception raised during employee creation process"""
    
    def __init__(self, step: str, original_error: Exception):
        self.step = step
        self.original_error = original_error
        super().__init__(
            message=f"Employee creation failed at step: {step}",
            code="EMPLOYEE_CREATION_ERROR",
            details={"step": step, "error": str(original_error)}
        )


class PersonAlreadyEmployeeException(BaseApplicationException):
    """Exception raised when person is already an employee"""
    
    def __init__(self, person_id: str):
        super().__init__(
            message=f"Person with id='{person_id}' is already registered as an employee",
            code="PERSON_ALREADY_EMPLOYEE",
            details={"person_id": person_id}
        )


class DatabaseTransactionException(BaseApplicationException):
    """Exception raised for database transaction errors"""
    
    def __init__(self, operation: str, original_error: Exception):
        super().__init__(
            message=f"Database transaction failed during: {operation}",
            code="DATABASE_TRANSACTION_ERROR",
            details={"operation": operation, "error": str(original_error)}
        )


class UnauthorizedException(BaseApplicationException):
    """Exception raised for unauthorized access"""
    
    def __init__(self, message: str = "Unauthorized access"):
        super().__init__(
            message=message,
            code="UNAUTHORIZED",
            details=None
        )


class ForbiddenException(BaseApplicationException):
    """Exception raised for forbidden access"""
    
    def __init__(self, message: str = "Access forbidden"):
        super().__init__(
            message=message,
            code="FORBIDDEN",
            details=None
        )