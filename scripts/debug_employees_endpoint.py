#!/usr/bin/env python3
"""Debug the employees endpoint to see exact response"""

import requests
import json

BASE_URL = "http://localhost:8000/api/v1"

# Get token
login_response = requests.post(
    f"{BASE_URL}/auth/login",
    data={"username": "admin@picobrain.com", "password": "admin123"},
    headers={"Content-Type": "application/x-www-form-urlencoded"}
)

if login_response.status_code != 200:
    print("Login failed!")
    exit(1)

token = login_response.json()["access_token"]
headers = {"Authorization": f"Bearer {token}"}

print("Testing /api/v1/employees endpoint...")
print("="*60)

# Test the exact URL that the frontend uses
response = requests.get(
    f"{BASE_URL}/employees",
    params={"skip": 0, "limit": 20},
    headers=headers
)

print(f"Status Code: {response.status_code}")
print(f"Response Headers: {dict(response.headers)}")
print("\nRaw Response Text (first 500 chars):")
print(response.text[:500])

if response.status_code == 200:
    data = response.json()
    print(f"\nResponse Type: {type(data)}")
    print(f"Is Array: {isinstance(data, list)}")
    
    if isinstance(data, list):
        print(f"Array Length: {len(data)}")
        if len(data) > 0:
            print("\nFirst Employee:")
            print(json.dumps(data[0], indent=2, default=str))
    else:
        print("Response is not an array!")
        print(json.dumps(data, indent=2, default=str))
