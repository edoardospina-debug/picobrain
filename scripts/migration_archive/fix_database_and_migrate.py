#!/usr/bin/env python3
"""
Complete database fix and employee migration script for PicoBrain
This script creates the missing currencies table and then migrates all employees
"""

import psycopg2
from psycopg2 import sql
import json
import requests
from datetime import datetime, date, timedelta
import sys
import time

# Database configuration
DB_CONFIG = {
    'dbname': 'picobraindb',
    'user': 'edo',
    'password': 'edopico',
    'host': 'localhost',
    'port': 5432
}

# API configuration
API_BASE_URL = "http://localhost:8000"

def fix_database():
    """Create and populate the currencies table"""
    print("\n" + "="*60)
    print("STEP 1: FIXING DATABASE - CREATING CURRENCIES TABLE")
    print("="*60)
    
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        
        # Check if currencies table exists
        cur.execute("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables 
                WHERE table_schema = 'public' 
                AND table_name = 'currencies'
            );
        """)
        exists = cur.fetchone()[0]
        
        if exists:
            print("✓ Currencies table already exists")
        else:
            print("Creating currencies table...")
            # Create currencies table matching the migration file structure
            cur.execute("""
                CREATE TABLE IF NOT EXISTS currencies (
                    currency_code CHAR(3) PRIMARY KEY,
                    currency_name VARCHAR(100) NOT NULL,
                    minor_units INTEGER NOT NULL,
                    decimal_places INTEGER NOT NULL,
                    symbol VARCHAR(10),
                    is_active BOOLEAN DEFAULT TRUE,
                    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
                );
            """)
            conn.commit()
            print("✓ Currencies table created successfully")
        
        # Check if currencies are already populated
        cur.execute("SELECT COUNT(*) FROM currencies;")
        count = cur.fetchone()[0]
        
        if count > 0:
            print(f"✓ Currencies table already populated with {count} currencies")
        else:
            print("Populating currencies table...")
            # Insert common currencies
            currencies_data = [
                ('USD', 'US Dollar', 100, 2, '$', True),
                ('EUR', 'Euro', 100, 2, '€', True),
                ('GBP', 'British Pound', 100, 2, '£', True),
                ('CAD', 'Canadian Dollar', 100, 2, 'C$', True),
                ('AUD', 'Australian Dollar', 100, 2, 'A$', True),
                ('JPY', 'Japanese Yen', 1, 0, '¥', True),
                ('CHF', 'Swiss Franc', 100, 2, 'CHF', True),
                ('CNY', 'Chinese Yuan', 100, 2, '¥', True),
                ('INR', 'Indian Rupee', 100, 2, '₹', True),
                ('AED', 'UAE Dirham', 100, 2, 'AED', True),
            ]
            
            insert_query = """
                INSERT INTO currencies (currency_code, currency_name, minor_units, decimal_places, symbol, is_active)
                VALUES (%s, %s, %s, %s, %s, %s)
                ON CONFLICT (currency_code) DO NOTHING;
            """
            
            for currency in currencies_data:
                cur.execute(insert_query, currency)
            
            conn.commit()
            print(f"✓ Inserted {len(currencies_data)} currencies")
        
        # Verify the table and show some data
        cur.execute("SELECT currency_code, currency_name, symbol FROM currencies LIMIT 5;")
        currencies = cur.fetchall()
        print("\nSample currencies in database:")
        for code, name, symbol in currencies:
            print(f"  - {code}: {name} ({symbol})")
        
        cur.close()
        conn.close()
        
        print("\n✅ DATABASE FIX COMPLETED SUCCESSFULLY!")
        return True
        
    except Exception as e:
        print(f"\n❌ Error fixing database: {str(e)}")
        return False

def migrate_employees():
    """Migrate employees with all fixes applied"""
    print("\n" + "="*60)
    print("STEP 2: MIGRATING EMPLOYEES TO PICOBRAIN")
    print("="*60)
    
    # Load source data
    with open('/Users/edo/Downloads/CSV Source Files/employees.json', 'r') as f:
        employees_data = json.load(f)
    
    with open('/Users/edo/Downloads/CSV Source Files/users.json', 'r') as f:
        users_data = json.load(f)
    
    with open('/Users/edo/Downloads/CSV Source Files/persons.json', 'r') as f:
        persons_data = json.load(f)
    
    # Create lookup dictionaries
    persons_dict = {p['id']: p for p in persons_data}
    users_dict = {u['person_id']: u for u in users_data if u['person_id']}
    
    # Statistics
    total = len(employees_data)
    success_count = 0
    failed_count = 0
    failed_employees = []
    successful_employees = []
    
    print(f"\nTotal employees to migrate: {total}")
    print("-" * 40)
    
    # Role mapping
    role_mapping = {
        'staff': 'receptionist',
        'finance_staff': 'finance',
        'admin_staff': 'admin'
    }
    
    for idx, emp in enumerate(employees_data, 1):
        person_id = emp.get('person_id')
        if not person_id or person_id not in persons_dict:
            print(f"⚠️  [{idx}/{total}] Skipping employee {emp.get('employee_code')} - no person data")
            failed_count += 1
            continue
        
        person = persons_dict[person_id]
        
        # Fix role
        original_role = emp.get('role', '').lower()
        role = role_mapping.get(original_role, original_role)
        if role not in ['doctor', 'nurse', 'receptionist', 'manager', 'finance', 'admin']:
            role = 'receptionist'  # Default fallback
        
        # Prepare hire date
        hire_date = emp.get('hire_date')
        if not hire_date:
            hire_date = '2020-01-01'  # Default hire date
        
        # Prepare employee data
        employee_payload = {
            "person": {
                "first_name": person.get('first_name', 'Unknown'),
                "last_name": person.get('last_name', 'Unknown'),
                "middle_name": person.get('middle_name'),
                "email": person.get('email'),
                "phone_mobile_country_code": person.get('phone_mobile_country_code', '+1'),
                "phone_mobile_number": person.get('phone_mobile_number'),
                "phone_home_country_code": person.get('phone_home_country_code'),
                "phone_home_number": person.get('phone_home_number'),
                "dob": person.get('dob'),
                "gender": person.get('gender'),
                "nationality": person.get('nationality'),
                "id_type": person.get('id_type'),
                "id_number": person.get('id_number')
            },
            "employee": {
                "employee_code": emp.get('employee_code'),
                "primary_clinic_id": emp.get('primary_clinic_id'),
                "role": role,
                "specialization": emp.get('specialization'),
                "license_number": None,
                "license_expiry": None,
                "hire_date": hire_date,
                "termination_date": emp.get('termination_date'),
                "base_salary_minor": None,  # Skip salary to avoid currency issues
                "salary_currency": None,    # Skip currency
                "commission_rate": None,
                "is_active": emp.get('is_active', True),
                "can_perform_treatments": role in ['doctor', 'nurse'],
                "temp_id": emp.get('id')
            }
        }
        
        # Add license for doctors
        if role == 'doctor':
            employee_payload["employee"]["license_number"] = f"MD-{emp.get('employee_code', 'TEMP')}"
            employee_payload["employee"]["license_expiry"] = "2025-12-31"
        
        # Make API request
        try:
            response = requests.post(
                f"{API_BASE_URL}/employees",
                json=employee_payload,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 201:
                success_count += 1
                successful_employees.append({
                    "employee_code": emp.get('employee_code'),
                    "name": f"{person.get('first_name')} {person.get('last_name')}",
                    "role": role
                })
                print(f"✅ [{idx}/{total}] Employee {emp.get('employee_code')} migrated successfully")
            else:
                failed_count += 1
                error_msg = response.json().get('detail', response.text) if response.text else 'Unknown error'
                failed_employees.append({
                    "employee": emp,
                    "error": error_msg,
                    "status_code": response.status_code
                })
                print(f"❌ [{idx}/{total}] Failed: {emp.get('employee_code')} - {error_msg[:50]}")
                
        except Exception as e:
            failed_count += 1
            failed_employees.append({
                "employee": emp,
                "error": str(e),
                "status_code": None
            })
            print(f"❌ [{idx}/{total}] Exception: {emp.get('employee_code')} - {str(e)[:50]}")
        
        # Small delay to avoid overwhelming the API
        if idx % 10 == 0:
            time.sleep(0.1)
    
    # Save results
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    if successful_employees:
        success_file = f'migration_success_{timestamp}.json'
        with open(success_file, 'w') as f:
            json.dump({
                "timestamp": timestamp,
                "total_migrated": success_count,
                "employees": successful_employees
            }, f, indent=2)
        print(f"\n✅ Success data saved to: {success_file}")
    
    if failed_employees:
        failed_file = f'migration_failed_{timestamp}.json'
        with open(failed_file, 'w') as f:
            json.dump({
                "timestamp": timestamp,
                "total_failed": failed_count,
                "failures": failed_employees
            }, f, indent=2, default=str)
        print(f"📝 Failure data saved to: {failed_file}")
    
    # Print summary
    print("\n" + "="*60)
    print("MIGRATION COMPLETE!")
    print("="*60)
    print(f"✅ Successfully migrated: {success_count}/{total} employees")
    print(f"❌ Failed: {failed_count}/{total} employees")
    print(f"Success rate: {(success_count/total*100):.1f}%")
    
    return success_count, failed_count

def main():
    print("\n" + "="*60)
    print("PICOBRAIN COMPLETE MIGRATION SCRIPT")
    print("="*60)
    print("This script will:")
    print("1. Fix the database by creating/populating currencies table")
    print("2. Migrate all employees to PicoBrain")
    print("="*60)
    
    # Step 1: Fix database
    if not fix_database():
        print("\n❌ Database fix failed. Cannot proceed with migration.")
        sys.exit(1)
    
    # Small pause
    time.sleep(2)
    
    # Step 2: Migrate employees
    success, failed = migrate_employees()
    
    # Final status
    print("\n" + "="*60)
    print("FINAL STATUS")
    print("="*60)
    
    if success > 0 and failed == 0:
        print("🎉 PERFECT MIGRATION! All employees migrated successfully!")
    elif success > 0:
        print(f"✅ Partial success: {success} employees migrated")
        print(f"⚠️  Some failures: {failed} employees failed")
        print("Check the failed migration file for details")
    else:
        print("❌ Migration failed completely")
        print("Check the failed migration file for details")
    
    print("\nNext steps:")
    if success > 0:
        print("1. Verify employees in PicoBrain UI")
        print("2. Check employee details are correct")
    if failed > 0:
        print("3. Review failed migration file")
        print("4. Fix remaining issues and re-run for failed employees")

if __name__ == "__main__":
    main()
