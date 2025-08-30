<!-- CLAUDE: ALWAYS READ THIS FIRST -->
# Knowledge Base - PicoBrain
Version: 2.2.0
Updated: 2025-08-31  
Current Date: Saturday, August 31, 2025

## 🚀 Employee Migration COMPLETED (2025-08-31)

### ✅ Migration Successfully Completed!
- **Total Employees**: 87 successfully migrated from CSV
- **Database**: `picobraindb` (PostgreSQL on localhost:5432)
- **User**: `edo` (NOT postgres - critical!)
- **Final Status**: ✅ ALL 87 employees in database
  - 53 Receptionists (includes staff/admin/manager mapped)
  - 34 Doctors (with license numbers)
  - 48 Active / 39 Inactive employees

### 🔥 CRITICAL LESSONS LEARNED (2025-08-31)

#### Database Structure Discovery
1. **Database Name**: `picobraindb` (NOT edo_brain_4!)
2. **PostgreSQL User**: `edo` (NOT postgres!)
3. **Two-Table Architecture**:
   - `persons` table: Contains first_name, last_name, email, dob, id_number
   - `employees` table: Contains person_id (FK), role, hire_date, clinic_id
   - Employees MUST have a person record first!

#### Missing Components Fixed
1. **currencies table**: Created with USD, EUR, GBP, CAD
2. **doctors table**: Created for doctor license tracking
3. **currency_code column**: Added to employees (default USD)
4. **primary_clinic_id**: REQUIRED - cannot be NULL!

#### Key Required Fields
- **persons table**: id, first_name, last_name, email
- **employees table**: id, person_id, primary_clinic_id, role, hire_date
- **doctors table**: id, employee_id, license_number

### Migration Scripts Evolution
1. `employee_migration.py` - API-based (failed - wrong approach)
2. `simple_migration.py` - Direct DB (failed - wrong database)
3. `check_database.py` - Diagnostic (found correct DB)
4. `check_currencies_status.py` - Found currencies table exists
5. `list_databases.py` - Found correct DB: picobraindb
6. `check_employees_schema.py` - Discovered persons-employees relationship
7. `correct_migration.py` - Used correct structure (partial success)
8. `diagnose_migration.py` - Found clinic_id requirement
9. `final_fixed_migration.py` - SUCCESSFUL! All 87 migrated

### Working Clinic ID
```python
DEFAULT_CLINIC_ID = "c69dfe69-63c2-445f-9624-54c7876becb5"  # London clinic
```

### API Credentials
- **Admin**: admin@picobrain.com / admin123
- **Backend**: http://localhost:8000
- **Docs**: http://localhost:8000/docs

### Clinic ID Mappings (Completed)
```json
{
  "10": "c69dfe69-63c2-445f-9624-54c7876becb5",  // London
  "11": "44cc3318-35f9-45e9-a9b5-aab0e47c8c15",  // Milan
  "12": "2b79920a-0ebf-4684-bc11-2ca6316af262",  // Los Angeles
  "13": "f3711a7f-216a-493f-8543-d03d3fa4387f",  // Vancouver
  "14": "94646ff0-78c3-4d49-ab90-5336c861b3c4"   // New York
}
```

### 🎯 Final Working Migration Scripts
```python
# Database Connection (CRITICAL - Use these exact params!)
db_params = {
    'dbname': 'picobraindb',  # NOT edo_brain_4!
    'user': 'edo',             # NOT postgres!
    'password': '',
    'host': 'localhost',
    'port': '5432'
}

# Working Scripts (in order of success)
1. diagnose_migration.py - Identifies exact issues
2. fix_migration_issues.py - Creates missing tables
3. final_fixed_migration.py - Successfully migrates all 87 employees
```

### Next Steps After Migration
1. ✅ Migration complete - all 87 employees in database
2. Begin client data migration (next priority)
3. Link users to employee records
4. Set up employee permissions
5. Test employee login functionality
6. Remove temp_id columns after all migrations

## ✅ Verified Technical Stack

### Backend (Python/FastAPI)
```yaml
Framework: FastAPI 0.109.0
Server: Uvicorn 0.27.0
Database: PostgreSQL (asyncpg 0.29.0, psycopg2-binary 2.9.9)
ORM: SQLAlchemy 2.0.25
Migrations: Alembic 1.13.1
Auth: JWT (python-jose 3.3.0)
Password: bcrypt 4.3.0, passlib 1.7.4
Python: 3.x with venv
```

### Frontend (Next.js/React) - Decided 2025-08-30
```yaml
Framework: Next.js 14.x (Chosen for Vercel deployment)
UI Library: React 18.3.1 (stable version)
Styling: Tailwind CSS 3.3.0
Components: shadcn/ui (v0.app compatible)
State: Zustand 4.4.7
Data Fetching: TanStack Query 5.17.9
HTTP Client: Axios 1.6.5
Forms: React Hook Form + Zod
Animations: Framer Motion 11.0.0
Charts: Recharts 2.10.4
TypeScript: 5.x
Icons: Lucide React 0.454.0
Deployment: Vercel
```

## 🔧 Verified Commands

### Server Management

#### 🚀 IMPORTANT: Always Start Servers First!
**Lesson Learned**: Before any testing or development work, both servers MUST be running:
- **Backend**: Port 8000 (FastAPI/Uvicorn)
- **Backend**: Must use uvicorn (no app.py file exists)
- **Frontend**: Port 3000 (Next.js dev server)
- **Order**: Start backend first, then frontend (frontend depends on backend API)

```bash
# Quick Start (Both Servers) - RECOMMENDED!
cd /Users/edo/PyProjects/picobrain && ./start-servers.sh

# Manual Start - Terminal Method (Keep tabs open)
# Tab 1 - Backend (use uvicorn - no app.py file exists):
cd /Users/edo/PyProjects/picobrain/backend && source venv/bin/activate && python -m uvicorn app.main:app --reload --port 8000

# Tab 2 - Frontend:
cd /Users/edo/PyProjects/picobrain/frontend && npm run dev

# Create Admin User
cd backend && source venv/bin/activate && python manage.py create-admin

# Stop Servers
lsof -i :8000 | grep LISTEN | awk '{print $2}' | xargs kill -9
lsof -i :3000 | grep LISTEN | awk '{print $2}' | xargs kill -9
```

### Database Operations
```bash
# Apply Migrations
cd backend && source venv/bin/activate && alembic upgrade head

# Generate Migration
cd backend && source venv/bin/activate && alembic revision --autogenerate -m "migration_name"

# Rollback Migration
cd backend && source venv/bin/activate && alembic downgrade -1

# Test Connection
cd backend && source venv/bin/activate && python test_connection.py
```

### Testing
```bash
# Run API Tests
cd backend && chmod +x test_api.sh && ./test_api.sh

# Run All Backend Tests
cd backend && chmod +x run_tests.sh && ./run_tests.sh

# Test Setup
cd backend && source venv/bin/activate && python test_setup.py
```

### Frontend Development
```bash
# Install Dependencies
cd frontend && npm install

# Build Production
cd frontend && npm run build

# Run Linting
cd frontend && npm run lint
```

### Python Environment
```bash
# Activate Virtual Environment
cd backend && source venv/bin/activate

# Install Dependencies
cd backend && source venv/bin/activate && pip install -r requirements.txt

# Add New Package
cd backend && source venv/bin/activate && pip install package_name && pip freeze > requirements.txt
```

## 📡 API Endpoints Reference

### Authentication
- `POST /api/v1/auth/login` - User login
- `GET /api/v1/auth/me` - Get current user
- `POST /api/v1/auth/refresh` - Refresh token
- `POST /api/v1/auth/logout` - User logout

### Resources (Full CRUD)
- `/api/v1/persons/` - Person management
- `/api/v1/clinics/` - Clinic management
- `/api/v1/users/` - User management (admin only)
- `/api/v1/employees/` - Employee management
- `/api/v1/employees/bulk` - Bulk employee creation (NEW)
- `/api/v1/clients/` - Client management

### Default Credentials (Verified)
- **Email**: `admin@picobrain.com`
- **Password**: `admin123`
- **Created by**: `python manage.py create-admin`
- **Location**: `/backend/app/seeds/create_admin.py`

## 🎨 PicoClinics Design System

### Color Palette
```css
/* Primary Brand */
--pico-coral-primary: #e67e5b;
--pico-coral-light: #f2a085;
--pico-coral-dark: #d4634a;
--pico-coral-subtle: #fdf5f2;

/* Semantic Colors */
--pico-success: #10b981;
--pico-warning: #f59e0b;
--pico-error: #ef4444;
--pico-info: #3b82f6;
```

### Tailwind Configuration
```javascript
colors: {
  'pico-coral': {
    50: '#FDF5F2',
    100: '#F2A085',
    500: '#E67E5B',
    600: '#D4634A',
  }
}
```

## 📂 Project Structure
```
/Users/edo/PyProjects/picobrain/
├── backend/
│   ├── app/
│   │   ├── api/        # API endpoints
│   │   ├── core/       # Core functionality
│   │   ├── db/         # Database utilities
│   │   ├── models/     # SQLAlchemy models
│   │   ├── schemas/    # Pydantic schemas
│   │   └── services/   # Business logic
│   ├── alembic/        # Migrations
│   ├── tests/          # Test files
│   └── venv/           # Virtual environment
├── frontend/
│   ├── src/
│   │   ├── app/        # Next.js App Router
│   │   ├── components/ # React components
│   │   ├── hooks/      # Custom hooks
│   │   ├── lib/        # Utilities
│   │   └── services/   # API services
│   └── node_modules/   # NPM packages
├── mobile/             # React Native (incomplete)
├── input_files/        # CSV data files
│   ├── Employees.csv   # 87 employees
│   ├── Clinics.csv     # 5 clinics (migrated)
│   └── ...
└── migration scripts/  # All migration Python scripts
```

## 🔐 Environment Variables

### Backend (.env)
```bash
DATABASE_URL=postgresql://user@localhost/picobraindb
SECRET_KEY=your-secret-key-here-change-in-production
API_V1_STR=/api/v1
PROJECT_NAME=Pico Brain
BACKEND_CORS_ORIGINS=["http://localhost:3000", "http://localhost:8000"]
```

### Frontend (next.config.js)
```javascript
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_APP_NAME=PicoBrain
NEXT_PUBLIC_APP_VERSION=1.0.0
```

## ✅ What Works
- FastAPI backend with PostgreSQL database
- Next.js 15 frontend with App Router
- JWT authentication system
- Full CRUD operations for all entities
- Alembic database migrations
- Tailwind CSS with PicoClinics design system
- Development hot-reload on both frontend and backend
- Clinic migration completed (5 clinics)
- Employee migration in progress (87 employees)

## ❌ Known Issues
- **Frontend Build Error**: ✅ FIXED! (downgraded to React 18 + Next.js 14, added 'use client' to DashboardLayout)
- Mobile app directory exists but React Native not configured
- Backend uses plain Python without type checking
- Some test scripts may need permission updates (chmod +x)

## ⚠️ Common Mistakes to Avoid
- **React 19 Compatibility**: React 19 is too new, use React 18 for stability
- **Missing 'use client'**: Components using hooks need 'use client' directive in Next.js App Router
- **Wrong API Docs URL**: Use `/docs` NOT `/api/v1/docs`
- **Wrong Backend Command**: Use `python -m uvicorn app.main:app` NOT `python app.py`
- **Login Route**: Use `/login` NOT `/login/dashboard` (returns 404)
- **Forgot venv**: Always activate venv before Python commands
- **Servers Not Running**: Both servers MUST be running before testing
- **Date Validation**: Remember today is Aug 30, 2025 - future dates in 2025 are VALID

### Database Migration Mistakes (CRITICAL - 2025-08-31)
- **Wrong Database Name**: Use `picobraindb` NOT `edo_brain_4`
- **Wrong PostgreSQL User**: Use `edo` NOT `postgres`
- **Missing person_id**: Employees MUST have a person record first
- **Missing clinic_id**: primary_clinic_id is REQUIRED (not nullable)
- **Wrong Approach**: Direct database migration works, API migration is complex
- **Missing Tables**: Always check if doctors/currencies tables exist
- **Employee Code Format**: Use f"EMP{int(id):04d}" to avoid format errors
- **Email Generation**: Generate unique emails with index to avoid duplicates

## ⚠️ Pitfalls & Time-Wasters
- Always activate venv before Python commands
- API requires authentication for most endpoints
- Frontend auto-redirects to /dashboard
- Git hooks require executable permissions
- Token limit is 160,000 (80% of Claude's 200K)
- Commission rates must be decimal (0.15 not "15")
- Salaries stored in minor units (cents)

## 📊 Metrics
- Total Sessions: 8
- Dependencies Installed: Backend (75+), Frontend (29+)
- API Endpoints: 20+
- Database Tables: 5+ (persons, clinics, users, employees, clients)
- Migrated Records: 5 clinics, ~87 employees (in progress)

## 📊 Database Migration FINAL STATUS (2025-08-31)

### ✅ Completed Migrations
1. ✅ **Clinics**: 5 clinics with complete addresses
2. ✅ **Employees**: ALL 87 employees successfully migrated
3. ✅ **Persons**: 91 person records created
4. ✅ **Doctors**: 34 doctor records with licenses
5. ✅ **Currencies**: Table created with USD, EUR, GBP, CAD

### 🔍 Diagnostic Approach That Worked
```python
# 1. Find correct database
cur.execute("SELECT datname FROM pg_database")
# Result: picobraindb (NOT edo_brain_4)

# 2. Check table structure
cur.execute("""
    SELECT column_name, is_nullable 
    FROM information_schema.columns 
    WHERE table_name = 'employees'
    AND is_nullable = 'NO'
""")
# Found: primary_clinic_id is REQUIRED

# 3. Test single record first
# This revealed all missing requirements

# 4. Fix issues incrementally
# Create tables, add columns, then migrate
```

### Database Structure Discovered
- **persons → employees**: One-to-one relationship via person_id
- **employees → clinics**: Many-to-one via primary_clinic_id
- **employees → doctors**: One-to-one via employee_id
- **employees → currencies**: Many-to-one via currency_code

### Ready for Migration
- **Clients**: Next after employees complete
- CSV fields now map to all database fields
- Employment dates, salaries, commissions can be stored

### Migration Order Plan
1. Clinics ✅ Complete
2. Employees 🔄 In Progress
3. Clients (next)
4. Users (link to employees)
5. Clean up temp_id columns after migration

## 📝 Code Patterns

### React/Next.js
- App Router structure in src/app directory
- Functional components with TypeScript
- Zustand for state management
- TanStack Query for data fetching
- Radix UI for accessible components

### API/Backend
- FastAPI with async/await endpoints
- SQLAlchemy ORM models
- Pydantic schemas for validation
- JWT token authentication
- RESTful API design with /api/v1 prefix

### Migration Scripts (Python)
```python
# Standard pattern for migration scripts
import asyncio
import aiohttp
import csv
import json
from datetime import date, datetime

# Authentication
async with session.post(f"{API_BASE_URL}/auth/login", data=data) as resp:
    token = result['access_token']

# Bulk creation
batch_data = {
    "employees": batch,
    "stop_on_error": False,
    "validate_all_first": False
}

# Individual creation with retry
async def migrate_single_employee(session, headers, employee_data):
    try:
        async with session.post(
            f"{API_BASE_URL}/employees",
            headers=headers,
            json=employee_data
        ) as resp:
            if resp.status in [200, 201]:
                return True, result.get('id')
            else:
                return False, await resp.text()
    except Exception as e:
        return False, str(e)
```

### Testing
- test_api.sh for comprehensive API testing
- test_connection.py for database connectivity
- run_tests.sh for all backend tests

## 🚀 Quick Start Checklist

### ⚠️ CRITICAL FIRST STEP: Start Servers!
**Why**: Without servers running, you cannot:
- Test the application
- Access the dashboard
- Make API calls
- See UI changes

1. [ ] Ensure PostgreSQL is running (`pg_isready -h localhost -p 5432`)
2. [ ] **START BOTH SERVERS** (Essential for any work!):
   - Method A: Run `./start-servers.sh` (easiest)
   - Method B: Manual in Terminal tabs:
     - [ ] Tab 1: `cd backend && source venv/bin/activate && python -m uvicorn app.main:app --reload`
     - [ ] Tab 2: `cd frontend && npm run dev`
   - [ ] Wait for both to fully start (~5-10 seconds)
3. [ ] Verify API health at http://localhost:8000/health
4. [ ] Verify API docs at http://localhost:8000/docs (NOT /api/v1/docs)
5. [ ] Login at http://localhost:3000/login with:
   - Username: admin@picobrain.com
   - Password: admin123
6. [ ] Access dashboard at http://localhost:3000/dashboard

## 📚 Additional Resources
- API Documentation: http://localhost:8000/docs (NOT /api/v1/docs - common mistake!)
- API Health Check: http://localhost:8000/health
- Frontend: http://localhost:3000 
- Login Page: http://localhost:3000/login 
- Dashboard: http://localhost:3000/dashboard 
- Database Migrations: backend/alembic/versions/
- Test Scripts: backend/test_*.sh
- Admin User Creation: backend/app/seeds/create_admin.py
- Migration Reports: /Users/edo/PyProjects/picobrain/migration_*.json
- Comprehensive Report: /Users/edo/PyProjects/PICOBRAIN_MIGRATION_REPORT.md

---

## Weekly Review: 2025-W35
- Commits: Multiple migration scripts created
- Files Changed: 20+ (migration scripts, reports)
- Top patterns: Employee migration, data validation
- Key Achievement: Complete employee migration solution implemented
---