#!/usr/bin/env python3
"""
Test the employee API endpoint to verify it's returning data
"""
import requests
import json
from datetime import datetime

# API configuration
API_BASE = "http://localhost:8000/api/v1"
LOGIN_ENDPOINT = f"{API_BASE}/auth/login"
EMPLOYEES_ENDPOINT = f"{API_BASE}/employees"

def test_api():
    print("\n" + "="*50)
    print("🔍 TESTING EMPLOYEE API ENDPOINT")
    print("="*50)
    
    # Step 1: Login to get token
    print("\n1. Attempting login...")
    login_data = {
        "username": "admin@picobrain.com",
        "password": "admin123"
    }
    
    try:
        response = requests.post(LOGIN_ENDPOINT, data=login_data)
        if response.status_code == 200:
            auth_data = response.json()
            access_token = auth_data.get("access_token")
            print("   ✅ Login successful")
            print(f"   Token: {access_token[:20]}...")
        else:
            print(f"   ❌ Login failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return
    except Exception as e:
        print(f"   ❌ Connection error: {e}")
        print("   Make sure the backend is running on http://localhost:8000")
        return
    
    # Step 2: Test employees endpoint
    print("\n2. Testing /api/v1/employees endpoint...")
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    
    try:
        # Test with pagination parameters
        params = {
            "skip": 0,
            "limit": 10
        }
        
        response = requests.get(EMPLOYEES_ENDPOINT, headers=headers, params=params)
        
        print(f"   Status Code: {response.status_code}")
        
        if response.status_code == 200:
            employees = response.json()
            print(f"   ✅ Endpoint returned data")
            print(f"   Number of employees: {len(employees)}")
            
            if employees:
                print("\n   Sample data (first employee):")
                emp = employees[0]
                print(f"   - ID: {emp.get('id')}")
                print(f"   - Code: {emp.get('employee_code')}")
                print(f"   - Role: {emp.get('role')}")
                
                if emp.get('person'):
                    person = emp['person']
                    print(f"   - Name: {person.get('first_name')} {person.get('last_name')}")
                    print(f"   - Email: {person.get('email')}")
                else:
                    print("   ⚠️ Person data missing!")
                
                if emp.get('clinic'):
                    print(f"   - Clinic: {emp['clinic'].get('name')}")
                
                print(f"\n   JSON Structure (first employee):")
                print(json.dumps(emp, indent=2, default=str)[:500] + "...")
            else:
                print("   ⚠️ Empty array returned")
        else:
            print(f"   ❌ Request failed: {response.status_code}")
            print(f"   Response: {response.text}")
            
    except Exception as e:
        print(f"   ❌ Error calling API: {e}")
    
    # Step 3: Test CORS headers
    print("\n3. Checking CORS configuration...")
    try:
        response = requests.options(EMPLOYEES_ENDPOINT, headers={
            "Origin": "http://localhost:3000",
            "Access-Control-Request-Method": "GET",
            "Access-Control-Request-Headers": "authorization"
        })
        
        cors_headers = {
            "Access-Control-Allow-Origin": response.headers.get("Access-Control-Allow-Origin"),
            "Access-Control-Allow-Methods": response.headers.get("Access-Control-Allow-Methods"),
            "Access-Control-Allow-Headers": response.headers.get("Access-Control-Allow-Headers"),
            "Access-Control-Allow-Credentials": response.headers.get("Access-Control-Allow-Credentials")
        }
        
        print("   CORS Headers:")
        for header, value in cors_headers.items():
            if value:
                print(f"   - {header}: {value}")
            else:
                print(f"   - {header}: NOT SET ⚠️")
                
    except Exception as e:
        print(f"   ❌ Error checking CORS: {e}")
    
    print("\n" + "="*50)
    print("SUMMARY")
    print("="*50)
    print("\nIf the API returns data but the frontend doesn't show it:")
    print("1. Check browser console for errors")
    print("2. Verify CORS is properly configured")
    print("3. Check if token is being sent in requests")
    print("4. Verify the frontend is expecting the correct data format")

if __name__ == "__main__":
    test_api()
