#!/usr/bin/env python3
"""
Diagnose and fix migration issues - Find exactly what's blocking
"""

import psycopg2
import csv
import json
import uuid
from datetime import datetime

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

def diagnose_table_structure():
    """Check exact table structures and constraints"""
    conn = None
    try:
        conn = psycopg2.connect(**db_params)
        cur = conn.cursor()
        
        print("=" * 80)
        print("DIAGNOSING TABLE STRUCTURES")
        print("=" * 80)
        
        # Check employees table columns and constraints
        cur.execute("""
            SELECT 
                column_name,
                data_type,
                is_nullable,
                column_default
            FROM information_schema.columns
            WHERE table_name = 'employees'
            ORDER BY ordinal_position;
        """)
        
        print("\n📋 EMPLOYEES TABLE STRUCTURE:")
        print("-" * 80)
        for col in cur.fetchall():
            nullable = "NULL" if col[2] == 'YES' else "NOT NULL"
            default = f"DEFAULT {col[3]}" if col[3] else ""
            print(f"  {col[0]:<25} {col[1]:<20} {nullable:<10} {default}")
        
        # Check foreign key constraints
        cur.execute("""
            SELECT
                tc.constraint_name,
                kcu.column_name,
                ccu.table_name AS foreign_table,
                ccu.column_name AS foreign_column
            FROM information_schema.table_constraints AS tc
            JOIN information_schema.key_column_usage AS kcu
                ON tc.constraint_name = kcu.constraint_name
            JOIN information_schema.constraint_column_usage AS ccu
                ON ccu.constraint_name = tc.constraint_name
            WHERE tc.constraint_type = 'FOREIGN KEY' 
            AND tc.table_name = 'employees';
        """)
        
        print("\n🔗 FOREIGN KEY CONSTRAINTS:")
        print("-" * 80)
        for constraint in cur.fetchall():
            print(f"  {constraint[1]} → {constraint[2]}.{constraint[3]}")
        
        # Check if clinics table exists and has data
        cur.execute("""
            SELECT COUNT(*) FROM clinics;
        """)
        clinic_count = cur.fetchone()[0]
        print(f"\n🏥 Clinics in database: {clinic_count}")
        
        if clinic_count > 0:
            cur.execute("SELECT id, name FROM clinics LIMIT 1;")
            clinic = cur.fetchone()
            print(f"  Default clinic ID: {clinic[0]} ({clinic[1]})")
            return clinic[0]
        else:
            print("  ⚠️ No clinics found!")
            return None
        
    except Exception as e:
        print(f"❌ Diagnosis error: {e}")
        return None
    finally:
        if conn:
            conn.close()

def test_single_employee_migration(clinic_id):
    """Try to migrate just one employee to find the exact error"""
    conn = None
    try:
        conn = psycopg2.connect(**db_params)
        cur = conn.cursor()
        
        print("\n" + "=" * 80)
        print("TESTING SINGLE EMPLOYEE MIGRATION")
        print("=" * 80)
        
        # Read first employee from CSV
        with open(CSV_FILE_PATH, 'r', encoding='utf-8-sig') as file:
            reader = csv.DictReader(file)
            first_employee = next(reader)
        
        print(f"\n📋 Test employee: {first_employee.get('name', 'Unknown')}")
        print(f"  Role: {first_employee.get('role', 'Unknown')}")
        
        # Create person first
        person_id = str(uuid.uuid4())
        first_name = first_employee.get('first_name', 'Test')
        last_name = first_employee.get('last_name', 'Employee')
        email = f"test.employee@clinic.com"
        
        print(f"\n1️⃣ Creating person: {first_name} {last_name}")
        cur.execute("""
            INSERT INTO persons 
            (id, first_name, last_name, email, created_at, updated_at)
            VALUES (%s, %s, %s, %s, NOW(), NOW())
            RETURNING id;
        """, (person_id, first_name, last_name, email))
        
        person_id = cur.fetchone()[0]
        print(f"  ✅ Person created with ID: {person_id}")
        
        # Try to create employee
        print(f"\n2️⃣ Creating employee record...")
        employee_id = str(uuid.uuid4())
        
        # Get all required fields for employees table
        cur.execute("""
            SELECT column_name, is_nullable
            FROM information_schema.columns
            WHERE table_name = 'employees'
            AND is_nullable = 'NO'
            AND column_default IS NULL
            ORDER BY ordinal_position;
        """)
        
        required_fields = cur.fetchall()
        print("\n  Required fields (NOT NULL without defaults):")
        for field, _ in required_fields:
            print(f"    • {field}")
        
        # Prepare employee data based on what we found
        try:
            cur.execute("""
                INSERT INTO employees 
                (id, person_id, employee_code, primary_clinic_id, role, 
                 hire_date, is_active, created_at, updated_at)
                VALUES (%s, %s, %s, %s, %s, %s, %s, NOW(), NOW())
                RETURNING id;
            """, (
                employee_id,
                person_id,
                'EMP0001',
                clinic_id,
                'receptionist',
                '2024-01-01',
                True
            ))
            
            emp_id = cur.fetchone()[0]
            conn.commit()
            print(f"  ✅ Employee created successfully with ID: {emp_id}")
            return True
            
        except Exception as e:
            print(f"  ❌ Employee creation failed: {e}")
            print(f"\n  🔍 Error details: {str(e)}")
            conn.rollback()
            
            # Try to identify the exact issue
            if "null value" in str(e).lower():
                print("  ⚠️ Missing required field(s)")
            elif "foreign key" in str(e).lower():
                print("  ⚠️ Foreign key constraint violation")
            elif "unique" in str(e).lower():
                print("  ⚠️ Duplicate key violation")
            
            return False
        
    except Exception as e:
        print(f"❌ Test migration error: {e}")
        return False
    finally:
        if conn:
            conn.close()

def fix_missing_requirements():
    """Fix any missing requirements"""
    conn = None
    try:
        conn = psycopg2.connect(**db_params)
        cur = conn.cursor()
        
        print("\n" + "=" * 80)
        print("FIXING MISSING REQUIREMENTS")
        print("=" * 80)
        
        # Ensure clinics table exists and has at least one clinic
        cur.execute("""
            SELECT COUNT(*) FROM clinics;
        """)
        
        if cur.fetchone()[0] == 0:
            print("Creating default clinic...")
            clinic_id = str(uuid.uuid4())
            cur.execute("""
                INSERT INTO clinics 
                (id, name, address, city, country, created_at, updated_at)
                VALUES (%s, %s, %s, %s, %s, NOW(), NOW())
                RETURNING id;
            """, (clinic_id, "PicoClinics Main", "123 Main St", "London", "UK"))
            
            clinic_id = cur.fetchone()[0]
            conn.commit()
            print(f"✅ Created default clinic: {clinic_id}")
            return clinic_id
        else:
            cur.execute("SELECT id FROM clinics LIMIT 1;")
            clinic_id = cur.fetchone()[0]
            print(f"✅ Using existing clinic: {clinic_id}")
            return clinic_id
        
    except Exception as e:
        print(f"❌ Fix error: {e}")
        return None
    finally:
        if conn:
            conn.close()

def main():
    """Main diagnostic execution"""
    print("\n" + "=" * 80)
    print("🔍 MIGRATION DIAGNOSTIC AND FIX")
    print("=" * 80)
    
    # Step 1: Diagnose table structure
    clinic_id = diagnose_table_structure()
    
    # Step 2: Fix missing requirements
    if not clinic_id:
        clinic_id = fix_missing_requirements()
    
    if not clinic_id:
        print("\n❌ Could not establish clinic")
        return
    
    # Step 3: Test single employee migration
    print(f"\n🏥 Using clinic ID: {clinic_id}")
    
    if test_single_employee_migration(clinic_id):
        print("\n" + "=" * 80)
        print("✅ DIAGNOSTIC COMPLETE - MIGRATION IS POSSIBLE!")
        print("=" * 80)
        print("\nThe test migration succeeded! The issue was likely:")
        print("• Missing clinic ID")
        print("• Or missing required fields")
        print("\nYou can now run the full migration with the correct clinic ID.")
        print(f"\nUse this clinic ID for migration: {clinic_id}")
    else:
        print("\n" + "=" * 80)
        print("❌ DIAGNOSTIC FOUND BLOCKING ISSUES")
        print("=" * 80)
        print("\nPlease check the error details above to understand what's blocking.")

if __name__ == "__main__":
    main()
