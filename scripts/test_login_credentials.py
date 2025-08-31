#!/usr/bin/env python3
"""
Test all possible login combinations
"""

import requests
import json

print("=" * 60)
print("TESTING LOGIN CREDENTIALS")
print("=" * 60)

# Test combinations
test_credentials = [
    ("admin", "admin123"),
    ("admin@picobrain.com", "admin123"),
    ("manager", "manager123"),
    ("manager@picobrain.com", "manager123"),
    ("staff", "staff123"),
    ("staff@picobrain.com", "staff123"),
    ("testuser", "testpass123"),
    ("test@example.com", "testpass123"),
]

print("\nTesting login endpoint: http://localhost:8000/api/v1/auth/login")
print("\nTrying different credential combinations:\n")

for username, password in test_credentials:
    # Test with form-urlencoded (as we fixed in AuthProvider)
    login_data = {
        'username': username,
        'password': password
    }
    
    try:
        response = requests.post(
            'http://localhost:8000/api/v1/auth/login',
            data=login_data,  # This sends as form-urlencoded
            headers={'Content-Type': 'application/x-www-form-urlencoded'},
            timeout=2
        )
        
        if response.status_code == 200:
            print(f"✅ SUCCESS: {username} / {password}")
            token_data = response.json()
            if 'access_token' in token_data:
                print(f"   Token: {token_data['access_token'][:30]}...")
            break
        elif response.status_code == 401:
            print(f"❌ FAILED:  {username} / {password} - Incorrect credentials")
        else:
            print(f"⚠️  ERROR:   {username} / {password} - Status {response.status_code}")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ CONNECTION ERROR: Backend might not be running")
        print(f"   Error: {e}")
        break

print("\n" + "=" * 60)
