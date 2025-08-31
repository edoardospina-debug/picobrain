#!/usr/bin/env python3
"""
Quick diagnostic to check if currencies table exists and show employee migration readiness
"""

import psycopg2
import json
import sys

DB_CONFIG = {
    'dbname': 'picobraindb',
    'user': 'edo',
    'password': 'edopico',
    'host': 'localhost',
    'port': 5432
}

def check_database():
    print("\n" + "="*60)
    print("PICOBRAIN DATABASE DIAGNOSTIC")
    print("="*60)
    
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        print("✅ Database connection successful")
        
        # Check for currencies table
        print("\n1. Checking currencies table...")
        cur.execute("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables 
                WHERE table_schema = 'public' 
                AND table_name = 'currencies'
            );
        """)
        currencies_exists = cur.fetchone()[0]
        
        if currencies_exists:
            print("   ✅ Currencies table EXISTS")
            cur.execute("SELECT COUNT(*) FROM currencies;")
            count = cur.fetchone()[0]
            print(f"   ✅ Contains {count} currencies")
            
            cur.execute("SELECT currency_code, currency_name FROM currencies LIMIT 3;")
            for code, name in cur.fetchall():
                print(f"      - {code}: {name}")
        else:
            print("   ❌ Currencies table DOES NOT EXIST")
            return False
        
        # Check for other required tables
        print("\n2. Checking other required tables...")
        tables = ['persons', 'employees', 'clinics', 'users']
        for table in tables:
            cur.execute(f"""
                SELECT EXISTS (
                    SELECT FROM information_schema.tables 
                    WHERE table_schema = 'public' 
                    AND table_name = '{table}'
                );
            """)
            exists = cur.fetchone()[0]
            if exists:
                cur.execute(f"SELECT COUNT(*) FROM {table};")
                count = cur.fetchone()[0]
                print(f"   ✅ {table}: EXISTS ({count} records)")
            else:
                print(f"   ❌ {table}: MISSING")
        
        # Check foreign key constraint
        print("\n3. Checking employees table foreign keys...")
        cur.execute("""
            SELECT
                tc.constraint_name,
                kcu.column_name,
                ccu.table_name AS foreign_table_name,
                ccu.column_name AS foreign_column_name
            FROM
                information_schema.table_constraints AS tc
                JOIN information_schema.key_column_usage AS kcu
                  ON tc.constraint_name = kcu.constraint_name
                JOIN information_schema.constraint_column_usage AS ccu
                  ON ccu.constraint_name = tc.constraint_name
            WHERE tc.table_name = 'employees'
                AND tc.constraint_type = 'FOREIGN KEY';
        """)
        
        fks = cur.fetchall()
        if fks:
            for constraint_name, column_name, foreign_table, foreign_column in fks:
                if 'currencies' in foreign_table:
                    print(f"   ⚠️  {column_name} -> {foreign_table}.{foreign_column}")
                else:
                    print(f"   ✅ {column_name} -> {foreign_table}.{foreign_column}")
        else:
            print("   ℹ️  No foreign keys found")
        
        cur.close()
        conn.close()
        
        print("\n" + "="*60)
        if currencies_exists:
            print("✅ DATABASE IS READY FOR MIGRATION!")
            print("\nRun: python3 minimal_migration.py")
        else:
            print("❌ DATABASE NOT READY - Currencies table missing")
            print("\nRun: python3 create_currencies_table.py")
        print("="*60)
        
        return currencies_exists
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return False

if __name__ == "__main__":
    success = check_database()
    sys.exit(0 if success else 1)
