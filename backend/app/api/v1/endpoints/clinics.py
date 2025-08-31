from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Any
from uuid import UUID

from app.api import deps
from app.models import Clinic, User
from app import schemas

router = APIRouter()

@router.get("/", response_model=List[schemas.ClinicResponse])
def get_clinics(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, le=100),
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
) -> Any:
    """Get all clinics (requires authentication)"""
    clinics = db.query(Clinic).offset(skip).limit(limit).all()
    return clinics

@router.get("/{clinic_id}", response_model=schemas.ClinicResponse)
def get_clinic(
    clinic_id: UUID, 
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
) -> Any:
    """Get clinic by ID (requires authentication)"""
    clinic = db.query(Clinic).filter(Clinic.id == clinic_id).first()
    if not clinic:
        raise HTTPException(status_code=404, detail="Clinic not found")
    return clinic

@router.post("/", response_model=schemas.ClinicResponse)
def create_clinic(
    clinic: schemas.ClinicCreate, 
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_superuser)
) -> Any:
    """
    Create new clinic (admin only)
    
    Now supports:
    - Full address fields (address_line_1, address_line_2, city, state_province, postal_code, country_code)
    - Split phone fields (phone_country_code, phone_number)
    - Email and tax_id
    """
    # Check if clinic code already exists
    existing = db.query(Clinic).filter(Clinic.code == clinic.code).first()
    if existing:
        raise HTTPException(
            status_code=400, 
            detail="Clinic code already exists"
        )
    
    # Validate phone number pair - if one part is provided, both should be provided
    if (clinic.phone_country_code and not clinic.phone_number) or \
       (clinic.phone_number and not clinic.phone_country_code):
        raise HTTPException(
            status_code=400,
            detail="Both country code and number must be provided for clinic phone"
        )
    
    # Validate email if provided
    if clinic.email:
        # Check if email is already used by another clinic
        existing_email = db.query(Clinic).filter(
            Clinic.email == clinic.email
        ).first()
        if existing_email:
            raise HTTPException(
                status_code=400,
                detail="Email already used by another clinic"
            )
    
    db_clinic = Clinic(**clinic.dict())
    db.add(db_clinic)
    db.commit()
    db.refresh(db_clinic)
    return db_clinic

@router.put("/{clinic_id}", response_model=schemas.ClinicResponse)
def update_clinic(
    clinic_id: UUID,
    clinic_update: schemas.ClinicUpdate,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_superuser)
) -> Any:
    """
    Update clinic (admin only)
    
    Now supports:
    - Full address fields (address_line_1, address_line_2, city, state_province, postal_code, country_code)
    - Split phone fields (phone_country_code, phone_number)
    - Email and tax_id
    """
    clinic = db.query(Clinic).filter(Clinic.id == clinic_id).first()
    if not clinic:
        raise HTTPException(status_code=404, detail="Clinic not found")
    
    update_data = clinic_update.dict(exclude_unset=True)
    
    # Validate phone number pair if being updated
    phone_country_update = "phone_country_code" in update_data
    phone_number_update = "phone_number" in update_data
    
    if phone_country_update or phone_number_update:
        # Get current values
        current_country = clinic.phone_country_code
        current_number = clinic.phone_number
        
        # Determine new values
        new_country = update_data.get("phone_country_code", current_country)
        new_number = update_data.get("phone_number", current_number)
        
        # Validate pair consistency
        if (new_country and not new_number) or \
           (new_number and not new_country):
            raise HTTPException(
                status_code=400,
                detail="Both country code and number must be provided for clinic phone"
            )
    
    # Check if email is being updated and already exists
    if "email" in update_data and update_data["email"]:
        existing_email = db.query(Clinic).filter(
            Clinic.email == update_data["email"],
            Clinic.id != clinic_id
        ).first()
        if existing_email:
            raise HTTPException(
                status_code=400,
                detail="Email already used by another clinic"
            )
    
    for field, value in update_data.items():
        setattr(clinic, field, value)
    
    db.commit()
    db.refresh(clinic)
    return clinic

@router.delete("/{clinic_id}")
def delete_clinic(
    clinic_id: UUID, 
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_superuser)
) -> Any:
    """Delete clinic (admin only)"""
    clinic = db.query(Clinic).filter(Clinic.id == clinic_id).first()
    if not clinic:
        raise HTTPException(status_code=404, detail="Clinic not found")
    
    # Check if clinic has associated employees or clients
    if clinic.employees or clinic.clients:
        raise HTTPException(
            status_code=400,
            detail="Cannot delete clinic with associated records"
        )
    
    db.delete(clinic)
    db.commit()
    return {"message": "Clinic deleted successfully"}

# Utility endpoints for clinic information
@router.get("/{clinic_id}/formatted-address")
def get_formatted_address(
    clinic_id: UUID,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
) -> Any:
    """
    Get clinic's full formatted address
    """
    clinic = db.query(Clinic).filter(Clinic.id == clinic_id).first()
    if not clinic:
        raise HTTPException(status_code=404, detail="Clinic not found")
    
    address_parts = []
    
    if clinic.address_line_1:
        address_parts.append(clinic.address_line_1)
    if clinic.address_line_2:
        address_parts.append(clinic.address_line_2)
    if clinic.city:
        address_parts.append(clinic.city)
    if clinic.state_province:
        address_parts.append(clinic.state_province)
    if clinic.postal_code:
        address_parts.append(clinic.postal_code)
    if clinic.country_code:
        address_parts.append(clinic.country_code)
    
    formatted_phone = None
    if clinic.phone_country_code and clinic.phone_number:
        formatted_phone = f"{clinic.phone_country_code} {clinic.phone_number}"
    
    return {
        "address": ", ".join(address_parts) if address_parts else None,
        "phone": formatted_phone,
        "email": clinic.email
    }

@router.get("/{clinic_id}/contact-info")
def get_contact_info(
    clinic_id: UUID,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
) -> Any:
    """
    Get clinic's contact information
    """
    clinic = db.query(Clinic).filter(Clinic.id == clinic_id).first()
    if not clinic:
        raise HTTPException(status_code=404, detail="Clinic not found")
    
    return {
        "phone": {
            "country_code": clinic.phone_country_code,
            "number": clinic.phone_number,
            "formatted": f"{clinic.phone_country_code} {clinic.phone_number}" 
                        if clinic.phone_country_code and clinic.phone_number else None
        },
        "email": clinic.email,
        "address": {
            "line_1": clinic.address_line_1,
            "line_2": clinic.address_line_2,
            "city": clinic.city,
            "state_province": clinic.state_province,
            "postal_code": clinic.postal_code,
            "country_code": clinic.country_code
        }
    }
