#!/usr/bin/env python3
"""
Test the clinics API endpoint
"""

import requests
import json
import sys

# Configuration
BASE_URL = "http://localhost:8000/api/v1"
USERNAME = "admin"
PASSWORD = "admin123"

def get_auth_token():
    """Login and get authentication token"""
    login_url = f"{BASE_URL}/auth/login"
    login_data = {
        "username": USERNAME,
        "password": PASSWORD
    }
    
    print(f"Logging in as {USERNAME}...")
    response = requests.post(login_url, data=login_data)
    
    if response.status_code == 200:
        token_data = response.json()
        print("✓ Login successful")
        return token_data.get("access_token")
    else:
        print(f"✗ Login failed: {response.status_code}")
        print(f"Response: {response.text}")
        return None

def test_clinics_endpoint(token):
    """Test the clinics GET endpoint"""
    clinics_url = f"{BASE_URL}/clinics"
    headers = {
        "Authorization": f"Bearer {token}"
    }
    
    print(f"\nFetching clinics from {clinics_url}...")
    response = requests.get(clinics_url, headers=headers)
    
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        clinics = response.json()
        print(f"✓ Successfully fetched {len(clinics)} clinics")
        
        if clinics:
            print("\nFirst 3 clinics:")
            for i, clinic in enumerate(clinics[:3], 1):
                print(f"\n{i}. {clinic.get('name', 'N/A')}")
                print(f"   - Code: {clinic.get('code', 'N/A')}")
                print(f"   - City: {clinic.get('city', 'N/A')}")
                print(f"   - Active: {clinic.get('is_active', 'N/A')}")
        else:
            print("⚠️  No clinics returned from API")
            
        return clinics
    else:
        print(f"✗ Failed to fetch clinics: {response.status_code}")
        print(f"Response: {response.text}")
        return None

def test_clinics_raw():
    """Test clinics endpoint without authentication to see raw response"""
    clinics_url = f"{BASE_URL}/clinics"
    
    print(f"\nTesting {clinics_url} without authentication...")
    response = requests.get(clinics_url)
    
    print(f"Status Code: {response.status_code}")
    print(f"Response Headers: {dict(response.headers)}")
    print(f"Response Body: {response.text[:500]}")  # First 500 chars

if __name__ == "__main__":
    print("=" * 60)
    print("TESTING CLINICS API ENDPOINT")
    print("=" * 60)
    
    # Test without auth first
    test_clinics_raw()
    
    # Get authentication token
    token = get_auth_token()
    
    if token:
        # Test clinics endpoint
        clinics = test_clinics_endpoint(token)
        
        if clinics:
            print("\n" + "=" * 60)
            print(f"SUMMARY: API returned {len(clinics)} clinics")
            print("=" * 60)
    else:
        print("\n✗ Could not authenticate. Check if backend is running.")
        sys.exit(1)
