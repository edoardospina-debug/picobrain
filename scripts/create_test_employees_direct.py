#!/usr/bin/env python3
"""
Quick script to create test employee data directly in the database
This bypasses the API and creates records directly
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
import uuid
from datetime import datetime, date

DATABASE_URL = "postgresql://edo@localhost:5432/picobraindb"

def create_test_employees():
    """Create test employees directly in database"""
    engine = create_engine(DATABASE_URL)
    Session = sessionmaker(bind=engine)
    session = Session()
    
    print("\n" + "="*60)
    print("CREATING TEST EMPLOYEES DIRECTLY IN DATABASE")
    print("="*60)
    
    try:
        # First, get a clinic ID
        result = session.execute(text("SELECT id FROM clinics LIMIT 1"))
        clinic = result.fetchone()
        
        if not clinic:
            print("No clinic found! Creating one...")
            clinic_id = str(uuid.uuid4())
            session.execute(text("""
                INSERT INTO clinics (id, code, name, functional_currency, city, country_code)
                VALUES (:id, 'NYC', 'New York Clinic', 'USD', 'New York', 'US')
            """), {"id": clinic_id})
            session.commit()
        else:
            clinic_id = str(clinic.id)
        
        print(f"Using clinic ID: {clinic_id}")
        
        # Create test employees with persons
        test_data = [
            {
                'first_name': 'Test', 'last_name': 'Doctor1', 
                'email': 'test.doctor1@clinic.com',
                'code': 'TD001', 'role': 'doctor', 
                'specialization': 'Cardiology'
            },
            {
                'first_name': 'Test', 'last_name': 'Nurse1',
                'email': 'test.nurse1@clinic.com',
                'code': 'TN001', 'role': 'nurse',
                'specialization': 'Emergency'
            },
            {
                'first_name': 'Test', 'last_name': 'Reception1',
                'email': 'test.reception1@clinic.com',
                'code': 'TR001', 'role': 'receptionist',
                'specialization': None
            }
        ]
        
        created_count = 0
        
        for data in test_data:
            # Check if person exists
            result = session.execute(
                text("SELECT id FROM persons WHERE email = :email"),
                {"email": data['email']}
            )
            person = result.fetchone()
            
            if not person:
                # Create person
                person_id = str(uuid.uuid4())
                session.execute(text("""
                    INSERT INTO persons (id, first_name, last_name, email, dob, gender)
                    VALUES (:id, :first_name, :last_name, :email, :dob, :gender)
                """), {
                    'id': person_id,
                    'first_name': data['first_name'],
                    'last_name': data['last_name'],
                    'email': data['email'],
                    'dob': date(1985, 1, 15),
                    'gender': 'M'
                })
                print(f"Created person: {data['first_name']} {data['last_name']}")
            else:
                person_id = str(person.id)
                print(f"Person already exists: {data['email']}")
            
            # Check if employee exists
            result = session.execute(
                text("SELECT id FROM employees WHERE person_id = :person_id"),
                {"person_id": person_id}
            )
            
            if not result.fetchone():
                # Create employee
                employee_id = str(uuid.uuid4())
                session.execute(text("""
                    INSERT INTO employees (
                        id, person_id, employee_code, primary_clinic_id,
                        role, specialization, hire_date, is_active,
                        can_perform_treatments
                    ) VALUES (
                        :id, :person_id, :code, :clinic_id,
                        :role, :specialization, :hire_date, :is_active,
                        :can_treat
                    )
                """), {
                    'id': employee_id,
                    'person_id': person_id,
                    'code': data['code'],
                    'clinic_id': clinic_id,
                    'role': data['role'],
                    'specialization': data['specialization'],
                    'hire_date': date.today(),
                    'is_active': True,
                    'can_treat': data['role'] in ['doctor', 'nurse']
                })
                created_count += 1
                print(f"✅ Created employee: {data['code']} ({data['role']})")
            else:
                print(f"Employee already exists for person: {data['email']}")
        
        session.commit()
        print(f"\n✅ Created {created_count} new employees")
        
        # Verify
        result = session.execute(text("""
            SELECT COUNT(*) FROM employees e
            JOIN persons p ON e.person_id = p.id
            JOIN clinics c ON e.primary_clinic_id = c.id
        """))
        total = result.scalar()
        print(f"Total employees with complete relationships: {total}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        session.rollback()
    finally:
        session.close()

if __name__ == "__main__":
    create_test_employees()
