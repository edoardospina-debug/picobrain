#!/usr/bin/env python3
"""Complete diagnostic of the employees data flow"""

import requests
import json
import subprocess
import time

BASE_URL = "http://localhost:8000/api/v1"

def run_diagnostic():
    print("\n" + "="*60)
    print("EMPLOYEES DATA FLOW DIAGNOSTIC")
    print("="*60)
    
    # Step 1: Check backend health
    print("\n1. Checking backend health...")
    try:
        response = requests.get("http://localhost:8000/health")
        print(f"   ✅ Backend is running (status: {response.status_code})")
    except:
        print("   ❌ Backend is not responding!")
        print("   Run: ./start-servers.sh")
        return
    
    # Step 2: Login and get token
    print("\n2. Getting authentication token...")
    login_response = requests.post(
        f"{BASE_URL}/auth/login",
        data={"username": "admin@picobrain.com", "password": "admin123"},
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    
    if login_response.status_code != 200:
        print(f"   ❌ Login failed: {login_response.status_code}")
        print(f"   Response: {login_response.text}")
        return
    
    token = login_response.json()["access_token"]
    print(f"   ✅ Token obtained: {token[:20]}...")
    
    # Step 3: Check employees endpoint
    print("\n3. Testing /api/v1/employees endpoint...")
    headers = {"Authorization": f"Bearer {token}"}
    
    emp_response = requests.get(f"{BASE_URL}/employees", headers=headers)
    print(f"   Status: {emp_response.status_code}")
    
    if emp_response.status_code == 200:
        employees = emp_response.json()
        print(f"   ✅ Response is valid JSON")
        print(f"   Data type: {type(employees)}")
        print(f"   Is array: {isinstance(employees, list)}")
        
        if isinstance(employees, list):
            print(f"   Total employees: {len(employees)}")
            
            if len(employees) > 0:
                print("\n   Sample employees:")
                for i, emp in enumerate(employees[:3]):
                    if emp.get('person'):
                        name = f"{emp['person'].get('first_name', '')} {emp['person'].get('last_name', '')}"
                    else:
                        name = "No person data"
                    print(f"     {i+1}. {emp.get('employee_code', 'N/A')} - {name} ({emp.get('role', 'N/A')})")
            else:
                print("   ⚠️  No employees in database!")
                print("   Run: python3 create_sample_employees.py")
        else:
            print(f"   ❌ Response is not an array!")
            print(f"   Response: {json.dumps(employees, indent=2)}")
    else:
        print(f"   ❌ Failed to get employees: {emp_response.status_code}")
        print(f"   Response: {emp_response.text}")
    
    # Step 4: Check with query parameters (as frontend does)
    print("\n4. Testing with frontend parameters...")
    params = {"skip": 0, "limit": 20}
    emp_response2 = requests.get(f"{BASE_URL}/employees", params=params, headers=headers)
    
    if emp_response2.status_code == 200:
        employees2 = emp_response2.json()
        print(f"   ✅ With params: {len(employees2) if isinstance(employees2, list) else 'not array'} employees")
    else:
        print(f"   ❌ Failed with params: {emp_response2.status_code}")
    
    # Step 5: Check frontend
    print("\n5. Checking frontend...")
    try:
        response = requests.get("http://localhost:3000")
        print(f"   ✅ Frontend is running (status: {response.status_code})")
    except:
        print("   ❌ Frontend is not responding!")
        print("   Run: cd frontend && npm run dev")
        return
    
    # Step 6: Summary
    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)
    
    if emp_response.status_code == 200 and isinstance(employees, list):
        if len(employees) > 0:
            print("✅ Backend has employee data")
            print(f"   Total: {len(employees)} employees")
            print("\n📋 NEXT STEPS:")
            print("1. Clear browser cache: Cmd+Shift+R")
            print("2. Check browser console for errors")
            print("3. Verify localStorage has token:")
            print("   - Open DevTools Console")
            print("   - Type: localStorage.getItem('picobrain_access_token')")
            print("4. Check Network tab for /employees request")
        else:
            print("⚠️  Backend has no employee data")
            print("\n📋 FIX:")
            print("Run: python3 create_sample_employees.py")
    else:
        print("❌ Backend API issue detected")
        print("Check backend logs: Check the terminal running start-servers.sh")
    
    print("\n✅ Diagnostic complete")

if __name__ == "__main__":
    run_diagnostic()
