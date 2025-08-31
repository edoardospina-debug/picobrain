#!/bin/bash

echo "======================================"
echo "RUNNING LOGIN DEBUG DIAGNOSTIC"
echo "======================================"

# First check if Python 3 is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed"
    exit 1
fi

# Check if requests module is available
python3 -c "import requests" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "⚠️  Installing requests module..."
    pip3 install requests
fi

# Run the debug script
python3 debug_login.py

echo ""
echo "======================================"
echo "ADDITIONAL CHECKS"
echo "======================================"

# Check if backend process is running
echo ""
echo "Checking for backend process..."
if pgrep -f "uvicorn app.main:app" > /dev/null; then
    echo "✅ Backend process found"
else
    echo "❌ Backend process not found"
    echo "   Start it with:"
    echo "   cd backend && source venv/bin/activate && uvicorn app.main:app --reload --port 8000"
fi

# Check if frontend process is running
echo ""
echo "Checking for frontend process..."
if pgrep -f "next dev" > /dev/null; then
    echo "✅ Frontend process found"
else
    echo "❌ Frontend process not found"
    echo "   Start it with:"
    echo "   cd frontend && npm run dev"
fi

# Check database connection
echo ""
echo "Checking database..."
psql -U edo -d picobraindb -c "SELECT COUNT(*) FROM users;" > /dev/null 2>&1
if [ $? -eq 0 ]; then
    user_count=$(psql -U edo -d picobraindb -t -c "SELECT COUNT(*) FROM users WHERE username='admin@picobrain.com';")
    if [ "$user_count" -gt 0 ]; then
        echo "✅ Database accessible and admin user exists"
    else
        echo "⚠️  Database accessible but admin user not found"
        echo "   You may need to reseed the database"
    fi
else
    echo "❌ Cannot connect to database"
fi

echo ""
echo "======================================"
echo "NEXT STEPS"
echo "======================================"
echo ""
echo "1. If backend is not running, start it:"
echo "   cd backend && source venv/bin/activate && uvicorn app.main:app --reload --port 8000"
echo ""
echo "2. If frontend is not running, start it:"
echo "   cd frontend && npm run dev"
echo ""
echo "3. Once both are running, test login at:"
echo "   http://localhost:3000/login"
echo ""
echo "4. Or use the debug page:"
echo "   http://localhost:3000/login/debug"
echo ""
