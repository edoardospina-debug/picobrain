#!/usr/bin/env python3
"""
Fixed Employee Migration Script - All Validation Issues Resolved
Migrates employees with proper validation for PicoBrain API
"""

import asyncio
import csv
import json
from datetime import date, datetime
from decimal import Decimal
from pathlib import Path
from typing import Dict, List, Optional
import aiohttp

# Configuration
API_BASE_URL = "http://localhost:8000/api/v1"
CSV_FILE_PATH = "/Users/edo/PyProjects/input_files/Employees.csv"
BATCH_SIZE = 10  # Reasonable batch size

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
            # Create date and return ISO format
            return date(year, month, day).isoformat()
    except:
        return None

def parse_commission(commission_str: str) -> Optional[float]:
    """Parse commission percentage as float"""
    if not commission_str or commission_str.strip() == "" or commission_str == "0":
        return None
    try:
        # Convert to float (API expects decimal 0-1 range)
        value = float(commission_str)
        # If it's already in decimal format (0.15, 0.3), keep as is
        # If it's in percentage format (15, 30), convert to decimal
        if value > 1:
            value = value / 100
        return value
    except:
        return None

def parse_salary(salary_str: str) -> Optional[int]:
    """Parse salary to minor units (cents)"""
    if not salary_str or salary_str.strip() == "" or salary_str == "0":
        return None
    try:
        # Convert to cents (minor units)
        salary = float(salary_str)
        return int(salary * 100)  # Convert to cents
    except:
        return None

def determine_currency(country: str) -> str:
    """Determine currency based on country"""
    currency_map = {
        "GB": "GBP",
        "UK": "GBP",
        "US": "USD",
        "USA": "USD",
        "CA": "CAD",
        "IT": "EUR",
    }
    return currency_map.get(country, "USD")  # Default to USD

def transform_employee(row: Dict) -> Optional[Dict]:
    """Transform CSV row to API-compatible employee object"""
    try:
        # Map clinic
        clinic_id = CLINIC_ID_MAPPING.get(row.get('clinic_temp_id', '').strip())
        if not clinic_id:
            print(f"Warning: No clinic mapping for {row.get('name')}")
            return None
        
        # Get first and last name directly from CSV columns
        first_name = row.get('first_name', '').strip()
        last_name = row.get('last_name', '').strip()
        
        if not first_name or not last_name:
            print(f"Warning: Missing name for employee {row.get('temp_id')}")
            return None
        
        # Map role - the CSV now has "admin" but API might need different mapping
        role_raw = row.get('role', '').strip().lower()
        role_map = {
            "doctor": "doctor",
            "staff": "staff",
            "manager": "manager",
            "finance": "admin",
            "admin": "admin"  # Handle admin directly
        }
        role = role_map.get(role_raw, "staff")
        
        # Parse dates
        hire_date = parse_date(row.get('from_date', ''))
        termination_date = parse_date(row.get('to_date', ''))
        dob = parse_date(row.get('dob', ''))
        
        # Default hire date if missing
        if not hire_date:
            hire_date = "2024-01-01"
        
        # Determine active status
        is_active = not bool(termination_date)
        
        # Build employee object with minimal required fields
        employee = {
            "first_name": first_name,
            "last_name": last_name,
            "primary_clinic_id": clinic_id,
            "role": role,
            "hire_date": hire_date,
            "is_active": is_active,
            "can_perform_treatments": (role == "doctor")
        }
        
        # Add employee code (make it uppercase)
        if row.get('temp_id'):
            employee["employee_code"] = row['temp_id'].upper()
        
        # Add optional fields
        
        # Email - prioritize work email
        email = row.get('work_email', '').strip() or row.get('personal_email', '').strip()
        if email and "@" in email:
            employee["email"] = email.lower()
        
        # Date of birth
        if dob:
            employee["dob"] = dob
        
        # Termination date
        if termination_date:
            employee["termination_date"] = termination_date
        
        # Salary and commission - only if employee has them
        base_salary = parse_salary(row.get('base_salary', ''))
        if base_salary and base_salary > 0:
            employee["base_salary_minor"] = base_salary
            # Add currency based on country
            country = row.get('country', '').strip()
            if country:
                employee["salary_currency"] = determine_currency(country)
            else:
                # Determine by clinic location
                if clinic_id == CLINIC_ID_MAPPING["10"]:  # London
                    employee["salary_currency"] = "GBP"
                elif clinic_id == CLINIC_ID_MAPPING["11"]:  # Milan
                    employee["salary_currency"] = "EUR"
                elif clinic_id in [CLINIC_ID_MAPPING["12"], CLINIC_ID_MAPPING["14"]]:  # US clinics
                    employee["salary_currency"] = "USD"
                elif clinic_id == CLINIC_ID_MAPPING["13"]:  # Vancouver
                    employee["salary_currency"] = "CAD"
                else:
                    employee["salary_currency"] = "USD"
        
        # Commission rate as decimal
        commission = parse_commission(row.get('commission_percentage', ''))
        if commission is not None and commission > 0:
            employee["commission_rate"] = commission
        
        # License information for doctors
        if role == "doctor":
            license_num = row.get('license_number', '').strip()
            if license_num:
                employee["license_number"] = license_num
            
            license_exp = parse_date(row.get('license_expiration', ''))
            if license_exp:
                employee["license_expiry"] = license_exp
        
        # Add address information if available
        if row.get('address_line_1', '').strip():
            employee["address_line_1"] = row['address_line_1'].strip()
        if row.get('address_line_2', '').strip():
            employee["address_line_2"] = row['address_line_2'].strip()
        if row.get('postcode', '').strip():
            employee["postcode"] = row['postcode'].strip()
        if row.get('city', '').strip():
            employee["city"] = row['city'].strip()
        if row.get('state', '').strip():
            employee["state"] = row['state'].strip()
        
        # Country as 2-letter code
        country = row.get('country', '').strip()
        if country:
            # Map common country codes
            country_map = {
                "GB": "GB", "UK": "GB", "United Kingdom": "GB",
                "US": "US", "USA": "US", "United States": "US",
                "CA": "CA", "Canada": "CA",
                "IT": "IT", "Italy": "IT",
            }
            nationality = country_map.get(country, country[:2].upper() if len(country) >= 2 else "US")
            employee["nationality"] = nationality
        
        return employee
        
    except Exception as e:
        print(f"Error transforming {row.get('name')}: {e}")
        return None

async def test_single_employee(session, headers):
    """Test with a single well-formed employee first"""
    test_employee = {
        "first_name": "Test",
        "last_name": "Employee",
        "email": "test.employee@picoclinics.com",
        "primary_clinic_id": "c69dfe69-63c2-445f-9624-54c7876becb5",
        "role": "staff",
        "hire_date": "2024-01-01",
        "is_active": True,
        "can_perform_treatments": False,
        "employee_code": "TEST001"
    }
    
    print("\nTesting with single employee...")
    print(json.dumps(test_employee, indent=2))
    
    batch_data = {
        "employees": [test_employee],
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
            print(f"✅ Test successful! Response: {json.dumps(result, indent=2)}")
            return True
        else:
            text = await resp.text()
            print(f"❌ Test failed: {resp.status} - {text}")
            return False

async def migrate():
    """Run migration with fixes"""
    print("=" * 60)
    print("EMPLOYEE MIGRATION - FIXED VERSION")
    print("=" * 60)
    print(f"Today's date: {datetime.now().date()} (August 30, 2025)")
    
    print("\nLoading CSV...")
    with open(CSV_FILE_PATH, 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    
    print(f"Loaded {len(rows)} employees from CSV")
    
    # Transform employees
    employees = []
    skipped = []
    for row in rows:
        emp = transform_employee(row)
        if emp:
            employees.append(emp)
        else:
            skipped.append(row.get('name', 'Unknown'))
    
    print(f"Transformed {len(employees)} employees successfully")
    if skipped:
        print(f"Skipped {len(skipped)} employees: {', '.join(skipped[:5])}...")
    
    # Create batches
    batches = [employees[i:i+BATCH_SIZE] for i in range(0, len(employees), BATCH_SIZE)]
    
    async with aiohttp.ClientSession() as session:
        # Login
        print("\nAuthenticating...")
        data = aiohttp.FormData()
        data.add_field('username', 'admin@picobrain.com')
        data.add_field('password', 'admin123')
        
        async with session.post(f"{API_BASE_URL}/auth/login", data=data) as resp:
            if resp.status != 200:
                print(f"❌ Authentication failed: {resp.status}")
                text = await resp.text()
                print(f"Response: {text}")
                return
            result = await resp.json()
            token = result['access_token']
        
        print("✅ Authenticated successfully!")
        headers = {"Authorization": f"Bearer {token}"}
        
        # Test with single employee first
        test_success = await test_single_employee(session, headers)
        if not test_success:
            print("\n⚠️  Test employee failed. Continuing anyway...")
        
        # Process batches
        print(f"\nProcessing {len(batches)} batches...")
        total_created = 0
        total_failed = 0
        failed_details = []
        
        for i, batch in enumerate(batches, 1):
            print(f"\n{'='*40}")
            print(f"Batch {i}/{len(batches)} ({len(batch)} employees)")
            
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
                    
                    print(f"✅ Created: {created}")
                    print(f"❌ Failed: {failed}")
                    
                    # Show first few failures for debugging
                    for failure in result.get('failed', [])[:3]:
                        failed_details.append(failure)
                        if isinstance(failure, dict):
                            emp_code = failure.get('employee_code', 'Unknown')
                            error = failure.get('error', 'Unknown error')
                            print(f"   - {emp_code}: {error}")
                else:
                    text = await resp.text()
                    print(f"❌ Batch failed entirely: {resp.status}")
                    print(f"   Response: {text[:500]}...")  # First 500 chars
                    total_failed += len(batch)
                    
                    # Try to parse error details
                    try:
                        error_data = json.loads(text)
                        if 'detail' in error_data:
                            print(f"   Error detail: {error_data['detail']}")
                    except:
                        pass
        
        # Final summary
        print(f"\n{'='*60}")
        print(f"MIGRATION COMPLETE")
        print(f"{'='*60}")
        print(f"✅ Successfully created: {total_created} employees")
        print(f"❌ Failed: {total_failed} employees")
        print(f"📊 Success rate: {(total_created/(total_created+total_failed)*100):.1f}%")
        
        # Save failed details for debugging
        if failed_details:
            report_file = f"migration_failed_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(report_file, 'w') as f:
                json.dump(failed_details, f, indent=2)
            print(f"\n💾 Failed employee details saved to: {report_file}")
        
        # Save successful IDs if any
        if total_created > 0:
            print(f"\n🎉 Migration successful for {total_created} employees!")

if __name__ == "__main__":
    asyncio.run(migrate())
