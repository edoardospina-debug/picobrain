#!/usr/bin/env python
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Test imports
print("Testing imports...")
try:
    from pydantic_settings import BaseSettings
    print("✅ pydantic_settings imported successfully")
except ImportError as e:
    print(f"❌ pydantic_settings import failed: {e}")

try:
    from app.config import settings
    print(f"✅ Config loaded: {settings.PROJECT_NAME}")
    print(f"✅ Database URL: {settings.DATABASE_URL}")
except Exception as e:
    print(f"❌ Config failed: {e}")

# Test database connection
try:
    from app.database import engine, SessionLocal
    from app.models.core import Clinic
    
    db = SessionLocal()
    clinics = db.query(Clinic).all()
    print(f"✅ Database connected: Found {len(clinics)} clinics")
    for clinic in clinics:
        print(f"  - {clinic.code}: {clinic.name}")
    db.close()
except Exception as e:
    print(f"❌ Database connection failed: {e}")

# Test FastAPI app
try:
    from app.main import app
    print(f"✅ FastAPI app loaded: {app.title}")
except Exception as e:
    print(f"❌ FastAPI app failed: {e}")