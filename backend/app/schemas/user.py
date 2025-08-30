from typing import Optional
from uuid import UUID
from pydantic import BaseModel
from .core import PersonResponse

class UserBase(BaseModel):
    username: str
    role: str = "user"
    is_active: bool = True
    person_id: Optional[UUID] = None

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    username: Optional[str] = None
    password: Optional[str] = None
    role: Optional[str] = None
    is_active: Optional[bool] = None
    person_id: Optional[UUID] = None

class UserInDB(UserBase):
    id: UUID
    password_hash: str
    
    class Config:
        from_attributes = True

class User(UserBase):
    id: UUID
    
    class Config:
        from_attributes = True

class UserWithPerson(User):
    person: Optional[PersonResponse] = None
