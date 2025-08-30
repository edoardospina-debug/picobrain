from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Any
from uuid import UUID

from app.api import deps
from app.models import Person, User
from app import schemas

router = APIRouter()

@router.get("/", response_model=List[schemas.PersonResponse])
def get_persons(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, le=100),
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
) -> Any:
    """Get all persons (requires authentication)"""
    persons = db.query(Person).offset(skip).limit(limit).all()
    return persons

@router.get("/{person_id}", response_model=schemas.PersonResponse)
def get_person(
    person_id: UUID, 
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
) -> Any:
    """Get person by ID (requires authentication)"""
    person = db.query(Person).filter(Person.id == person_id).first()
    if not person:
        raise HTTPException(status_code=404, detail="Person not found")
    return person

@router.post("/", response_model=schemas.PersonResponse)
def create_person(
    person: schemas.PersonCreate, 
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
) -> Any:
    """Create new person (requires authentication)"""
    # Check if email already exists
    if person.email:
        existing = db.query(Person).filter(Person.email == person.email).first()
        if existing:
            raise HTTPException(
                status_code=400, 
                detail="Email already registered"
            )
    
    db_person = Person(**person.dict())
    db.add(db_person)
    db.commit()
    db.refresh(db_person)
    return db_person

@router.put("/{person_id}", response_model=schemas.PersonResponse)
def update_person(
    person_id: UUID,
    person_update: schemas.PersonUpdate,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
) -> Any:
    """Update person (requires authentication)"""
    person = db.query(Person).filter(Person.id == person_id).first()
    if not person:
        raise HTTPException(status_code=404, detail="Person not found")
    
    update_data = person_update.dict(exclude_unset=True)
    
    # Check if email is being updated and already exists
    if "email" in update_data and update_data["email"]:
        existing = db.query(Person).filter(
            Person.email == update_data["email"],
            Person.id != person_id
        ).first()
        if existing:
            raise HTTPException(
                status_code=400, 
                detail="Email already registered"
            )
    
    for field, value in update_data.items():
        setattr(person, field, value)
    
    db.commit()
    db.refresh(person)
    return person

@router.delete("/{person_id}")
def delete_person(
    person_id: UUID, 
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_superuser)
) -> Any:
    """Delete person (admin only)"""
    person = db.query(Person).filter(Person.id == person_id).first()
    if not person:
        raise HTTPException(status_code=404, detail="Person not found")
    
    # Check if person has associated client, employee, or user records
    if person.client or person.employee or person.user:
        raise HTTPException(
            status_code=400,
            detail="Cannot delete person with associated records"
        )
    
    db.delete(person)
    db.commit()
    return {"message": "Person deleted successfully"}
