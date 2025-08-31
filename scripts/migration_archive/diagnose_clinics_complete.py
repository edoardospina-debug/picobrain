#!/usr/bin/env python3
"""
Complete diagnostic of the clinics display issue
"""

import requests
import json
import sys
from datetime import datetime

def colored(text, color):
    colors = {
        'red': '\033[91m',
        'green': '\033[92m',
        'yellow': '\033[93m',
        'blue': '\033[94m',
        'reset': '\033[0m'
    }
    return f"{colors.get(color, '')}{text}{colors['reset']}"

print(colored("="*60, 'blue'))
print(colored("PICOBRAIN CLINICS DIAGNOSTIC", 'blue'))
print(colored("="*60, 'blue'))
print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print()

# Step 1: Check if backend is running
print(colored("1. Checking Backend Status...", 'yellow'))
try:
    health = requests.get('http://localhost:8000/health', timeout=2)
    if health.status_code == 200:
        print(colored("   ✅ Backend is running", 'green'))
    else:
        print(colored(f"   ⚠️ Backend responded with status {health.status_code}", 'yellow'))
except Exception as e:
    print(colored(f"   ❌ Backend not reachable: {e}", 'red'))
    print(colored("\n   Please start the backend with: cd backend && uvicorn app.main:app --reload", 'yellow'))
    sys.exit(1)

# Step 2: Test login
print(colored("\n2. Testing Authentication...", 'yellow'))
login_data = {
    'username': 'admin',
    'password': 'admin123'
}

try:
    # Use form-urlencoded as we fixed in AuthProvider
    login_response = requests.post(
        'http://localhost:8000/api/v1/auth/login',
        data=login_data,  # This sends as form-urlencoded by default
        headers={'Content-Type': 'application/x-www-form-urlencoded'}
    )
    
    if login_response.status_code == 200:
        token_data = login_response.json()
        access_token = token_data.get('access_token')
        if access_token:
            print(colored("   ✅ Login successful", 'green'))
            print(f"   Token: {access_token[:50]}...")
        else:
            print(colored("   ❌ No access token in response", 'red'))
            print(f"   Response: {login_response.json()}")
            sys.exit(1)
    else:
        print(colored(f"   ❌ Login failed with status {login_response.status_code}", 'red'))
        print(f"   Response: {login_response.text}")
        sys.exit(1)
except Exception as e:
    print(colored(f"   ❌ Login error: {e}", 'red'))
    sys.exit(1)

# Step 3: Test clinics API
print(colored("\n3. Testing Clinics API...", 'yellow'))
headers = {
    'Authorization': f'Bearer {access_token}',
    'Content-Type': 'application/json'
}

try:
    clinics_response = requests.get('http://localhost:8000/api/v1/clinics', headers=headers)
    
    if clinics_response.status_code == 200:
        clinics_data = clinics_response.json()
        print(colored("   ✅ Clinics API responded successfully", 'green'))
        
        # Check the format
        if isinstance(clinics_data, list):
            print(colored(f"   📊 Response format: Array with {len(clinics_data)} clinics", 'yellow'))
            if clinics_data:
                print("   First clinic:")
                first_clinic = clinics_data[0]
                for key in ['id', 'code', 'name', 'city']:
                    if key in first_clinic:
                        print(f"     - {key}: {first_clinic[key]}")
            
            print(colored("\n   ⚠️ ISSUE IDENTIFIED:", 'yellow'))
            print(colored("   Backend returns: [array]", 'red'))
            print(colored("   DataTable expects: {items: [], total: number}", 'red'))
            
        elif isinstance(clinics_data, dict) and 'items' in clinics_data:
            print(colored("   ✅ Response already in correct format!", 'green'))
            print(f"   Items: {len(clinics_data.get('items', []))}")
            print(f"   Total: {clinics_data.get('total', 0)}")
        else:
            print(colored(f"   ❓ Unexpected format: {type(clinics_data)}", 'yellow'))
            print(f"   Data: {json.dumps(clinics_data, indent=2)[:500]}")
    else:
        print(colored(f"   ❌ Clinics API failed with status {clinics_response.status_code}", 'red'))
        print(f"   Response: {clinics_response.text}")
except Exception as e:
    print(colored(f"   ❌ Clinics API error: {e}", 'red'))

# Step 4: Check frontend
print(colored("\n4. Checking Frontend...", 'yellow'))
try:
    frontend_response = requests.get('http://localhost:3000', timeout=2)
    if frontend_response.status_code in [200, 304]:
        print(colored("   ✅ Frontend is running", 'green'))
    else:
        print(colored(f"   ⚠️ Frontend responded with status {frontend_response.status_code}", 'yellow'))
except Exception as e:
    print(colored(f"   ❌ Frontend not reachable: {e}", 'red'))
    print(colored("   Please check if Next.js dev server is running", 'yellow'))

# Step 5: Solution
print(colored("\n" + "="*60, 'blue'))
print(colored("SOLUTION", 'blue'))
print(colored("="*60, 'blue'))

print("\nWe've already added transformation in:")
print(colored("  /frontend/src/lib/api/endpoints/clinics.ts", 'green'))

print("\nThe transformation code should convert:")
print("  FROM: " + colored("[array]", 'red'))
print("  TO:   " + colored("{items: [array], total: number}", 'green'))

print("\nNext steps to fix:")
print("1. " + colored("Check if frontend server has restarted to pick up changes", 'yellow'))
print("2. " + colored("Clear browser cache and localStorage", 'yellow'))
print("3. " + colored("Check browser console for our debug logs (🔍 📦 ✅)", 'yellow'))

print("\nTo restart frontend:")
print(colored("  cd frontend && npm run dev", 'blue'))

print("\nTo see if transformation is working, look for these in browser console:")
print("  🔍 clinicsApi.list called with params")
print("  📦 Raw response from backend")
print("  ✅ Transformed data")

print(colored("\n" + "="*60, 'blue'))
