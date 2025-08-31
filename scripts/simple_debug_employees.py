#!/usr/bin/env python3
"""
Simple diagnostic script to find where employees data is lost
Run with: python3 simple_debug_employees.py
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

def test_database_direct():
    """Test 1: Check if data exists in database"""
    print("\n" + "="*50)
    print("TEST 1: Database Direct Query")
    print("="*50)
    
    import psycopg2
    
    try:
        conn = psycopg2.connect(
            host="localhost",
            database="picobraindb",
            user="edo",
            port=5432
        )
        cursor = conn.cursor()
        
        # Count employees
        cursor.execute("SELECT COUNT(*) FROM employees")
        count = cursor.fetchone()[0]
        print(f"✅ Employees in DB: {count}")
        
        # Get sample
        cursor.execute("""
            SELECT e.id, e.employee_code, p.first_name, p.last_name 
            FROM employees e 
            JOIN persons p ON e.person_id = p.id 
            LIMIT 1
        """)
        
        sample = cursor.fetchone()
        if sample:
            print(f"✅ Sample: {sample[1]} - {sample[2]} {sample[3]}")
        
        cursor.close()
        conn.close()
        return count > 0
        
    except Exception as e:
        print(f"❌ Database error: {e}")
        return False

def test_sqlalchemy_models():
    """Test 2: Check SQLAlchemy can load data"""
    print("\n" + "="*50)
    print("TEST 2: SQLAlchemy Models")
    print("="*50)
    
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker, joinedload
    from app.models.core import Employee, Person
    
    try:
        engine = create_engine("postgresql://edo@localhost:5432/picobraindb")
        Session = sessionmaker(bind=engine)
        session = Session()
        
        # Count employees
        count = session.query(Employee).count()
        print(f"✅ SQLAlchemy count: {count}")
        
        # Get one with person
        employee = session.query(Employee).options(
            joinedload(Employee.person)
        ).first()
        
        if employee:
            print(f"✅ Employee found: {employee.employee_code}")
            if employee.person:
                print(f"✅ Person loaded: {employee.person.first_name} {employee.person.last_name}")
            else:
                print(f"❌ Person is None!")
                return False
        
        session.close()
        return True
        
    except Exception as e:
        print(f"❌ SQLAlchemy error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_schema_serialization():
    """Test 3: Check Pydantic serialization"""
    print("\n" + "="*50)
    print("TEST 3: Pydantic Serialization")
    print("="*50)
    
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker, joinedload
    from app.models.core import Employee
    from app.schemas.core import EmployeeResponse
    
    try:
        engine = create_engine("postgresql://edo@localhost:5432/picobraindb")
        Session = sessionmaker(bind=engine)
        session = Session()
        
        # Get employee with person
        employee = session.query(Employee).options(
            joinedload(Employee.person),
            joinedload(Employee.clinic)
        ).first()
        
        if not employee:
            print("❌ No employee to test!")
            return False
        
        print(f"Employee model: {employee.employee_code}")
        print(f"Person attached: {employee.person is not None}")
        
        # Try serialization
        try:
            response = EmployeeResponse.from_orm(employee)
            print(f"✅ Serialization successful")
            
            # Check if person data is included
            data = response.dict()
            print(f"Has person in dict: {'person' in data}")
            if 'person' in data and data['person']:
                print(f"✅ Person data included: {data['person'].get('first_name', 'NO NAME')}")
            else:
                print(f"❌ Person data missing in serialized response!")
                return False
                
        except Exception as e:
            print(f"❌ Serialization failed: {e}")
            return False
        
        session.close()
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_service_layer():
    """Test 4: Check service layer"""
    print("\n" + "="*50)
    print("TEST 4: Service Layer")
    print("="*50)
    
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker
    from app.services.employee import EmployeeService
    import asyncio
    
    try:
        engine = create_engine("postgresql://edo@localhost:5432/picobraindb")
        Session = sessionmaker(bind=engine)
        session = Session()
        
        service = EmployeeService(session)
        
        async def test():
            employees = await service.get_employees(skip=0, limit=5)
            print(f"Service returned: {len(employees)} employees")
            
            if employees:
                first = employees[0]
                print(f"✅ First employee: {first.employee_code}")
                
                # Check if person data is there
                if hasattr(first, 'person') and first.person:
                    print(f"✅ Person data: {first.person.first_name}")
                else:
                    # Try accessing directly
                    data = first.dict()
                    if 'person' in data:
                        print(f"Person in dict: {data['person']}")
                    else:
                        print("❌ No person data in response!")
                        return False
            else:
                print("❌ Empty list from service!")
                return False
            
            return True
        
        result = asyncio.run(test())
        session.close()
        return result
        
    except Exception as e:
        print(f"❌ Service error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_api_endpoint():
    """Test 5: Check API endpoint"""
    print("\n" + "="*50)
    print("TEST 5: API Endpoint")
    print("="*50)
    
    import requests
    
    try:
        # Login
        login_resp = requests.post(
            "http://localhost:8000/api/v1/auth/login",
            data={"username": "admin@picobrain.com", "password": "admin123"},
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )
        
        if login_resp.status_code != 200:
            print(f"❌ Login failed: {login_resp.status_code}")
            return False
        
        token = login_resp.json()["access_token"]
        
        # Get employees
        resp = requests.get(
            "http://localhost:8000/api/v1/employees",
            headers={"Authorization": f"Bearer {token}"},
            params={"skip": 0, "limit": 5}
        )
        
        print(f"API status: {resp.status_code}")
        
        if resp.status_code == 200:
            data = resp.json()
            print(f"API returned: {len(data)} items")
            
            if len(data) > 0:
                print(f"✅ Data received")
                first = data[0]
                if 'person' in first and first['person']:
                    print(f"✅ Person data included: {first['person'].get('first_name', 'NO NAME')}")
                else:
                    print(f"❌ No person data in API response!")
                    print(f"First item keys: {list(first.keys())}")
            else:
                print("❌ Empty array from API!")
                return False
        else:
            print(f"❌ API error: {resp.text}")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ API test error: {e}")
        return False

def main():
    """Run all tests sequentially"""
    print("\n🔍 EMPLOYEE DEBUG - SIMPLE VERSION")
    print("=" * 50)
    
    tests = [
        ("Database", test_database_direct),
        ("SQLAlchemy", test_sqlalchemy_models),
        ("Serialization", test_schema_serialization),
        ("Service", test_service_layer),
        ("API", test_api_endpoint)
    ]
    
    results = []
    for name, test_func in tests:
        try:
            success = test_func()
            results.append((name, success))
            if not success:
                print(f"\n⚠️ FAILED AT: {name}")
                break  # Stop at first failure
        except Exception as e:
            print(f"\n❌ Error in {name}: {e}")
            results.append((name, False))
            break
    
    # Summary
    print("\n" + "="*50)
    print("SUMMARY")
    print("="*50)
    
    for name, success in results:
        status = "✅" if success else "❌"
        print(f"{status} {name}")
    
    # Find the failure point
    for i, (name, success) in enumerate(results):
        if not success:
            print(f"\n🎯 ISSUE FOUND: Data is lost at the {name} layer")
            print(f"   Previous layer ({tests[i-1][0] if i > 0 else 'Start'}) was OK")
            print(f"   Check the {name} implementation")
            break

if __name__ == "__main__":
    main()
