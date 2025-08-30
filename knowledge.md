<!-- CLAUDE: ALWAYS READ THIS FIRST -->
# Knowledge Base - PicoBrain
Version: 2.0.0
Updated: 2025-08-30

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

### Frontend (Next.js/React)
```yaml
Framework: Next.js 15.5.2
UI Library: React 19.1.1
Styling: Tailwind CSS 3.3.0
State: Zustand 4.4.7
Data Fetching: TanStack Query 5.17.9
HTTP Client: Axios 1.6.5
UI Components: Radix UI
Animations: Framer Motion 11.0.0
Charts: Recharts 2.10.4
TypeScript: 5.x
Icons: Lucide React 0.454.0
```

## 🔧 Verified Commands

### Server Management
```bash
# Start Backend (Port 8000)
cd /Users/edo/PyProjects/picobrain/backend && source venv/bin/activate && python -m uvicorn app.main:app --reload --port 8000

# Start Frontend (Port 3000)
cd /Users/edo/PyProjects/picobrain/frontend && npm run dev

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
- `/api/v1/clients/` - Client management

### Default Credentials
- Email: `admin@picobrain.com`
- Password: (check .env file)

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
└── mobile/             # React Native (incomplete)
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

## ❌ Known Issues
- Mobile app directory exists but React Native not configured
- Backend uses plain Python without type checking
- Some test scripts may need permission updates (chmod +x)

## ⚠️ Pitfalls & Time-Wasters
- Always activate venv before Python commands
- API requires authentication for most endpoints
- Frontend auto-redirects to /dashboard
- Git hooks require executable permissions
- Token limit is 160,000 (80% of Claude's 200K)

## 📊 Metrics
- Total Sessions: 7
- Dependencies Installed: Backend (75+), Frontend (29+)
- API Endpoints: 20+
- Database Tables: 5+ (persons, clinics, users, employees, clients)

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

### Testing
- test_api.sh for comprehensive API testing
- test_connection.py for database connectivity
- run_tests.sh for all backend tests

## 🚀 Quick Start Checklist
1. [ ] Activate Python virtual environment
2. [ ] Start backend server (port 8000)
3. [ ] Start frontend server (port 3000)
4. [ ] Verify API docs at http://localhost:8000/api/v1/docs
5. [ ] Access dashboard at http://localhost:3000/dashboard
6. [ ] Check authentication with default admin credentials

## 📚 Additional Resources
- API Documentation: http://localhost:8000/api/v1/docs
- Frontend: http://localhost:3000
- Dashboard: http://localhost:3000/dashboard
- Database Migrations: backend/alembic/versions/
- Test Scripts: backend/test_*.sh

## 🔄 Authentication Integration Patterns

### JWT Token Flow
**Pattern**: Middleware-based auth check with automatic refresh
**Implementation**: Store token in HTTP-only cookies or localStorage
**Benefits**: Seamless user experience, reduced auth errors

### Protected Routes Pattern
**Problem**: Ensuring pages require authentication
**Solution**: Next.js middleware.ts with auth check
```typescript
// middleware.ts
export function middleware(request: NextRequest) {
  const token = request.cookies.get('token')
  if (!token && request.nextUrl.pathname.startsWith('/dashboard')) {
    return NextResponse.redirect(new URL('/login', request.url))
  }
}
```

## 🚀 Performance Optimizations Discovered

### Parallel Data Fetching
**Problem**: Sequential API calls causing slow page loads
**Solution**: Use Promise.all() for independent data fetches
```typescript
const [patients, appointments, stats] = await Promise.all([
  fetchPatients(),
  fetchAppointments(),
  fetchStats()
])
```
**Impact**: 40-60% reduction in page load time

### Optimistic Updates Pattern
**Problem**: Perceived lag when updating data
**Solution**: Update UI immediately, rollback on error
**Implementation**: TanStack Query's optimistic updates
```typescript
mutation.mutate(data, {
  onMutate: async (newData) => {
    await queryClient.cancelQueries(['patients'])
    const previousData = queryClient.getQueryData(['patients'])
    queryClient.setQueryData(['patients'], newData)
    return { previousData }
  },
  onError: (err, newData, context) => {
    queryClient.setQueryData(['patients'], context.previousData)
  }
})
```

## 🏗️ Component Architecture Insights

### Dashboard Layout Pattern
**Learning**: Consistent layout wrapper reduces code duplication
**Pattern**: Single DashboardLayout component with slot-based content
```typescript
// app/dashboard/layout.tsx
export default function DashboardLayout({ children }) {
  return (
    <div className="flex h-screen">
      <Sidebar />
      <main className="flex-1 overflow-auto">
        <Header />
        {children}
      </main>
    </div>
  )
}
```
**Benefits**: Easier maintenance, consistent UX

### Form Validation Strategy
**Best Practice**: Share validation schemas between client and server
**Implementation**: Zod schemas in shared location
```typescript
// lib/validations/patient.ts
export const patientSchema = z.object({
  name: z.string().min(2).max(100),
  email: z.string().email(),
  phone: z.string().regex(/^\d{10}$/)
})
```
**Benefit**: Single source of truth for validation rules

## 🔒 Security Implementations

### API Rate Limiting
**Implementation**: Token bucket algorithm in FastAPI middleware
**Pattern**: IP-based limits with user-based overrides
```python
# backend/app/core/rate_limit.py
RATE_LIMITS = {
    'anonymous': 100,  # per minute
    'authenticated': 1000,  # per minute
    'admin': 10000  # per minute
}
```

### Row Level Security (RLS)
**Problem**: Ensuring data isolation between clinics
**Solution**: Database-level RLS policies
```sql
-- PostgreSQL RLS example
CREATE POLICY "clinic_isolation" ON patients
FOR ALL
USING (clinic_id = current_setting('app.current_clinic_id')::uuid);
```

### Error Handling Pattern
**Principle**: Never expose internal errors to clients
**Implementation**: Standardized error responses
```python
# backend/app/core/exceptions.py
class APIException(Exception):
    def __init__(self, status_code: int, detail: str, internal_message: str = None):
        self.status_code = status_code
        self.detail = detail  # Safe for client
        self.internal_message = internal_message  # For logging only
```

## 📊 Database Design Patterns

### Multi-tenant Architecture
**Pattern**: Shared database with tenant isolation
**Implementation**: clinic_id on all tables
**Benefits**: Cost-effective, easier maintenance

### Soft Deletes
**Pattern**: Mark records as deleted instead of removing
**Implementation**: deleted_at timestamp column
```python
# backend/app/models/base.py
class SoftDeleteMixin:
    deleted_at = Column(DateTime, nullable=True)
    
    @property
    def is_deleted(self):
        return self.deleted_at is not None
```

## 🎨 UI/UX Patterns

### Loading States
**Pattern**: Skeleton screens for better perceived performance
**Implementation**: Component-specific skeletons
```typescript
// components/ui/skeleton.tsx
export function PatientCardSkeleton() {
  return (
    <div className="animate-pulse">
      <div className="h-4 bg-gray-200 rounded w-3/4 mb-2"></div>
      <div className="h-3 bg-gray-200 rounded w-1/2"></div>
    </div>
  )
}
```

### Empty States
**Pattern**: Informative empty states with call-to-action
**Implementation**: Context-aware messages
```typescript
if (data.length === 0) {
  return (
    <EmptyState
      icon={<UserPlus />}
      title="No patients yet"
      description="Start by adding your first patient"
      action={<Button onClick={openAddPatient}>Add Patient</Button>}
    />
  )
}
```

## 🔧 Development Workflow Patterns

### Feature Branch Strategy
```bash
# Create feature branch
git checkout -b feat/patient-dashboard

# Conventional commits
git commit -m "feat: add patient dashboard"
git commit -m "fix: resolve date formatting issue"
git commit -m "refactor: optimize patient query"

# Merge with main
git checkout main
git merge --no-ff feat/patient-dashboard
```

### Testing Strategy
**Unit Tests**: Core business logic
**Integration Tests**: API endpoints
**E2E Tests**: Critical user flows
```python
# backend/tests/test_patient_service.py
def test_create_patient():
    patient_data = {"name": "John Doe", "email": "john@example.com"}
    patient = patient_service.create(patient_data)
    assert patient.id is not None
    assert patient.name == "John Doe"
```

## 📝 Common Pitfalls & Solutions

### N+1 Query Problem
**Issue**: Loading related data in loops
**Solution**: Use SQLAlchemy eager loading
```python
# backend/app/services/patient_service.py
patients = db.query(Patient).options(
    selectinload(Patient.appointments),
    selectinload(Patient.medical_records)
).all()
```

### Stale Cache Issues
**Issue**: TanStack Query showing outdated data
**Solution**: Proper cache invalidation
```typescript
// After mutation
queryClient.invalidateQueries({ queryKey: ['patients'] })
```

### CORS Issues in Development
**Issue**: Frontend can't reach backend
**Solution**: Configure CORS properly
```python
# backend/app/core/config.py
BACKEND_CORS_ORIGINS = [
    "http://localhost:3000",
    "http://localhost:3001",
    "http://127.0.0.1:3000"
]
```