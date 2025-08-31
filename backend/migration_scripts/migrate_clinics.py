#!/usr/bin/env python3
"""
Clinic Data Migration Script
Maps historical clinic data from CSV to database
"""

import csv
import uuid
import sys
import os
from pathlib import Path

# Add the backend directory to Python path
sys.path.append(str(Path(__file__).parent))

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from app.models.core import Clinic
from app.database import Base

# Database connection
DATABASE_URL = "postgresql://edo@localhost/picobraindb"
engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(bind=engine)

def parse_address(address_string):
    """
    Extract city and country from address string
    Returns: (city, country_code)
    """
    if not address_string:
        return None, None
    
    # Split by comma and analyze parts
    parts = [p.strip() for p in address_string.split(',')]
    
    # Mapping for country codes based on known patterns
    country_mapping = {
        'UK': 'GB',
        'USA': 'US',
        'Italy': 'IT',
        'Canada': 'CA'
    }
    
    city = None
    country_code = None
    
    # Extract country and city from last parts
    if len(parts) >= 2:
        # Last part usually contains country
        last_part = parts[-1]
        for country_key, code in country_mapping.items():
            if country_key in last_part:
                country_code = code
                # Second to last is usually city
                if len(parts) >= 2:
                    city = parts[-2].split()[0] if country_key == 'UK' else parts[-2]
                break
    
    return city, country_code

def migrate_clinics():
    """Main migration function for clinics"""
    
    csv_file = "/Users/edo/PyProjects/input_files/Clinics.csv"
    
    print("=" * 60)
    print("CLINIC DATA MIGRATION")
    print("=" * 60)
    
    # Read CSV data
    print("\n1. Reading CSV data...")
    clinics_data = []
    with open(csv_file, 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        clinics_data = list(reader)
    
    print(f"   ✓ Found {len(clinics_data)} clinics in CSV")
    
    # Create session
    session = SessionLocal()
    
    try:
        # Delete existing clinics
        print("\n2. Cleaning existing clinic data...")
        existing_count = session.query(Clinic).count()
        if existing_count > 0:
            session.query(Clinic).delete()
            session.commit()
            print(f"   ✓ Deleted {existing_count} existing clinic records")
        else:
            print("   ✓ No existing clinics to delete")
        
        # Mapping statistics
        mapping_report = {
            'total_records': len(clinics_data),
            'successful': 0,
            'failed': 0,
            'field_mappings': [],
            'data_transformations': [],
            'missing_fields': [],
            'warnings': []
        }
        
        # Create ID mapping (old CSV ID -> new UUID)
        id_mapping = {}
        
        print("\n3. Processing clinic records...")
        print("-" * 40)
        
        for row in clinics_data:
            try:
                # Extract and transform data
                csv_id = row['id']
                name = row['name']
                address = row.get('address', '')
                currency = row['currency']
                short_name = row['short_name']
                
                # Parse address to extract city and country
                city, country_code = parse_address(address)
                
                # Generate new UUID
                new_id = uuid.uuid4()
                id_mapping[csv_id] = new_id
                
                # Create clinic record
                clinic = Clinic(
                    id=new_id,
                    code=short_name,  # Map short_name to code
                    name=name,
                    functional_currency=currency,
                    city=city,
                    country_code=country_code,
                    is_active=True  # Default all to active
                )
                
                session.add(clinic)
                mapping_report['successful'] += 1
                
                # Print individual mapping
                print(f"\n   Clinic: {name}")
                print(f"   • CSV ID {csv_id} → UUID {new_id}")
                print(f"   • Code: {short_name}")
                print(f"   • Currency: {currency}")
                print(f"   • Location: {city}, {country_code}")
                print(f"   • Original address: {address[:50]}..." if len(address) > 50 else f"   • Original address: {address}")
                
                # Track field mappings
                if mapping_report['successful'] == 1:
                    mapping_report['field_mappings'] = [
                        "CSV 'id' → Generated UUID (stored mapping for reference)",
                        "CSV 'short_name' → DB 'code'",
                        "CSV 'name' → DB 'name'",
                        "CSV 'currency' → DB 'functional_currency'",
                        "CSV 'address' → Parsed to 'city' and 'country_code'"
                    ]
                
            except Exception as e:
                mapping_report['failed'] += 1
                mapping_report['warnings'].append(f"Failed to process clinic {row.get('name', 'Unknown')}: {str(e)}")
                print(f"\n   ✗ Error processing clinic {row.get('name', 'Unknown')}: {str(e)}")
        
        # Commit all changes
        session.commit()
        print("\n" + "=" * 60)
        
        # Print final report
        print("\n4. MIGRATION REPORT")
        print("-" * 40)
        print(f"   Total records processed: {mapping_report['total_records']}")
        print(f"   ✓ Successfully migrated: {mapping_report['successful']}")
        print(f"   ✗ Failed: {mapping_report['failed']}")
        
        print("\n5. FIELD MAPPINGS APPLIED:")
        for mapping in mapping_report['field_mappings']:
            print(f"   • {mapping}")
        
        print("\n6. DATA TRANSFORMATIONS:")
        print("   • Address parsing: Extracted city and country_code from full address")
        print("   • ID generation: Created new UUIDs while preserving CSV ID mapping")
        print("   • Default values: Set all clinics as active (is_active=True)")
        
        print("\n7. DATA LOSS/WARNINGS:")
        print("   ⚠️ Full address details lost (no street/postal code fields in DB)")
        print("   ⚠️ CSV numeric IDs replaced with UUIDs (mapping preserved)")
        
        if mapping_report['warnings']:
            print("\n8. PROCESSING WARNINGS:")
            for warning in mapping_report['warnings']:
                print(f"   ⚠️ {warning}")
        
        # Save ID mapping for future reference
        print("\n9. ID MAPPING (for Staff/Doctor migration):")
        print("-" * 40)
        for csv_id, uuid_id in id_mapping.items():
            clinic = session.query(Clinic).filter_by(id=uuid_id).first()
            print(f"   CSV ID {csv_id} → {clinic.code} ({clinic.name}) → UUID {uuid_id}")
        
        # Verify migration
        print("\n10. VERIFICATION:")
        final_count = session.query(Clinic).count()
        print(f"   Database now contains {final_count} clinic records")
        
        # Show sample of migrated data
        print("\n11. SAMPLE OF MIGRATED DATA:")
        print("-" * 40)
        sample_clinics = session.query(Clinic).limit(3).all()
        for clinic in sample_clinics:
            print(f"   • {clinic.name}")
            print(f"     - Code: {clinic.code}")
            print(f"     - Currency: {clinic.functional_currency}")
            print(f"     - Location: {clinic.city}, {clinic.country_code}")
            print(f"     - Active: {clinic.is_active}")
            print()
        
        # Return ID mapping for use in subsequent migrations
        return id_mapping
        
    except Exception as e:
        session.rollback()
        print(f"\n✗ Migration failed: {str(e)}")
        raise
    finally:
        session.close()

if __name__ == "__main__":
    try:
        id_mapping = migrate_clinics()
        print("\n" + "=" * 60)
        print("✓ CLINIC MIGRATION COMPLETED SUCCESSFULLY")
        print("=" * 60)
        
        # Save mapping for next migrations
        import json
        mapping_file = "/Users/edo/PyProjects/picobrain/backend/clinic_id_mapping.json"
        with open(mapping_file, 'w') as f:
            # Convert UUID to string for JSON serialization
            json_mapping = {k: str(v) for k, v in id_mapping.items()}
            json.dump(json_mapping, f, indent=2)
        print(f"\n✓ ID mapping saved to: {mapping_file}")
        
    except Exception as e:
        print(f"\n✗ Migration failed with error: {str(e)}")
        sys.exit(1)
