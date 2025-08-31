#!/usr/bin/env python3
"""Create sample employees for testing the Employees page"""

import requests
import json
from datetime import datetime, timedelta
import random

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
        data=login_data,
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    
    if response.status_code == 200:
        return response.json()["access_token"]
    else:
        print(f"Login failed: {response.status_code}")
        return None

def get_first_clinic_id(token):
    """Get the ID of the first clinic"""
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/clinics", headers=headers)
    
    if response.status_code == 200:
        clinics = response.json()
        if clinics:
            return clinics[0]["id"]
    return None

def create_sample_employees():
    """Create sample employees of different types"""
    token = get_token()
    if not token:
        print("Failed to get auth token")
        return
    
    clinic_id = get_first_clinic_id(token)
    if not clinic_id:
        print("No clinic found. Please create a clinic first.")
        return
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    print("\n" + "="*60)
    print("CREATING SAMPLE EMPLOYEES")
    print("="*60)
    
    # Sample employee data
    employees = [
        {
            # Doctor 1
            "first_name": "John",
            "last_name": "Smith",
            "email": "john.smith@picobrain.com",
            "phone_mobile_country_code": "+1",
            "phone_mobile_number": "5551234567",
            "dob": "1985-03-15",
            "gender": "M",
            "nationality": "US",
            "employee_code": "DR001",
            "primary_clinic_id": clinic_id,
            "role": "doctor",
            "specialization": "Cardiology",
            "license_number": "MD-12345",
            "license_expiry": "2026-12-31",
            "hire_date": "2020-01-15",
            "base_salary_minor": 15000000,  # $150,000
            "salary_currency": "USD",
            "commission_rate": 10,
            "is_active": True,
            "can_perform_treatments": True
        },
        {
            # Doctor 2
            "first_name": "Sarah",
            "last_name": "Johnson",
            "email": "sarah.johnson@picobrain.com",
            "phone_mobile_country_code": "+1",
            "phone_mobile_number": "5551234568",
            "dob": "1982-07-22",
            "gender": "F",
            "nationality": "US",
            "employee_code": "DR002",
            "primary_clinic_id": clinic_id,
            "role": "doctor",
            "specialization": "Dermatology",
            "license_number": "MD-67890",
            "license_expiry": "2025-06-30",
            "hire_date": "2019-03-01",
            "base_salary_minor": 17500000,  # $175,000
            "salary_currency": "USD",
            "commission_rate": 12,
            "is_active": True,
            "can_perform_treatments": True
        },
        {
            # Nurse 1
            "first_name": "Emily",
            "last_name": "Davis",
            "email": "emily.davis@picobrain.com",
            "phone_mobile_country_code": "+1",
            "phone_mobile_number": "5551234569",
            "dob": "1990-11-10",
            "gender": "F",
            "nationality": "US",
            "employee_code": "NR001",
            "primary_clinic_id": clinic_id,
            "role": "nurse",
            "specialization": "Emergency Care",
            "license_number": "RN-11111",
            "license_expiry": "2025-12-31",
            "hire_date": "2021-06-01",
            "base_salary_minor": 7500000,  # $75,000
            "salary_currency": "USD",
            "commission_rate": 5,
            "is_active": True,
            "can_perform_treatments": True
        },
        {
            # Nurse 2
            "first_name": "Michael",
            "last_name": "Brown",
            "email": "michael.brown@picobrain.com",
            "phone_mobile_country_code": "+1",
            "phone_mobile_number": "5551234570",
            "dob": "1988-04-25",
            "gender": "M",
            "nationality": "US",
            "employee_code": "NR002",
            "primary_clinic_id": clinic_id,
            "role": "nurse",
            "specialization": "Pediatric Nursing",
            "license_number": "RN-22222",
            "license_expiry": "2024-09-30",
            "hire_date": "2020-09-15",
            "base_salary_minor": 8000000,  # $80,000
            "salary_currency": "USD",
            "commission_rate": 5,
            "is_active": True,
            "can_perform_treatments": True
        },
        {
            # Receptionist 1
            "first_name": "Jessica",
            "last_name": "Wilson",
            "email": "jessica.wilson@picobrain.com",
            "phone_mobile_country_code": "+1",
            "phone_mobile_number": "5551234571",
            "dob": "1995-08-18",
            "gender": "F",
            "nationality": "US",
            "employee_code": "RC001",
            "primary_clinic_id": clinic_id,
            "role": "receptionist",
            "hire_date": "2022-03-01",
            "base_salary_minor": 3500000,  # $35,000
            "salary_currency": "USD",
            "is_active": True,
            "can_perform_treatments": False
        },
        {
            # Receptionist 2
            "first_name": "David",
            "last_name": "Martinez",
            "email": "david.martinez@picobrain.com",
            "phone_mobile_country_code": "+1",
            "phone_mobile_number": "5551234572",
            "dob": "1992-12-05",
            "gender": "M",
            "nationality": "US",
            "employee_code": "RC002",
            "primary_clinic_id": clinic_id,
            "role": "receptionist",
            "hire_date": "2023-01-15",
            "base_salary_minor": 3800000,  # $38,000
            "salary_currency": "USD",
            "is_active": True,
            "can_perform_treatments": False
        },
        {
            # Manager
            "first_name": "Robert",
            "last_name": "Anderson",
            "email": "robert.anderson@picobrain.com",
            "phone_mobile_country_code": "+1",
            "phone_mobile_number": "5551234573",
            "dob": "1980-05-30",
            "gender": "M",
            "nationality": "US",
            "employee_code": "MG001",
            "primary_clinic_id": clinic_id,
            "role": "manager",
            "hire_date": "2018-01-01",
            "base_salary_minor": 9500000,  # $95,000
            "salary_currency": "USD",
            "commission_rate": 15,
            "is_active": True,
            "can_perform_treatments": False
        },
        {
            # Finance Staff
            "first_name": "Lisa",
            "last_name": "Thompson",
            "email": "lisa.thompson@picobrain.com",
            "phone_mobile_country_code": "+1",
            "phone_mobile_number": "5551234574",
            "dob": "1987-09-12",
            "gender": "F",
            "nationality": "US",
            "employee_code": "FN001",
            "primary_clinic_id": clinic_id,
            "role": "finance",
            "hire_date": "2019-07-01",
            "base_salary_minor": 6500000,  # $65,000
            "salary_currency": "USD",
            "is_active": True,
            "can_perform_treatments": False
        },
        {
            # Admin Staff
            "first_name": "James",
            "last_name": "Taylor",
            "email": "james.taylor@picobrain.com",
            "phone_mobile_country_code": "+1",
            "phone_mobile_number": "5551234575",
            "dob": "1983-02-28",
            "gender": "M",
            "nationality": "US",
            "employee_code": "AD001",
            "primary_clinic_id": clinic_id,
            "role": "admin",
            "hire_date": "2017-05-15",
            "base_salary_minor": 5500000,  # $55,000
            "salary_currency": "USD",
            "is_active": True,
            "can_perform_treatments": False
        },
        {
            # Inactive Doctor
            "first_name": "William",
            "last_name": "Clark",
            "email": "william.clark@picobrain.com",
            "phone_mobile_country_code": "+1",
            "phone_mobile_number": "5551234576",
            "dob": "1975-06-20",
            "gender": "M",
            "nationality": "US",
            "employee_code": "DR003",
            "primary_clinic_id": clinic_id,
            "role": "doctor",
            "specialization": "Orthopedics",
            "license_number": "MD-33333",
            "license_expiry": "2024-03-31",
            "hire_date": "2015-02-01",
            "termination_date": "2023-12-31",
            "base_salary_minor": 20000000,  # $200,000
            "salary_currency": "USD",
            "commission_rate": 15,
            "is_active": False,
            "can_perform_treatments": False
        }
    ]
    
    # Create each employee
    created_count = 0
    failed_count = 0
    
    for emp_data in employees:
        print(f"\nCreating {emp_data['role']}: {emp_data['first_name']} {emp_data['last_name']}...")
        
        response = requests.post(
            f"{BASE_URL}/employees/",
            json=emp_data,
            headers=headers
        )
        
        if response.status_code in [200, 201]:
            created_count += 1
            print(f"  ✅ Created successfully")
        else:
            failed_count += 1
            print(f"  ❌ Failed: {response.status_code}")
            if response.text:
                try:
                    error_detail = response.json()
                    print(f"     Error: {error_detail}")
                except:
                    print(f"     Error: {response.text[:200]}")
    
    print("\n" + "="*60)
    print(f"SUMMARY: Created {created_count} employees, {failed_count} failed")
    print("="*60)
    
    # Verify by listing all employees
    print("\nVerifying created employees...")
    response = requests.get(f"{BASE_URL}/employees", headers=headers)
    if response.status_code == 200:
        employees = response.json()
        print(f"Total employees in database: {len(employees)}")
        
        # Count by role
        role_counts = {}
        for emp in employees:
            role = emp.get('role', 'unknown')
            role_counts[role] = role_counts.get(role, 0) + 1
        
        print("\nEmployees by role:")
        for role, count in sorted(role_counts.items()):
            print(f"  {role.capitalize()}: {count}")

if __name__ == "__main__":
    create_sample_employees()
