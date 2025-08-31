#!/bin/bash

# Make scripts executable
chmod +x check_changes.sh
chmod +x health_check.sh

echo "🔧 Quick Recovery Script"
echo "========================"
echo ""

# Test current state
echo "Testing current system state..."
echo ""

# Test backend health
echo "1. Backend Health Check:"
response=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/health)
if [ "$response" = "200" ]; then
    echo "   ✅ Backend is healthy"
else
    echo "   ❌ Backend issue detected (HTTP $response)"
    echo "   Fix: cd backend && source venv/bin/activate && uvicorn app.main:app --reload"
fi

# Test login
echo ""
echo "2. Login Test:"
login_response=$(curl -s -X POST http://localhost:8000/api/v1/auth/login \
    -H "Content-Type: application/x-www-form-urlencoded" \
    -d "username=admin@picobrain.com&password=admin123" \
    -o /dev/null -w "%{http_code}")

if [ "$login_response" = "200" ]; then
    echo "   ✅ Login endpoint working"
else
    echo "   ❌ Login endpoint issue (HTTP $login_response)"
fi

echo ""
echo "Recovery Options:"
echo "-----------------"
echo ""
echo "Option 1: Check what changed"
echo "  ./check_changes.sh"
echo ""
echo "Option 2: Full system health check"
echo "  ./health_check.sh"
echo ""
echo "Option 3: Revert recent changes (if using git)"
echo "  git status                    # See what changed"
echo "  git diff                       # See detailed changes"
echo "  git checkout -- <filename>    # Revert specific file"
echo ""
echo "Option 4: Test login directly"
echo "  Go to: http://localhost:3000/login/debug"
echo ""
echo "Option 5: Test employees directly"
echo "  Go to: http://localhost:3000/staff/employees/debug"
echo ""

# Check if login page exists
if [ -f "frontend/src/app/(auth)/login/page.tsx" ]; then
    echo "✅ Login page file exists"
else
    echo "❌ Login page file missing!"
fi
