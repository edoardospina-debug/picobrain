#!/usr/bin/env python3
"""
Display all clinics from the database with field types and values
"""

import sys
from pathlib import Path
from sqlalchemy import create_engine, inspect, text
from sqlalchemy.orm import sessionmaker
from tabulate import tabulate
import json

# Add the backend directory to Python path
sys.path.append(str(Path(__file__).parent))

from app.models.core import Clinic

# Database connection
DATABASE_URL = "postgresql://edo@localhost/picobraindb"
engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(bind=engine)

def show_clinics_data():
    """Display all clinics with their field types and values"""
    
    print("=" * 80)
    print("CLINICS TABLE - DATABASE INSPECTION")
    print("=" * 80)
    
    session = SessionLocal()
    
    try:
        # Get table metadata using SQLAlchemy inspector
        inspector = inspect(engine)
        
        # Get column information
        columns = inspector.get_columns('clinics')
        
        print("\n📋 TABLE SCHEMA (Field Types):")
        print("-" * 60)
        
        schema_data = []
        for col in columns:
            col_type = str(col['type'])
            nullable = "NULL" if col['nullable'] else "NOT NULL"
            default = col.get('default', '')
            
            schema_data.append([
                col['name'],
                col_type,
                nullable,
                default if default else '-'
            ])
        
        print(tabulate(schema_data, 
                      headers=['Field Name', 'Data Type', 'Nullable', 'Default'],
                      tablefmt='grid'))
        
        # Get all clinic records
        clinics = session.query(Clinic).order_by(Clinic.code).all()
        
        print(f"\n📊 DATA RECORDS (Total: {len(clinics)} clinics):")
        print("-" * 60)
        
        # Display each clinic with all fields
        for i, clinic in enumerate(clinics, 1):
            print(f"\n🏥 Clinic {i}:")
            print("  " + "-" * 56)
            
            # Display all fields
            fields = [
                ('ID (UUID)', str(clinic.id)),
                ('Code', clinic.code),
                ('Name', clinic.name),
                ('Currency', clinic.functional_currency),
                ('City', clinic.city),
                ('Country Code', clinic.country_code),
                ('Is Active', clinic.is_active),
            ]
            
            for field_name, field_value in fields:
                # Format the output nicely
                print(f"  {field_name:<20}: {field_value}")
        
        # Create a summary table
        print("\n📈 SUMMARY TABLE:")
        print("-" * 60)
        
        table_data = []
        for clinic in clinics:
            table_data.append([
                clinic.code,
                clinic.name,
                clinic.functional_currency,
                f"{clinic.city}, {clinic.country_code}",
                "✅" if clinic.is_active else "❌"
            ])
        
        print(tabulate(table_data,
                      headers=['Code', 'Name', 'Currency', 'Location', 'Active'],
                      tablefmt='pretty'))
        
        # Show data types for each field from actual Python objects
        print("\n🔍 PYTHON DATA TYPES (from SQLAlchemy model):")
        print("-" * 60)
        
        if clinics:
            sample = clinics[0]
            type_info = []
            for field in ['id', 'code', 'name', 'functional_currency', 'city', 'country_code', 'is_active']:
                value = getattr(sample, field)
                type_info.append([
                    field,
                    type(value).__name__,
                    str(value)[:50] + ('...' if len(str(value)) > 50 else '')
                ])
            
            print(tabulate(type_info,
                          headers=['Field', 'Python Type', 'Sample Value'],
                          tablefmt='grid'))
        
        # Raw SQL query to double-check
        print("\n🔧 RAW SQL VERIFICATION:")
        print("-" * 60)
        
        result = session.execute(text("""
            SELECT 
                column_name,
                data_type,
                character_maximum_length,
                is_nullable,
                column_default
            FROM information_schema.columns
            WHERE table_name = 'clinics'
            ORDER BY ordinal_position;
        """))
        
        sql_schema = []
        for row in result:
            max_length = f"({row[2]})" if row[2] else ""
            data_type = f"{row[1]}{max_length}"
            sql_schema.append([
                row[0],  # column_name
                data_type,  # data_type with length
                row[3],  # is_nullable
                row[4] if row[4] else '-'  # column_default
            ])
        
        print(tabulate(sql_schema,
                      headers=['Column', 'PostgreSQL Type', 'Nullable', 'Default'],
                      tablefmt='grid'))
        
        # Check for the ID mapping file
        mapping_file = Path(__file__).parent / 'clinic_id_mapping.json'
        if mapping_file.exists():
            print("\n🔗 ID MAPPING (CSV ID → Database UUID):")
            print("-" * 60)
            with open(mapping_file) as f:
                mapping = json.load(f)
            
            for csv_id, uuid_str in mapping.items():
                clinic = session.query(Clinic).filter_by(id=uuid_str).first()
                if clinic:
                    print(f"  CSV ID {csv_id} → {clinic.code} ({clinic.name})")
        
        # Database statistics
        print("\n📊 DATABASE STATISTICS:")
        print("-" * 60)
        
        # Count by currency
        currency_counts = {}
        for clinic in clinics:
            curr = clinic.functional_currency
            currency_counts[curr] = currency_counts.get(curr, 0) + 1
        
        print("  Clinics by Currency:")
        for curr, count in sorted(currency_counts.items()):
            print(f"    • {curr}: {count} clinic(s)")
        
        # Count by country
        country_counts = {}
        for clinic in clinics:
            country = clinic.country_code
            country_counts[country] = country_counts.get(country, 0) + 1
        
        print("\n  Clinics by Country:")
        for country, count in sorted(country_counts.items()):
            print(f"    • {country}: {count} clinic(s)")
        
        print("\n" + "=" * 80)
        print("✅ INSPECTION COMPLETE")
        print("=" * 80)
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
    finally:
        session.close()

if __name__ == "__main__":
    show_clinics_data()
