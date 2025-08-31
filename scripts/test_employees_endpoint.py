#!/usr/bin/env python3
"""Test the actual employees API endpoint response"""

import requests
import json

BASE_URL = "http://localhost:8000/api/v1"

# Login
print("Logging in...")
login_response = requests.post(
    f"{BASE_URL}/auth/login",
    data={"username": "admin@picobrain.com", "password": "admin123"},
    headers={"Content-Type": "application/x-www-form-urlencoded"}
)

if login_response.status_code != 200:
    print(f"Login failed: {login_response.status_code}")
    exit(1)

token = login_response.json()["access_token"]
headers = {"Authorization": f"Bearer {token}"}

print("\nTesting /api/v1/employees endpoint...")
print("="*60)

# Test the endpoint
response = requests.get(f"{BASE_URL}/employees", headers=headers)

print(f"Status Code: {response.status_code}")

if response.status_code == 200:
    data = response.json()
    print(f"Response type: {type(data)}")
    print(f"Is list: {isinstance(data, list)}")
    
    if isinstance(data, list):
        print(f"Number of employees: {len(data)}")
        
        if len(data) > 0:
            print("\nFirst employee (full structure):")
            print(json.dumps(data[0], indent=2, default=str))
            
            print("\n\nAll employees summary:")
            for i, emp in enumerate(data, 1):
                person = emp.get('person', {})
                name = f"{person.get('first_name', 'Unknown')} {person.get('last_name', '')}"
                print(f"{i}. {emp.get('employee_code', 'N/A')} - {name} ({emp.get('role', 'N/A')})")
        else:
            print("\n❌ Empty list returned!")
    else:
        print(f"\n❌ Unexpected response type: {type(data)}")
        print(json.dumps(data, indent=2, default=str))
else:
    print(f"Error: {response.text}")

# Also test with query params
print("\n\nTesting with query params (skip=0, limit=20)...")
response2 = requests.get(
    f"{BASE_URL}/employees",
    params={"skip": 0, "limit": 20},
    headers=headers
)

if response2.status_code == 200:
    data2 = response2.json()
    print(f"With params - Number of employees: {len(data2) if isinstance(data2, list) else 'N/A'}")
