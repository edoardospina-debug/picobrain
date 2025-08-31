#!/usr/bin/env python3
"""
Diagnostic script to check database and API status
"""

import sys
import os
from pathlib import Path
import psycopg2
from psycopg2 import sql
import requests
import json

# Add the backend directory to Python path
sys.path.append(str(Path(__file__).parent))

def check_database():
    """Check if we can connect to the database and see clinics"""
    print("\n📊 CHECKING DATABASE CONNECTION")
    print("=" * 60)
    
    try:
        # Connect to the database
        conn = psycopg2.connect(
            host="localhost",
            database="picobraindb",
            user="edo",
            port=5432
        )
        cursor = conn.cursor()
        
        print("✅ Connected to database: picobraindb")
        
        # Check if clinics table exists
        cursor.execute("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables 
                WHERE table_name = 'clinics'
            );
        """)
        
        if cursor.fetchone()[0]:
            print("✅ Clinics table exists")
            
            # Count clinics
            cursor.execute("SELECT COUNT(*) FROM clinics;")
            count = cursor.fetchone()[0]
            print(f"📈 Total clinics in database: {count}")
            
            if count > 0:
                # Show first 3 clinics
                cursor.execute("""
                    SELECT id, code, name, city, is_active 
                    FROM clinics 
                    ORDER BY code 
                    LIMIT 3;
                """)
                
                print("\n📋 Sample clinics:")
                for row in cursor.fetchall():
                    print(f"  - {row[1]}: {row[2]} ({row[3]}) - Active: {row[4]}")
            else:
                print("⚠️  No clinics found in database!")
                
        else:
            print("❌ Clinics table does not exist!")
            
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False
    
    return True

def check_backend_api():
    """Check if the backend API is running"""
    print("\n🔧 CHECKING BACKEND API")
    print("=" * 60)
    
    api_url = "http://localhost:8000"
    
    try:
        # Check health endpoint
        response = requests.get(f"{api_url}/health", timeout=5)
        if response.status_code == 200:
            print(f"✅ Backend API is running at {api_url}")
            return True
        else:
            print(f"⚠️  Backend API responded with status: {response.status_code}")
            
    except requests.exceptions.ConnectionError:
        print(f"❌ Backend API is not running at {api_url}")
        print("   Run: cd backend && uvicorn app.main:app --reload")
    except Exception as e:
        print(f"❌ Error checking backend: {e}")
    
    return False

def check_frontend():
    """Check if the frontend is running"""
    print("\n🎨 CHECKING FRONTEND")
    print("=" * 60)
    
    frontend_url = "http://localhost:3000"
    
    try:
        response = requests.get(frontend_url, timeout=5)
        if response.status_code in [200, 304]:
            print(f"✅ Frontend is running at {frontend_url}")
            return True
        else:
            print(f"⚠️  Frontend responded with status: {response.status_code}")
            
    except requests.exceptions.ConnectionError:
        print(f"❌ Frontend is not running at {frontend_url}")
        print("   Run: cd frontend && npm run dev")
    except Exception as e:
        print(f"❌ Error checking frontend: {e}")
    
    return False

def test_api_with_auth():
    """Test the API with authentication"""
    print("\n🔐 TESTING API WITH AUTHENTICATION")
    print("=" * 60)
    
    base_url = "http://localhost:8000/api/v1"
    
    # First check if API is running
    try:
        requests.get("http://localhost:8000/health", timeout=2)
    except:
        print("❌ Backend API is not running. Cannot test authentication.")
        return False
    
    # Try to login
    try:
        login_response = requests.post(
            f"{base_url}/auth/login",
            data={"username": "admin", "password": "admin123"}
        )
        
        if login_response.status_code == 200:
            print("✅ Authentication successful")
            token = login_response.json().get("access_token")
            
            # Try to fetch clinics
            headers = {"Authorization": f"Bearer {token}"}
            clinics_response = requests.get(f"{base_url}/clinics", headers=headers)
            
            if clinics_response.status_code == 200:
                clinics = clinics_response.json()
                print(f"✅ API returned {len(clinics)} clinics")
                
                if len(clinics) == 0:
                    print("⚠️  API returned empty list - check if data exists in DB")
                
                return True
            else:
                print(f"❌ Failed to fetch clinics: {clinics_response.status_code}")
                
        else:
            print(f"❌ Authentication failed: {login_response.status_code}")
            
    except Exception as e:
        print(f"❌ API test failed: {e}")
    
    return False

def main():
    print("\n" + "=" * 60)
    print("🏥 PICOBRAIN DIAGNOSTIC REPORT")
    print("=" * 60)
    
    # Run all checks
    db_ok = check_database()
    backend_ok = check_backend_api()
    frontend_ok = check_frontend()
    
    if backend_ok:
        api_ok = test_api_with_auth()
    else:
        api_ok = False
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 SUMMARY")
    print("=" * 60)
    
    status_icon = lambda ok: "✅" if ok else "❌"
    
    print(f"{status_icon(db_ok)} Database Connection")
    print(f"{status_icon(backend_ok)} Backend API")
    print(f"{status_icon(frontend_ok)} Frontend")
    print(f"{status_icon(api_ok)} API Authentication & Data")
    
    # Recommendations
    print("\n📝 RECOMMENDATIONS:")
    
    if not backend_ok:
        print("1. Start the backend server:")
        print("   cd backend && source venv/bin/activate && uvicorn app.main:app --reload")
    
    if not frontend_ok:
        print("2. Start the frontend server:")
        print("   cd frontend && npm run dev")
    
    if db_ok and backend_ok and not api_ok:
        print("3. Check API authentication and permissions")
    
    if db_ok and api_ok and backend_ok and frontend_ok:
        print("✅ All systems operational! Check browser console for frontend errors.")

if __name__ == "__main__":
    main()
