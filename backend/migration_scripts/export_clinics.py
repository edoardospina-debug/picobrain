#!/usr/bin/env python3
"""
Export clinics table data to JSON for inspection
"""

import sys
import json
from pathlib import Path
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from datetime import date
from uuid import UUID

# Add the backend directory to Python path
sys.path.append(str(Path(__file__).parent))

from app.models.core import Clinic

# Custom JSON encoder for UUID and other types
class CustomEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, UUID):
            return str(obj)
        if isinstance(obj, date):
            return obj.isoformat()
        return super().default(obj)

# Database connection
DATABASE_URL = "postgresql://edo@localhost/picobraindb"
engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(bind=engine)

def export_clinics():
    session = SessionLocal()
    
    try:
        # Get all clinics
        clinics = session.query(Clinic).order_by(Clinic.code).all()
        
        # Get schema info
        schema_result = session.execute(text("""
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
        
        schema_info = []
        for row in schema_result:
            schema_info.append({
                'column_name': row[0],
                'data_type': row[1],
                'max_length': row[2],
                'nullable': row[3] == 'YES',
                'default': row[4]
            })
        
        # Convert clinics to dict
        clinics_data = []
        for clinic in clinics:
            clinics_data.append({
                'id': clinic.id,
                'code': clinic.code,
                'name': clinic.name,
                'functional_currency': clinic.functional_currency,
                'city': clinic.city,
                'country_code': clinic.country_code,
                'is_active': clinic.is_active
            })
        
        # Create output
        output = {
            'table_name': 'clinics',
            'record_count': len(clinics),
            'schema': schema_info,
            'data': clinics_data
        }
        
        # Save to file
        output_file = Path(__file__).parent / 'clinics_table_data.json'
        with open(output_file, 'w') as f:
            json.dump(output, f, indent=2, cls=CustomEncoder)
        
        print(f"✅ Exported {len(clinics)} clinics to {output_file}")
        
        # Also print summary to console
        print("\n📊 CLINICS TABLE SUMMARY:")
        print("-" * 40)
        print(f"Total Records: {len(clinics)}")
        print("\nRecords:")
        for clinic in clinics_data:
            print(f"  • {clinic['code']}: {clinic['name']} ({clinic['functional_currency']})")
        
        print("\nField Types:")
        for field in schema_info:
            type_str = field['data_type']
            if field['max_length']:
                type_str += f"({field['max_length']})"
            nullable = "NULL" if field['nullable'] else "NOT NULL"
            print(f"  • {field['column_name']}: {type_str} {nullable}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        session.close()

if __name__ == "__main__":
    export_clinics()
