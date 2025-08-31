#!/usr/bin/env python3
"""Test the employees API endpoint to see what data exists"""

import requests
import json
from datetime import datetime

# API configuration
BASE_URL = "http://localhost:8000/api/v1"

def get_token():
    """Get authentication token"""
    login_data = {
        "username": "admin@picobrain.com",
        "password": "admin123"
    }
    
    response = requests.post(
        f"{BASE_URL}/auth/login",
        data=login_data,  # Form data, not JSON
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    
    if response.status_code == 200:
        return response.json()["access_token"]
    else:
        print(f"Login failed: {response.status_code}")
        print(response.text)
        return None

def test_employees_endpoint():
    """Test the employees endpoint"""
    token = get_token()
    if not token:
        print("Failed to get auth token")
        return
    
    headers = {
        "Authorization": f"Bearer {token}"
    }
    
    print("\n" + "="*60)
    print("TESTING EMPLOYEES API")
    print("="*60)
    
    # Test 1: Get all employees
    print("\n1. GET /api/v1/employees (all employees)")
    print("-" * 40)
    response = requests.get(f"{BASE_URL}/employees", headers=headers)
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        employees = response.json()
        print(f"Total employees found: {len(employees)}")
        
        if employees:
            print("\nEmployee Details:")
            for emp in employees:
                print(f"\n  ID: {emp.get('id')}")
                print(f"  Code: {emp.get('employee_code')}")
                print(f"  Role: {emp.get('role')}")
                print(f"  Active: {emp.get('is_active')}")
                if emp.get('person'):
                    print(f"  Name: {emp['person'].get('first_name')} {emp['person'].get('last_name')}")
                if emp.get('clinic'):
                    print(f"  Clinic: {emp['clinic'].get('name')}")
        else:
            print("No employees found in database!")
    else:
        print(f"Error: {response.text}")
    
    # Test 2: Get employees by role
    print("\n2. Testing role-specific queries")
    print("-" * 40)
    for role in ['doctor', 'nurse', 'receptionist', 'manager']:
        response = requests.get(f"{BASE_URL}/employees?role={role}", headers=headers)
        if response.status_code == 200:
            count = len(response.json())
            print(f"  {role.capitalize()}s: {count}")
    
    # Test 3: Check persons table
    print("\n3. GET /api/v1/persons (checking persons table)")
    print("-" * 40)
    response = requests.get(f"{BASE_URL}/persons", headers=headers)
    if response.status_code == 200:
        persons = response.json()
        print(f"Total persons found: {len(persons)}")
        if persons:
            print("Sample persons:")
            for person in persons[:3]:
                print(f"  - {person.get('first_name')} {person.get('last_name')} (ID: {person.get('id')})")
    else:
        print(f"Error accessing persons: {response.status_code}")

if __name__ == "__main__":
    test_employees_endpoint()
