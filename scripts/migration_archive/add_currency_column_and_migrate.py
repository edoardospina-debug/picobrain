#!/usr/bin/env python3
"""
Add currency_code column to employees table and run migration
"""

import psycopg2
import json
from datetime import datetime
import sys

# Database connection parameters
db_params = {
    'dbname': 'picobraindb',
    'user': 'edo',
    'password': '',
    'host': 'localhost',
    'port': '5432'
}

def add_currency_column():
    """Add currency_code column to employees table"""
    conn = None
    try:
        conn = psycopg2.connect(**db_params)
        cur = conn.cursor()
        
        print("=" * 80)
        print("ADDING CURRENCY_CODE COLUMN TO EMPLOYEES TABLE")
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
            REFERENCES currencies(currency_code);
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

def migrate_employees():
    """Migrate employees from the Excel source"""
    conn = None
    try:
        conn = psycopg2.connect(**db_params)
        cur = conn.cursor()
        
        print("\n" + "=" * 80)
        print("MIGRATING EMPLOYEES FROM EXCEL DATA")
        print("=" * 80)
        
        # Read the employee data from the Excel JSON export
        import os
        json_file = '/Users/edo/Desktop/Excel Employee Data Export.json'
        
        if not os.path.exists(json_file):
            print(f"❌ Excel data file not found: {json_file}")
            return False
        
        with open(json_file, 'r', encoding='utf-8') as f:
            excel_data = json.load(f)
        
        employees = excel_data.get('employees', [])
        print(f"Found {len(employees)} employees to migrate")
        
        success_count = 0
        error_count = 0
        errors = []
        
        for emp in employees:
            try:
                # Map role from Excel
                role_mapping = {
                    'staff': 'receptionist',
                    'doctor': 'doctor',
                    'nurse': 'nurse',
                    'receptionist': 'receptionist'
                }
                
                role = role_mapping.get(emp.get('Role', '').lower(), 'receptionist')
                
                # Prepare employee data
                first_name = emp.get('First Name', '')
                last_name = emp.get('Last Name', '')
                email = emp.get('Email', '')
                phone = emp.get('Phone', '')
                id_number = emp.get('ID', '')
                
                # Generate email if missing
                if not email and first_name and last_name:
                    email = f"{first_name.lower()}.{last_name.lower()}@clinic.com"
                
                # Check if employee already exists
                cur.execute("""
                    SELECT id FROM employees 
                    WHERE email = %s OR id_number = %s
                """, (email, id_number))
                
                if cur.fetchone():
                    print(f"  ⚠️ Skipping {first_name} {last_name} - already exists")
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
                    license_number = f"DOC{emp_id:05d}"
                    cur.execute("""
                        INSERT INTO doctors 
                        (employee_id, license_number, created_at, updated_at)
                        VALUES (%s, %s, NOW(), NOW())
                        ON CONFLICT (employee_id) DO NOTHING;
                    """, (emp_id, license_number))
                
                success_count += 1
                print(f"  ✅ Migrated: {first_name} {last_name} ({role})")
                
            except Exception as e:
                error_count += 1
                error_msg = f"{emp.get('First Name', '')} {emp.get('Last Name', '')}: {str(e)}"
                errors.append(error_msg)
                print(f"  ❌ Error: {error_msg}")
        
        conn.commit()
        
        # Print summary
        print("\n" + "=" * 80)
        print("MIGRATION SUMMARY")
        print("=" * 80)
        print(f"✅ Successfully migrated: {success_count} employees")
        print(f"❌ Errors encountered: {error_count}")
        
        if errors:
            print("\nError details:")
            for error in errors[:10]:  # Show first 10 errors
                print(f"  • {error}")
        
        # Save results to file
        results = {
            'timestamp': datetime.now().isoformat(),
            'database': db_params['dbname'],
            'total_employees': len(employees),
            'success_count': success_count,
            'error_count': error_count,
            'errors': errors
        }
        
        results_file = f"migration_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
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
            ORDER BY role;
        """)
        
        print("\n📊 Employees by role:")
        for role, count in cur.fetchall():
            print(f"  • {role}: {count}")
        
        # Count total employees
        cur.execute("SELECT COUNT(*) FROM employees;")
        total = cur.fetchone()[0]
        print(f"\n✅ Total employees in database: {total}")
        
        # Check currency distribution
        cur.execute("""
            SELECT currency_code, COUNT(*) as count 
            FROM employees 
            GROUP BY currency_code 
            ORDER BY currency_code;
        """)
        
        print("\n💰 Employees by currency:")
        for currency, count in cur.fetchall():
            print(f"  • {currency}: {count}")
        
        # Check doctors
        cur.execute("SELECT COUNT(*) FROM doctors;")
        doctor_count = cur.fetchone()[0]
        print(f"\n👨‍⚕️ Doctors registered: {doctor_count}")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Verification error: {e}")
        return False
    finally:
        if conn:
            conn.close()

def main():
    """Main execution"""
    print("\n🚀 STARTING CURRENCY COLUMN ADDITION AND MIGRATION")
    print("=" * 80)
    
    # Step 1: Add currency column
    if not add_currency_column():
        print("\n❌ Failed to add currency column. Aborting.")
        sys.exit(1)
    
    # Step 2: Migrate employees
    if not migrate_employees():
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
    print("2. Test the application with the migrated data")
    print("3. Update any application configurations if needed")

if __name__ == "__main__":
    main()
