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
    """Create new clinic (admin only)"""
    # Check if clinic code already exists
    existing = db.query(Clinic).filter(Clinic.code == clinic.code).first()
    if existing:
        raise HTTPException(
            status_code=400, 
            detail="Clinic code already exists"
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
    """Update clinic (admin only)"""
    clinic = db.query(Clinic).filter(Clinic.id == clinic_id).first()
    if not clinic:
        raise HTTPException(status_code=404, detail="Clinic not found")
    
    for field, value in clinic_update.dict(exclude_unset=True).items():
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
