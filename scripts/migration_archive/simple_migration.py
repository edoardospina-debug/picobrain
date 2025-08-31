#!/usr/bin/env python3
"""
Simple Employee Migration Script - Validation Fixed
Migrates employees with proper validation
"""

import asyncio
import csv
import json
from datetime import date
from pathlib import Path
from typing import Dict, List, Optional
import aiohttp

# Configuration
API_BASE_URL = "http://localhost:8000/api/v1"
CSV_FILE_PATH = "/Users/edo/PyProjects/input_files/Employees.csv"
BATCH_SIZE = 5  # Smaller batches for testing

# Clinic ID Mapping
CLINIC_ID_MAPPING = {
    "10": "c69dfe69-63c2-445f-9624-54c7876becb5",  # London
    "11": "44cc3318-35f9-45e9-a9b5-aab0e47c8c15",  # Milan
    "12": "2b79920a-0ebf-4684-bc11-2ca6316af262",  # Los Angeles
    "13": "f3711a7f-216a-493f-8543-d03d3fa4387f",  # Vancouver
    "14": "94646ff0-78c3-4d49-ab90-5336c861b3c4",  # New York
}

def parse_date(date_str: str) -> Optional[str]:
    """Parse date and return ISO format string"""
    if not date_str or date_str.strip() == "":
        return None
    try:
        parts = date_str.strip().split('/')
        if len(parts) == 3:
            day, month, year = int(parts[0]), int(parts[1]), int(parts[2])
            if year > 2025:
                year = 2025
            return date(year, month, day).isoformat()
    except:
        return None

def transform_employee_simple(row: Dict) -> Optional[Dict]:
    """Transform with minimal required fields only"""
    try:
        # Map clinic
        clinic_id = CLINIC_ID_MAPPING.get(row.get('clinic_temp_id', '').strip())
        if not clinic_id:
            return None
        
        # Parse name - use placeholder for single names
        name = row.get('name', '').strip()
        if not name:
            return None
        
        parts = name.split()
        if len(parts) == 1:
            first_name = parts[0]
            last_name = "Staff"  # Use generic last name instead of "(Single)"
        elif len(parts) == 2:
            first_name, last_name = parts[0], parts[1]
        else:
            first_name = parts[0]
            last_name = parts[-1]
        
        # Get role
        role_raw = row.get('role', '').strip().lower()
        role_map = {
            "doctor": "doctor",
            "staff": "staff",
            "manager": "manager",
            "finance": "admin"
        }
        role = role_map.get(role_raw, "staff")
        
        # Get dates
        hire_date = parse_date(row.get('from_date', ''))
        if not hire_date:
            hire_date = "2024-01-01"  # Default
        
        # Build minimal employee object
        employee = {
            "first_name": first_name,
            "last_name": last_name,
            "primary_clinic_id": clinic_id,
            "role": role,
            "hire_date": hire_date,
            "is_active": True,
            "can_perform_treatments": (role == "doctor")
        }
        
        # Add optional fields if valid
        email = row.get('work_email', '').strip() or row.get('personal_email', '').strip()
        if email and "@" in email:
            employee["email"] = email.lower()
        
        if row.get('temp_id'):
            employee["employee_code"] = row['temp_id']
        
        return employee
    except Exception as e:
        print(f"Error transforming {row.get('name')}: {e}")
        return None

async def migrate():
    """Run migration"""
    print("Loading CSV...")
    with open(CSV_FILE_PATH, 'r') as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    
    print(f"Loaded {len(rows)} employees")
    
    # Transform
    employees = []
    for row in rows:
        emp = transform_employee_simple(row)
        if emp:
            employees.append(emp)
    
    print(f"Transformed {len(employees)} employees")
    
    # Create batches
    batches = [employees[i:i+BATCH_SIZE] for i in range(0, len(employees), BATCH_SIZE)]
    
    async with aiohttp.ClientSession() as session:
        # Login
        print("Authenticating...")
        data = aiohttp.FormData()
        data.add_field('username', 'admin@picobrain.com')
        data.add_field('password', 'admin123')
        
        async with session.post(f"{API_BASE_URL}/auth/login", data=data) as resp:
            if resp.status != 200:
                print(f"Auth failed: {resp.status}")
                return
            result = await resp.json()
            token = result['access_token']
        
        print("Authenticated!")
        
        # Process batches
        headers = {"Authorization": f"Bearer {token}"}
        total_created = 0
        total_failed = 0
        
        for i, batch in enumerate(batches, 1):
            print(f"\nBatch {i}/{len(batches)}")
            
            batch_data = {
                "employees": batch,
                "stop_on_error": False,
                "validate_all_first": False
            }
            
            async with session.post(
                f"{API_BASE_URL}/employees/bulk",
                headers=headers,
                json=batch_data
            ) as resp:
                if resp.status in [200, 201]:
                    result = await resp.json()
                    created = len(result.get('created', []))
                    failed = len(result.get('failed', []))
                    total_created += created
                    total_failed += failed
                    print(f"  Created: {created}, Failed: {failed}")
                    
                    # Show failures
                    for failure in result.get('failed', []):
                        print(f"  Failed: {failure}")
                else:
                    text = await resp.text()
                    print(f"  Batch failed: {resp.status} - {text}")
                    total_failed += len(batch)
        
        print(f"\n{'='*50}")
        print(f"MIGRATION COMPLETE")
        print(f"  Total Created: {total_created}")
        print(f"  Total Failed: {total_failed}")
        print(f"{'='*50}")

if __name__ == "__main__":
    asyncio.run(migrate())
