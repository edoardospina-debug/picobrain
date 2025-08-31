#!/bin/bash

# PicoBrain Health Check Script
# Run this before and after making changes to ensure nothing breaks

echo "🏥 PICOBRAIN SYSTEM HEALTH CHECK"
echo "================================="
echo ""

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if backend is running
echo "1. Checking Backend..."
if curl -s http://localhost:8000/health > /dev/null; then
    echo -e "${GREEN}✅ Backend is running${NC}"
    
    # Test login endpoint
    echo "   Testing login endpoint..."
    response=$(curl -s -X POST http://localhost:8000/api/v1/auth/login \
        -H "Content-Type: application/x-www-form-urlencoded" \
        -d "username=admin@picobrain.com&password=admin123" \
        -w "\n%{http_code}")
    
    http_code=$(echo "$response" | tail -n1)
    
    if [ "$http_code" = "200" ]; then
        echo -e "${GREEN}   ✅ Login endpoint working${NC}"
        
        # Extract token
        token=$(echo "$response" | head -n-1 | grep -o '"access_token":"[^"]*' | cut -d'"' -f4)
        
        if [ ! -z "$token" ]; then
            # Test employees endpoint
            echo "   Testing employees endpoint..."
            emp_response=$(curl -s -X GET "http://localhost:8000/api/v1/employees?skip=0&limit=1" \
                -H "Authorization: Bearer $token" \
                -w "\n%{http_code}")
            
            emp_code=$(echo "$emp_response" | tail -n1)
            
            if [ "$emp_code" = "200" ]; then
                echo -e "${GREEN}   ✅ Employees endpoint working${NC}"
            else
                echo -e "${RED}   ❌ Employees endpoint failed (HTTP $emp_code)${NC}"
            fi
        fi
    else
        echo -e "${RED}   ❌ Login endpoint failed (HTTP $http_code)${NC}"
    fi
else
    echo -e "${RED}❌ Backend is not running${NC}"
    echo "   Start it with:"
    echo "   cd backend && source venv/bin/activate && uvicorn app.main:app --reload"
fi

echo ""

# Check if frontend is running
echo "2. Checking Frontend..."
if curl -s http://localhost:3000 > /dev/null 2>&1; then
    echo -e "${GREEN}✅ Frontend is running${NC}"
    
    # Check specific pages
    pages=("/login" "/clinics" "/staff/employees")
    for page in "${pages[@]}"; do
        if curl -s "http://localhost:3000$page" > /dev/null 2>&1; then
            echo -e "${GREEN}   ✅ Page $page is accessible${NC}"
        else
            echo -e "${YELLOW}   ⚠️  Page $page might have issues${NC}"
        fi
    done
else
    echo -e "${RED}❌ Frontend is not running${NC}"
    echo "   Start it with:"
    echo "   cd frontend && npm run dev"
fi

echo ""

# Check database
echo "3. Checking Database..."
if psql -U edo -d picobraindb -c "SELECT COUNT(*) FROM employees;" > /dev/null 2>&1; then
    echo -e "${GREEN}✅ Database is accessible${NC}"
    
    # Count records
    emp_count=$(psql -U edo -d picobraindb -t -c "SELECT COUNT(*) FROM employees;")
    person_count=$(psql -U edo -d picobraindb -t -c "SELECT COUNT(*) FROM persons;")
    clinic_count=$(psql -U edo -d picobraindb -t -c "SELECT COUNT(*) FROM clinics;")
    
    echo "   Records found:"
    echo "   - Employees: $emp_count"
    echo "   - Persons: $person_count"
    echo "   - Clinics: $clinic_count"
else
    echo -e "${RED}❌ Database is not accessible${NC}"
fi

echo ""
echo "================================="
echo "HEALTH CHECK COMPLETE"
echo ""
echo "If any checks failed, fix them before making changes."
echo "Run this script again after changes to ensure nothing broke."
