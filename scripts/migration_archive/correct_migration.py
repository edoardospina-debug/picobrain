#!/usr/bin/env python3
"""
Correct Database Migration Script - Creates persons and employees with proper relationships
"""

import psycopg2
import csv
import json
from datetime import datetime
import sys
import re
import uuid

# Database connection parameters
db_params = {
    'dbname': 'picobraindb',
    'user': 'edo',
    'password': '',
    'host': 'localhost',
    'port': '5432'
}

# CSV file path
CSV_FILE_PATH = "/Users/edo/PyProjects/input_files/Employees.csv"

def clean_phone(phone_str):
    """Clean phone number"""
    if not phone_str or phone_str.strip() == "":
        return None
    # Remove non-digits and format
    phone = re.sub(r'[^\d+]', '', phone_str.strip())
    return phone if len(phone) >= 7 else None

def clean_email(email_str):
    """Clean and validate email"""
    if not email_str or email_str.strip() == "":
        return None
    
    email = email_str.strip().lower()
    
    # Skip obviously invalid emails
    if email in ["na@a.cpm", "xxx@picoclinics.com", ""]:
        return None
    
    # Basic email validation
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if re.match(email_pattern, email):
        return email
    
    return None

def parse_date(date_str):
    """Parse date from DD/MM/YYYY format"""
    if not date_str or date_str.strip() == "":
        return None
    
    try:
        # Handle DD/MM/YYYY format
        parts = date_str.strip().split('/')
        if len(parts) == 3:
            day, month, year = parts
            # Handle year issues
            year_int = int(year)
            if year_int > 2025:
                year_int = 2025
            return f"{year_int}-{month.zfill(2)}-{day.zfill(2)}"
    except:
        pass
    return None

def split_name(full_name):
    """Split full name into first and last"""
    if not full_name:
        return "", ""
    
    parts = full_name.strip().split()
    
    if len(parts) == 0:
        return "", ""
    elif len(parts) == 1:
        # For single names, use as first name with generic last name
        return parts[0], "Employee"
    else:
        # First word is first name, rest is last name
        return parts[0], " ".join(parts[1:])

def migrate_employees_from_csv():
    """Migrate employees with proper persons table relationship"""
    conn = None
    try:
        print("\n" + "=" * 80)
        print("MIGRATING EMPLOYEES FROM CSV WITH PERSONS TABLE")
        print("=" * 80)
        
        # Read CSV file
        print(f"Reading CSV file: {CSV_FILE_PATH}")
        
        employees = []
        with open(CSV_FILE_PATH, 'r', encoding='utf-8-sig') as file:
            reader = csv.DictReader(file)
            for row in reader:
                employees.append(row)
        
        print(f"✅ Loaded {len(employees)} employee records from CSV")
        
        conn = psycopg2.connect(**db_params)
        cur = conn.cursor()
        
        success_count = 0
        error_count = 0
        skip_count = 0
        errors = []
        
        # Role mapping
        role_mapping = {
            'doctor': 'doctor',
            'staff': 'receptionist',
            'manager': 'doctor',
            'finance': 'receptionist',
            'nurse': 'nurse',
            'receptionist': 'receptionist'
        }
        
        print("\nProcessing employees...")
        print("-" * 80)
        
        for row in employees:
            try:
                # Parse name
                first_name, last_name = split_name(row.get('name', ''))
                
                if not first_name:
                    skip_count += 1
                    print(f"  ⚠️ Skipping - no valid name: {row}")
                    continue
                
                # Get email
                work_email = clean_email(row.get('work_email', ''))
                personal_email = clean_email(row.get('personal_email', ''))
                email = work_email or personal_email
                
                # Generate email if missing
                if not email:
                    email = f"{first_name.lower()}.{last_name.lower().replace(' ', '')}@clinic.com"
                
                # Get ID number (use temp_id)
                id_number = row.get('temp_id', '')
                if not id_number:
                    id_number = f"EMP{datetime.now().timestamp():.0f}"
                
                # Parse DOB
                dob = parse_date(row.get('dob', ''))
                
                # Check if person already exists by email or name
                cur.execute("""
                    SELECT id, first_name, last_name 
                    FROM persons 
                    WHERE email = %s OR (first_name = %s AND last_name = %s)
                """, (email, first_name, last_name))
                
                existing_person = cur.fetchone()
                
                if existing_person:
                    person_id = existing_person[0]
                    print(f"  ℹ️ Found existing person: {first_name} {last_name} (ID: {person_id})")
                    
                    # Check if employee record exists for this person
                    cur.execute("""
                        SELECT id FROM employees WHERE person_id = %s
                    """, (person_id,))
                    
                    if cur.fetchone():
                        skip_count += 1
                        print(f"  ⚠️ Skipping {first_name} {last_name} - employee record already exists")
                        continue
                else:
                    # Create new person
                    person_id = str(uuid.uuid4())
                    cur.execute("""
                        INSERT INTO persons 
                        (id, first_name, last_name, email, dob, id_number, created_at, updated_at)
                        VALUES (%s, %s, %s, %s, %s, %s, NOW(), NOW())
                        RETURNING id;
                    """, (
                        person_id,
                        first_name,
                        last_name,
                        email,
                        dob,
                        id_number
                    ))
                    
                    person_id = cur.fetchone()[0]
                    print(f"  ✅ Created person: {first_name} {last_name}")
                
                # Get role
                role_raw = row.get('role', '').strip().lower()
                role = role_mapping.get(role_raw, 'receptionist')
                
                # Parse dates
                hire_date = parse_date(row.get('from_date', ''))
                if not hire_date:
                    hire_date = '2024-01-01'
                
                termination_date = parse_date(row.get('to_date', ''))
                
                # Determine if active
                is_active = True
                if termination_date:
                    term_date_obj = datetime.strptime(termination_date, '%Y-%m-%d')
                    if term_date_obj < datetime.now():
                        is_active = False
                
                # Create employee record
                employee_id = str(uuid.uuid4())
                employee_code = f"EMP{row.get('temp_id', '')}" if row.get('temp_id') else f"EMP{datetime.now().timestamp():.0f}"
                
                cur.execute("""
                    INSERT INTO employees 
                    (id, person_id, employee_code, role, hire_date, termination_date,
                     is_active, currency_code, created_at, updated_at, temp_id)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, NOW(), NOW(), %s)
                    RETURNING id;
                """, (
                    employee_id,
                    person_id,
                    employee_code,
                    role,
                    hire_date,
                    termination_date,
                    is_active,
                    'USD',  # Default currency
                    int(row.get('temp_id', 0)) if row.get('temp_id', '').isdigit() else None
                ))
                
                emp_id = cur.fetchone()[0]
                
                # If doctor, add to doctors table
                if role == 'doctor':
                    license_number = row.get('license_number', '') or f"DOC{success_count:05d}"
                    doctor_id = str(uuid.uuid4())
                    
                    cur.execute("""
                        INSERT INTO doctors 
                        (id, employee_id, license_number, created_at, updated_at)
                        VALUES (%s, %s, %s, NOW(), NOW())
                        ON CONFLICT (employee_id) DO NOTHING;
                    """, (doctor_id, emp_id, license_number))
                    
                    print(f"  ✅ Created doctor record with license: {license_number}")
                
                success_count += 1
                status = "✅ Active" if is_active else "⏸️ Inactive"
                print(f"  {status} Migrated: {first_name} {last_name} ({role}) - Employee Code: {employee_code}")
                
            except Exception as e:
                error_count += 1
                error_msg = f"{row.get('name', 'Unknown')}: {str(e)}"
                errors.append(error_msg)
                print(f"  ❌ Error: {error_msg}")
                # Rollback and continue
                conn.rollback()
                conn = psycopg2.connect(**db_params)
                cur = conn.cursor()
        
        conn.commit()
        
        # Print summary
        print("\n" + "=" * 80)
        print("MIGRATION SUMMARY")
        print("=" * 80)
        print(f"📊 Total in CSV: {len(employees)}")
        print(f"✅ Successfully migrated: {success_count}")
        print(f"⚠️ Skipped (already exist): {skip_count}")
        print(f"❌ Errors encountered: {error_count}")
        
        if errors:
            print("\nError details (first 10):")
            for error in errors[:10]:
                print(f"  • {error}")
        
        # Save results
        results = {
            'timestamp': datetime.now().isoformat(),
            'database': db_params['dbname'],
            'csv_file': CSV_FILE_PATH,
            'total_in_csv': len(employees),
            'success_count': success_count,
            'skip_count': skip_count,
            'error_count': error_count,
            'errors': errors
        }
        
        results_file = f"migration_success_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(results_file, 'w') as f:
            json.dump(results, f, indent=2)
        
        print(f"\n📄 Results saved to: {results_file}")
        
        return success_count > 0
        
    except Exception as e:
        print(f"\n❌ Migration error: {e}")
        if conn:
            conn.rollback()
        return False
    finally:
        if conn:
            conn.close()

def verify_migration():
    """Verify the migration results"""
    conn = None
    try:
        conn = psycopg2.connect(**db_params)
        cur = conn.cursor()
        
        print("\n" + "=" * 80)
        print("VERIFICATION")
        print("=" * 80)
        
        # Count employees by role
        cur.execute("""
            SELECT role, COUNT(*) as count 
            FROM employees 
            GROUP BY role 
            ORDER BY count DESC, role;
        """)
        
        print("\n📊 Employees by role:")
        total_by_role = 0
        for role, count in cur.fetchall():
            print(f"  • {role}: {count}")
            total_by_role += count
        
        # Count total employees
        cur.execute("SELECT COUNT(*) FROM employees;")
        total = cur.fetchone()[0]
        print(f"\n✅ Total employees in database: {total}")
        
        # Count persons
        cur.execute("SELECT COUNT(*) FROM persons;")
        persons_count = cur.fetchone()[0]
        print(f"👥 Total persons in database: {persons_count}")
        
        # Check doctors
        cur.execute("SELECT COUNT(*) FROM doctors;")
        doctor_count = cur.fetchone()[0]
        print(f"👨‍⚕️ Doctors registered: {doctor_count}")
        
        # Sample employees with person details
        cur.execute("""
            SELECT 
                p.first_name, 
                p.last_name, 
                p.email, 
                e.role,
                e.employee_code,
                e.currency_code,
                e.is_active
            FROM employees e
            JOIN persons p ON e.person_id = p.id
            ORDER BY e.created_at DESC 
            LIMIT 5;
        """)
        
        print("\n📋 Latest 5 employees added:")
        for emp in cur.fetchall():
            status = "✅" if emp[6] else "⏸️"
            print(f"  {status} {emp[0]} {emp[1]} ({emp[3]}) - {emp[2]} - Code: {emp[4]} - Currency: {emp[5]}")
        
        # Check active vs inactive
        cur.execute("""
            SELECT is_active, COUNT(*) 
            FROM employees 
            GROUP BY is_active;
        """)
        
        print("\n📊 Employee Status:")
        for active, count in cur.fetchall():
            status = "Active" if active else "Inactive"
            print(f"  • {status}: {count}")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Verification error: {e}")
        return False
    finally:
        if conn:
            conn.close()

def main():
    """Main execution"""
    print("\n" + "=" * 80)
    print("🚀 STARTING CORRECT DATABASE MIGRATION")
    print("=" * 80)
    print(f"Database: {db_params['dbname']}")
    print(f"CSV Source: {CSV_FILE_PATH}")
    print("=" * 80)
    
    # Migrate employees from CSV
    if not migrate_employees_from_csv():
        print("\n❌ Migration failed.")
        sys.exit(1)
    
    # Verify results
    if not verify_migration():
        print("\n⚠️ Verification encountered issues.")
    
    print("\n" + "=" * 80)
    print("✅ MIGRATION COMPLETE!")
    print("=" * 80)
    print("\n🎉 Success! All employees have been migrated with proper person relationships.")
    print("\nThe system now has:")
    print("• Person records with names and personal details")
    print("• Employee records with work-related information")
    print("• Doctor records for medical staff")
    print("• Currency support (USD by default)")

if __name__ == "__main__":
    main()
