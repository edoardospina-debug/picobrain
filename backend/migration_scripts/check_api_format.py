#!/usr/bin/env python3
"""
Quick test to see the exact format of the clinics API response
"""

import requests
import json

# Login
login_response = requests.post(
    "http://localhost:8000/api/v1/auth/login",
    data={"username": "admin", "password": "admin123"}
)

if login_response.status_code == 200:
    token = login_response.json()["access_token"]
    
    # Get clinics
    headers = {"Authorization": f"Bearer {token}"}
    clinics_response = requests.get(
        "http://localhost:8000/api/v1/clinics",
        headers=headers
    )
    
    print("Status Code:", clinics_response.status_code)
    print("\nResponse Type:", type(clinics_response.json()))
    print("\nResponse Content:")
    response_data = clinics_response.json()
    
    if isinstance(response_data, list):
        print(f"  - It's a LIST with {len(response_data)} items")
        if response_data:
            print(f"  - First item keys: {list(response_data[0].keys())}")
    elif isinstance(response_data, dict):
        print(f"  - It's a DICT with keys: {list(response_data.keys())}")
    
    print("\nFull response (first 500 chars):")
    print(json.dumps(response_data, indent=2)[:500])
else:
    print("Login failed")
