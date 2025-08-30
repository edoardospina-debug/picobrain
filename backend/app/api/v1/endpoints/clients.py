from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from typing import List, Any, Optional
from uuid import UUID

from app.api import deps
from app.models import Client, User, Person, Clinic
from app import schemas

router = APIRouter()

@router.get("/", response_model=List[schemas.ClientResponse])
def get_clients(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, le=100),
    clinic_id: Optional[UUID] = None,
    is_active: Optional[bool] = None,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
) -> Any:
    """Get all clients with optional filters (requires authentication)"""
    query = db.query(Client)
    
    # Apply filters
    if clinic_id:
        query = query.filter(Client.preferred_clinic_id == clinic_id)
    if is_active is not None:
        query = query.filter(Client.is_active == is_active)
    
    clients = query.offset(skip).limit(limit).all()
    return clients

@router.get("/{client_id}", response_model=schemas.ClientResponse)
def get_client(
    client_id: UUID, 
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
) -> Any:
    """Get client by ID (requires authentication)"""
    client = db.query(Client).filter(Client.id == client_id).first()
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    return client

@router.post("/", response_model=schemas.ClientResponse)
def create_client(
    client: schemas.ClientCreate, 
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_superuser)
) -> Any:
    """Create new client (admin only)"""
    # Verify person exists
    person = db.query(Person).filter(Person.id == client.person_id).first()
    if not person:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Person not found"
        )
    
    # Verify clinic exists if provided
    if client.preferred_clinic_id:
        clinic = db.query(Clinic).filter(Clinic.id == client.preferred_clinic_id).first()
        if not clinic:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Clinic not found"
            )

    
    # Check if person is already a client
    existing = db.query(Client).filter(Client.person_id == client.person_id).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Person is already registered as a client"
        )
    
    # Check if client code is unique if provided
    if client.client_code:
        code_exists = db.query(Client).filter(Client.client_code == client.client_code).first()
        if code_exists:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Client code already exists"
            )
    
    db_client = Client(**client.dict())
    db.add(db_client)
    db.commit()
    db.refresh(db_client)
    return db_client

@router.put("/{client_id}", response_model=schemas.ClientResponse)
def update_client(
    client_id: UUID,
    client_update: schemas.ClientUpdate,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_superuser)
) -> Any:
    """Update client (admin only)"""
    client = db.query(Client).filter(Client.id == client_id).first()
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    
    # If updating clinic, verify it exists
    if client_update.preferred_clinic_id:
        clinic = db.query(Clinic).filter(Clinic.id == client_update.preferred_clinic_id).first()
        if not clinic:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Clinic not found"
            )
    
    # If updating client code, check uniqueness
    if client_update.client_code and client_update.client_code != client.client_code:
        code_exists = db.query(Client).filter(Client.client_code == client_update.client_code).first()
        if code_exists:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Client code already exists"
            )
    
    for field, value in client_update.dict(exclude_unset=True).items():
        setattr(client, field, value)
    
    db.commit()
    db.refresh(client)
    return client

@router.delete("/{client_id}")
def delete_client(
    client_id: UUID, 
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_superuser)
) -> Any:
    """Delete client (admin only)"""
    client = db.query(Client).filter(Client.id == client_id).first()
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    
    db.delete(client)
    db.commit()
    return {"message": "Client deleted successfully"}

@router.get("/person/{person_id}", response_model=Optional[schemas.ClientResponse])
def get_client_by_person(
    person_id: UUID,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
) -> Any:
    """Get client by person ID"""
    client = db.query(Client).filter(Client.person_id == person_id).first()
    return client

@router.get("/clinic/{clinic_id}", response_model=List[schemas.ClientResponse])
def get_clients_by_clinic(
    clinic_id: UUID,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, le=100),
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
) -> Any:
    """Get all clients for a specific clinic"""
    # Verify clinic exists
    clinic = db.query(Clinic).filter(Clinic.id == clinic_id).first()
    if not clinic:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Clinic not found"
        )
    
    clients = db.query(Client).filter(
        Client.preferred_clinic_id == clinic_id
    ).offset(skip).limit(limit).all()
    
    return clients
