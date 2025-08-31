#!/bin/bash

echo "🔄 Restarting Frontend Server..."

# Find and kill the existing Next.js process
echo "Stopping current frontend server..."
lsof -ti:3000 | xargs kill -9 2>/dev/null || true

# Wait a moment
sleep 2

# Navigate to frontend directory
cd /Users/edo/PyProjects/picobrain/frontend

# Start the dev server
echo "Starting frontend server..."
npm run dev &

echo "✅ Frontend server restarting..."
echo "Wait 10-15 seconds for it to compile..."
echo "Then refresh your browser at http://localhost:3000/clinics"
