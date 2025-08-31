#!/usr/bin/env python3
"""
Diagnostic Migration Script - Debug validation errors
"""

import asyncio
import csv
import json
import aiohttp
from datetime import date, datetime

# Configuration
API_BASE_URL = "http://localhost:8000/api/v1"
CSV_FILE_PATH = "/Users/edo/PyProjects/input_files/Employees.csv"

# Clinic ID Mapping
CLINIC_ID_MAPPING = {
    "10": "c69dfe69-63c2-445f-9624-54c7876becb5",  # London
    "11": "44cc3318-35f9-45e9-a9b5-aab0e47c8c15",  # Milan
    "12": "2b79920a-0ebf-4684-bc11-2ca6316af262",  # Los Angeles
    "13": "f3711a7f-216a-493f-8543-d03d3fa4387f",  # Vancouver
    "14": "94646ff0-78c3-4d49-ab90-5336c861b3c4",  # New York
}

# Known failing employee codes
FAILING_CODES = ["78", "75", "77", "76", "82", "89", "71", "99", "98", "108", "109", "110"]

def parse_date(date_str):
    """Parse date and return ISO format string"""
    if not date_str or date_str.strip() == "":
        return None
    try:
        parts = date_str.strip().split('/')
        if len(parts) == 3:
            day, month, year = int(parts[0]), int(parts[1]), int(parts[2])
            return date(year, month, day).isoformat()
    except:
        return None

async def test_employee(session, headers, employee_data):
    """Test a single employee and get detailed error"""
    print(f"\nTesting employee: {employee_data.get('employee_code')} - {employee_data.get('first_name')} {employee_data.get('last_name')}")
    print(f"Data being sent:")
    print(json.dumps(employee_data, indent=2))
    
    # Try single employee endpoint first
    try:
        async with session.post(
            f"{API_BASE_URL}/employees",
            headers=headers,
            json=employee_data
        ) as resp:
            if resp.status in [200, 201]:
                result = await resp.json()
                print(f"✅ SUCCESS! Created employee with ID: {result.get('id')}")
                return True
            else:
                text = await resp.text()
                print(f"❌ FAILED with status {resp.status}")
                print(f"Error response: {text}")
                
                # Try to parse error details
                try:
                    error_data = json.loads(text)
                    if 'detail' in error_data:
                        if isinstance(error_data['detail'], list):
                            for err in error_data['detail']:
                                field = err.get('loc', ['unknown'])[-1]
                                msg = err.get('msg', 'Unknown error')
                                print(f"  - Field '{field}': {msg}")
                        else:
                            print(f"  - {error_data['detail']}")
                except:
                    print(f"  Raw error: {text[:500]}")
                return False
    except Exception as e:
        print(f"❌ Exception: {e}")
        return False

async def diagnose():
    """Run diagnostic on failing employees"""
    print("=" * 60)
    print("EMPLOYEE MIGRATION DIAGNOSTIC")
    print("=" * 60)
    
    # Load CSV
    print("\nLoading CSV...")
    with open(CSV_FILE_PATH, 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    
    # Find failing employees
    failing_employees = []
    for row in rows:
        if row.get('temp_id') in FAILING_CODES:
            failing_employees.append(row)
    
    print(f"Found {len(failing_employees)} failing employees to diagnose")
    
    async with aiohttp.ClientSession() as session:
        # Login
        print("\nAuthenticating...")
        data = aiohttp.FormData()
        data.add_field('username', 'admin@picobrain.com')
        data.add_field('password', 'admin123')
        
        async with session.post(f"{API_BASE_URL}/auth/login", data=data) as resp:
            if resp.status != 200:
                print(f"❌ Authentication failed: {resp.status}")
                return
            result = await resp.json()
            token = result['access_token']
        
        print("✅ Authenticated successfully!")
        headers = {"Authorization": f"Bearer {token}"}
        
        # Test each failing employee
        for row in failing_employees:
            print("\n" + "="*40)
            
            # Transform employee with minimal fields first
            clinic_id = CLINIC_ID_MAPPING.get(row.get('clinic_temp_id', '').strip())
            if not clinic_id:
                print(f"❌ No clinic mapping for employee {row.get('temp_id')}")
                continue
            
            # Start with absolute minimum required fields
            employee_data = {
                "first_name": row.get('first_name', '').strip(),
                "last_name": row.get('last_name', '').strip(),
                "primary_clinic_id": clinic_id,
                "role": row.get('role', 'staff').lower(),
                "hire_date": parse_date(row.get('from_date', '')) or "2024-01-01",
                "is_active": not bool(parse_date(row.get('to_date', ''))),
                "can_perform_treatments": row.get('role', '').lower() == 'doctor',
                "employee_code": row.get('temp_id', '').upper()
            }
            
            # Add email if present
            email = row.get('work_email', '').strip() or row.get('personal_email', '').strip()
            if email and "@" in email:
                employee_data["email"] = email.lower()
            
            # Try with minimal data
            print("\n1. Testing with MINIMAL data:")
            success = await test_employee(session, headers, employee_data)
            
            if not success:
                # Try without employee_code (might be duplicate)
                print("\n2. Testing WITHOUT employee_code:")
                data_no_code = {k: v for k, v in employee_data.items() if k != 'employee_code'}
                success = await test_employee(session, headers, data_no_code)
                
                if not success and email:
                    # Try without email (might be duplicate)
                    print("\n3. Testing WITHOUT email:")
                    data_no_email = {k: v for k, v in employee_data.items() if k != 'email'}
                    success = await test_employee(session, headers, data_no_email)
                    
                    if not success:
                        # Try with neither
                        print("\n4. Testing WITHOUT email AND employee_code:")
                        data_minimal = {k: v for k, v in employee_data.items() if k not in ['email', 'employee_code']}
                        success = await test_employee(session, headers, data_minimal)
        
        print("\n" + "="*60)
        print("DIAGNOSTIC COMPLETE")
        print("="*60)

if __name__ == "__main__":
    asyncio.run(diagnose())
