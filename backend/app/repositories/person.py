"""Person repository for database operations"""
from typing import Optional, List
from sqlalchemy.orm import Session
from uuid import UUID
from app.models.core import Person
from app.repositories.base import BaseRepository


class PersonRepository(BaseRepository[Person]):
    """Repository for Person entity operations"""
    
    def __init__(self, db: Session):
        """Initialize Person repository"""
        super().__init__(Person, db)
    
    def get_by_email(self, email: str) -> Optional[Person]:
        """
        Get person by email address
        
        Args:
            email: Email address to search for
            
        Returns:
            Person instance or None if not found
        """
        return self.db.query(Person).filter(Person.email == email).first()
    
    def exists_by_email(self, email: str) -> bool:
        """
        Check if a person with given email exists
        
        Args:
            email: Email address to check
            
        Returns:
            True if person with email exists, False otherwise
        """
        return self.exists(email=email)
    
    def get_by_phone(self, country_code: str, number: str, phone_type: str = "mobile") -> Optional[Person]:
        """
        Get person by phone number
        
        Args:
            country_code: Phone country code
            number: Phone number
            phone_type: Type of phone ('mobile' or 'home')
            
        Returns:
            Person instance or None if not found
        """
        if phone_type == "mobile":
            return self.db.query(Person).filter(
                Person.phone_mobile_country_code == country_code,
                Person.phone_mobile_number == number
            ).first()
        else:
            return self.db.query(Person).filter(
                Person.phone_home_country_code == country_code,
                Person.phone_home_number == number
            ).first()
    
    def search_by_name(self, first_name: Optional[str] = None, last_name: Optional[str] = None) -> List[Person]:
        """
        Search persons by name (partial match)
        
        Args:
            first_name: First name to search (partial match)
            last_name: Last name to search (partial match)
            
        Returns:
            List of matching Person instances
        """
        query = self.db.query(Person)
        
        if first_name:
            query = query.filter(Person.first_name.ilike(f"%{first_name}%"))
        if last_name:
            query = query.filter(Person.last_name.ilike(f"%{last_name}%"))
        
        return query.all()
    
    def get_persons_without_employee(self) -> List[Person]:
        """
        Get all persons who are not employees
        
        Returns:
            List of Person instances without associated Employee records
        """
        return self.db.query(Person).filter(Person.employee == None).all()
    
    def get_persons_without_client(self) -> List[Person]:
        """
        Get all persons who are not clients
        
        Returns:
            List of Person instances without associated Client records
        """
        return self.db.query(Person).filter(Person.client == None).all()
