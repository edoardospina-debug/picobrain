#!/usr/bin/env python3
"""
Create all demo users and test login
"""

import sys
import os
from pathlib import Path

# Add the backend directory to Python path
backend_dir = Path(__file__).resolve().parent / "backend"
sys.path.insert(0, str(backend_dir))

from app.db.session import SessionLocal
from app.models.user import User
from app.models.person import Person
from app.core.security import get_password_hash
import uuid
import requests

print("=" * 60)
print("CREATING/CHECKING DEMO USERS")
print("=" * 60)

db = SessionLocal()

demo_users = [
    {
        "username": "admin@picobrain.com",
        "password": "admin123",
        "role": "admin",
        "first_name": "System",
        "last_name": "Administrator"
    },
    {
        "username": "manager@picobrain.com", 
        "password": "manager123",
        "role": "manager",
        "first_name": "John",
        "last_name": "Manager"
    },
    {
        "username": "staff@picobrain.com",
        "password": "staff123", 
        "role": "staff",
        "first_name": "Jane",
        "last_name": "Staff"
    }
]

try:
    for user_data in demo_users:
        # Check if user exists
        existing_user = db.query(User).filter(User.username == user_data["username"]).first()
        
        if existing_user:
            print(f"✓ User already exists: {user_data['username']}")
        else:
            # Create person
            person = Person(
                id=uuid.uuid4(),
                first_name=user_data["first_name"],
                last_name=user_data["last_name"],
                email=user_data["username"],
                phone_mobile="+1234567890"
            )
            db.add(person)
            db.flush()
            
            # Create user
            user = User(
                id=uuid.uuid4(),
                username=user_data["username"],
                email=user_data["username"],
                full_name=f"{user_data['first_name']} {user_data['last_name']}",
                password_hash=get_password_hash(user_data["password"]),
                role=user_data["role"],
                person_id=person.id,
                is_active=True
            )
            db.add(user)
            print(f"✅ Created user: {user_data['username']}")
    
    db.commit()
    print("\n✅ All demo users ready!")
    
except Exception as e:
    print(f"❌ Error: {e}")
    db.rollback()
finally:
    db.close()

# Test login for each user
print("\n" + "=" * 60)
print("TESTING LOGIN FOR EACH USER")
print("=" * 60 + "\n")

for user_data in demo_users:
    login_data = {
        'username': user_data["username"],
        'password': user_data["password"]
    }
    
    try:
        response = requests.post(
            'http://localhost:8000/api/v1/auth/login',
            data=login_data,
            headers={'Content-Type': 'application/x-www-form-urlencoded'},
            timeout=2
        )
        
        if response.status_code == 200:
            print(f"✅ LOGIN SUCCESS: {user_data['username']} / {user_data['password']}")
        else:
            print(f"❌ LOGIN FAILED: {user_data['username']} - Status {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error testing login: {e}")

print("\n" + "=" * 60)
print("DEMO CREDENTIALS TO USE:")
print("=" * 60)
for user_data in demo_users:
    print(f"Username: {user_data['username']}")
    print(f"Password: {user_data['password']}")
    print(f"Role: {user_data['role']}")
    print("-" * 30)
