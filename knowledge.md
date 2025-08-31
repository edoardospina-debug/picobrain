<!-- CLAUDE: ALWAYS READ THIS FIRST -->
# Knowledge Base - PicoBrain
Version: 3.0.0
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

## 🎯 Frontend Architecture Plan (2025-08-31)

### Technology Stack Decided
```yaml
Framework: Next.js 14.x (App Router)
UI Components: Ant Design 5.x  # Chosen for robust tables & forms
State Management: TanStack Query v5 (server state) + Zustand (UI state)
HTTP Client: Axios  # Better error handling than fetch
Forms: React Hook Form + Zod
Authentication: JWT with automatic refresh
TypeScript: 5.x (strict mode)
Deployment: Vercel
```

### Why Ant Design Over Alternatives
- **Complete Components**: Tables with virtualization for 100k+ records
- **Form Handling**: Built-in validation and complex forms
- **Medical/Enterprise Look**: Professional aesthetic
- **Performance**: Virtual scrolling out-of-box
- **Less Custom Code**: Simpler maintenance

### Frontend Project Structure
```
/frontend
├── app/
│   ├── (auth)/
│   │   ├── login/
│   │   └── layout.tsx
│   ├── (dashboard)/
│   │   ├── clinics/
│   │   │   ├── page.tsx           # List view
│   │   │   ├── [id]/page.tsx      # Detail/Edit view
│   │   │   └── new/page.tsx       # Create view
│   │   ├── staff/                 # Employees + Doctors combined
│   │   ├── clients/
│   │   ├── users/
│   │   └── layout.tsx
├── components/
│   ├── layouts/
│   │   ├── AuthLayout.tsx
│   │   └── DashboardLayout.tsx
│   ├── shared/
│   │   ├── DataTable/             # ONE table for all entities
│   │   ├── EntityForm/            # ONE form for all CRUD
│   │   └── PageWrapper/           # Consistent page structure
│   └── features/
│       └── [entity]/              # Entity-specific overrides only
├── lib/
│   ├── api/
│   │   ├── client.ts              # Axios instance with interceptors
│   │   ├── auth.ts                # Auth endpoints & token management
│   │   └── endpoints/
│   ├── hooks/
│   │   ├── useAuth.ts
│   │   ├── usePermissions.ts
│   │   └── useCrud.ts            # Generic CRUD operations
│   └── utils/
├── types/
│   ├── generated/                 # Auto-generated from OpenAPI
│   └── app.ts                     # Frontend-specific types
└── config/
```

### Implementation Phases
1. **Phase 1: Foundation (Days 1-2)**
   - Next.js setup with TypeScript
   - Ant Design configuration
   - API client with interceptors
   - Authentication flow

2. **Phase 2: Shared Components (Days 3-4)**
   - Generic DataTable with virtualization
   - Dynamic EntityForm
   - Loading states & error boundaries

3. **Phase 3: Clinics POC (Days 5-6)** 🎯 **FIRST DELIVERABLE**
   - Full CRUD for Clinics
   - Pagination for 100k+ records
   - Audit logging

4. **Phase 4: Complete CRUD (Days 7-10)**
   - Staff management (Persons + Employees)
   - Clients management
   - Users with role assignment

5. **Phase 5: Polish (Days 11-12)**
   - Error handling
   - Performance optimization
   - Accessibility

## 📊 Complete API Structure (Discovered 2025-08-31)

### Authentication & Security
```python
# JWT-based authentication
- Access Token: 8 days expiry
- Refresh Token: Longer expiry
- Algorithm: HS256
- Token stored in memory (frontend)
- Refresh token as httpOnly cookie
```

### User Roles & Permissions
```python
UserRole Enum:
- admin      # Full system access
- manager    # Clinic management
- staff      # General staff access  
- medical    # Doctors, nurses
- finance    # Financial operations
- readonly   # View-only access
```

### Database Models & Relationships
```python
# Core Entities
Person (Base entity for humans)
├── id: UUID (primary key)
├── first_name, last_name, middle_name
├── email (unique)
├── phone_mobile_country_code, phone_mobile_number
├── phone_home_country_code, phone_home_number
├── dob, gender, nationality
├── id_type, id_number
└── created_at, updated_at

Employee (Person who works)
├── id: UUID
├── person_id: UUID (FK → Person)
├── employee_code (unique)
├── primary_clinic_id: UUID (FK → Clinic, REQUIRED)
├── role: Enum (doctor, nurse, receptionist, manager, finance, admin)
├── specialization, license_number, license_expiry
├── hire_date, termination_date
├── base_salary_minor, salary_currency, commission_rate
├── is_active, can_perform_treatments
└── created_at, updated_at

Client (Person who receives treatment)
├── id: UUID
├── person_id: UUID (FK → Person)
├── client_code (unique)
├── acquisition_date
├── preferred_clinic_id: UUID (FK → Clinic)
└── is_active

Clinic (Medical facility)
├── id: UUID
├── code (unique), name
├── functional_currency
├── address_line_1, address_line_2
├── city, state_province, postal_code, country_code
├── phone_country_code, phone_number, email
├── tax_id, is_active
└── created_at, updated_at

User (System access)
├── id: UUID
├── person_id: UUID (FK → Person)
├── username (unique), password_hash
├── role: UserRole Enum
└── is_active
```

### API Endpoints (Complete List)
```yaml
Authentication:
  POST   /api/v1/auth/login         # OAuth2 compatible
  POST   /api/v1/auth/refresh       # Refresh access token
  GET    /api/v1/auth/me           # Current user info
  POST   /api/v1/auth/logout        # Client-side logout

Persons:
  GET    /api/v1/persons           # List with pagination
  POST   /api/v1/persons           # Create person
  GET    /api/v1/persons/{id}      # Get person details
  PUT    /api/v1/persons/{id}      # Update person
  DELETE /api/v1/persons/{id}      # Delete person

Clinics:
  GET    /api/v1/clinics           # List clinics
  POST   /api/v1/clinics           # Create clinic
  GET    /api/v1/clinics/{id}      # Get clinic
  PUT    /api/v1/clinics/{id}      # Update clinic
  DELETE /api/v1/clinics/{id}      # Delete clinic

Employees:
  GET    /api/v1/employees         # List employees
  POST   /api/v1/employees         # Create employee
  POST   /api/v1/employees/bulk    # Bulk creation
  GET    /api/v1/employees/{id}    # Get employee
  PUT    /api/v1/employees/{id}    # Update employee
  DELETE /api/v1/employees/{id}    # Delete employee

Clients:
  GET    /api/v1/clients           # List clients
  POST   /api/v1/clients           # Create client
  GET    /api/v1/clients/{id}      # Get client
  PUT    /api/v1/clients/{id}      # Update client
  DELETE /api/v1/clients/{id}      # Delete client

Users:
  GET    /api/v1/users             # List users (admin only)
  POST   /api/v1/users             # Create user
  GET    /api/v1/users/{id}        # Get user
  PUT    /api/v1/users/{id}        # Update user
  DELETE /api/v1/users/{id}        # Delete user
```

### API Integration Patterns
```typescript
// Axios Client Configuration
const apiClient = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL,
  timeout: 30000,
});

// Auto Token Refresh
apiClient.interceptors.response.use(
  response => response,
  async error => {
    if (error.response?.status === 401) {
      await refreshToken();
      return apiClient.request(error.config);
    }
    return Promise.reject(error);
  }
);

// Generic CRUD Hook
function useCrud<T>(endpoint: string) {
  const list = useQuery({ queryKey: [endpoint] });
  const create = useMutation({ 
    mutationFn: (data: T) => apiClient.post(endpoint, data)
  });
  const update = useMutation({
    mutationFn: ({ id, data }) => apiClient.put(`${endpoint}/${id}`, data)
  });
  return { list, create, update };
}
```

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
Validation: Pydantic 2.5.0
Settings: pydantic-settings 2.1.0
CORS: fastapi_cors 0.0.6
Python: 3.12 with venv
```

### Frontend (Finalized Architecture - 2025-08-31)
```yaml
Framework: Next.js 14.x (App Router)
UI Components: Ant Design 5.20.x
State Management: 
  - TanStack Query 5.51.x (server state)
  - Zustand 4.x (UI state)
HTTP Client: Axios 1.7.x
Forms: React Hook Form 7.52.x + Zod 3.23.x
Date Handling: Day.js 1.11.x
TypeScript: 5.5.x (strict mode)
Build Tool: Turbopack (Next.js built-in)
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

# Generate Types from OpenAPI
npx openapi-typescript http://localhost:8000/api/v1/openapi.json \
  --output ./types/generated/api.ts

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

## 📂 Complete Project Structure
```
/Users/edo/PyProjects/picobrain/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   └── v1/
│   │   │       ├── api.py      # Main router aggregation
│   │   │       └── endpoints/  # All endpoint modules
│   │   │           ├── auth.py     # JWT authentication
│   │   │           ├── persons.py  # Person CRUD
│   │   │           ├── clinics.py  # Clinic CRUD
│   │   │           ├── employees.py # Employee CRUD + bulk
│   │   │           ├── clients.py  # Client CRUD
│   │   │           └── users.py    # User management
│   │   ├── core/
│   │   │   ├── config.py      # Settings with pydantic
│   │   │   └── security.py    # JWT & password handling
│   │   ├── db/
│   │   │   └── database.py    # SQLAlchemy setup
│   │   ├── models/
│   │   │   ├── core.py        # Main entities
│   │   │   ├── person.py      # Person model
│   │   │   └── user.py        # User model
│   │   ├── schemas/           # Pydantic validation
│   │   ├── services/          # Business logic
│   │   └── main.py           # FastAPI app entry
│   ├── alembic/              # Database migrations
│   ├── tests/                # Test files
│   ├── requirements.txt      # Python dependencies
│   └── venv/                 # Virtual environment
├── frontend/
│   ├── app/                  # Next.js App Router
│   ├── components/           # React components
│   ├── lib/                  # Utilities & API client
│   ├── types/                # TypeScript definitions
│   ├── package.json          # Node dependencies
│   └── next.config.js        # Next.js config
├── mobile/                   # React Native (incomplete)
├── input_files/             # CSV data files
│   ├── Employees.csv        # 87 employees (MIGRATED)
│   ├── Clinics.csv          # 5 clinics (MIGRATED)
│   └── ...
├── migration scripts/       # All migration Python scripts
└── picobrain-frontend-plan.md  # Complete frontend development plan
```

## 🔐 Environment Variables

### Backend (.env)
```bash
DATABASE_URL=postgresql://edo@localhost/picobraindb
SECRET_KEY=your-secret-key-here-change-in-production
ENCRYPTION_KEY=your-encryption-key-here
ACCESS_TOKEN_EXPIRE_MINUTES=11520  # 8 days
JWT_ALGORITHM=HS256
API_V1_STR=/api/v1
PROJECT_NAME=PicoBrain Healthcare System
APP_NAME=PicoBrain
APP_VERSION=1.0.0
ENVIRONMENT=development
DEBUG=True
BACKEND_CORS_ORIGINS=["http://localhost:3000", "http://localhost:8000"]
DEFAULT_PAGE_SIZE=20
MAX_PAGE_SIZE=100
```

### Frontend (.env.local)
```bash
NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1
NEXT_PUBLIC_APP_URL=http://localhost:3000
NEXT_PUBLIC_APP_NAME=PicoBrain
NEXT_PUBLIC_APP_VERSION=1.0.0

# Deployment environments
# Staging:
# NEXT_PUBLIC_API_URL=https://api-staging.picobrain.com/api/v1
# Production:
# NEXT_PUBLIC_API_URL=https://api.picobrain.com/api/v1
```

## 🎨 Design System

### UI Component Library: Ant Design
```typescript
// Theme Configuration
const theme = {
  token: {
    colorPrimary: '#e67e5b',     // PicoCoral primary
    colorSuccess: '#10b981',
    colorWarning: '#f59e0b',
    colorError: '#ef4444',
    colorInfo: '#3b82f6',
    borderRadius: 6,
    fontFamily: '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto',
  },
};

// Component Usage
import { Table, Form, Button, Modal, message } from 'antd';
```

### Data Table Features
- Server-side pagination (100k+ records)
- Virtual scrolling
- Column sorting & filtering
- Search functionality
- Row actions (edit, delete)
- Bulk operations
- CSV export

### Form Handling Pattern
```typescript
// Single form with sections (not wizard)
const EmployeeForm = () => {
  return (
    <Form layout="vertical">
      <Collapse defaultActiveKey={['1', '2', '3']}>
        <Panel header="Personal Information" key="1">
          {/* Person fields */}
        </Panel>
        <Panel header="Employment Details" key="2">
          {/* Employee fields */}
        </Panel>
        <Panel header="Clinic Assignment" key="3">
          {/* Clinic selection */}
        </Panel>
      </Collapse>
    </Form>
  );
};
```

## ✅ What Works
- FastAPI backend with PostgreSQL database
- Complete database schema with all relationships
- JWT authentication with refresh tokens
- Full CRUD operations for all entities
- Bulk employee creation endpoint
- Alembic database migrations
- 5 clinics fully migrated
- 87 employees fully migrated
- Frontend architecture fully planned
- Ant Design chosen for UI components
- Deployment strategy for Vercel defined

## ❌ Known Issues & Pending
- Frontend implementation not started (plan complete)
- Mobile app directory exists but React Native not configured
- Permission matrix needs definition
- Audit logging implementation pending
- Client data migration pending

## ⚠️ Critical Knowledge

### Database Gotchas
- **Database**: `picobraindb` NOT `edo_brain_4`
- **User**: `edo` NOT `postgres`
- **Relationships**: Person → Employee/Client (one-to-one)
- **Required Fields**: primary_clinic_id CANNOT be NULL
- **Phone Fields**: Split into country_code and number
- **Salaries**: Stored in minor units (cents)

### API Patterns
- All endpoints under `/api/v1/`
- Auth required for most endpoints (Bearer token)
- Pagination: `?page=1&limit=20`
- Bulk operations: `/employees/bulk`
- OpenAPI spec: `/api/v1/openapi.json`

### Frontend Architecture Decisions
- **Ant Design** over shadcn/ui for enterprise features
- **Single forms with sections** over wizards
- **Traditional pagination** over infinite scroll
- **No offline support** to keep it simple
- **Edit audit logging only** (no view tracking)
- **Server-side operations** for large datasets

## 📊 Project Metrics
- Total Sessions: 9
- Backend Dependencies: 75+
- Frontend Dependencies (planned): 8 core
- API Endpoints: 30+
- Database Tables: 7 (persons, clinics, users, employees, clients, doctors, currencies)
- Migrated Records: 5 clinics, 87 employees
- Frontend Components Planned: 10+ shared
- Estimated Development Time: 2-3 weeks

## 🚀 Next Steps

### Immediate (Phase 1-2)
1. Initialize Next.js 14 with TypeScript
2. Set up Ant Design with custom theme
3. Create API client with interceptors
4. Generate types from OpenAPI
5. Implement authentication flow
6. Build shared components (DataTable, EntityForm)

### Clinics POC (Phase 3) - FIRST DELIVERABLE
1. List page with pagination
2. Create/Edit forms
3. Delete with confirmation
4. Search and filtering
5. Test with 100k records simulation
6. Validate audit logging

### Pending Decisions
1. **Permission Matrix**: Define CRUD permissions per role
2. **Business Rules**: Person-Employee-Client relationships
3. **UI Preferences**: Theme, date format, table density
4. **Deployment**: Staging environment needs

## 📚 Reference Documents
- Frontend Plan: `/Users/edo/PyProjects/picobrain-frontend-plan.md`
- API Documentation: http://localhost:8000/docs
- Migration Report: `/Users/edo/PyProjects/PICOBRAIN_MIGRATION_REPORT.md`
- This Knowledge Base: `/Users/edo/PyProjects/picobrain/knowledge.md`

## 💡 Prompt for Next Session
```
Read the frontend development plan at:
/Users/edo/PyProjects/picobrain-frontend-plan.md

And the knowledge base at:
/Users/edo/PyProjects/picobrain/knowledge.md

Then:
1. Initialize Next.js 14 project with TypeScript and Ant Design
2. Set up the project structure from section 1.3
3. Implement Phase 1 (Foundation Setup)
4. Create the Clinics POC as first deliverable

Permission matrix: [DEFINE YOUR PERMISSIONS]
```

---

## Weekly Review: 2025-W35
- Commits: Multiple migration scripts, frontend planning
- Files Changed: 30+ (migration scripts, reports, plans)
- Top patterns: Employee migration, frontend architecture, API integration
- Key Achievements: 
  - Complete employee migration (87 records)
  - Complete frontend architecture design
  - Technology stack finalized
  - Clinics POC specification ready
---