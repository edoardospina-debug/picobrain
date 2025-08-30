#!/bin/bash

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# API Base URL
BASE_URL="http://localhost:8000/api/v1"

# Test results
PASSED=0
FAILED=0

echo "========================================="
echo "🧪 PicoBrain API Comprehensive Test Suite"
echo "========================================="

# Function to print test result
print_result() {
    if [ $1 -eq 0 ]; then
        echo -e "${GREEN}✓ PASS${NC}: $2"
        ((PASSED++))
    else
        echo -e "${RED}✗ FAIL${NC}: $2"
        ((FAILED++))
    fi
}

# Step 1: Test public endpoints
echo -e "\n${YELLOW}Testing Public Endpoints...${NC}"

# Test root
curl -s http://localhost:8000/ > /dev/null 2>&1
print_result $? "GET / (root)"

# Test health
curl -s http://localhost:8000/health > /dev/null 2>&1
print_result $? "GET /health"

# Step 2: Login and get token
echo -e "\n${YELLOW}Testing Authentication...${NC}"

LOGIN_RESPONSE=$(curl -s -X POST "$BASE_URL/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin@picobrain.com&password=admin123")

if echo "$LOGIN_RESPONSE" | grep -q "access_token"; then
    print_result 0 "POST /auth/login"
    TOKEN=$(echo "$LOGIN_RESPONSE" | grep -o '"access_token":"[^"]*' | cut -d'"' -f4)
    REFRESH_TOKEN=$(echo "$LOGIN_RESPONSE" | grep -o '"refresh_token":"[^"]*' | cut -d'"' -f4)
    echo -e "${GREEN}Token obtained successfully${NC}"
else
    print_result 1 "POST /auth/login"
    echo -e "${RED}Failed to get token. Response: $LOGIN_RESPONSE${NC}"
    exit 1
fi

# Step 3: Test authenticated endpoints
echo -e "\n${YELLOW}Testing Auth Endpoints with Token...${NC}"

# Test /auth/me
ME_RESPONSE=$(curl -s -X GET "$BASE_URL/auth/me" \
  -H "Authorization: Bearer $TOKEN")
if echo "$ME_RESPONSE" | grep -q "username"; then
    print_result 0 "GET /auth/me"
    USER_ID=$(echo "$ME_RESPONSE" | grep -o '"id":"[^"]*' | cut -d'"' -f4)
else
    print_result 1 "GET /auth/me"
fi

# Test refresh token
REFRESH_RESPONSE=$(curl -s -X POST "$BASE_URL/auth/refresh" \
  -H "Content-Type: application/json" \
  -d "{\"refresh_token\":\"$REFRESH_TOKEN\"}")
if echo "$REFRESH_RESPONSE" | grep -q "access_token"; then
    print_result 0 "POST /auth/refresh"
else
    print_result 1 "POST /auth/refresh"
fi

# Test logout
LOGOUT_RESPONSE=$(curl -s -X POST "$BASE_URL/auth/logout" \
  -H "Authorization: Bearer $TOKEN")
if echo "$LOGOUT_RESPONSE" | grep -q "Successfully logged out"; then
    print_result 0 "POST /auth/logout"
else
    print_result 1 "POST /auth/logout"
fi

# Step 4: Test Person endpoints
echo -e "\n${YELLOW}Testing Person Endpoints...${NC}"

# List persons
PERSONS_RESPONSE=$(curl -s -X GET "$BASE_URL/persons/" \
  -H "Authorization: Bearer $TOKEN")
if [ $? -eq 0 ]; then
    print_result 0 "GET /persons/"
else
    print_result 1 "GET /persons/"
fi

# Create a test person
CREATE_PERSON=$(curl -s -X POST "$BASE_URL/persons/" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "Test",
    "last_name": "User",
    "email": "test.user@example.com",
    "phone_mobile": "+1234567890",
    "dob": "1990-01-01",
    "gender": "M"
  }')

if echo "$CREATE_PERSON" | grep -q "id"; then
    print_result 0 "POST /persons/"
    PERSON_ID=$(echo "$CREATE_PERSON" | grep -o '"id":"[^"]*' | cut -d'"' -f4)
    
    # Get specific person
    GET_PERSON=$(curl -s -X GET "$BASE_URL/persons/$PERSON_ID" \
      -H "Authorization: Bearer $TOKEN")
    if echo "$GET_PERSON" | grep -q "$PERSON_ID"; then
        print_result 0 "GET /persons/{id}"
    else
        print_result 1 "GET /persons/{id}"
    fi
    
    # Update person
    UPDATE_PERSON=$(curl -s -X PUT "$BASE_URL/persons/$PERSON_ID" \
      -H "Authorization: Bearer $TOKEN" \
      -H "Content-Type: application/json" \
      -d '{"last_name": "UpdatedUser"}')
    if echo "$UPDATE_PERSON" | grep -q "UpdatedUser"; then
        print_result 0 "PUT /persons/{id}"
    else
        print_result 1 "PUT /persons/{id}"
    fi
    
    # Delete person (admin only)
    DELETE_PERSON=$(curl -s -X DELETE "$BASE_URL/persons/$PERSON_ID" \
      -H "Authorization: Bearer $TOKEN")
    if echo "$DELETE_PERSON" | grep -q "deleted successfully"; then
        print_result 0 "DELETE /persons/{id}"
    else
        print_result 1 "DELETE /persons/{id}"
    fi
else
    print_result 1 "POST /persons/"
    echo "Could not create test person: $CREATE_PERSON"
fi

# Step 5: Test Clinic endpoints
echo -e "\n${YELLOW}Testing Clinic Endpoints...${NC}"

# List clinics
CLINICS_RESPONSE=$(curl -s -X GET "$BASE_URL/clinics/" \
  -H "Authorization: Bearer $TOKEN")
if [ $? -eq 0 ]; then
    print_result 0 "GET /clinics/"
else
    print_result 1 "GET /clinics/"
fi

# Create a test clinic (admin only)
CREATE_CLINIC=$(curl -s -X POST "$BASE_URL/clinics/" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "code": "TEST001",
    "name": "Test Clinic",
    "functional_currency": "USD",
    "city": "Test City",
    "country_code": "US"
  }')

if echo "$CREATE_CLINIC" | grep -q "id"; then
    print_result 0 "POST /clinics/"
    CLINIC_ID=$(echo "$CREATE_CLINIC" | grep -o '"id":"[^"]*' | cut -d'"' -f4)
    
    # Get specific clinic
    GET_CLINIC=$(curl -s -X GET "$BASE_URL/clinics/$CLINIC_ID" \
      -H "Authorization: Bearer $TOKEN")
    if echo "$GET_CLINIC" | grep -q "$CLINIC_ID"; then
        print_result 0 "GET /clinics/{id}"
    else
        print_result 1 "GET /clinics/{id}"
    fi
    
    # Update clinic
    UPDATE_CLINIC=$(curl -s -X PUT "$BASE_URL/clinics/$CLINIC_ID" \
      -H "Authorization: Bearer $TOKEN" \
      -H "Content-Type: application/json" \
      -d '{"name": "Updated Test Clinic"}')
    if echo "$UPDATE_CLINIC" | grep -q "Updated Test Clinic"; then
        print_result 0 "PUT /clinics/{id}"
    else
        print_result 1 "PUT /clinics/{id}"
    fi
    
    # Delete clinic
    DELETE_CLINIC=$(curl -s -X DELETE "$BASE_URL/clinics/$CLINIC_ID" \
      -H "Authorization: Bearer $TOKEN")
    if echo "$DELETE_CLINIC" | grep -q "deleted successfully"; then
        print_result 0 "DELETE /clinics/{id}"
    else
        print_result 1 "DELETE /clinics/{id}"
    fi
else
    print_result 1 "POST /clinics/"
    echo "Could not create test clinic: $CREATE_CLINIC"
fi

# Step 6: Test User endpoints
echo -e "\n${YELLOW}Testing User Endpoints...${NC}"

# List users (admin only)
USERS_RESPONSE=$(curl -s -X GET "$BASE_URL/users/" \
  -H "Authorization: Bearer $TOKEN")
if echo "$USERS_RESPONSE" | grep -q "username"; then
    print_result 0 "GET /users/"
else
    print_result 1 "GET /users/"
fi

# Create a test user (admin only)
CREATE_USER=$(curl -s -X POST "$BASE_URL/users/" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser@picobrain.com",
    "password": "testpass123",
    "role": "staff",
    "is_active": true
  }')

if echo "$CREATE_USER" | grep -q "id"; then
    print_result 0 "POST /users/"
    TEST_USER_ID=$(echo "$CREATE_USER" | grep -o '"id":"[^"]*' | cut -d'"' -f4)
    
    # Get specific user
    GET_USER=$(curl -s -X GET "$BASE_URL/users/$TEST_USER_ID" \
      -H "Authorization: Bearer $TOKEN")
    if echo "$GET_USER" | grep -q "$TEST_USER_ID"; then
        print_result 0 "GET /users/{id}"
    else
        print_result 1 "GET /users/{id}"
    fi
    
    # Update user
    UPDATE_USER=$(curl -s -X PUT "$BASE_URL/users/$TEST_USER_ID" \
      -H "Authorization: Bearer $TOKEN" \
      -H "Content-Type: application/json" \
      -d '{"role": "medical"}')
    if echo "$UPDATE_USER" | grep -q "medical"; then
        print_result 0 "PUT /users/{id}"
    else
        print_result 1 "PUT /users/{id}"
    fi
    
    # Reset password
    RESET_PASSWORD=$(curl -s -X POST "$BASE_URL/users/$TEST_USER_ID/reset-password" \
      -H "Authorization: Bearer $TOKEN" \
      -H "Content-Type: application/json" \
      -d '{"password": "newpass123"}')
    if echo "$RESET_PASSWORD" | grep -q "$TEST_USER_ID"; then
        print_result 0 "POST /users/{id}/reset-password"
    else
        print_result 1 "POST /users/{id}/reset-password"
    fi
    
    # Delete user
    DELETE_USER=$(curl -s -X DELETE "$BASE_URL/users/$TEST_USER_ID" \
      -H "Authorization: Bearer $TOKEN")
    if echo "$DELETE_USER" | grep -q "deleted successfully"; then
        print_result 0 "DELETE /users/{id}"
    else
        print_result 1 "DELETE /users/{id}"
    fi
else
    print_result 1 "POST /users/"
    echo "Could not create test user: $CREATE_USER"
fi

# Final Report
echo -e "\n========================================="
echo "📊 Test Results Summary"
echo "========================================="
echo -e "${GREEN}Passed: $PASSED${NC}"
echo -e "${RED}Failed: $FAILED${NC}"
TOTAL=$((PASSED + FAILED))
PERCENTAGE=$((PASSED * 100 / TOTAL))
echo "Success Rate: $PERCENTAGE%"

if [ $FAILED -eq 0 ]; then
    echo -e "\n${GREEN}🎉 All tests passed! Your API is working perfectly!${NC}"
else
    echo -e "\n${YELLOW}⚠️ Some tests failed. Please review the output above.${NC}"
fi
