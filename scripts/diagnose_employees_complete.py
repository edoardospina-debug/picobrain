#!/usr/bin/env python3
"""
Comprehensive diagnostic script for Employees page data issue
Run this to check all aspects of the employees data flow
"""

import requests
import json
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

BASE_URL = "http://localhost:8000/api/v1"
DATABASE_URL = "postgresql://edo@localhost:5432/picobraindb"

def check_database():
    """Check database directly"""
    print("\n" + "="*60)
    print("1. DATABASE CHECK")
    print("="*60)
    
    engine = create_engine(DATABASE_URL)
    Session = sessionmaker(bind=engine)
    session = Session()
    
    try:
        # Check employees count
        result = session.execute(text("SELECT COUNT(*) FROM employees"))
        emp_count = result.scalar()
        print(f"Total employees in database: {emp_count}")
        
        # Get sample with joins
        result = session.execute(text("""
            SELECT 
                e.id,
                e.employee_code,
                e.role,
                e.is_active,
                e.person_id,
                e.primary_clinic_id,
                p.first_name,
                p.last_name,
                p.email,
                c.name as clinic_name
            FROM employees e
            LEFT JOIN persons p ON e.person_id = p.id
            LEFT JOIN clinics c ON e.primary_clinic_id = c.id
            LIMIT 5
        """))
        
        employees = result.fetchall()
        if employees:
            print("\nSample employees with relationships:")
            for emp in employees:
                print(f"  - {emp.employee_code}: {emp.first_name} {emp.last_name}")
                print(f"    Role: {emp.role}, Clinic: {emp.clinic_name}")
                print(f"    Person ID: {emp.person_id}, Clinic ID: {emp.primary_clinic_id}")
        else:
            print("No employees found in database!")
            
    except Exception as e:
        print(f"Database error: {e}")
    finally:
        session.close()

def check_backend_api():
    """Test backend API endpoint"""
    print("\n" + "="*60)
    print("2. BACKEND API CHECK")
    print("="*60)
    
    # Login first
    login_response = requests.post(
        f"{BASE_URL}/auth/login",
        data={"username": "admin@picobrain.com", "password": "admin123"},
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    
    if login_response.status_code != 200:
        print(f"❌ Login failed: {login_response.status_code}")
        return
    
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    print(f"✅ Logged in successfully")
    
    # Test employees endpoint
    print("\nTesting /api/v1/employees endpoint...")
    response = requests.get(f"{BASE_URL}/employees", headers=headers)
    
    print(f"Response status: {response.status_code}")
    print(f"Response headers: Content-Type: {response.headers.get('content-type')}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"Response type: {type(data)}")
        print(f"Is array: {isinstance(data, list)}")
        print(f"Array length: {len(data) if isinstance(data, list) else 'N/A'}")
        
        if isinstance(data, list) and len(data) > 0:
            print("\nFirst employee structure:")
            print(json.dumps(data[0], indent=2, default=str))
        elif isinstance(data, list):
            print("\n⚠️ Empty array returned!")
        else:
            print(f"\n❌ Unexpected response type: {data}")
    else:
        print(f"❌ Error: {response.text}")
    
    # Test with query params
    print("\nTesting with query params (skip=0, limit=20)...")
    response2 = requests.get(
        f"{BASE_URL}/employees",
        params={"skip": 0, "limit": 20},
        headers=headers
    )
    
    if response2.status_code == 200:
        data2 = response2.json()
        print(f"With params - Array length: {len(data2) if isinstance(data2, list) else 'N/A'}")

def check_frontend_transform():
    """Simulate frontend transform"""
    print("\n" + "="*60)
    print("3. FRONTEND TRANSFORM SIMULATION")
    print("="*60)
    
    # Get token and test
    login_response = requests.post(
        f"{BASE_URL}/auth/login",
        data={"username": "admin@picobrain.com", "password": "admin123"},
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    
    if login_response.status_code == 200:
        token = login_response.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
        
        response = requests.get(
            f"{BASE_URL}/employees",
            params={"skip": 0, "limit": 20},
            headers=headers
        )
        
        if response.status_code == 200:
            data = response.json()
            
            # Simulate frontend transform
            transformed = {
                "items": data if isinstance(data, list) else [],
                "total": len(data) if isinstance(data, list) else 0
            }
            
            print(f"Backend returns: {type(data)}")
            print(f"After transform:")
            print(f"  items: {len(transformed['items'])} employees")
            print(f"  total: {transformed['total']}")
            
            if transformed['total'] == 0:
                print("\n⚠️ Transform results in empty items array!")

def run_full_diagnostic():
    """Run all checks"""
    print("\n" + "🔍"*30)
    print("EMPLOYEES PAGE DIAGNOSTIC")
    print("🔍"*30)
    
    # Check if servers are running
    print("\nChecking server status...")
    try:
        backend_health = requests.get("http://localhost:8000/health", timeout=2)
        print("✅ Backend is running")
    except:
        print("❌ Backend not responding - run: ./start-servers.sh")
        return
    
    try:
        frontend = requests.get("http://localhost:3000", timeout=2)
        print("✅ Frontend is running")
    except:
        print("❌ Frontend not responding - run: ./start-servers.sh")
        return
    
    # Run all checks
    check_database()
    check_backend_api()
    check_frontend_transform()
    
    # Summary
    print("\n" + "="*60)
    print("DIAGNOSTIC SUMMARY")
    print("="*60)
    print("""
Next steps to debug:
1. Check backend logs in the terminal running the server
2. Add logging to /backend/app/services/employee.py
3. Check if Employee model relationships are properly defined
4. Verify that EmployeeResponse schema includes all fields
5. Test with a fresh database connection
    """)

if __name__ == "__main__":
    run_full_diagnostic()
