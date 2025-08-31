"""Schemas package for PicoBrain API"""

# Import from core schemas
from .core import (
    PersonBase, PersonCreate, PersonUpdate, PersonResponse,
    ClinicBase, ClinicCreate, ClinicUpdate, ClinicResponse,
    ClientBase, ClientCreate, ClientUpdate, ClientResponse,
    EmployeeBase, EmployeeCreate, EmployeeUpdate, EmployeeResponse,
    GenderType, EmployeeRole, UserRole,
    PhoneNumber, PhoneNumberUpdate
)

# Import from user schemas
from .user import (
    User, UserCreate, UserUpdate, UserInDB, UserWithPerson
)

# Import from token schemas
from .token import (
    Token, TokenPayload, TokenRefresh, PasswordReset
)

# Create aliases for backward compatibility
Person = PersonResponse
PersonInDB = PersonResponse
Clinic = ClinicResponse
Client = ClientResponse
Employee = EmployeeResponse

__all__ = [
    # Person schemas
    "Person", "PersonBase", "PersonCreate", "PersonUpdate", "PersonResponse", "PersonInDB",
    # Clinic schemas
    "Clinic", "ClinicBase", "ClinicCreate", "ClinicUpdate", "ClinicResponse",
    # Client schemas
    "Client", "ClientBase", "ClientCreate", "ClientUpdate", "ClientResponse",
    # Employee schemas
    "Employee", "EmployeeBase", "EmployeeCreate", "EmployeeUpdate", "EmployeeResponse",
    # User schemas
    "User", "UserCreate", "UserUpdate", "UserInDB", "UserWithPerson",
    # Token schemas
    "Token", "TokenPayload", "TokenRefresh", "PasswordReset",
    # Enums
    "GenderType", "EmployeeRole", "UserRole",
    # Utility schemas
    "PhoneNumber", "PhoneNumberUpdate"
]
