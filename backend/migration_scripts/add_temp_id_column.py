#!/usr/bin/env python3
"""
Add temp_id column to clinics table for migration tracking
"""

import sys
from pathlib import Path
from sqlalchemy import create_engine, text

# Database connection
DATABASE_URL = "postgresql://edo@localhost/picobraindb"
engine = create_engine(DATABASE_URL, echo=True)

def add_temp_id_column():
    """Add temp_id INTEGER column to clinics table"""
    
    print("=" * 60)
    print("ADDING temp_id COLUMN TO CLINICS TABLE")
    print("=" * 60)
    
    with engine.connect() as conn:
        try:
            # Check if column already exists
            check_sql = """
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name = 'clinics' 
                AND column_name = 'temp_id';
            """
            result = conn.execute(text(check_sql))
            if result.fetchone():
                print("⚠️  Column 'temp_id' already exists, skipping creation")
                return
            
            # Add the column
            alter_sql = """
                ALTER TABLE clinics 
                ADD COLUMN temp_id INTEGER;
            """
            
            print("\nExecuting SQL:")
            print(alter_sql)
            
            conn.execute(text(alter_sql))
            conn.commit()
            
            print("\n✅ Successfully added temp_id column")
            
            # Verify the column was added
            verify_sql = """
                SELECT column_name, data_type, is_nullable
                FROM information_schema.columns
                WHERE table_name = 'clinics'
                AND column_name = 'temp_id';
            """
            
            result = conn.execute(text(verify_sql))
            row = result.fetchone()
            
            if row:
                print("\n📊 Column Details:")
                print(f"  • Name: {row[0]}")
                print(f"  • Type: {row[1]}")
                print(f"  • Nullable: {row[2]}")
            
        except Exception as e:
            print(f"\n❌ Error adding column: {e}")
            raise

if __name__ == "__main__":
    add_temp_id_column()
