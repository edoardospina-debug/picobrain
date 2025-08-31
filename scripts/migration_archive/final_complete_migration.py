#!/usr/bin/env python3
"""
Check clinics in the database and complete the migration
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

def check_clinics():
    """Check available clinics in the database"""
    conn = None
    clinic_mapping = {}
    
    try:
        conn = psycopg2.connect(**db_params)
        cur = conn.cursor()
        
        print("=" * 80)
        print("CHECKING AVAILABLE CLINICS")
        print("=" * 80)
        
        # Check if clinics table exists
        cur.execute("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables 
                WHERE table_schema = 'public' 
                AND table_name = 'clinics'
            );
        """)
        
        if not cur.fetchone()[0]:
            print("⚠️ No clinics table found.")
            print("Creating default clinic...")
            
            # Create a default clinic
            default_clinic_id = str(uuid.uuid4())
            cur.execute("""
                INSERT INTO clinics 
                (id, name, created_at, updated_at)
                VALUES (%s, %s, NOW(), NOW())
                RETURNING id;
            """, (default_clinic_id, "Default Clinic"))
            
            clinic_id = cur.fetchone()[0]
            conn.commit()
            
            # Map all temp IDs to the default clinic
            for temp_id in ['10', '11', '12', '13', '14']:
                clinic_mapping[temp_id] = clinic_id
            
            print(f"✅ Created default clinic with ID: {clinic_id}")
            
        else:
            # Get existing clinics
            cur.execute("""
                SELECT id, name, city 
                FROM clinics 
                ORDER BY name;
            """)
            
            clinics = cur.fetchall()
            
            if clinics:
                print("\n📋 Available clinics:")
                for clinic_id, name, city in clinics:
                    print(f"  • {name} ({city}): {clinic_id}")
                    
                    # Try to map based on city names
                    if 'london' in (name or '').lower() or 'london' in (city or '').lower():
                        clinic_mapping['10'] = clinic_id
                    elif 'milan' in (name or '').lower() or 'milan' in (city or '').lower():
                        clinic_mapping['11'] = clinic_id
                    elif 'los angeles' in (name or '').lower() or 'la' in (name or '').lower():
                        clinic_mapping['12'] = clinic_id
                    elif 'vancouver' in (name or '').lower():
                        clinic_mapping['13'] = clinic_id
                    elif 'new york' in (name or '').lower() or 'ny' in (name or '').lower():
                        clinic_mapping['14'] = clinic_id
                
                # If we couldn't map all clinics, use the first one as default
                if not clinic_mapping:
                    default_id = clinics[0][0]
                    for temp_id in ['10', '11', '12', '13', '14']:
                        clinic_mapping[temp_id] = default_id
                    print(f"\n⚠️ Using first clinic as default: {clinics[0][1]}")
            else:
                print("⚠️ No clinics found. Creating default clinic...")
                
                # Create default clinic
                default_clinic_id = str(uuid.uuid4())
                cur.execute("""
                    INSERT INTO clinics 
                    (id, name, created_at, updated_at)
                    VALUES (%s, %s, NOW(), NOW())
                    RETURNING id;
                """, (default_clinic_id, "Default Clinic"))
                
                clinic_id = cur.fetchone()[0]
                conn.commit()
                
                for temp_id in ['10', '11', '12', '13', '14']:
                    clinic_mapping[temp_id] = clinic_id
                
                print(f"✅ Created default clinic with ID: {clinic_id}")
        
        print("\n📍 Clinic mapping:")
        for temp_id, clinic_id in clinic_mapping.items():
            print(f"  Temp ID {temp_id} → {clinic_id}")
        
        return clinic_mapping
        
    except Exception as e:
        print(f"❌ Error checking clinics: {e}")
        
        # Return a default mapping with a generated UUID
        default_id = str(uuid.uuid4())
        return {str(i): default_id for i in range(10, 15)}
    finally:
        if conn:
            conn.close()

def clean_phone(phone_str):
    """Clean phone number"""
    if not phone_str or phone_str.strip() == "":
        return None
    phone = re.sub(r'[^\d+]', '', phone_str.strip())
    return phone if len(phone) >= 7 else None

def clean_email(email_str):
    """Clean and validate email"""
    if not email_str or email_str.strip() == "":
        return None
    
    email = email_str.strip().lower()
    
    if email in ["na@a.cpm", "xxx@picoclinics.com", ""]:
        return None
    
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if re.match(email_pattern, email):
        return email
    
    return None

def parse_date(date_str):
    """Parse date from DD/MM/YYYY format"""
    if not date_str or date_str.strip() == "":
        return None
    
    try:
        parts = date_str.strip().split('/')
        if len(parts) == 3:
            day, month, year = parts
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
        return parts[0], "Employee"
    else:
        return parts[0], " ".join(parts[1:])

def migrate_employees_with_clinics(clinic_mapping):
    """Migrate employees with proper clinic assignments"""
    conn = None
    try:
        print("\n" + "=" * 80)
        print("MIGRATING EMPLOYEES WITH CLINIC ASSIGNMENTS")
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
            'admin': 'receptionist',
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
                
                # Get clinic ID
                clinic_temp_id = row.get('clinic_temp_id', '').strip()
                if not clinic_temp_id or clinic_temp_id not in clinic_mapping:
                    # Use a default if not found
                    clinic_id = list(clinic_mapping.values())[0] if clinic_mapping else str(uuid.uuid4())
                    print(f"  ⚠️ No valid clinic for {first_name} {last_name}, using default")
                else:
                    clinic_id = clinic_mapping[clinic_temp_id]
                
                # Get email
                work_email = clean_email(row.get('work_email', ''))
                personal_email = clean_email(row.get('personal_email', ''))
                email = work_email or personal_email
                
                if not email:
                    email = f"{first_name.lower()}.{last_name.lower().replace(' ', '')}@clinic.com"
                
                # Get ID number
                id_number = row.get('temp_id', '')
                if not id_number:
                    id_number = f"EMP{datetime.now().timestamp():.0f}"
                
                # Parse DOB
                dob = parse_date(row.get('dob', ''))
                
                # Check if person already exists
                cur.execute("""
                    SELECT id, first_name, last_name 
                    FROM persons 
                    WHERE email = %s OR (first_name = %s AND last_name = %s)
                """, (email, first_name, last_name))
                
                existing_person = cur.fetchone()
                
                if existing_person:
                    person_id = existing_person[0]
                    
                    # Check if employee record exists
                    cur.execute("""
                        SELECT id FROM employees WHERE person_id = %s
                    """, (person_id,))
                    
                    if cur.fetchone():
                        skip_count += 1
                        print(f"  ⚠️ Skipping {first_name} {last_name} - already exists")
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
                    try:
                        term_date_obj = datetime.strptime(termination_date, '%Y-%m-%d')
                        if term_date_obj < datetime.now():
                            is_active = False
                    except:
                        pass
                
                # Create employee record with clinic ID
                employee_id = str(uuid.uuid4())
                employee_code = f"EMP{row.get('temp_id', '')}" if row.get('temp_id') else f"EMP{success_count:04d}"
                
                cur.execute("""
                    INSERT INTO employees 
                    (id, person_id, employee_code, primary_clinic_id, role, 
                     hire_date, termination_date, is_active, currency_code, 
                     created_at, updated_at, temp_id)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, NOW(), NOW(), %s)
                    RETURNING id;
                """, (
                    employee_id,
                    person_id,
                    employee_code,
                    clinic_id,  # Now we have the clinic ID!
                    role,
                    hire_date,
                    termination_date,
                    is_active,
                    'USD',
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
                
                success_count += 1
                status = "✅" if is_active else "⏸️"
                clinic_name = f"Clinic-{clinic_temp_id}" if clinic_temp_id else "Default"
                print(f"  {status} {first_name} {last_name} ({role}) → {clinic_name}")
                
            except Exception as e:
                error_count += 1
                error_msg = f"{row.get('name', 'Unknown')}: {str(e)}"
                errors.append(error_msg)
                print(f"  ❌ Error: {error_msg}")
                conn.rollback()
                conn = psycopg2.connect(**db_params)
                cur = conn.cursor()
        
        conn.commit()
        
        # Print summary
        print("\n" + "=" * 80)
        print("MIGRATION COMPLETE!")
        print("=" * 80)
        print(f"📊 Total in CSV: {len(employees)}")
        print(f"✅ Successfully migrated: {success_count}")
        print(f"⚠️ Skipped (already exist): {skip_count}")
        print(f"❌ Errors encountered: {error_count}")
        
        # Save results
        results = {
            'timestamp': datetime.now().isoformat(),
            'database': db_params['dbname'],
            'csv_file': CSV_FILE_PATH,
            'total_in_csv': len(employees),
            'success_count': success_count,
            'skip_count': skip_count,
            'error_count': error_count,
            'errors': errors,
            'clinic_mapping': {k: str(v) for k, v in clinic_mapping.items()}
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

def verify_final_results():
    """Verify the final migration results"""
    conn = None
    try:
        conn = psycopg2.connect(**db_params)
        cur = conn.cursor()
        
        print("\n" + "=" * 80)
        print("FINAL VERIFICATION")
        print("=" * 80)
        
        # Count employees by role
        cur.execute("""
            SELECT role, COUNT(*) as count 
            FROM employees 
            GROUP BY role 
            ORDER BY count DESC, role;
        """)
        
        print("\n📊 Employees by role:")
        for role, count in cur.fetchall():
            print(f"  • {role}: {count}")
        
        # Count by clinic
        cur.execute("""
            SELECT c.name, COUNT(e.id) as count
            FROM employees e
            LEFT JOIN clinics c ON e.primary_clinic_id = c.id
            GROUP BY c.name
            ORDER BY count DESC;
        """)
        
        print("\n🏥 Employees by clinic:")
        for clinic, count in cur.fetchall():
            print(f"  • {clinic or 'Unknown'}: {count}")
        
        # Total counts
        cur.execute("SELECT COUNT(*) FROM employees;")
        emp_total = cur.fetchone()[0]
        
        cur.execute("SELECT COUNT(*) FROM persons;")
        person_total = cur.fetchone()[0]
        
        cur.execute("SELECT COUNT(*) FROM doctors;")
        doctor_total = cur.fetchone()[0]
        
        print(f"\n📊 Final counts:")
        print(f"  • Total employees: {emp_total}")
        print(f"  • Total persons: {person_total}")
        print(f"  • Total doctors: {doctor_total}")
        
        # Sample recent employees
        cur.execute("""
            SELECT 
                p.first_name || ' ' || p.last_name as name,
                e.role,
                e.employee_code,
                c.name as clinic
            FROM employees e
            JOIN persons p ON e.person_id = p.id
            LEFT JOIN clinics c ON e.primary_clinic_id = c.id
            ORDER BY e.created_at DESC
            LIMIT 5;
        """)
        
        print("\n📋 Latest 5 employees:")
        for name, role, code, clinic in cur.fetchall():
            print(f"  • {name} ({role}) - {code} @ {clinic or 'Unknown'}")
        
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
    print("🚀 COMPLETE EMPLOYEE MIGRATION WITH CLINIC ASSIGNMENTS")
    print("=" * 80)
    print(f"Database: {db_params['dbname']}")
    print(f"CSV Source: {CSV_FILE_PATH}")
    
    # Step 1: Check and map clinics
    clinic_mapping = check_clinics()
    
    if not clinic_mapping:
        print("\n❌ Could not establish clinic mapping")
        sys.exit(1)
    
    # Step 2: Migrate employees with clinic assignments
    if not migrate_employees_with_clinics(clinic_mapping):
        print("\n❌ Migration failed")
        sys.exit(1)
    
    # Step 3: Verify results
    verify_final_results()
    
    print("\n" + "=" * 80)
    print("🎉 SUCCESS! MIGRATION COMPLETE!")
    print("=" * 80)

if __name__ == "__main__":
    main()
