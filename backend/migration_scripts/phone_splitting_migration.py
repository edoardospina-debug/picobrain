#!/usr/bin/env python3
"""
Database migration script to:
1. Add temp_id to Employees and Clients tables
2. Split phone fields in Persons and Clinics tables
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy import create_engine, text, inspect
from sqlalchemy.exc import SQLAlchemyError
from app.core.config import settings

def execute_migration():
    """Execute the phone splitting migration"""
    
    # Create database connection
    engine = create_engine(settings.DATABASE_URL)
    
    print("🔄 Starting database migration...")
    print(f"Database: {settings.DATABASE_URL}")
    
    try:
        with engine.connect() as conn:
            # Start transaction
            trans = conn.begin()
            
            try:
                # 1. Get Clients table schema first
                print("\n📊 Current Clients table schema:")
                result = conn.execute(text("""
                    SELECT column_name, data_type, character_maximum_length, is_nullable
                    FROM information_schema.columns
                    WHERE table_name = 'clients'
                    ORDER BY ordinal_position;
                """))
                
                for row in result:
                    print(f"  - {row[0]}: {row[1]}({row[2] if row[2] else ''}) {'NULL' if row[3] == 'YES' else 'NOT NULL'}")
                
                # 2. Add temp_id to Employees table
                print("\n✅ Adding temp_id to Employees table...")
                conn.execute(text("""
                    ALTER TABLE employees 
                    ADD COLUMN IF NOT EXISTS temp_id INTEGER;
                """))
                
                # 3. Add temp_id to Clients table
                print("✅ Adding temp_id to Clients table...")
                conn.execute(text("""
                    ALTER TABLE clients 
                    ADD COLUMN IF NOT EXISTS temp_id INTEGER;
                """))
                
                # 4. Split phone_mobile in Persons table
                print("\n📱 Splitting phone_mobile in Persons table...")
                # First drop the old column
                conn.execute(text("""
                    ALTER TABLE persons 
                    DROP COLUMN IF EXISTS phone_mobile;
                """))
                # Add new columns
                conn.execute(text("""
                    ALTER TABLE persons 
                    ADD COLUMN IF NOT EXISTS phone_mobile_country_code VARCHAR(6),
                    ADD COLUMN IF NOT EXISTS phone_mobile_number VARCHAR(20);
                """))
                
                # 5. Split phone_home in Persons table
                print("🏠 Splitting phone_home in Persons table...")
                # First drop the old column
                conn.execute(text("""
                    ALTER TABLE persons 
                    DROP COLUMN IF EXISTS phone_home;
                """))
                # Add new columns
                conn.execute(text("""
                    ALTER TABLE persons 
                    ADD COLUMN IF NOT EXISTS phone_home_country_code VARCHAR(6),
                    ADD COLUMN IF NOT EXISTS phone_home_number VARCHAR(20);
                """))
                
                # 6. Split phone in Clinics table
                print("🏥 Splitting phone in Clinics table...")
                # First drop the old column
                conn.execute(text("""
                    ALTER TABLE clinics 
                    DROP COLUMN IF EXISTS phone;
                """))
                # Add new columns
                conn.execute(text("""
                    ALTER TABLE clinics 
                    ADD COLUMN IF NOT EXISTS phone_country_code VARCHAR(6),
                    ADD COLUMN IF NOT EXISTS phone_number VARCHAR(20);
                """))
                
                # Commit transaction
                trans.commit()
                print("\n✅ Migration completed successfully!")
                
                # Verify changes
                print("\n📋 Verification - Updated schemas:")
                
                # Verify Employees
                print("\n  Employees table (checking temp_id):")
                result = conn.execute(text("""
                    SELECT column_name FROM information_schema.columns
                    WHERE table_name = 'employees' AND column_name = 'temp_id';
                """))
                if result.fetchone():
                    print("    ✓ temp_id column added")
                
                # Verify Clients
                print("\n  Clients table (checking temp_id):")
                result = conn.execute(text("""
                    SELECT column_name FROM information_schema.columns
                    WHERE table_name = 'clients' AND column_name = 'temp_id';
                """))
                if result.fetchone():
                    print("    ✓ temp_id column added")
                
                # Verify Persons phone fields
                print("\n  Persons table (phone fields):")
                result = conn.execute(text("""
                    SELECT column_name FROM information_schema.columns
                    WHERE table_name = 'persons' 
                    AND column_name IN ('phone_mobile_country_code', 'phone_mobile_number', 
                                        'phone_home_country_code', 'phone_home_number')
                    ORDER BY column_name;
                """))
                for row in result:
                    print(f"    ✓ {row[0]}")
                
                # Verify Clinics phone fields
                print("\n  Clinics table (phone fields):")
                result = conn.execute(text("""
                    SELECT column_name FROM information_schema.columns
                    WHERE table_name = 'clinics' 
                    AND column_name IN ('phone_country_code', 'phone_number')
                    ORDER BY column_name;
                """))
                for row in result:
                    print(f"    ✓ {row[0]}")
                
                # Show final Clients schema
                print("\n📊 Final Clients table schema:")
                result = conn.execute(text("""
                    SELECT column_name, data_type, character_maximum_length, is_nullable
                    FROM information_schema.columns
                    WHERE table_name = 'clients'
                    ORDER BY ordinal_position;
                """))
                
                for row in result:
                    print(f"  - {row[0]}: {row[1]}({row[2] if row[2] else ''}) {'NULL' if row[3] == 'YES' else 'NOT NULL'}")
                
            except Exception as e:
                trans.rollback()
                print(f"\n❌ Error during migration: {e}")
                raise
                
    except SQLAlchemyError as e:
        print(f"\n❌ Database error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    execute_migration()
