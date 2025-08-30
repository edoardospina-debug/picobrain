from fastapi import APIRouter
from app.api.v1.endpoints import persons, clinics, auth, users, clients, employees

api_router = APIRouter()

# Public endpoints (no auth required)
api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])

# Protected endpoints
api_router.include_router(persons.router, prefix="/persons", tags=["persons"])
api_router.include_router(clinics.router, prefix="/clinics", tags=["clinics"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(clients.router, prefix="/clients", tags=["clients"])
api_router.include_router(employees.router, prefix="/employees", tags=["employees"])
