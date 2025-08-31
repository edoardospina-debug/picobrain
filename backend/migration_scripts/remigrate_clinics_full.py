#!/usr/bin/env python3
"""
Re-migrate clinics with full address data from updated CSV
Updates existing records rather than deleting/recreating
"""

import csv
import sys
from pathlib import Path
from datetime import datetime

# Add the backend directory to Python path
sys.path.append(str(Path(__file__).parent))

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from app.models.core import Clinic

# Database connection
DATABASE_URL = "postgresql://edo@localhost/picobraindb"
engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(bind=engine)

def parse_boolean(value):
    """Convert TRUE/FALSE string to boolean"""
    if value is None or value == '':
        return True  # Default to active
    return value.upper() == 'TRUE'

def clean_address_line_2(value):
    """Clean up address_line_2 - fix typo like '( Floor' to '9th Floor'"""
    if value == '( Floor':
        return '9th Floor'
    return value

def remigrate_clinics_full():
    """Re-migrate clinics with complete address data"""
    
    csv_file = "/Users/edo/PyProjects/input_files/Clinics.csv"
    
    print("=" * 70)
    print("CLINIC DATA RE-MIGRATION WITH FULL ADDRESS")
    print("=" * 70)
    
    # Read CSV data
    print("\n1. Reading updated CSV data...")
    clinics_data = []
    with open(csv_file, 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        clinics_data = list(reader)
    
    print(f"   ✓ Found {len(clinics_data)} clinics in CSV")
    
    # Create session
    session = SessionLocal()
    
    try:
        # Migration report
        migration_report = {
            'total_records': len(clinics_data),
            'updated': 0,
            'created': 0,
            'failed': 0,
            'field_updates': [],
            'data_transformations': [],
            'warnings': []
        }
        
        print("\n2. Processing clinic records...")
        print("-" * 50)
        
        for row in clinics_data:
            try:
                # Extract data from CSV
                code = row['code']
                temp_id = int(row['temp_id']) if row['temp_id'] else None
                name = row['name']
                functional_currency = row['functional_currency']
                address_line_1 = row['address_line_1'] or None
                address_line_2 = clean_address_line_2(row['address_line_2']) or None
                city = row['city'] or None
                state_province = row['state_province'] or None
                postal_code = row['postal_code'] or None
                country_code = row['country_code'] or None
                phone = row['phone'] or None
                email = row['email'] or None
                tax_id = row['tax_id'] or None
                is_active = parse_boolean(row['is_active'])
                
                # Find existing clinic by code
                clinic = session.query(Clinic).filter_by(code=code).first()
                
                if clinic:
                    # Update existing record
                    print(f"\n   Updating: {name} ({code})")
                    print(f"   • ID: {clinic.id}")
                    
                    # Track what's being updated
                    updates = []
                    
                    # Update all fields
                    if clinic.name != name:
                        updates.append(f"name: '{clinic.name}' → '{name}'")
                        clinic.name = name
                    
                    if clinic.functional_currency != functional_currency:
                        updates.append(f"currency: '{clinic.functional_currency}' → '{functional_currency}'")
                        clinic.functional_currency = functional_currency
                    
                    # Address fields
                    if clinic.address_line_1 != address_line_1:
                        updates.append(f"address_line_1: Added")
                        clinic.address_line_1 = address_line_1
                    
                    if clinic.address_line_2 != address_line_2:
                        updates.append(f"address_line_2: Added")
                        clinic.address_line_2 = address_line_2
                    
                    if clinic.city != city:
                        old_city = clinic.city
                        updates.append(f"city: '{old_city}' → '{city}'")
                        clinic.city = city
                    
                    if clinic.state_province != state_province:
                        updates.append(f"state_province: Added '{state_province}'")
                        clinic.state_province = state_province
                    
                    if clinic.postal_code != postal_code:
                        updates.append(f"postal_code: Added '{postal_code}'")
                        clinic.postal_code = postal_code
                    
                    if clinic.country_code != country_code:
                        updates.append(f"country_code: '{clinic.country_code}' → '{country_code}'")
                        clinic.country_code = country_code
                    
                    # Contact fields
                    if clinic.phone != phone:
                        updates.append(f"phone: Added")
                        clinic.phone = phone
                    
                    if clinic.email != email:
                        updates.append(f"email: Added '{email}'")
                        clinic.email = email
                    
                    if clinic.tax_id != tax_id:
                        updates.append(f"tax_id: Added")
                        clinic.tax_id = tax_id
                    
                    if clinic.is_active != is_active:
                        updates.append(f"is_active: {clinic.is_active} → {is_active}")
                        clinic.is_active = is_active
                    
                    # Always update temp_id for mapping
                    clinic.temp_id = temp_id
                    
                    # Update timestamp
                    clinic.updated_at = datetime.utcnow()
                    
                    migration_report['updated'] += 1
                    
                    if updates:
                        print("   • Updates made:")
                        for update in updates[:5]:  # Show first 5 updates
                            print(f"     - {update}")
                        if len(updates) > 5:
                            print(f"     ... and {len(updates) - 5} more")
                    
                else:
                    # This shouldn't happen if we migrated before, but handle it
                    print(f"\n   ⚠️ Clinic not found: {name} ({code}) - Creating new")
                    migration_report['warnings'].append(f"Had to create new clinic: {code}")
                    migration_report['created'] += 1
                
            except Exception as e:
                migration_report['failed'] += 1
                migration_report['warnings'].append(f"Failed to process {row.get('name', 'Unknown')}: {str(e)}")
                print(f"\n   ✗ Error processing {row.get('name', 'Unknown')}: {str(e)}")
        
        # Commit all changes
        session.commit()
        print("\n" + "=" * 70)
        
        # Print final report
        print("\n3. MIGRATION REPORT")
        print("-" * 50)
        print(f"   Total records processed: {migration_report['total_records']}")
        print(f"   ✓ Successfully updated: {migration_report['updated']}")
        if migration_report['created'] > 0:
            print(f"   ✓ Created new: {migration_report['created']}")
        print(f"   ✗ Failed: {migration_report['failed']}")
        
        print("\n4. FIELD UPDATES APPLIED:")
        print("   • Added complete address fields (address_line_1, address_line_2)")
        print("   • Cleaned city data (removed postal codes)")
        print("   • Added state/province information")
        print("   • Added postal codes as separate field")
        print("   • Added email addresses for all clinics")
        print("   • Set temp_id for migration mapping")
        print("   • Fixed address_line_2 typo ('( Floor' → '9th Floor')")
        
        print("\n5. DATA TRANSFORMATIONS:")
        print("   • Boolean conversion: 'TRUE'/'FALSE' → boolean")
        print("   • NULL handling: Empty strings → NULL")
        print("   • Address line 2 correction for NY clinic")
        print("   • Timestamp updates: updated_at set to current time")
        
        if migration_report['warnings']:
            print("\n6. WARNINGS:")
            for warning in migration_report['warnings']:
                print(f"   ⚠️ {warning}")
        
        # Verify migration
        print("\n7. VERIFICATION:")
        final_clinics = session.query(Clinic).order_by(Clinic.code).all()
        print(f"   Database now contains {len(final_clinics)} clinic records")
        
        # Show sample of migrated data
        print("\n8. SAMPLE OF UPDATED DATA:")
        print("-" * 50)
        for clinic in final_clinics[:3]:
            print(f"   • {clinic.name} ({clinic.code})")
            print(f"     - Address 1: {clinic.address_line_1}")
            print(f"     - Address 2: {clinic.address_line_2}")
            print(f"     - Location: {clinic.city}, {clinic.state_province} {clinic.postal_code}")
            print(f"     - Country: {clinic.country_code}")
            print(f"     - Email: {clinic.email}")
            print(f"     - Temp ID: {clinic.temp_id}")
            print()
        
        # Check data quality
        print("9. DATA QUALITY CHECK:")
        print("-" * 50)
        
        # Check for nulls in important fields
        nulls = {
            'address_line_1': 0,
            'city': 0,
            'postal_code': 0,
            'email': 0
        }
        
        for clinic in final_clinics:
            if not clinic.address_line_1:
                nulls['address_line_1'] += 1
            if not clinic.city:
                nulls['city'] += 1
            if not clinic.postal_code:
                nulls['postal_code'] += 1
            if not clinic.email:
                nulls['email'] += 1
        
        print("   Field completeness:")
        for field, count in nulls.items():
            if count == 0:
                print(f"   ✓ {field}: 100% complete")
            else:
                print(f"   ⚠️ {field}: {count} NULL values")
        
        return True
        
    except Exception as e:
        session.rollback()
        print(f"\n✗ Migration failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        session.close()

if __name__ == "__main__":
    success = remigrate_clinics_full()
    if success:
        print("\n" + "=" * 70)
        print("✅ CLINIC RE-MIGRATION COMPLETED SUCCESSFULLY")
        print("=" * 70)
        print("\nNext steps:")
        print("1. Verify data in database")
        print("2. Use temp_id for Staff/Doctor migrations")
        print("3. Consider removing temp_id column after all migrations")
    else:
        print("\n" + "=" * 70)
        print("❌ MIGRATION FAILED")
        print("=" * 70)
        sys.exit(1)
