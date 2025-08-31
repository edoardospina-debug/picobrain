#!/usr/bin/env python3
"""Verify and fix employees data in the database"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
import json
from datetime import datetime

# Database connection
DATABASE_URL = "postgresql://edo@localhost:5432/picobraindb"
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)

def check_and_fix_employees():
    session = Session()
    
    print("\n" + "="*60)
    print("DATABASE EMPLOYEES CHECK")
    print("="*60)
    
    try:
        # Check persons table
        persons_result = session.execute(text("SELECT COUNT(*) FROM persons"))
        person_count = persons_result.scalar()
        print(f"\n1. Persons table: {person_count} records")
        
        # Check employees table
        employees_result = session.execute(text("SELECT COUNT(*) FROM employees"))
        employee_count = employees_result.scalar()
        print(f"2. Employees table: {employee_count} records")
        
        # Check if employees have person_id links
        orphan_result = session.execute(text("""
            SELECT COUNT(*) FROM employees 
            WHERE person_id IS NULL
        """))
        orphan_count = orphan_result.scalar()
        print(f"3. Employees without person_id: {orphan_count}")
        
        # Get sample employees with details
        print("\n4. Sample employees with joins:")
        sample_result = session.execute(text("""
            SELECT 
                e.id,
                e.employee_code,
                e.role,
                e.is_active,
                p.first_name,
                p.last_name,
                c.name as clinic_name
            FROM employees e
            LEFT JOIN persons p ON e.person_id = p.id
            LEFT JOIN clinics c ON e.primary_clinic_id = c.id
            LIMIT 5
        """))
        
        employees = sample_result.fetchall()
        if employees:
            for emp in employees:
                print(f"   - {emp.employee_code}: {emp.first_name} {emp.last_name} ({emp.role}) at {emp.clinic_name}")
        else:
            print("   No employees found!")
            
        # If no employees, check if we need to create them
        if employee_count == 0:
            print("\n❌ No employees in database!")
            print("Creating sample employees...")
            
            # Get first clinic
            clinic_result = session.execute(text("SELECT id FROM clinics LIMIT 1"))
            clinic = clinic_result.fetchone()
            
            if not clinic:
                print("   ❌ No clinics found! Creating one...")
                session.execute(text("""
                    INSERT INTO clinics (code, name, functional_currency, city, country_code)
                    VALUES ('NYC', 'New York Clinic', 'USD', 'New York', 'US')
                    ON CONFLICT (code) DO NOTHING
                """))
                session.commit()
                clinic_result = session.execute(text("SELECT id FROM clinics WHERE code = 'NYC'"))
                clinic = clinic_result.fetchone()
            
            clinic_id = clinic.id
            print(f"   Using clinic ID: {clinic_id}")
            
            # Create sample employees with persons
            sample_employees = [
                {
                    'first_name': 'John', 'last_name': 'Smith', 'email': 'john.smith@clinic.com',
                    'code': 'DR001', 'role': 'doctor', 'specialization': 'Cardiology'
                },
                {
                    'first_name': 'Sarah', 'last_name': 'Johnson', 'email': 'sarah.johnson@clinic.com',
                    'code': 'DR002', 'role': 'doctor', 'specialization': 'Dermatology'
                },
                {
                    'first_name': 'Emily', 'last_name': 'Davis', 'email': 'emily.davis@clinic.com',
                    'code': 'NR001', 'role': 'nurse', 'specialization': 'Emergency Care'
                },
                {
                    'first_name': 'Michael', 'last_name': 'Brown', 'email': 'michael.brown@clinic.com',
                    'code': 'NR002', 'role': 'nurse', 'specialization': 'Pediatric'
                },
                {
                    'first_name': 'Jessica', 'last_name': 'Wilson', 'email': 'jessica.wilson@clinic.com',
                    'code': 'RC001', 'role': 'receptionist', 'specialization': None
                }
            ]
            
            for emp_data in sample_employees:
                # Create person first
                result = session.execute(text("""
                    INSERT INTO persons (first_name, last_name, email, dob, gender)
                    VALUES (:first_name, :last_name, :email, '1985-01-15', 'M')
                    RETURNING id
                """), {
                    'first_name': emp_data['first_name'],
                    'last_name': emp_data['last_name'],
                    'email': emp_data['email']
                })
                person_id = result.scalar()
                
                # Create employee
                session.execute(text("""
                    INSERT INTO employees (
                        person_id, employee_code, primary_clinic_id, role,
                        specialization, hire_date, is_active, can_perform_treatments
                    ) VALUES (
                        :person_id, :code, :clinic_id, :role,
                        :specialization, CURRENT_DATE, true, :can_treat
                    )
                """), {
                    'person_id': person_id,
                    'code': emp_data['code'],
                    'clinic_id': clinic_id,
                    'role': emp_data['role'],
                    'specialization': emp_data['specialization'],
                    'can_treat': emp_data['role'] in ['doctor', 'nurse']
                })
                
                print(f"   ✅ Created: {emp_data['code']} - {emp_data['first_name']} {emp_data['last_name']}")
            
            session.commit()
            print("\n✅ Sample employees created successfully!")
            
        else:
            print(f"\n✅ Database has {employee_count} employees")
            
    except Exception as e:
        print(f"\n❌ Error: {e}")
        session.rollback()
    finally:
        session.close()
    
    print("\n" + "="*60)
    print("CHECK COMPLETE")
    print("="*60)

if __name__ == "__main__":
    check_and_fix_employees()
