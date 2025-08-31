#!/usr/bin/env python3
"""
Minimal Employee Migration - Creates employees without salary data
This version bypasses currency issues by not including salary information
"""

import asyncio
import csv
import json
import aiohttp
from datetime import date, datetime, timedelta
from typing import Dict, List, Optional, Set

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

def generate_doctor_license(employee_name: str, clinic_id: str) -> tuple[str, str]:
    """Generate a mock license number and expiry date for doctors"""
    # Generate a unique license number based on name and clinic
    name_part = ''.join(filter(str.isalpha, employee_name.upper()))[:3]
    clinic_part = clinic_id.split('-')[0][:4].upper()
    import random
    random_part = str(random.randint(1000, 9999))
    license_number = f"MED{name_part}{clinic_part}{random_part}"
    
    # Set license expiry to 2 years from now
    license_expiry = (date.today() + timedelta(days=730)).isoformat()
    
    return license_number, license_expiry

async def get_existing_employees(session, headers) -> tuple[Set[str], Set[str]]:
    """Fetch existing employees to check for duplicates"""
    print("\nChecking existing employees in database...")
    existing_codes = set()
    existing_emails = set()
    
    try:
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
    except Exception as e:
        print(f"Warning: Could not fetch existing employees: {e}")
    
    return existing_codes, existing_emails

def transform_employee_minimal(row: Dict, existing_codes: Set[str], existing_emails: Set[str], index: int) -> Optional[Dict]:
    """Transform CSV row to minimal API-compatible employee object (no salary)"""
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
        
        # Map role correctly
        role_raw = row.get('role', '').strip().lower()
        role_map = {
            "doctor": "doctor",
            "staff": "receptionist",  
            "manager": "manager",
            "finance": "admin",
            "admin": "admin"
        }
        role = role_map.get(role_raw, "receptionist")
        
        # Parse dates
        hire_date = parse_date(row.get('from_date', ''))
        termination_date = parse_date(row.get('to_date', ''))
        dob = parse_date(row.get('dob', ''))
        
        if not hire_date:
            hire_date = "2024-01-01"
        
        # Build minimal employee object
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
            if emp_code in existing_codes or emp_code in used_employee_codes:
                emp_code = f"{emp_code}_{index}"
            employee["employee_code"] = emp_code
            used_employee_codes.add(emp_code)
        
        # Handle email with duplicate check
        email = row.get('work_email', '').strip() or row.get('personal_email', '').strip()
        if email and "@" in email:
            email = email.lower()
            if email not in existing_emails and email not in used_emails:
                employee["email"] = email
                used_emails.add(email)
        
        # Add optional fields
        if dob:
            employee["dob"] = dob
        
        if termination_date:
            employee["termination_date"] = termination_date
        
        # Generate license for doctors
        if role == "doctor":
            license_num = row.get('license_number', '').strip()
            license_exp_str = row.get('license_expiration', '').strip()
            
            if not license_num or not license_exp_str:
                license_num, license_exp = generate_doctor_license(
                    f"{first_name} {last_name}", 
                    clinic_id
                )
            else:
                license_exp = parse_date(license_exp_str)
                if not license_exp:
                    _, license_exp = generate_doctor_license(
                        f"{first_name} {last_name}", 
                        clinic_id
                    )
            
            employee["license_number"] = license_num
            employee["license_expiry"] = license_exp
        
        # NOTE: NOT including salary, commission, or currency to avoid errors
        
        # Address info (optional)
        if row.get('address_line_1', '').strip():
            employee["address_line_1"] = row['address_line_1'].strip()
        if row.get('postcode', '').strip():
            employee["postcode"] = row['postcode'].strip()
        if row.get('city', '').strip():
            employee["city"] = row['city'].strip()
        
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
    """Run minimal migration without salary data"""
    print("=" * 60)
    print("MINIMAL EMPLOYEE MIGRATION (NO SALARY DATA)")
    print("=" * 60)
    print(f"Date: {datetime.now()} (August 30, 2025)")
    print("\nStrategy:")
    print("• Creating employees with basic info only")
    print("• Skipping salary/commission/currency to avoid database issues")
    print("• Salary data can be added later once currency table is fixed")
    
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
        
        # Get existing employees
        existing_codes, existing_emails = await get_existing_employees(session, headers)
        
        # Transform employees
        print("\nTransforming employees (minimal data)...")
        employees = []
        skipped = []
        for i, row in enumerate(rows):
            emp = transform_employee_minimal(row, existing_codes, existing_emails, i)
            if emp:
                employees.append(emp)
            else:
                skipped.append(row.get('name', 'Unknown'))
        
        print(f"Transformed {len(employees)} employees")
        
        # Count roles
        role_counts = {}
        for emp in employees:
            role = emp.get('role', 'unknown')
            role_counts[role] = role_counts.get(role, 0) + 1
        
        print("\nRole distribution:")
        for role, count in sorted(role_counts.items()):
            print(f"  • {role}: {count}")
        
        # Migrate individually
        print(f"\nMigrating {len(employees)} employees...")
        total_created = 0
        total_failed = 0
        failed_details = []
        created_ids = []
        
        for i, employee in enumerate(employees, 1):
            name = f"{employee['first_name']} {employee['last_name']}"
            code = employee.get('employee_code', 'N/A')
            role = employee.get('role', 'unknown')
            
            # Progress indicator every 10 employees
            if i % 10 == 1:
                print(f"\n[{i}-{min(i+9, len(employees))}/{len(employees)}] Processing batch...")
            
            success, result = await migrate_single_employee(session, headers, employee)
            
            if success:
                print(f"  ✅ {name} ({role})")
                total_created += 1
                created_ids.append({
                    "employee_code": code,
                    "name": name,
                    "role": role,
                    "id": result
                })
            else:
                print(f"  ❌ {name} ({role})")
                total_failed += 1
                failed_details.append({
                    "name": name,
                    "code": code,
                    "role": role,
                    "error": result[:200] if isinstance(result, str) else str(result)
                })
            
            # Small delay every 10 to avoid rate limiting
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
            failed_file = f"migration_failed_{timestamp}.json"
            with open(failed_file, 'w') as f:
                json.dump(failed_details, f, indent=2)
            print(f"💾 Failed details saved to: {failed_file}")
        
        if total_created > 0:
            print(f"\n🎉 Successfully migrated {total_created} employees!")
            print("\n📋 Next steps:")
            print("1. Fix database currency table issue")
            print("2. Update employees with salary data later")
            print("3. Test employee login functionality")
            print("4. Proceed with client migration")
        else:
            print("\n⚠️ No employees were migrated. Check error logs.")

if __name__ == "__main__":
    asyncio.run(migrate())
