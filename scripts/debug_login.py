#!/usr/bin/env python3
"""
Debug script to test login functionality step by step
"""
import requests
import json
import sys
from datetime import datetime

# Color codes for output
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'

def print_header(text):
    print(f"\n{BLUE}{'=' * 60}{RESET}")
    print(f"{BLUE}{text}{RESET}")
    print(f"{BLUE}{'=' * 60}{RESET}")

def print_success(text):
    print(f"{GREEN}✅ {text}{RESET}")

def print_error(text):
    print(f"{RED}❌ {text}{RESET}")

def print_warning(text):
    print(f"{YELLOW}⚠️  {text}{RESET}")

def print_info(text):
    print(f"   {text}")

# Step 1: Check Backend Health
def test_backend_health():
    print_header("STEP 1: BACKEND HEALTH CHECK")
    try:
        response = requests.get('http://localhost:8000/health', timeout=5)
        if response.status_code == 200:
            print_success("Backend is healthy!")
            print_info(f"Response: {response.json()}")
            return True
        else:
            print_error(f"Backend returned status {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print_error("Backend is not running!")
        print_info("Start it with:")
        print_info("cd backend && source venv/bin/activate && uvicorn app.main:app --reload --port 8000")
        return False
    except Exception as e:
        print_error(f"Backend check failed: {e}")
        return False

# Step 2: Check Frontend
def test_frontend():
    print_header("STEP 2: FRONTEND CHECK")
    try:
        response = requests.get('http://localhost:3000', timeout=5)
        if response.status_code in [200, 304]:
            print_success("Frontend is running!")
            return True
        else:
            print_warning(f"Frontend returned status {response.status_code}")
            return True  # Frontend might still be working
    except requests.exceptions.ConnectionError:
        print_error("Frontend is not running!")
        print_info("Start it with:")
        print_info("cd frontend && npm run dev")
        return False
    except Exception as e:
        print_error(f"Frontend check failed: {e}")
        return False

# Step 3: Test CORS
def test_cors():
    print_header("STEP 3: CORS CONFIGURATION CHECK")
    try:
        response = requests.options(
            'http://localhost:8000/api/v1/auth/login',
            headers={
                'Origin': 'http://localhost:3000',
                'Access-Control-Request-Method': 'POST',
                'Access-Control-Request-Headers': 'content-type'
            },
            timeout=5
        )
        
        cors_headers = {
            'Access-Control-Allow-Origin': response.headers.get('access-control-allow-origin'),
            'Access-Control-Allow-Methods': response.headers.get('access-control-allow-methods'),
            'Access-Control-Allow-Headers': response.headers.get('access-control-allow-headers'),
            'Access-Control-Allow-Credentials': response.headers.get('access-control-allow-credentials')
        }
        
        all_good = True
        for header, value in cors_headers.items():
            if value:
                print_success(f"{header}: {value}")
            else:
                print_warning(f"{header}: NOT SET")
                all_good = False
        
        return all_good
    except Exception as e:
        print_error(f"CORS check failed: {e}")
        return False

# Step 4: Test Login Endpoint
def test_login():
    print_header("STEP 4: LOGIN ENDPOINT TEST")
    
    # Test with correct credentials
    print("\nTesting with correct credentials...")
    try:
        response = requests.post(
            'http://localhost:8000/api/v1/auth/login',
            data={
                'username': 'admin@picobrain.com',
                'password': 'admin123'
            },
            headers={
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            timeout=5
        )
        
        print_info(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print_success("Login successful!")
            
            if 'access_token' in data:
                token = data['access_token']
                print_success(f"Token received: {token[:30]}...")
                
                # Also check if user data is included
                if 'user' in data:
                    user = data['user']
                    print_success(f"User data received: {user.get('username', 'N/A')}")
                
                return token
            else:
                print_error("No access_token in response!")
                print_info(f"Response: {json.dumps(data, indent=2)}")
                return None
        else:
            print_error(f"Login failed with status {response.status_code}")
            print_info(f"Response: {response.text}")
            return None
            
    except Exception as e:
        print_error(f"Login test failed: {e}")
        return None

# Step 5: Test Auth/Me Endpoint
def test_auth_me(token):
    print_header("STEP 5: AUTH/ME ENDPOINT TEST")
    
    if not token:
        print_warning("No token available, skipping auth/me test")
        return False
    
    try:
        response = requests.get(
            'http://localhost:8000/api/v1/auth/me',
            headers={
                'Authorization': f'Bearer {token}'
            },
            timeout=5
        )
        
        print_info(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            user_data = response.json()
            print_success("User data retrieved successfully!")
            print_info(f"Username: {user_data.get('username', 'N/A')}")
            print_info(f"Email: {user_data.get('email', 'N/A')}")
            print_info(f"Role: {user_data.get('role', 'N/A')}")
            return True
        else:
            print_error(f"Auth/me failed with status {response.status_code}")
            print_info(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print_error(f"Auth/me test failed: {e}")
        return False

# Step 6: Test Employee Endpoint
def test_employees(token):
    print_header("STEP 6: EMPLOYEE ENDPOINT TEST")
    
    if not token:
        print_warning("No token available, skipping employee test")
        return False
    
    try:
        response = requests.get(
            'http://localhost:8000/api/v1/employees?skip=0&limit=5',
            headers={
                'Authorization': f'Bearer {token}'
            },
            timeout=5
        )
        
        print_info(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            employees = response.json()
            print_success(f"Employee data retrieved! Count: {len(employees)}")
            
            if employees and len(employees) > 0:
                emp = employees[0]
                print_info(f"Sample employee:")
                print_info(f"  Code: {emp.get('employee_code', 'N/A')}")
                print_info(f"  Role: {emp.get('role', 'N/A')}")
                
                if emp.get('person'):
                    person = emp['person']
                    print_info(f"  Name: {person.get('first_name', '')} {person.get('last_name', '')}")
                    print_info(f"  Email: {person.get('email', 'N/A')}")
                else:
                    print_warning("  Person data missing!")
            else:
                print_warning("No employees returned (empty array)")
            
            return True
        else:
            print_error(f"Employee endpoint failed with status {response.status_code}")
            print_info(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print_error(f"Employee test failed: {e}")
        return False

# Main execution
def main():
    print(f"\n{BLUE}PICOBRAIN LOGIN DEBUG DIAGNOSTIC{RESET}")
    print(f"{BLUE}Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}{RESET}")
    
    # Track results
    results = {}
    
    # Run tests
    results['backend'] = test_backend_health()
    if not results['backend']:
        print_error("\n⚠️  Backend must be running to continue tests!")
        return
    
    results['frontend'] = test_frontend()
    results['cors'] = test_cors()
    
    token = test_login()
    results['login'] = token is not None
    
    if token:
        results['auth_me'] = test_auth_me(token)
        results['employees'] = test_employees(token)
    else:
        results['auth_me'] = False
        results['employees'] = False
    
    # Summary
    print_header("DIAGNOSTIC SUMMARY")
    
    all_passed = True
    for test, passed in results.items():
        if passed:
            print_success(f"{test.upper()}: PASSED")
        else:
            print_error(f"{test.upper()}: FAILED")
            all_passed = False
    
    print_header("DIAGNOSIS")
    
    if all_passed:
        print_success("All tests passed! The system is working correctly.")
        print_info("\nYou should be able to:")
        print_info("1. Login at http://localhost:3000/login")
        print_info("2. View employees at http://localhost:3000/staff/employees")
    else:
        print_warning("Some tests failed. Here's what to fix:")
        
        if not results['backend']:
            print_error("\n1. Start the backend:")
            print_info("   cd backend && source venv/bin/activate && uvicorn app.main:app --reload")
        
        if not results['frontend']:
            print_error("\n2. Start the frontend:")
            print_info("   cd frontend && npm run dev")
        
        if not results['cors']:
            print_error("\n3. CORS issue detected")
            print_info("   Check backend/app/core/config.py BACKEND_CORS_ORIGINS")
        
        if not results['login']:
            print_error("\n4. Login endpoint issue")
            print_info("   - Check if admin@picobrain.com user exists in database")
            print_info("   - Verify password is 'admin123'")
            print_info("   - Check backend logs for errors")
        
        if results['login'] and not results['auth_me']:
            print_error("\n5. Token validation issue")
            print_info("   - Token might be malformed")
            print_info("   - Check JWT configuration")
        
        if results['login'] and not results['employees']:
            print_error("\n6. Employee data issue")
            print_info("   - Check if employees exist in database")
            print_info("   - Verify expire_on_commit=False in database.py")
    
    print(f"\n{BLUE}Diagnostic completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}{RESET}")

if __name__ == "__main__":
    main()
