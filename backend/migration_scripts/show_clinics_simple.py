#!/usr/bin/env python3
"""
Simple display of clinics table data
"""

import sys
from pathlib import Path
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
import json

# Add the backend directory to Python path
sys.path.append(str(Path(__file__).parent))

from app.models.core import Clinic

# Database connection
DATABASE_URL = "postgresql://edo@localhost/picobraindb"
engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(bind=engine)

def show_clinics_simple():
    session = SessionLocal()
    
    try:
        print("\n" + "=" * 70)
        print("CLINICS TABLE DATA FROM DATABASE")
        print("=" * 70)
        
        # Get all clinics
        clinics = session.query(Clinic).order_by(Clinic.code).all()
        
        print(f"\nTotal Records: {len(clinics)}")
        print("-" * 70)
        
        for clinic in clinics:
            print(f"\nClinic: {clinic.name}")
            print(f"  • ID:       {clinic.id} (UUID)")
            print(f"  • Code:     {clinic.code}")
            print(f"  • Currency: {clinic.functional_currency}")
            print(f"  • City:     {clinic.city}")
            print(f"  • Country:  {clinic.country_code}")
            print(f"  • Active:   {clinic.is_active}")
        
        # Show field types from database
        print("\n" + "-" * 70)
        print("FIELD TYPES (from PostgreSQL):")
        print("-" * 70)
        
        result = session.execute(text("""
            SELECT 
                column_name,
                data_type,
                character_maximum_length,
                is_nullable
            FROM information_schema.columns
            WHERE table_name = 'clinics'
            ORDER BY ordinal_position;
        """))
        
        for row in result:
            col_name = row[0]
            data_type = row[1]
            max_length = row[2]
            nullable = "NULL" if row[3] == 'YES' else "NOT NULL"
            
            if max_length:
                type_str = f"{data_type}({max_length})"
            else:
                type_str = data_type
            
            print(f"  {col_name:<25} {type_str:<20} {nullable}")
        
        print("\n" + "=" * 70)
        
    except Exception as e:
        print(f"Error: {e}")
    finally:
        session.close()

if __name__ == "__main__":
    show_clinics_simple()
