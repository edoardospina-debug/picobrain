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
    """
    Create new person (requires authentication)
    
    Now supports split phone fields:
    - phone_mobile_country_code: Country code (e.g., '+1', '+44')
    - phone_mobile_number: National number portion
    - phone_home_country_code: Country code for home phone
    - phone_home_number: Home phone number
    """
    # Check if email already exists
    if person.email:
        existing = db.query(Person).filter(Person.email == person.email).first()
        if existing:
            raise HTTPException(
                status_code=400, 
                detail="Email already registered"
            )
    
    # Validate phone number pairs - if one part is provided, both should be provided
    if (person.phone_mobile_country_code and not person.phone_mobile_number) or \
       (person.phone_mobile_number and not person.phone_mobile_country_code):
        raise HTTPException(
            status_code=400,
            detail="Both country code and number must be provided for mobile phone"
        )
    
    if (person.phone_home_country_code and not person.phone_home_number) or \
       (person.phone_home_number and not person.phone_home_country_code):
        raise HTTPException(
            status_code=400,
            detail="Both country code and number must be provided for home phone"
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
    """
    Update person (requires authentication)
    
    Now supports split phone fields:
    - phone_mobile_country_code: Country code (e.g., '+1', '+44')
    - phone_mobile_number: National number portion
    - phone_home_country_code: Country code for home phone
    - phone_home_number: Home phone number
    """
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
    
    # Validate phone number pairs for mobile
    mobile_country_update = "phone_mobile_country_code" in update_data
    mobile_number_update = "phone_mobile_number" in update_data
    
    if mobile_country_update or mobile_number_update:
        # Get current values
        current_mobile_country = person.phone_mobile_country_code
        current_mobile_number = person.phone_mobile_number
        
        # Determine new values
        new_mobile_country = update_data.get("phone_mobile_country_code", current_mobile_country)
        new_mobile_number = update_data.get("phone_mobile_number", current_mobile_number)
        
        # Validate pair consistency
        if (new_mobile_country and not new_mobile_number) or \
           (new_mobile_number and not new_mobile_country):
            raise HTTPException(
                status_code=400,
                detail="Both country code and number must be provided for mobile phone"
            )
    
    # Validate phone number pairs for home
    home_country_update = "phone_home_country_code" in update_data
    home_number_update = "phone_home_number" in update_data
    
    if home_country_update or home_number_update:
        # Get current values
        current_home_country = person.phone_home_country_code
        current_home_number = person.phone_home_number
        
        # Determine new values
        new_home_country = update_data.get("phone_home_country_code", current_home_country)
        new_home_number = update_data.get("phone_home_number", current_home_number)
        
        # Validate pair consistency
        if (new_home_country and not new_home_number) or \
           (new_home_number and not new_home_country):
            raise HTTPException(
                status_code=400,
                detail="Both country code and number must be provided for home phone"
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

# Utility endpoints for phone number formatting
@router.post("/validate-phone", response_model=schemas.PhoneNumber)
def validate_phone_number(
    phone: schemas.PhoneNumber,
    current_user: User = Depends(deps.get_current_user)
) -> Any:
    """
    Validate a phone number format
    Returns the validated phone number with proper formatting
    """
    # Here you could add additional validation logic
    # such as checking if the country code is valid
    # or if the number length is appropriate for the country
    return phone

@router.get("/{person_id}/formatted-phones")
def get_formatted_phone_numbers(
    person_id: UUID,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
) -> Any:
    """
    Get person's phone numbers in formatted display format
    """
    person = db.query(Person).filter(Person.id == person_id).first()
    if not person:
        raise HTTPException(status_code=404, detail="Person not found")
    
    result = {}
    
    if person.phone_mobile_country_code and person.phone_mobile_number:
        result["mobile"] = f"{person.phone_mobile_country_code} {person.phone_mobile_number}"
    
    if person.phone_home_country_code and person.phone_home_number:
        result["home"] = f"{person.phone_home_country_code} {person.phone_home_number}"
    
    return result
