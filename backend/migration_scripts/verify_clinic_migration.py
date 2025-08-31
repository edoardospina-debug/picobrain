#!/usr/bin/env python3
"""
Verify the clinic remigration results
"""

import sys
from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Add the backend directory to Python path
sys.path.append(str(Path(__file__).parent))

from app.models.core import Clinic

# Database connection
DATABASE_URL = "postgresql://edo@localhost/picobraindb"
engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(bind=engine)

def verify_migration():
    session = SessionLocal()
    
    try:
        print("\n" + "=" * 70)
        print("CLINIC DATA VERIFICATION AFTER RE-MIGRATION")
        print("=" * 70)
        
        clinics = session.query(Clinic).order_by(Clinic.code).all()
        
        print(f"\nTotal Clinics: {len(clinics)}")
        print("-" * 70)
        
        for clinic in clinics:
            print(f"\n🏥 {clinic.name} ({clinic.code})")
            print(f"   Temp ID: {clinic.temp_id}")
            print(f"   Address:")
            print(f"     Line 1: {clinic.address_line_1}")
            print(f"     Line 2: {clinic.address_line_2}")
            print(f"     City: {clinic.city}")
            print(f"     State/Province: {clinic.state_province}")
            print(f"     Postal Code: {clinic.postal_code}")
            print(f"     Country: {clinic.country_code}")
            print(f"   Contact:")
            print(f"     Phone: {clinic.phone or 'Not provided'}")
            print(f"     Email: {clinic.email}")
            print(f"   Business:")
            print(f"     Currency: {clinic.functional_currency}")
            print(f"     Tax ID: {clinic.tax_id or 'Not provided'}")
            print(f"     Active: {'✅' if clinic.is_active else '❌'}")
        
        print("\n" + "=" * 70)
        print("✅ VERIFICATION COMPLETE")
        print("=" * 70)
        
    except Exception as e:
        print(f"Error: {e}")
    finally:
        session.close()

if __name__ == "__main__":
    verify_migration()
