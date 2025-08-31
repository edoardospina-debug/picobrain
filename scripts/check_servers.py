#!/usr/bin/env python3
"""Check if PicoBrain servers are running"""

import subprocess
import requests
import sys

def check_port(port):
    """Check if a port is in use"""
    try:
        result = subprocess.run(
            ['lsof', '-i', f':{port}'],
            capture_output=True,
            text=True
        )
        return result.returncode == 0
    except:
        return False

def check_backend():
    """Check if backend is running and healthy"""
    try:
        response = requests.get('http://localhost:8000/health', timeout=2)
        return response.status_code == 200
    except:
        return False

def check_frontend():
    """Check if frontend is running"""
    try:
        response = requests.get('http://localhost:3000', timeout=2)
        return response.status_code in [200, 304]
    except:
        return False

def main():
    print("🔍 Checking PicoBrain Server Status...")
    print("=" * 40)
    
    # Check PostgreSQL
    postgres_running = subprocess.run(
        ['pg_isready', '-h', 'localhost', '-p', '5432'],
        capture_output=True
    ).returncode == 0
    
    print(f"📊 PostgreSQL: {'✅ Running' if postgres_running else '❌ Not running'}")
    
    # Check Backend
    backend_port = check_port(8000)
    backend_healthy = check_backend()
    
    if backend_healthy:
        print(f"🔧 Backend API: ✅ Running and healthy (port 8000)")
    elif backend_port:
        print(f"🔧 Backend API: ⚠️ Port 8000 in use but not responding")
    else:
        print(f"🔧 Backend API: ❌ Not running")
    
    # Check Frontend
    frontend_port = check_port(3000)
    frontend_responding = check_frontend()
    
    if frontend_responding:
        print(f"🎨 Frontend: ✅ Running (port 3000)")
    elif frontend_port:
        print(f"🎨 Frontend: ⚠️ Port 3000 in use but not responding")
    else:
        print(f"🎨 Frontend: ❌ Not running")
    
    print("=" * 40)
    
    # Provide instructions
    if not postgres_running:
        print("\n⚠️ PostgreSQL needs to be started:")
        print("   brew services start postgresql@16")
        print("   OR")
        print("   docker-compose up postgres -d")
    
    if backend_healthy and frontend_responding:
        print("\n✅ All services are running!")
        print("\n📱 Access the app at:")
        print("   🌐 Frontend: http://localhost:3000")
        print("   📚 API Docs: http://localhost:8000/docs")
        print("\n🔐 Login with:")
        print("   Username: admin@picobrain.com")
        print("   Password: admin123")
    else:
        print("\n⚠️ Some services are not running.")
        print("Run this command to start all servers:")
        print("   cd /Users/edo/PyProjects/picobrain && ./start-servers.sh")
    
    return 0 if (backend_healthy and frontend_responding) else 1

if __name__ == "__main__":
    sys.exit(main())
