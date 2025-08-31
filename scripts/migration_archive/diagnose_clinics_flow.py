#!/usr/bin/env python3
"""
Complete diagnostic of clinics data flow
"""

import requests
import json
import psycopg2
from datetime import datetime

print("=" * 60)
print("PICOBRAIN CLINICS DATA FLOW DIAGNOSTIC")
print("=" * 60)
print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print()

# Step 1: Check database
print("1. DATABASE CHECK")
print("-" * 40)
try:
    conn = psycopg2.connect(
        host="localhost",
        database="picobraindb",
        user="edo",
        port=5432
    )
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(*) FROM clinics;")
    count = cursor.fetchone()[0]
    print(f"✅ Database connected")
    print(f"   Clinics in database: {count}")
    
    if count > 0:
        cursor.execute("SELECT code, name, city FROM clinics LIMIT 3;")
        print("   Sample clinics:")
        for row in cursor.fetchall():
            print(f"     - {row[0]}: {row[1]} ({row[2]})")
    
    cursor.close()
    conn.close()
except Exception as e:
    print(f"❌ Database error: {e}")

print()

# Step 2: Check backend API health
print("2. BACKEND API CHECK")
print("-" * 40)
try:
    health_response = requests.get("http://localhost:8000/health", timeout=2)
    if health_response.status_code == 200:
        print("✅ Backend API is running")
        print(f"   Response: {health_response.json()}")
    else:
        print(f"⚠️ Backend API status: {health_response.status_code}")
except Exception as e:
    print(f"❌ Backend API not accessible: {e}")

print()

# Step 3: Test authentication
print("3. AUTHENTICATION CHECK")
print("-" * 40)
try:
    login_data = {
        "username": "admin",
        "password": "admin123"
    }
    
    login_response = requests.post(
        "http://localhost:8000/api/v1/auth/login",
        data=login_data  # Form data, not JSON
    )
    
    if login_response.status_code == 200:
        token_data = login_response.json()
        token = token_data.get("access_token")
        print("✅ Authentication successful")
        print(f"   Token received: {token[:20]}...")
        
        # Step 4: Test clinics endpoint
        print()
        print("4. CLINICS API ENDPOINT CHECK")
        print("-" * 40)
        
        headers = {"Authorization": f"Bearer {token}"}
        
        # Test without parameters
        clinics_response = requests.get(
            "http://localhost:8000/api/v1/clinics",
            headers=headers
        )
        
        print(f"   Status code: {clinics_response.status_code}")
        
        if clinics_response.status_code == 200:
            clinics_data = clinics_response.json()
            print(f"✅ API returned data")
            print(f"   Response type: {type(clinics_data).__name__}")
            
            if isinstance(clinics_data, list):
                print(f"   Number of clinics: {len(clinics_data)}")
                if clinics_data:
                    print(f"   First clinic keys: {list(clinics_data[0].keys())}")
                    print(f"   First clinic:")
                    for key, value in list(clinics_data[0].items())[:5]:
                        print(f"     - {key}: {value}")
            elif isinstance(clinics_data, dict):
                print(f"   Response keys: {list(clinics_data.keys())}")
        else:
            print(f"❌ Failed to fetch clinics")
            print(f"   Response: {clinics_response.text}")
            
        # Test with pagination parameters
        print()
        print("5. CLINICS API WITH PAGINATION")
        print("-" * 40)
        
        paginated_response = requests.get(
            "http://localhost:8000/api/v1/clinics?skip=0&limit=20",
            headers=headers
        )
        
        print(f"   Status code: {paginated_response.status_code}")
        
        if paginated_response.status_code == 200:
            paginated_data = paginated_response.json()
            print(f"✅ Paginated API returned data")
            print(f"   Response type: {type(paginated_data).__name__}")
            if isinstance(paginated_data, list):
                print(f"   Number of items: {len(paginated_data)}")
                
    else:
        print(f"❌ Authentication failed: {login_response.status_code}")
        print(f"   Response: {login_response.text}")
        
except Exception as e:
    print(f"❌ Error during testing: {e}")

print()
print("=" * 60)
print("DIAGNOSTIC COMPLETE")
print("=" * 60)

# Summary
print("\nSUMMARY:")
print("-" * 40)
print("If all checks pass but frontend shows 'No data':")
print("1. The frontend DataTable expects { items: [], total: number }")
print("2. But the backend returns a plain array []")
print("3. The transformation in clinics.ts may not be working")
print("4. Check browser console for JavaScript errors")
print("5. Check Network tab in browser DevTools for API calls")
