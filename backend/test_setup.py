#!/usr/bin/env python3
"""Test database connection and configuration"""

import sys
from pathlib import Path

# Add the backend directory to Python path
backend_dir = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(backend_dir))

def test_config():
    """Test configuration loading"""
    print("Testing configuration...")
    try:
        from app.core.config import settings
        print(f"✓ Configuration loaded successfully")
        print(f"  - Environment: {settings.ENVIRONMENT}")
        print(f"  - Database URL: {settings.DATABASE_URL[:30]}...")
        print(f"  - Debug: {settings.DEBUG}")
        return True
    except Exception as e:
        print(f"✗ Failed to load configuration: {e}")
        return False

def test_database():
    """Test database connection"""
    print("\nTesting database connection...")
    try:
        from app.database import engine
        from sqlalchemy import text
        
        with engine.connect() as conn:
            result = conn.execute(text("SELECT version()"))
            version = result.scalar()
            print(f"✓ Database connected successfully")
            print(f"  - PostgreSQL version: {version}")
        return True
    except Exception as e:
        print(f"✗ Failed to connect to database: {e}")
        print(f"  Make sure PostgreSQL is running and the database exists")
        print(f"  You can create the database with: createdb picobraindb")
        return False

def test_models():
    """Test model imports"""
    print("\nTesting model imports...")
    try:
        from app.models.person import Person
        from app.models.user import User
        from app.models.core import Client, Employee, Clinic
        print(f"✓ All models imported successfully")
        return True
    except Exception as e:
        print(f"✗ Failed to import models: {e}")
        return False

def main():
    """Run all tests"""
    print("=" * 60)
    print("PicoBrain Configuration and Database Test")
    print("=" * 60)
    
    tests = [
        test_config(),
        test_database(),
        test_models()
    ]
    
    print("\n" + "=" * 60)
    if all(tests):
        print("✓ All tests passed! Your setup is ready.")
        print("\nYou can now run:")
        print("  python manage.py create-admin")
    else:
        print("✗ Some tests failed. Please fix the issues above.")
    print("=" * 60)

if __name__ == "__main__":
    main()
