#!/usr/bin/env python3
"""
Direct Database Migration Script - Add currency column and migrate employees from CSV
"""

import psycopg2
import csv
import json
from datetime import datetime
import sys
import re

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

def add_currency_column():
    """Add currency_code column to employees table if it doesn't exist"""
    conn = None
    try:
        conn = psycopg2.connect(**db_params)
        cur = conn.cursor()
        
        print("=" * 80)
        print("STEP 1: ADDING CURRENCY_CODE COLUMN TO EMPLOYEES TABLE")
        print("=" * 80)
        print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("-" * 80)
        
        # Check if column already exists
        cur.execute("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name = 'employees' 
            AND column_name = 'currency_code';
        """)
        
        if cur.fetchone():
            print("✅ currency_code column already exists in employees table")
            return True
        
        # Add the currency_code column with default USD
        print("Adding currency_code column to employees table...")
        cur.execute("""
            ALTER TABLE employees 
            ADD COLUMN currency_code VARCHAR(3) DEFAULT 'USD';
        """)
        
        print("✅ Column added successfully")
        
        # Add foreign key constraint
        print("\nAdding foreign key constraint...")
        cur.execute("""
            ALTER TABLE employees 
            ADD CONSTRAINT fk_employee_currency 
            FOREIGN KEY (currency_code) 
            REFERENCES currencies(currency_code)
            ON DELETE SET NULL;
        """)
        
        print("✅ Foreign key constraint added")
        
        # Update all existing employees to have USD as default
        print("\nSetting default currency for existing employees...")
        cur.execute("""
            UPDATE employees 
            SET currency_code = 'USD' 
            WHERE currency_code IS NULL;
        """)
        
        affected = cur.rowcount
        print(f"✅ Updated {affected} employee records with default currency (USD)")
        
        conn.commit()
        print("\n✅ Database changes committed successfully!")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Error adding currency column: {e}")
        if conn:
            conn.rollback()
        return False
    finally:
        if conn:
            conn.close()

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
            return f"{year}-{month.zfill(2)}-{day.zfill(2)}"
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
    """Migrate employees directly from CSV to database"""
    conn = None
    try:
        print("\n" + "=" * 80)
        print("STEP 2: MIGRATING EMPLOYEES FROM CSV")
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
            'staff': 'receptionist',  # Map staff to receptionist
            'manager': 'doctor',  # Map manager to doctor for now
            'finance': 'receptionist',  # Map finance to receptionist
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
                
                # Get phone
                phone = clean_phone(row.get('phone_mobile', '')) or clean_phone(row.get('phone_home', ''))
                
                # Get role
                role_raw = row.get('role', '').strip().lower()
                role = role_mapping.get(role_raw, 'receptionist')
                
                # Get ID number (use temp_id as ID)
                id_number = row.get('temp_id', '')
                if not id_number:
                    id_number = f"EMP{datetime.now().timestamp():.0f}"
                
                # Parse dates
                hire_date = parse_date(row.get('from_date', ''))
                if not hire_date:
                    hire_date = '2024-01-01'  # Default hire date
                
                # Check if employee already exists
                cur.execute("""
                    SELECT id, first_name, last_name 
                    FROM employees 
                    WHERE email = %s OR (first_name = %s AND last_name = %s)
                """, (email, first_name, last_name))
                
                existing = cur.fetchone()
                if existing:
                    skip_count += 1
                    print(f"  ⚠️ Skipping {first_name} {last_name} - already exists (ID: {existing[0]})")
                    continue
                
                # Insert employee
                cur.execute("""
                    INSERT INTO employees 
                    (first_name, last_name, email, phone, role, id_number, 
                     is_active, currency_code, created_at, updated_at)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, NOW(), NOW())
                    RETURNING id;
                """, (
                    first_name,
                    last_name,
                    email,
                    phone,
                    role,
                    id_number,
                    True,
                    'USD'  # Default currency
                ))
                
                emp_id = cur.fetchone()[0]
                
                # If doctor, add to doctors table
                if role == 'doctor':
                    license_number = row.get('license_number', '') or f"DOC{emp_id:05d}"
                    cur.execute("""
                        INSERT INTO doctors 
                        (employee_id, license_number, created_at, updated_at)
                        VALUES (%s, %s, NOW(), NOW())
                        ON CONFLICT (employee_id) DO NOTHING;
                    """, (emp_id, license_number))
                
                success_count += 1
                print(f"  ✅ Migrated: {first_name} {last_name} ({role}) - ID: {emp_id}")
                
            except Exception as e:
                error_count += 1
                error_msg = f"{row.get('name', 'Unknown')}: {str(e)}"
                errors.append(error_msg)
                print(f"  ❌ Error: {error_msg}")
                # Don't stop on error, continue with next employee
                conn.rollback()  # Rollback this transaction
                conn = psycopg2.connect(**db_params)  # Reconnect
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
        
        # Save results to file
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
        
        results_file = f"migration_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(results_file, 'w') as f:
            json.dump(results, f, indent=2)
        
        print(f"\n📄 Detailed results saved to: {results_file}")
        
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
        print("STEP 3: VERIFICATION")
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
        
        # Check currency distribution
        cur.execute("""
            SELECT currency_code, COUNT(*) as count 
            FROM employees 
            WHERE currency_code IS NOT NULL
            GROUP BY currency_code 
            ORDER BY currency_code;
        """)
        
        currency_results = cur.fetchall()
        if currency_results:
            print("\n💰 Employees by currency:")
            for currency, count in currency_results:
                print(f"  • {currency}: {count}")
        
        # Check doctors
        cur.execute("SELECT COUNT(*) FROM doctors;")
        doctor_count = cur.fetchone()[0]
        print(f"\n👨‍⚕️ Doctors registered: {doctor_count}")
        
        # Sample employees
        cur.execute("""
            SELECT first_name, last_name, email, role, currency_code 
            FROM employees 
            ORDER BY created_at DESC 
            LIMIT 5;
        """)
        
        print("\n📋 Latest 5 employees added:")
        for emp in cur.fetchall():
            print(f"  • {emp[0]} {emp[1]} ({emp[3]}) - {emp[2]} - Currency: {emp[4]}")
        
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
    print("🚀 STARTING DIRECT DATABASE MIGRATION")
    print("=" * 80)
    print(f"Database: {db_params['dbname']}")
    print(f"CSV Source: {CSV_FILE_PATH}")
    print("=" * 80)
    
    # Step 1: Add currency column
    if not add_currency_column():
        print("\n⚠️ Currency column issue, but continuing...")
    
    # Step 2: Migrate employees from CSV
    if not migrate_employees_from_csv():
        print("\n❌ Migration failed.")
        sys.exit(1)
    
    # Step 3: Verify results
    if not verify_migration():
        print("\n⚠️ Verification encountered issues.")
    
    print("\n" + "=" * 80)
    print("✅ MIGRATION COMPLETE!")
    print("=" * 80)
    print("\nNext steps:")
    print("1. Review the migration results file")
    print("2. Check the database for migrated employees")
    print("3. Test application with the new data")
    print("4. Consider updating employee salaries and other details as needed")

if __name__ == "__main__":
    main()
