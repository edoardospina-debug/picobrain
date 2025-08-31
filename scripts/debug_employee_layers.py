#!/usr/bin/env python3
"""
Debug script for Employee data loading issue
This script checks each layer of the data flow to identify where the data is lost
"""

import sys
import os
import json
import logging
from datetime import datetime

# Add backend to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

# Setup logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Database connection
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, Session

DATABASE_URL = "postgresql://edo@localhost:5432/picobraindb"

def debug_layer_1_database():
    """Check database directly with raw SQL"""
    print("\n" + "="*60)
    print("LAYER 1: DATABASE CHECK (Raw SQL)")
    print("="*60)
    
    engine = create_engine(DATABASE_URL, echo=True)
    
    with engine.connect() as conn:
        # Check employees count
        result = conn.execute(text("SELECT COUNT(*) FROM employees"))
        count = result.scalar()
        print(f"\n✅ Total employees in database: {count}")
        
        # Get sample employees
        result = conn.execute(text("""
            SELECT e.id, e.employee_code, e.role, e.is_active, 
                   e.person_id, e.primary_clinic_id,
                   p.first_name, p.last_name, p.email
            FROM employees e
            LEFT JOIN persons p ON e.person_id = p.id
            LIMIT 3
        """))
        
        employees = result.fetchall()
        if employees:
            print("\n✅ Sample employees found:")
            for emp in employees:
                print(f"  - ID: {emp[0]}")
                print(f"    Code: {emp[1]}, Name: {emp[6]} {emp[7]}")
                print(f"    Person ID: {emp[4]}, Active: {emp[3]}")
        else:
            print("❌ No employees found in database!")
            return False
    
    return True

def debug_layer_2_repository():
    """Test repository layer directly"""
    print("\n" + "="*60)
    print("LAYER 2: REPOSITORY CHECK")
    print("="*60)
    
    from app.models.core import Employee
    from app.repositories.employee import EmployeeRepository
    
    engine = create_engine(DATABASE_URL)
    SessionLocal = sessionmaker(bind=engine)
    db = SessionLocal()
    
    try:
        repo = EmployeeRepository(db)
        
        # Test basic get_all
        print("\nTesting repo.get_all()...")
        all_employees = repo.get_all()
        print(f"  Result type: {type(all_employees)}")
        print(f"  Count: {len(all_employees)}")
        
        if all_employees:
            first = all_employees[0]
            print(f"  First employee type: {type(first)}")
            print(f"  First employee ID: {first.id}")
            print(f"  Has person? {hasattr(first, 'person')}")
            if hasattr(first, 'person') and first.person:
                print(f"  Person loaded? {first.person is not None}")
        
        # Test get_all_with_person
        print("\nTesting repo.get_all_with_person()...")
        employees_with_person = repo.get_all_with_person(skip=0, limit=10)
        print(f"  Result type: {type(employees_with_person)}")
        print(f"  Count: {len(employees_with_person)}")
        
        if employees_with_person:
            first = employees_with_person[0]
            print(f"  First employee ID: {first.id}")
            print(f"  First employee code: {first.employee_code}")
            
            # Check if person is loaded
            if hasattr(first, 'person'):
                if first.person:
                    print(f"  ✅ Person loaded: {first.person.first_name} {first.person.last_name}")
                else:
                    print(f"  ❌ Person is None!")
            else:
                print(f"  ❌ No person attribute!")
        else:
            print("  ❌ Empty result from get_all_with_person!")
            
    except Exception as e:
        print(f"❌ Repository error: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        db.close()
    
    return True

def debug_layer_3_service():
    """Test service layer"""
    print("\n" + "="*60)
    print("LAYER 3: SERVICE CHECK")
    print("="*60)
    
    from app.services.employee import EmployeeService
    from app.schemas.core import EmployeeResponse
    
    engine = create_engine(DATABASE_URL)
    SessionLocal = sessionmaker(bind=engine)
    db = SessionLocal()
    
    try:
        service = EmployeeService(db)
        
        # Use asyncio to call async method
        import asyncio
        
        async def test_service():
            print("\nTesting service.get_employees()...")
            employees = await service.get_employees(skip=0, limit=10)
            print(f"  Result type: {type(employees)}")
            print(f"  Count: {len(employees)}")
            
            if employees:
                first = employees[0]
                print(f"  First item type: {type(first)}")
                if isinstance(first, EmployeeResponse):
                    print(f"  ✅ First employee ID: {first.id}")
                    print(f"  Employee code: {first.employee_code}")
                    
                    # Check serialized fields
                    print(f"\n  Checking serialized data:")
                    print(f"    - Has first_name? {hasattr(first, 'first_name')}")
                    print(f"    - Has last_name? {hasattr(first, 'last_name')}")
                    print(f"    - Has email? {hasattr(first, 'email')}")
                    
                    if hasattr(first, 'first_name'):
                        print(f"    - first_name value: {first.first_name}")
                    
                    # Try to convert to dict
                    try:
                        emp_dict = first.dict()
                        print(f"\n  ✅ Converted to dict successfully")
                        print(f"  Dict keys: {list(emp_dict.keys())[:5]}...")  # Show first 5 keys
                    except Exception as e:
                        print(f"  ❌ Failed to convert to dict: {e}")
            else:
                print("  ❌ Empty result from service!")
            
            return employees
        
        # Run async function
        employees = asyncio.run(test_service())
        
    except Exception as e:
        print(f"❌ Service error: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        db.close()
    
    return True

def debug_layer_4_schema():
    """Test schema serialization"""
    print("\n" + "="*60)
    print("LAYER 4: SCHEMA/SERIALIZATION CHECK")
    print("="*60)
    
    from app.models.core import Employee, Person
    from app.schemas.core import EmployeeResponse
    
    engine = create_engine(DATABASE_URL)
    SessionLocal = sessionmaker(bind=engine)
    db = SessionLocal()
    
    try:
        # Get a real employee from DB
        employee = db.query(Employee).first()
        
        if employee:
            print(f"Found employee: {employee.id}")
            print(f"  Employee code: {employee.employee_code}")
            print(f"  Has person_id? {employee.person_id}")
            
            # Check if person is loaded
            if hasattr(employee, 'person'):
                print(f"  Has person attribute: Yes")
                if employee.person:
                    print(f"  Person loaded: {employee.person.first_name} {employee.person.last_name}")
                else:
                    print(f"  Person is None - trying to load manually...")
                    # Manually load person
                    person = db.query(Person).filter(Person.id == employee.person_id).first()
                    if person:
                        print(f"  ✅ Manual load successful: {person.first_name} {person.last_name}")
                        employee.person = person
                    else:
                        print(f"  ❌ Person not found with ID: {employee.person_id}")
            
            # Try serialization
            print("\nTrying EmployeeResponse.from_orm()...")
            try:
                response = EmployeeResponse.from_orm(employee)
                print(f"  ✅ Serialization successful!")
                print(f"  Response type: {type(response)}")
                
                # Check serialized data
                response_dict = response.dict()
                print(f"  Dict keys count: {len(response_dict.keys())}")
                print(f"  Has first_name? {'first_name' in response_dict}")
                if 'first_name' in response_dict:
                    print(f"  first_name value: {response_dict['first_name']}")
                
            except Exception as e:
                print(f"  ❌ Serialization failed: {e}")
                import traceback
                traceback.print_exc()
        else:
            print("❌ No employees in database!")
            
    except Exception as e:
        print(f"❌ Schema check error: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        db.close()
    
    return True

def debug_layer_5_api_endpoint():
    """Test the actual API endpoint"""
    print("\n" + "="*60)
    print("LAYER 5: API ENDPOINT CHECK")
    print("="*60)
    
    import requests
    
    # Login first
    print("\nLogging in...")
    login_response = requests.post(
        "http://localhost:8000/api/v1/auth/login",
        data={"username": "admin@picobrain.com", "password": "admin123"},
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    
    if login_response.status_code != 200:
        print(f"❌ Login failed: {login_response.status_code}")
        print(f"Response: {login_response.text}")
        return False
    
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    print("✅ Login successful")
    
    # Test endpoint
    print("\nTesting GET /api/v1/employees...")
    response = requests.get(
        "http://localhost:8000/api/v1/employees",
        params={"skip": 0, "limit": 10},
        headers=headers
    )
    
    print(f"Response status: {response.status_code}")
    print(f"Response headers: {dict(response.headers)}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"\nResponse type: {type(data)}")
        print(f"Is list? {isinstance(data, list)}")
        
        if isinstance(data, list):
            print(f"List length: {len(data)}")
            
            if len(data) > 0:
                print("\n✅ Data received!")
                print(f"First employee: {json.dumps(data[0], indent=2, default=str)[:500]}...")
            else:
                print("\n❌ Empty array returned!")
        else:
            print(f"Unexpected response type: {data}")
    else:
        print(f"❌ API error: {response.text}")
    
    return True

def main():
    """Run all debug checks"""
    print("\n" + "🔍"*30)
    print("EMPLOYEE DATA LOADING DEBUGGER")
    print("🔍"*30)
    print(f"\nStarted at: {datetime.now()}")
    
    # Check each layer
    layers = [
        ("Database", debug_layer_1_database),
        ("Repository", debug_layer_2_repository),
        ("Service", debug_layer_3_service),
        ("Schema", debug_layer_4_schema),
        ("API Endpoint", debug_layer_5_api_endpoint)
    ]
    
    results = []
    for name, func in layers:
        try:
            success = func()
            results.append((name, success))
            if not success:
                print(f"\n⚠️ Issue found in {name} layer!")
                # Continue to check other layers anyway
        except Exception as e:
            print(f"\n❌ Critical error in {name}: {e}")
            results.append((name, False))
    
    # Summary
    print("\n" + "="*60)
    print("DIAGNOSTIC SUMMARY")
    print("="*60)
    
    for name, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{name:15} : {status}")
    
    print("\n" + "="*60)
    print("RECOMMENDED ACTIONS")
    print("="*60)
    
    # Analyze results and provide recommendations
    if not results[0][1]:  # Database
        print("1. Check database connection and data")
    elif not results[1][1]:  # Repository
        print("1. Check SQLAlchemy relationships and eager loading")
        print("2. Verify Employee.person relationship configuration")
    elif not results[2][1]:  # Service
        print("1. Check async/await handling in service layer")
        print("2. Verify list comprehension in get_employees method")
    elif not results[3][1]:  # Schema
        print("1. Check EmployeeResponse schema definition")
        print("2. Verify from_orm configuration and field mapping")
        print("3. Check if all required fields are present in the model")
    elif not results[4][1]:  # API
        print("1. Check FastAPI dependency injection")
        print("2. Verify response_model configuration")
    else:
        print("All layers appear functional - check for edge cases")
    
    print(f"\nCompleted at: {datetime.now()}")

if __name__ == "__main__":
    main()
