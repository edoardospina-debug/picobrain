#!/usr/bin/env python3
"""
Check the status of the currencies table in the database
"""

import psycopg2
import json
from datetime import datetime

# Database connection parameters
db_params = {
    'dbname': 'picobraindb',  # Correct database name
    'user': 'edo',
    'password': '',
    'host': 'localhost',
    'port': '5432'
}

def check_currencies_table():
    """Check if currencies table exists and get its data"""
    conn = None
    try:
        conn = psycopg2.connect(**db_params)
        cur = conn.cursor()
        
        print("=" * 80)
        print("CURRENCIES TABLE STATUS CHECK")
        print("=" * 80)
        print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Database: {db_params['dbname']}")
        print("-" * 80)
        
        # Check if currencies table exists
        cur.execute("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables 
                WHERE table_schema = 'public' 
                AND table_name = 'currencies'
            );
        """)
        table_exists = cur.fetchone()[0]
        
        if not table_exists:
            print("\n⚠️ CURRENCIES TABLE DOES NOT EXIST!")
            print("\nAction Required: Create the currencies table first")
            return False
        
        print("\n✅ CURRENCIES TABLE EXISTS!")
        
        # Get table schema
        print("\n📋 TABLE SCHEMA:")
        print("-" * 80)
        
        cur.execute("""
            SELECT 
                column_name,
                data_type,
                character_maximum_length,
                is_nullable,
                column_default
            FROM information_schema.columns
            WHERE table_name = 'currencies'
            ORDER BY ordinal_position;
        """)
        schema = cur.fetchall()
        
        print(f"{'Column Name':<20} | {'Data Type':<15} | {'Max Length':<10} | {'Nullable':<8} | {'Default'}")
        print("-" * 80)
        for col in schema:
            max_len = str(col[2]) if col[2] else '-'
            default = col[4] if col[4] else 'null'
            print(f"{col[0]:<20} | {col[1]:<15} | {max_len:<10} | {col[3]:<8} | {default}")
        
        # Get all data from currencies table
        print("\n📊 CURRENT DATA IN CURRENCIES TABLE:")
        print("-" * 80)
        
        cur.execute("SELECT * FROM currencies ORDER BY currency_code;")
        data = cur.fetchall()
        
        # Get column names for data display
        cur.execute("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name = 'currencies' 
            ORDER BY ordinal_position;
        """)
        columns = [col[0] for col in cur.fetchall()]
        
        if data:
            # Print header
            header = " | ".join(f"{col:<15}" for col in columns)
            print(header)
            print("-" * len(header))
            
            # Print data
            for row in data:
                row_str = " | ".join(f"{str(val):<15}" for val in row)
                print(row_str)
            
            print(f"\n✅ Total rows: {len(data)}")
        else:
            print("⚠️ Table is empty - no currency data found!")
        
        # Check foreign key constraints
        print("\n🔗 TABLES REFERENCING CURRENCIES:")
        print("-" * 80)
        
        cur.execute("""
            SELECT
                tc.table_name,
                kcu.column_name
            FROM information_schema.table_constraints AS tc
            JOIN information_schema.key_column_usage AS kcu
                ON tc.constraint_name = kcu.constraint_name
                AND tc.table_schema = kcu.table_schema
            JOIN information_schema.constraint_column_usage AS ccu
                ON ccu.constraint_name = tc.constraint_name
                AND ccu.table_schema = tc.table_schema
            WHERE tc.constraint_type = 'FOREIGN KEY' 
                AND ccu.table_name = 'currencies'
            ORDER BY tc.table_name;
        """)
        fk_constraints = cur.fetchall()
        
        if fk_constraints:
            for table, column in fk_constraints:
                print(f"  • {table}.{column} → currencies.currency_code")
        else:
            print("  No foreign key references found")
        
        # Check if employees table has currency_code column
        print("\n🔍 CHECKING EMPLOYEES TABLE:")
        print("-" * 80)
        
        cur.execute("""
            SELECT column_name, data_type
            FROM information_schema.columns
            WHERE table_name = 'employees' 
            AND column_name = 'currency_code'
        """)
        emp_currency_col = cur.fetchone()
        
        if emp_currency_col:
            print(f"  ✅ employees.currency_code exists (type: {emp_currency_col[1]})")
        else:
            print("  ⚠️ employees.currency_code column NOT FOUND")
        
        print("\n" + "=" * 80)
        print("STATUS CHECK COMPLETE")
        print("=" * 80)
        
        return True
        
    except Exception as e:
        print(f"\n❌ DATABASE ERROR: {e}")
        return False
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    check_currencies_table()
