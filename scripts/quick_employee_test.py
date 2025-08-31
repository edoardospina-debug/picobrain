#!/usr/bin/env python3
"""
Quick test to see where employee data is lost
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, joinedload
from app.models.core import Employee
from app.schemas.core import EmployeeResponse

DATABASE_URL = "postgresql://edo@localhost:5432/picobraindb"

def main():
    print("\n🔍 QUICK EMPLOYEE DATA TEST\n")
    
    # Create session
    engine = create_engine(DATABASE_URL)
    Session = sessionmaker(bind=engine)
    session = Session()
    
    try:
        # 1. Get employee without eager loading
        print("1. Testing WITHOUT eager loading:")
        emp = session.query(Employee).first()
        if emp:
            print(f"   Employee: {emp.employee_code}")
            print(f"   Person ID: {emp.person_id}")
            print(f"   Person loaded? {emp.person is not None}")
            if emp.person:
                print(f"   Person name: {emp.person.first_name}")
        print()
        
        # 2. Get employee WITH eager loading
        print("2. Testing WITH eager loading:")
        emp2 = session.query(Employee).options(
            joinedload(Employee.person),
            joinedload(Employee.clinic)
        ).first()
        if emp2:
            print(f"   Employee: {emp2.employee_code}")
            print(f"   Person loaded? {emp2.person is not None}")
            if emp2.person:
                print(f"   Person name: {emp2.person.first_name}")
        print()
        
        # 3. Test serialization without person
        print("3. Testing serialization WITHOUT person:")
        emp3 = session.query(Employee).first()
        try:
            resp = EmployeeResponse.from_orm(emp3)
            data = resp.dict()
            print(f"   Serialized successfully")
            print(f"   Has 'person' key? {'person' in data}")
            print(f"   Person value: {data.get('person')}")
        except Exception as e:
            print(f"   ❌ Serialization failed: {e}")
        print()
        
        # 4. Test serialization WITH person
        print("4. Testing serialization WITH person:")
        emp4 = session.query(Employee).options(
            joinedload(Employee.person)
        ).first()
        try:
            resp = EmployeeResponse.from_orm(emp4)
            data = resp.dict()
            print(f"   Serialized successfully")
            print(f"   Has 'person' key? {'person' in data}")
            if data.get('person'):
                print(f"   Person name from dict: {data['person'].get('first_name')}")
            else:
                print(f"   Person value: {data.get('person')}")
        except Exception as e:
            print(f"   ❌ Serialization failed: {e}")
        
    finally:
        session.close()
    
    print("\n" + "="*50)
    print("DIAGNOSIS:")
    print("If person is None without joinedload, the issue is lazy loading.")
    print("If serialization fails even with person loaded, check the schema.")
    print("="*50)

if __name__ == "__main__":
    main()
