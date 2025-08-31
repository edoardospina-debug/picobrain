#!/usr/bin/env python3
"""
Check the actual schema of the employees table
"""

import psycopg2
from datetime import datetime

# Database connection parameters
db_params = {
    'dbname': 'picobraindb',
    'user': 'edo',
    'password': '',
    'host': 'localhost',
    'port': '5432'
}

def check_employees_table():
    """Check the schema of employees table"""
    conn = None
    try:
        conn = psycopg2.connect(**db_params)
        cur = conn.cursor()
        
        print("=" * 80)
        print("EMPLOYEES TABLE SCHEMA CHECK")
        print("=" * 80)
        
        # Check if employees table exists
        cur.execute("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables 
                WHERE table_schema = 'public' 
                AND table_name = 'employees'
            );
        """)
        
        if not cur.fetchone()[0]:
            print("❌ Employees table does not exist!")
            return
        
        print("✅ Employees table exists\n")
        
        # Get all columns
        cur.execute("""
            SELECT 
                column_name,
                data_type,
                character_maximum_length,
                is_nullable,
                column_default
            FROM information_schema.columns
            WHERE table_name = 'employees'
            ORDER BY ordinal_position;
        """)
        
        columns = cur.fetchall()
        
        print("📋 COLUMNS IN EMPLOYEES TABLE:")
        print("-" * 80)
        print(f"{'Column Name':<25} | {'Data Type':<20} | {'Max Length':<10} | {'Nullable':<8}")
        print("-" * 80)
        
        for col in columns:
            col_name = col[0]
            data_type = col[1]
            max_len = str(col[2]) if col[2] else '-'
            nullable = col[3]
            print(f"{col_name:<25} | {data_type:<20} | {max_len:<10} | {nullable:<8}")
        
        # Count existing records
        cur.execute("SELECT COUNT(*) FROM employees;")
        count = cur.fetchone()[0]
        print(f"\n📊 Current record count: {count}")
        
        # Sample a few records if they exist
        if count > 0:
            cur.execute("""
                SELECT * FROM employees LIMIT 3;
            """)
            
            # Get column names
            col_names = [desc[0] for desc in cur.description]
            
            print("\n📋 SAMPLE RECORDS:")
            print("-" * 80)
            
            records = cur.fetchall()
            for record in records:
                print("\nRecord:")
                for i, value in enumerate(record):
                    if value is not None:
                        print(f"  {col_names[i]}: {value}")
        
        # Check related tables
        print("\n🔗 RELATED TABLES:")
        print("-" * 80)
        
        # Check persons table
        cur.execute("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables 
                WHERE table_schema = 'public' 
                AND table_name = 'persons'
            );
        """)
        
        if cur.fetchone()[0]:
            print("✅ persons table exists")
            
            # Get persons table columns
            cur.execute("""
                SELECT column_name, data_type
                FROM information_schema.columns
                WHERE table_name = 'persons'
                ORDER BY ordinal_position
                LIMIT 10;
            """)
            
            print("\n  Key columns in persons table:")
            for col in cur.fetchall():
                print(f"    • {col[0]} ({col[1]})")
        
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    check_employees_table()
