"""Base repository with common database operations"""
from typing import Type, TypeVar, Generic, List, Optional, Any, Dict
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from uuid import UUID
from app.database import Base

ModelType = TypeVar("ModelType", bound=Base)


class BaseRepository(Generic[ModelType]):
    """Base repository providing common CRUD operations"""
    
    def __init__(self, model: Type[ModelType], db: Session):
        """
        Initialize repository with model and database session
        
        Args:
            model: SQLAlchemy model class
            db: Database session
        """
        self.model = model
        self.db = db
    
    def get(self, id: UUID) -> Optional[ModelType]:
        """
        Get a single record by ID
        
        Args:
            id: Record UUID
            
        Returns:
            Model instance or None if not found
        """
        return self.db.query(self.model).filter(self.model.id == id).first()
    
    def get_all(
        self, 
        skip: int = 0, 
        limit: int = 100,
        filters: Optional[Dict[str, Any]] = None
    ) -> List[ModelType]:
        """
        Get all records with optional pagination and filters
        
        Args:
            skip: Number of records to skip
            limit: Maximum number of records to return
            filters: Dictionary of filter conditions
            
        Returns:
            List of model instances
        """
        query = self.db.query(self.model)
        
        if filters:
            for key, value in filters.items():
                if hasattr(self.model, key) and value is not None:
                    query = query.filter(getattr(self.model, key) == value)
        
        return query.offset(skip).limit(limit).all()
    
    def create(self, obj_data: Dict[str, Any]) -> ModelType:
        """
        Create a new record
        
        Args:
            obj_data: Dictionary containing model field values
            
        Returns:
            Created model instance
            
        Raises:
            IntegrityError: If database constraints are violated
        """
        db_obj = self.model(**obj_data)
        self.db.add(db_obj)
        self.db.flush()  # Flush to get ID without committing
        return db_obj
    
    def update(self, id: UUID, obj_data: Dict[str, Any]) -> Optional[ModelType]:
        """
        Update an existing record
        
        Args:
            id: Record UUID
            obj_data: Dictionary containing fields to update
            
        Returns:
            Updated model instance or None if not found
        """
        db_obj = self.get(id)
        if db_obj:
            for key, value in obj_data.items():
                if hasattr(db_obj, key):
                    setattr(db_obj, key, value)
            self.db.flush()
        return db_obj
    
    def delete(self, id: UUID) -> bool:
        """
        Delete a record by ID
        
        Args:
            id: Record UUID
            
        Returns:
            True if deleted, False if not found
        """
        db_obj = self.get(id)
        if db_obj:
            self.db.delete(db_obj)
            self.db.flush()
            return True
        return False
    
    def exists(self, **kwargs) -> bool:
        """
        Check if a record exists with given criteria
        
        Args:
            **kwargs: Field=value pairs to check
            
        Returns:
            True if record exists, False otherwise
        """
        query = self.db.query(self.model)
        for key, value in kwargs.items():
            if hasattr(self.model, key):
                query = query.filter(getattr(self.model, key) == value)
        return query.first() is not None
    
    def commit(self):
        """Commit the current transaction"""
        self.db.commit()
    
    def rollback(self):
        """Rollback the current transaction"""
        self.db.rollback()
    
    def refresh(self, obj: ModelType):
        """Refresh an object from the database"""
        self.db.refresh(obj)
