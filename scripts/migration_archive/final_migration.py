#!/usr/bin/env python3
"""
Final Employee Migration Solution - Complete with duplicate handling
"""

import asyncio
import csv
import json
import aiohttp
from datetime import date, datetime
from typing import Dict, List, Optional, Set

# Configuration
API_BASE_URL = "http://localhost:8000/api/v1"
CSV_FILE_PATH = "/Users/edo/PyProjects/input_files/Employees.csv"
BATCH_SIZE = 5  # Smaller batches for better error handling

# Clinic ID Mapping
CLINIC_ID_MAPPING = {
    "10": "c69dfe69-63c2-445f-9624-54c7876becb5",  # London
    "11": "44cc3318-35f9-45e9-a9b5-aab0e47c8c15",  # Milan
    "12": "2b79920a-0ebf-4684-bc11-2ca6316af262",  # Los Angeles
    "13": "f3711a7f-216a-493f-8543-d03d3fa4387f",  # Vancouver
    "14": "94646ff0-78c3-4d49-ab90-5336c861b3c4",  # New York
}

# Track used codes and emails
used_employee_codes: Set[str] = set()
used_emails: Set[str] = set()

def parse_date(date_str: str) -> Optional[str]:
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

def parse_commission(commission_str: str) -> Optional[float]:
    """Parse commission percentage as float"""
    if not commission_str or commission_str.strip() == "" or commission_str == "0":
        return None
    try:
        value = float(commission_str)
        # Convert to decimal format (0.15 instead of 15)
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
        salary = float(salary_str)
        return int(salary * 100)  # Convert to cents
    except:
        return None

def determine_currency(country: str, clinic_id: str) -> str:
    """Determine currency based on country or clinic location"""
    if country:
        currency_map = {
            "GB": "GBP", "UK": "GBP",
            "US": "USD", "USA": "USD",
            "CA": "CAD",
            "IT": "EUR",
        }
        if country in currency_map:
            return currency_map[country]
    
    # Fallback to clinic location
    if clinic_id == CLINIC_ID_MAPPING["10"]:  # London
        return "GBP"
    elif clinic_id == CLINIC_ID_MAPPING["11"]:  # Milan
        return "EUR"
    elif clinic_id in [CLINIC_ID_MAPPING["12"], CLINIC_ID_MAPPING["14"]]:  # US clinics
        return "USD"
    elif clinic_id == CLINIC_ID_MAPPING["13"]:  # Vancouver
        return "CAD"
    else:
        return "USD"  # Default

async def get_existing_employees(session, headers) -> tuple[Set[str], Set[str]]:
    """Fetch existing employees to check for duplicates"""
    print("\nChecking existing employees in database...")
    existing_codes = set()
    existing_emails = set()
    
    try:
        # Get existing employees
        async with session.get(
            f"{API_BASE_URL}/employees?limit=1000",
            headers=headers
        ) as resp:
            if resp.status == 200:
                result = await resp.json()
                employees = result.get('items', [])
                for emp in employees:
                    if emp.get('employee_code'):
                        existing_codes.add(emp['employee_code'].upper())
                    if emp.get('email'):
                        existing_emails.add(emp['email'].lower())
                print(f"Found {len(employees)} existing employees")
                print(f"  - {len(existing_codes)} with employee codes")
                print(f"  - {len(existing_emails)} with emails")
    except Exception as e:
        print(f"Warning: Could not fetch existing employees: {e}")
    
    return existing_codes, existing_emails

def transform_employee(row: Dict, existing_codes: Set[str], existing_emails: Set[str], index: int) -> Optional[Dict]:
    """Transform CSV row to API-compatible employee object"""
    global used_employee_codes, used_emails
    
    try:
        # Map clinic
        clinic_id = CLINIC_ID_MAPPING.get(row.get('clinic_temp_id', '').strip())
        if not clinic_id:
            return None
        
        # Get names
        first_name = row.get('first_name', '').strip()
        last_name = row.get('last_name', '').strip()
        
        if not first_name or not last_name:
            return None
        
        # Map role
        role_raw = row.get('role', '').strip().lower()
        role_map = {
            "doctor": "doctor",
            "staff": "staff",
            "manager": "manager",
            "finance": "admin",
            "admin": "admin"
        }
        role = role_map.get(role_raw, "staff")
        
        # Parse dates
        hire_date = parse_date(row.get('from_date', ''))
        termination_date = parse_date(row.get('to_date', ''))
        dob = parse_date(row.get('dob', ''))
        
        if not hire_date:
            hire_date = "2024-01-01"
        
        # Build employee object
        employee = {
            "first_name": first_name,
            "last_name": last_name,
            "primary_clinic_id": clinic_id,
            "role": role,
            "hire_date": hire_date,
            "is_active": not bool(termination_date),
            "can_perform_treatments": (role == "doctor")
        }
        
        # Handle employee code with duplicate check
        emp_code = row.get('temp_id', '').strip()
        if emp_code:
            emp_code = emp_code.upper()
            # Check for duplicates
            if emp_code in existing_codes or emp_code in used_employee_codes:
                # Generate unique code
                emp_code = f"{emp_code}_{index}"
                print(f"  Note: Generated unique code {emp_code} for {first_name} {last_name}")
            employee["employee_code"] = emp_code
            used_employee_codes.add(emp_code)
        
        # Handle email with duplicate check
        email = row.get('work_email', '').strip() or row.get('personal_email', '').strip()
        if email and "@" in email:
            email = email.lower()
            # Check for duplicates
            if email not in existing_emails and email not in used_emails:
                employee["email"] = email
                used_emails.add(email)
            else:
                print(f"  Note: Skipping duplicate email {email} for {first_name} {last_name}")
        
        # Add optional fields
        if dob:
            employee["dob"] = dob
        
        if termination_date:
            employee["termination_date"] = termination_date
        
        # Salary and commission
        base_salary = parse_salary(row.get('base_salary', ''))
        if base_salary and base_salary > 0:
            employee["base_salary_minor"] = base_salary
            country = row.get('country', '').strip()
            employee["salary_currency"] = determine_currency(country, clinic_id)
        
        commission = parse_commission(row.get('commission_percentage', ''))
        if commission is not None and commission > 0:
            employee["commission_rate"] = commission
        
        # License for doctors
        if role == "doctor":
            license_num = row.get('license_number', '').strip()
            if license_num:
                employee["license_number"] = license_num
            
            license_exp = parse_date(row.get('license_expiration', ''))
            if license_exp:
                employee["license_expiry"] = license_exp
        
        # Address info
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
        
        # Country/nationality
        country = row.get('country', '').strip()
        if country:
            country_map = {
                "GB": "GB", "UK": "GB",
                "US": "US", "USA": "US",
                "CA": "CA",
                "IT": "IT",
            }
            nationality = country_map.get(country, country[:2].upper() if len(country) >= 2 else None)
            if nationality:
                employee["nationality"] = nationality
        
        return employee
        
    except Exception as e:
        print(f"Error transforming {row.get('name')}: {e}")
        return None

async def migrate_single_employee(session, headers, employee_data):
    """Migrate a single employee with error handling"""
    try:
        async with session.post(
            f"{API_BASE_URL}/employees",
            headers=headers,
            json=employee_data
        ) as resp:
            if resp.status in [200, 201]:
                result = await resp.json()
                return True, result.get('id')
            else:
                text = await resp.text()
                return False, text
    except Exception as e:
        return False, str(e)

async def migrate():
    """Run final migration with all fixes"""
    print("=" * 60)
    print("FINAL EMPLOYEE MIGRATION - COMPLETE SOLUTION")
    print("=" * 60)
    print(f"Date: {datetime.now()} (August 30, 2025)")
    
    # Load CSV
    print("\nLoading CSV...")
    with open(CSV_FILE_PATH, 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    
    print(f"Loaded {len(rows)} employees from CSV")
    
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
        
        # Get existing employees to avoid duplicates
        existing_codes, existing_emails = await get_existing_employees(session, headers)
        
        # Transform employees
        print("\nTransforming employees...")
        employees = []
        skipped = []
        for i, row in enumerate(rows):
            emp = transform_employee(row, existing_codes, existing_emails, i)
            if emp:
                employees.append(emp)
            else:
                skipped.append(row.get('name', 'Unknown'))
        
        print(f"Transformed {len(employees)} employees")
        if skipped:
            print(f"Skipped {len(skipped)} employees")
        
        # Migrate individually for better error handling
        print(f"\nMigrating {len(employees)} employees individually...")
        total_created = 0
        total_failed = 0
        failed_details = []
        created_ids = []
        
        for i, employee in enumerate(employees, 1):
            name = f"{employee['first_name']} {employee['last_name']}"
            code = employee.get('employee_code', 'N/A')
            
            print(f"\n[{i}/{len(employees)}] Migrating {name} (Code: {code})...", end=" ")
            
            success, result = await migrate_single_employee(session, headers, employee)
            
            if success:
                print(f"✅ SUCCESS (ID: {result})")
                total_created += 1
                created_ids.append({
                    "employee_code": code,
                    "name": name,
                    "id": result
                })
            else:
                print(f"❌ FAILED")
                total_failed += 1
                
                # Try without employee_code if it might be duplicate
                if 'employee_code' in employee:
                    employee_no_code = {k: v for k, v in employee.items() if k != 'employee_code'}
                    print(f"  Retrying without employee_code...", end=" ")
                    success2, result2 = await migrate_single_employee(session, headers, employee_no_code)
                    if success2:
                        print(f"✅ SUCCESS (ID: {result2})")
                        total_created += 1
                        total_failed -= 1
                        created_ids.append({
                            "employee_code": "auto-generated",
                            "name": name,
                            "id": result2
                        })
                    else:
                        print(f"❌ Still failed")
                        failed_details.append({
                            "name": name,
                            "code": code,
                            "error": result2[:200] if isinstance(result2, str) else str(result2)
                        })
                else:
                    failed_details.append({
                        "name": name,
                        "code": code,
                        "error": result[:200] if isinstance(result, str) else str(result)
                    })
            
            # Small delay to avoid rate limiting
            if i % 10 == 0:
                await asyncio.sleep(0.5)
        
        # Final summary
        print(f"\n{'='*60}")
        print(f"MIGRATION COMPLETE")
        print(f"{'='*60}")
        print(f"✅ Successfully created: {total_created} employees")
        print(f"❌ Failed: {total_failed} employees")
        success_rate = (total_created/(total_created+total_failed)*100) if (total_created+total_failed) > 0 else 0
        print(f"📊 Success rate: {success_rate:.1f}%")
        
        # Save results
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        if created_ids:
            success_file = f"migration_success_{timestamp}.json"
            with open(success_file, 'w') as f:
                json.dump(created_ids, f, indent=2)
            print(f"\n💾 Successful IDs saved to: {success_file}")
        
        if failed_details:
            failed_file = f"migration_final_failed_{timestamp}.json"
            with open(failed_file, 'w') as f:
                json.dump(failed_details, f, indent=2)
            print(f"💾 Failed details saved to: {failed_file}")
            print("\nFailed employees:")
            for fail in failed_details[:5]:
                print(f"  - {fail['name']} ({fail['code']})")
        
        if total_created > 0:
            print(f"\n🎉 Successfully migrated {total_created} employees to PicoBrain!")

if __name__ == "__main__":
    asyncio.run(migrate())
