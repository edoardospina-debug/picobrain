import requests
import json
from datetime import datetime

# Colors for terminal output
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
RESET = '\033[0m'

BASE_URL = "http://localhost:8000/api/v1"
test_results = []

def log_test(name, passed, details=""):
    status = f"{GREEN}✓ PASS{RESET}" if passed else f"{RED}✗ FAIL{RESET}"
    print(f"{status}: {name}")
    if details and not passed:
        print(f"  Details: {details}")
    test_results.append({"name": name, "passed": passed, "details": details})

print("=" * 50)
print("🧪 PicoBrain API Test Suite")
print("=" * 50)

# Test 1: Public endpoints
print(f"\n{YELLOW}Testing Public Endpoints...{RESET}")
try:
    r = requests.get("http://localhost:8000/")
    log_test("GET / (root)", r.status_code == 200)
    
    r = requests.get("http://localhost:8000/health")
    log_test("GET /health", r.status_code == 200)
except Exception as e:
    log_test("Public endpoints", False, str(e))

# Test 2: Authentication
print(f"\n{YELLOW}Testing Authentication...{RESET}")
try:
    # Login
    login_data = {
        "username": "admin@picobrain.com",
        "password": "admin123"
    }
    r = requests.post(f"{BASE_URL}/auth/login", data=login_data)
    if r.status_code == 200:
        tokens = r.json()
        access_token = tokens["access_token"]
        refresh_token = tokens["refresh_token"]
        log_test("POST /auth/login", True)
        
        # Setup headers for authenticated requests
        headers = {"Authorization": f"Bearer {access_token}"}
        
        # Test /auth/me
        r = requests.get(f"{BASE_URL}/auth/me", headers=headers)
        user_data = r.json() if r.status_code == 200 else {}
        log_test("GET /auth/me", r.status_code == 200)
        
        # Test refresh
        r = requests.post(f"{BASE_URL}/auth/refresh", json={"refresh_token": refresh_token})
        log_test("POST /auth/refresh", r.status_code == 200)
        
        # Test logout
        r = requests.post(f"{BASE_URL}/auth/logout", headers=headers)
        log_test("POST /auth/logout", r.status_code == 200)
    else:
        log_test("POST /auth/login", False, r.text)
        print(f"{RED}Cannot continue without authentication{RESET}")
        exit(1)
except Exception as e:
    log_test("Authentication", False, str(e))
    exit(1)

# Test 3: Person endpoints
print(f"\n{YELLOW}Testing Person Endpoints...{RESET}")
try:
    # List persons
    r = requests.get(f"{BASE_URL}/persons/", headers=headers)
    log_test("GET /persons/", r.status_code == 200)
    
    # Create person
    person_data = {
        "first_name": "Test",
        "last_name": "User",
        "email": f"test.user.{datetime.now().timestamp()}@example.com",
        "phone_mobile": "+1234567890",
        "dob": "1990-01-01",
        "gender": "M"
    }
    r = requests.post(f"{BASE_URL}/persons/", json=person_data, headers=headers)
    if r.status_code == 200:
        person = r.json()
        person_id = person["id"]
        log_test("POST /persons/", True)
        
        # Get specific person
        r = requests.get(f"{BASE_URL}/persons/{person_id}", headers=headers)
        log_test(f"GET /persons/{person_id}", r.status_code == 200)
        
        # Update person
        update_data = {"last_name": "UpdatedUser"}
        r = requests.put(f"{BASE_URL}/persons/{person_id}", json=update_data, headers=headers)
        log_test(f"PUT /persons/{person_id}", r.status_code == 200)
        
        # Delete person
        r = requests.delete(f"{BASE_URL}/persons/{person_id}", headers=headers)
        log_test(f"DELETE /persons/{person_id}", r.status_code == 200)
    else:
        log_test("POST /persons/", False, r.text)
except Exception as e:
    log_test("Person endpoints", False, str(e))

# Test 4: Clinic endpoints
print(f"\n{YELLOW}Testing Clinic Endpoints...{RESET}")
try:
    # List clinics
    r = requests.get(f"{BASE_URL}/clinics/", headers=headers)
    log_test("GET /clinics/", r.status_code == 200)
    
    # Create clinic
    clinic_data = {
        "code": f"TEST{int(datetime.now().timestamp())}",
        "name": "Test Clinic",
        "functional_currency": "USD",
        "city": "Test City",
        "country_code": "US"
    }
    r = requests.post(f"{BASE_URL}/clinics/", json=clinic_data, headers=headers)
    if r.status_code == 200:
        clinic = r.json()
        clinic_id = clinic["id"]
        log_test("POST /clinics/", True)
        
        # Get specific clinic
        r = requests.get(f"{BASE_URL}/clinics/{clinic_id}", headers=headers)
        log_test(f"GET /clinics/{clinic_id}", r.status_code == 200)
        
        # Update clinic
        update_data = {"name": "Updated Test Clinic"}
        r = requests.put(f"{BASE_URL}/clinics/{clinic_id}", json=update_data, headers=headers)
        log_test(f"PUT /clinics/{clinic_id}", r.status_code == 200)
        
        # Delete clinic
        r = requests.delete(f"{BASE_URL}/clinics/{clinic_id}", headers=headers)
        log_test(f"DELETE /clinics/{clinic_id}", r.status_code == 200)
    else:
        log_test("POST /clinics/", False, r.text)
except Exception as e:
    log_test("Clinic endpoints", False, str(e))

# Test 5: User endpoints
print(f"\n{YELLOW}Testing User Endpoints...{RESET}")
try:
    # List users
    r = requests.get(f"{BASE_URL}/users/", headers=headers)
    log_test("GET /users/", r.status_code == 200)
    
    # Create user
    user_data = {
        "username": f"testuser{int(datetime.now().timestamp())}@picobrain.com",
        "password": "testpass123",
        "role": "staff",
        "is_active": True
    }
    r = requests.post(f"{BASE_URL}/users/", json=user_data, headers=headers)
    if r.status_code == 200:
        user = r.json()
        user_id = user["id"]
        log_test("POST /users/", True)
        
        # Get specific user
        r = requests.get(f"{BASE_URL}/users/{user_id}", headers=headers)
        log_test(f"GET /users/{user_id}", r.status_code == 200)
        
        # Update user
        update_data = {"role": "medical"}
        r = requests.put(f"{BASE_URL}/users/{user_id}", json=update_data, headers=headers)
        log_test(f"PUT /users/{user_id}", r.status_code == 200)
        
        # Reset password
        password_data = {"password": "newpass123"}
        r = requests.post(f"{BASE_URL}/users/{user_id}/reset-password", json=password_data, headers=headers)
        log_test(f"POST /users/{user_id}/reset-password", r.status_code == 200)
        
        # Delete user
        r = requests.delete(f"{BASE_URL}/users/{user_id}", headers=headers)
        log_test(f"DELETE /users/{user_id}", r.status_code == 200)
    else:
        log_test("POST /users/", False, r.text)
except Exception as e:
    log_test("User endpoints", False, str(e))

# Final Report
print("\n" + "=" * 50)
print("📊 Test Results Summary")
print("=" * 50)
passed = sum(1 for t in test_results if t["passed"])
failed = sum(1 for t in test_results if not t["passed"])
total = len(test_results)
percentage = (passed * 100 // total) if total > 0 else 0

print(f"{GREEN}Passed: {passed}{RESET}")
print(f"{RED}Failed: {failed}{RESET}")
print(f"Total: {total}")
print(f"Success Rate: {percentage}%")

if failed == 0:
    print(f"\n{GREEN}🎉 All tests passed! Your API is working perfectly!{RESET}")
else:
    print(f"\n{YELLOW}⚠️ Some tests failed. Details:{RESET}")
    for test in test_results:
        if not test["passed"]:
            print(f"  - {test['name']}: {test['details']}")

# Save detailed results
with open("test_results.json", "w") as f:
    json.dump({
        "timestamp": datetime.now().isoformat(),
        "summary": {
            "passed": passed,
            "failed": failed,
            "total": total,
            "percentage": percentage
        },
        "tests": test_results
    }, f, indent=2)
print(f"\n💾 Detailed results saved to test_results.json")
