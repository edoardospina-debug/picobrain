#!/bin/bash
# PicoBrain Development Server Startup Script

echo "🚀 Starting PicoBrain Development Servers..."
echo "==========================================="

# Check if PostgreSQL is running
echo "📊 Checking PostgreSQL..."
if pg_isready -h localhost -p 5432 > /dev/null 2>&1; then
    echo "✅ PostgreSQL is running"
else
    echo "⚠️ PostgreSQL is not running. Please start it first:"
    echo "   brew services start postgresql@16"
    echo "   Or use Docker: docker-compose up postgres -d"
    exit 1
fi

# Function to cleanup on exit
cleanup() {
    echo ""
    echo "🛑 Stopping servers..."
    kill $BACKEND_PID 2>/dev/null
    kill $FRONTEND_PID 2>/dev/null
    exit 0
}

trap cleanup INT TERM

# Start Backend Server
echo ""
echo "🔧 Starting Backend API Server (Port 8000)..."
cd backend
if [ ! -d "venv" ]; then
    echo "Creating Python virtual environment..."
    python3 -m venv venv
fi

source venv/bin/activate
pip install -q -r requirements.txt

# Create admin user if needed
echo "👤 Ensuring admin user exists..."
python manage.py create-admin 2>/dev/null || true

# Start FastAPI server
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload &
BACKEND_PID=$!
echo "✅ Backend started (PID: $BACKEND_PID)"

# Wait for backend to be ready
echo "⏳ Waiting for backend to be ready..."
for i in {1..30}; do
    if curl -s http://localhost:8000/health > /dev/null; then
        echo "✅ Backend is ready!"
        break
    fi
    sleep 1
done

# Start Frontend Server
echo ""
echo "🎨 Starting Frontend Server (Port 3000)..."
cd ../frontend

# Install dependencies if needed
if [ ! -d "node_modules" ]; then
    echo "Installing frontend dependencies..."
    npm install
fi

# Start Next.js development server
npm run dev &
FRONTEND_PID=$!
echo "✅ Frontend started (PID: $FRONTEND_PID)"

# Display access information
echo ""
echo "==========================================="
echo "✅ PicoBrain is ready!"
echo "==========================================="
echo "🌐 Frontend: http://localhost:3000"
echo "🔧 Backend API: http://localhost:8000"
echo "📚 API Docs: http://localhost:8000/docs"
echo ""
echo "🔐 Default Admin Credentials:"
echo "   Username: admin@picobrain.com"
echo "   Password: admin123"
echo ""
echo "Press Ctrl+C to stop all servers"
echo "==========================================="

# Keep script running
wait
