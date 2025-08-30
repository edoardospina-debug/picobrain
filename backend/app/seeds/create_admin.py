#!/usr/bin/env python3
"""Create initial admin user for PicoBrain system"""

import sys
import os
from pathlib import Path

# Add the backend directory to Python path
backend_dir = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(backend_dir))

from app.db.session import SessionLocal
from app.models.user import User
from app.models.person import Person
from app.core.security import get_password_hash
import uuid

def create_admin_user():
    """Create the initial admin user if it doesn't exist"""
    db = SessionLocal()
    
    try:
        # Check if admin exists
        admin = db.query(User).filter(User.username == "admin@picobrain.com").first()
        if admin:
            print("✓ Admin user already exists")
            return
        
        # Create person for admin
        admin_person = Person(
            id=uuid.uuid4(),
            first_name="System",
            last_name="Administrator",
            email="admin@picobrain.com",
            phone_mobile="+1234567890"
        )
        db.add(admin_person)
        db.flush()  # Get the ID without committing
        
        # Create admin user
        admin_user = User(
            id=uuid.uuid4(),
            username="admin@picobrain.com",
            password_hash=get_password_hash("admin123"),  # Change this!
            role="admin",
            person_id=admin_person.id,
            is_active=True
        )
        db.add(admin_user)
        db.commit()
        
        print("=" * 50)
        print("✓ Admin user created successfully!")
        print("=" * 50)
        print(f"Username: admin@picobrain.com")
        print(f"Password: admin123")
        print("=" * 50)
        print("⚠️  IMPORTANT: Change this password immediately!")
        print("=" * 50)
        
    except Exception as e:
        print(f"✗ Error creating admin user: {e}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    create_admin_user()
