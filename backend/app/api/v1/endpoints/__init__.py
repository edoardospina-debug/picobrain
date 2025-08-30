"""API v1 endpoints"""

# Import all endpoint modules for easy access
from . import persons, clinics, clients, employees, auth, users

__all__ = ["persons", "clinics", "clients", "employees", "auth", "users"]
