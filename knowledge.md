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

## 📊 Database Migration Summary (2025-08-30)

### Completed
1. ✅ **Clinics**: Fully migrated with complete addresses (5 records)
2. ✅ **SQLAlchemy Models**: All 3 models updated to match database schema
   - Clinic: 7→17 fields
   - Person: 7→14 fields  
   - Employee: 8→17 fields
3. ✅ **temp_id**: Added to clinics for CSV ID mapping

### Ready for Migration
- **Staff.csv**: 44 records → Person + Employee tables
- **Doctors.csv**: 53 records → Person + Employee tables
- CSV fields now map to all database fields
- Employment dates, salaries, commissions can be stored

### Migration Order Plan
1. Clinics ✅ Complete
2. Persons (from Staff + Doctors)
3. Employees (link to Persons + Clinics)
4. Handle role mapping (accountant→finance, etc.)
5. Clean up temp_id column after migration

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
- Frontend: http://localhost:3000 (currently has build errors)
- Login Page: http://localhost:3000/login (requires frontend fix)
- Dashboard: http://localhost:3000/dashboard (requires frontend fix)
- Database Migrations: backend/alembic/versions/
- Test Scripts: backend/test_*.sh
- Admin User Creation: backend/app/seeds/create_admin.py

## 🔄 Authentication Integration Patterns

### Login Process (Verified)
1. User accesses http://localhost:3000/login
2. Enters credentials (admin@picobrain.com / admin123)
3. Frontend POSTs to /api/v1/auth/login
4. Backend validates with bcrypt password hash
5. Returns JWT token on success
6. Frontend stores token and redirects to /dashboard
7. All subsequent API calls include JWT in headers

### JWT Token Flow
**Pattern**: Middleware-based auth check with automatic refresh
**Implementation**: Store token in HTTP-only cookies or localStorage
**Benefits**: Seamless user experience, reduced auth errors

### Admin User Creation
**Script**: `backend/app/seeds/create_admin.py`
**Command**: `python manage.py create-admin`
**Creates**:
- Person record (System Administrator)
- User record with admin role
- Password hash using bcrypt
**Note**: Script checks if admin exists before creating

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

### Dashboard Layout Pattern (Implemented 2025-08-30)
**Learning**: Consistent layout wrapper reduces code duplication
**Pattern**: Single DashboardLayout component with slot-based content
**Status**: ✅ Successfully implemented in Phase 1

```typescript
// components/layout/dashboard-layout.tsx
export function DashboardLayout({ children, className }: DashboardLayoutProps) {
  return (
    <div className="min-h-screen bg-gray-50">
      <TopNavigation />
      <div className="flex h-[calc(100vh-4rem)]">
        <SideNavigation />
        <main className={cn(
          "flex-1 overflow-y-auto bg-gray-50",
          "lg:pl-64", // Account for fixed sidebar
          className
        )}>
          <div className="px-4 sm:px-6 lg:px-8 py-6">
            {children}
          </div>
        </main>
      </div>
    </div>
  )
}
```

**Implementation Success**:
- Mobile-responsive with slide-out menu
- Active route highlighting
- PicoClinics branding integrated
- Consistent padding and spacing

**Benefits**: 
- Eliminated layout inconsistencies between pages
- Single source of truth for navigation
- Easier maintenance and updates
- Guaranteed consistent UX across all dashboard pages

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

### Design Token System (Implemented 2025-08-30)
**Pattern**: Centralized design tokens for consistency
**Implementation**: JavaScript object with semantic naming

```typescript
// Used in dashboard refactoring
const tokens = {
  spacing: {
    page: '1.5rem',
    section: '1.5rem',
    card: '1rem',
  },
  typography: {
    pageTitle: 'text-3xl font-bold tracking-tight',
    sectionTitle: 'text-xl font-semibold',
    cardTitle: 'text-lg font-medium',
  }
}
```

**Result**: Consistent spacing and typography across all components

### StatCard Component Pattern
**Pattern**: Reusable metrics display component
**Implementation**: Self-contained with props for customization

```typescript
interface StatCardProps {
  title: string
  value: string | number
  description?: string
  icon: React.ElementType
  trend?: 'up' | 'down' | 'neutral'
  trendValue?: string
}
```

**Features**:
- Trend indicators with color coding
- Icon support for visual context
- Hover effects for interactivity
- Responsive grid layout

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

### Layout Inconsistency Across Pages
**Issue**: Different pages had different layouts and navigation
**Root Cause**: No shared layout component
**Solution**: Implemented DashboardLayout wrapper pattern
**Result**: All dashboard pages now have consistent look and feel

### className Utility for Tailwind
**Issue**: Complex conditional classes become unreadable
**Solution**: Implemented cn() utility function
```typescript
// lib/utils.ts
import { type ClassValue, clsx } from "clsx"
import { twMerge } from "tailwind-merge"

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}
```
**Benefits**: Cleaner conditional styling, proper class merging

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
```## Implementation Phases Documentation

### Phase 1: Dashboard Foundation (Completed 2025-08-30)
**Scope**: Main dashboard page only
**Files Created**: 4
- `components/layout/dashboard-layout.tsx` (210 lines)
- `app/dashboard/layout.tsx` (10 lines)
- `app/dashboard/page.tsx` (200 lines)
- `lib/utils.ts` (6 lines)

**Achievements**:
1. ✅ Established layout wrapper pattern
2. ✅ Integrated PicoClinics design system
3. ✅ Created reusable StatCard component
4. ✅ Implemented responsive navigation
5. ✅ Applied design tokens for consistency

**Key Decisions**:
- Used composition over inheritance
- Kept StatCard local (extract in Phase 2)
- Preserved all sub-pages unchanged
- Mobile-first responsive approach

**Lessons Learned**:
- Layout wrapper pattern immediately solves consistency issues
- Design tokens should be defined early
- cn() utility essential for complex Tailwind classes
- Incremental refactoring reduces risk

### Phase 2: Component Extraction (Planned)
**Scope**: Extract and share components
- [ ] Move StatCard to shared components
- [ ] Create shared DataTable component
- [ ] Extract form components
- [ ] Build loading skeletons

### Phase 3: Sub-Page Refactoring (Planned)
**Scope**: Apply patterns to all dashboard pages
- [ ] /dashboard/persons
- [ ] /dashboard/clinics
- [ ] /dashboard/clients
- [ ] /dashboard/employees
- [ ] /dashboard/users

## 🌨 v0.app Development Strategy (Updated 2025-08-30)

### Login Page Generation Plan

**Component Requirements**:
1. **Design Consistency**: Match dashboard and CRUD templates
2. **Color Scheme**: PicoClinics coral (#e67e5b) as primary
3. **Framework**: Next.js 14 App Router structure
4. **Form Handling**: React Hook Form with Zod validation
5. **Authentication**: JWT with /api/v1/auth/login endpoint
6. **Error Handling**: Inline validation messages
7. **Loading States**: Button spinner during authentication
8. **Responsive**: Mobile-first design approach

**File Structure for Login**:
```
app/
  (auth)/
    login/
      page.tsx       # Main login page
      layout.tsx     # Auth-specific layout
components/
  auth/
    LoginForm.tsx    # Form component
    SocialLogin.tsx  # OAuth buttons
lib/
  auth/
    validation.ts    # Zod schemas
    api.ts          # Auth API calls
```

### v0.app Templates Status
- **Dashboard**: `/Users/edo/PyProjects/picobrain-dashboard.zip` ✅
- **CRUD**: `/Users/edo/PyProjects/crud-template.zip` ✅
- **Login**: To be generated with Next.js 14 compatibility

## 🤖 v0.app Programmatic Interaction Guide (Discovered 2025-08-30)

### Key Discovery
**Breakthrough**: Successfully figured out how to programmatically interact with v0.app AI through browser automation.

### Technical Details

#### Editor Technology
- **Editor Type**: ProseMirror (rich text editor framework)
- **Text Input Method**: `document.execCommand('insertText', false, 'text')`
- **Key Requirement**: Must focus the editor before inserting text

#### Submit Button Identification
**Multiple Methods to Find Submit Button**:
1. **XPath**: `/html/body/div[3]/div[2]/div[2]/main/div/div/div[1]/div[1]/div/form/div[3]/div[2]/button[2]`
2. **JavaScript Path**: Complex selector with multiple classes
3. **Fallback Methods**: Search by text content ("Submit", "Send") or button styling

### Implementation Pattern

#### Core Class Structure
```javascript
class V0AppInteraction {
    constructor() {
        this.editorSelector = '.ProseMirror';
        this.submitButtonXPath = '...';
    }
    
    async insertTextViaExecCommand(text) {
        // Focus editor, insert text using execCommand
    }
    
    async submitPrompt() {
        // Find and click submit button
    }
    
    async sendPrompt(promptText) {
        // Complete workflow: insert + submit
    }
    
    async waitForResponse() {
        // Monitor for AI response
    }
}
```

#### Usage Examples
```javascript
// Simple usage
const v0 = new V0AppInteraction();
await v0.sendPrompt('Create a React component for a todo list');

// Step-by-step control
await v0.insertTextViaExecCommand('Create a dashboard');
await v0.submitPrompt();
const response = await v0.waitForResponse();
```

### Key Implementation Details

#### Text Insertion Strategy
1. **Primary Method**: `document.execCommand('insertText', false, text)`
   - Most reliable for ProseMirror
   - Maintains undo/redo stack
   - Triggers proper input events

2. **Alternative Methods**:
   - Input/beforeinput events (less reliable)
   - Direct DOM manipulation (not recommended)

#### Submit Button Detection
**Multi-fallback Approach**:
1. Try complex CSS selector first
2. Fall back to searching all buttons
3. Use XPath as last resort
4. Check for text content matches

#### Response Monitoring
- Poll for new content in response area
- Check for assistant message elements
- Compare content changes over time
- Implement timeout for safety

### Important Considerations

#### Timing and Delays
- **Focus delay**: 100ms after focusing editor
- **Submit delay**: 500ms between text insertion and submit
- **Response polling**: 500ms intervals
- **Response completion**: 2s after last change

#### Error Handling
- Editor not found errors
- Submit button detection failures
- Response timeout handling
- Network error recovery

#### Browser Compatibility
- Requires modern browser with execCommand support
- Works best in Chrome/Edge
- May need adjustments for Firefox/Safari

### Integration with PicoBrain

**Potential Use Cases**:
1. **Code Generation**: Generate components for PicoBrain UI
2. **Documentation**: Auto-generate API documentation
3. **Testing**: Generate test cases for endpoints
4. **Migration Scripts**: Create database migrations
5. **UI Components**: Generate consistent UI components

**Workflow Integration**:
```javascript
// Example: Generate a new component for PicoBrain
const v0 = new V0AppInteraction();
const prompt = `
Create a React component for PicoBrain that:
- Uses our coral color scheme (#e67e5b)
- Follows our DashboardLayout pattern
- Includes TypeScript types
- Uses Tailwind CSS
- Component: PatientAppointmentCard
`;
await v0.sendPrompt(prompt);
```

### Security and Best Practices

#### Rate Limiting
- Implement delays between requests
- Avoid overwhelming the service
- Respect v0.app's terms of service

#### Error Recovery
- Implement retry logic with exponential backoff
- Log all interactions for debugging
- Graceful degradation on failures

#### Content Validation
- Verify generated code before use
- Test in isolated environment first
- Review for security vulnerabilities

### Future Enhancements

**Planned Improvements**:
1. [ ] Add response parsing for code extraction
2. [ ] Implement conversation context management
3. [ ] Add support for file uploads
4. [ ] Create CLI wrapper for automation
5. [ ] Build integration tests

**Research Areas**:
- WebSocket connection for real-time updates
- API endpoint discovery
- Authentication token management
- Session persistence strategies

---

## 🎨 Frontend Development with v0.app (2025-08-30)

### v0.app Integration Results

#### Successfully Completed
1. **Programmatic Connection**: Established browser automation with v0.app
2. **Dashboard Prompt**: Submitted design request with PicoClinics colors
3. **CRUD Templates**: Requested reusable CRUD components
4. **Color Integration**: Applied exact picoclinics.com palette

#### Key Learnings
- **Context Limits**: v0.app has prompt size limitations - use focused prompts
- **Generation Time**: Complex components take 5-10 seconds to generate
- **Editor Type**: ProseMirror requires execCommand for text insertion
- **Best Results**: Provide specific requirements and color values

### Recommended Frontend Stack (Based on v0.app Best Practices)

```yaml
Framework: Next.js 14+ (App Router)
Language: TypeScript 5.x
Styling: Tailwind CSS 3.x
Components: shadcn/ui
State: Zustand or Context API
Data Fetching: TanStack Query v5
Forms: React Hook Form + Zod
Animations: Framer Motion
Icons: Lucide React
Deployment: Vercel
```

### File Structure for Vercel Deployment

```bash
frontend/
├── app/                       # Next.js App Router
│   ├── (auth)/               # Authentication routes group
│   │   ├── login/
│   │   ├── register/
│   │   └── forgot-password/
│   ├── (dashboard)/          # Dashboard routes group
│   │   ├── layout.tsx        # Shared dashboard layout
│   │   ├── page.tsx          # Dashboard home
│   │   ├── patients/
│   │   ├── appointments/
│   │   ├── clinics/
│   │   └── settings/
│   ├── api/                  # API routes (if needed)
│   ├── layout.tsx            # Root layout
│   └── page.tsx              # Landing page
├── components/
│   ├── ui/                   # shadcn/ui components
│   │   ├── button.tsx
│   │   ├── card.tsx
│   │   ├── dialog.tsx
│   │   └── ...
│   ├── dashboard/            # Dashboard components
│   │   ├── stat-card.tsx
│   │   ├── activity-feed.tsx
│   │   └── quick-actions.tsx
│   ├── forms/                # Form components
│   │   ├── patient-form.tsx
│   │   └── appointment-form.tsx
│   └── shared/               # Shared components
│       ├── header.tsx
│       ├── sidebar.tsx
│       └── footer.tsx
├── lib/
│   ├── api/                  # API client functions
│   │   ├── auth.ts
│   │   ├── patients.ts
│   │   └── appointments.ts
│   ├── hooks/                # Custom React hooks
│   │   ├── use-auth.ts
│   │   └── use-patients.ts
│   └── utils/                # Utility functions
│       ├── cn.ts            # Class name utility
│       └── format.ts        # Formatting utilities
├── styles/
│   └── globals.css          # Global styles + Tailwind
├── types/                    # TypeScript types
│   ├── api.ts
│   ├── models.ts
│   └── components.ts
└── public/                   # Static assets
    ├── images/
    └── fonts/
```

### PicoClinics Design System Implementation

#### Tailwind Configuration
```javascript
// tailwind.config.js
module.exports = {
  theme: {
    extend: {
      colors: {
        'pico': {
          coral: {
            DEFAULT: '#e67e5b',
            light: '#f2a085',
            dark: '#d4634a',
            subtle: '#fdf5f2',
          },
          gray: {
            50: '#fafafa',
            100: '#f5f5f5',
            200: '#e5e5e5',
            600: '#525252',
            900: '#171717',
          },
          success: '#10b981',
          warning: '#f59e0b',
          error: '#ef4444',
          info: '#3b82f6',
        }
      }
    }
  }
}
```

#### CSS Variables
```css
/* styles/globals.css */
@layer base {
  :root {
    --pico-coral: 231 126 91;      /* #e67e5b */
    --pico-coral-light: 242 160 133; /* #f2a085 */
    --pico-coral-dark: 212 99 74;   /* #d4634a */
    --pico-coral-subtle: 253 245 242; /* #fdf5f2 */
    
    --background: 0 0% 100%;
    --foreground: 0 0% 9%;          /* #171717 */
    --primary: var(--pico-coral);
    --primary-foreground: 0 0% 100%;
  }
}
```

### Dashboard Components Specification

#### Main Dashboard Requirements
1. **Header**: Logo placeholder + User menu with logout
2. **Sidebar**: Navigation with active state indicators
3. **Metric Cards**: 
   - Patients count
   - Appointments today
   - Monthly revenue
   - Pending tasks
4. **Recent Activity**: Timeline of recent actions
5. **Quick Actions**: Buttons for common tasks

#### CRUD Template Features
1. **List View**:
   - Search bar with debounce
   - Column filters
   - Pagination
   - Bulk actions
   
2. **Create/Edit Modal**:
   - Form validation with Zod
   - Field-level errors
   - Loading states
   - Success feedback
   
3. **Delete Confirmation**:
   - Modal dialog
   - Consequence warning
   - Undo option (soft delete)
   
4. **Notifications**:
   - Toast for success/error
   - Position: top-right
   - Auto-dismiss: 5 seconds

### Vercel Deployment Configuration

#### Environment Variables
```bash
# .env.local
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_APP_NAME=PicoBrain
NEXT_PUBLIC_APP_VERSION=1.0.0

# .env.production
NEXT_PUBLIC_API_URL=https://api.picobrain.com
```

#### vercel.json
```json
{
  "buildCommand": "npm run build",
  "outputDirectory": ".next",
  "devCommand": "npm run dev",
  "installCommand": "npm install",
  "framework": "nextjs",
  "regions": ["iad1"],
  "env": {
    "NEXT_PUBLIC_API_URL": "@picobrain-api-url",
    "NEXT_PUBLIC_APP_NAME": "PicoBrain"
  }
}
```

### API Integration Pattern

#### Axios Configuration
```typescript
// lib/api/client.ts
import axios from 'axios';

const apiClient = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor for auth
apiClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Response interceptor for error handling
apiClient.interceptors.response.use(
  (response) => response,
  async (error) => {
    if (error.response?.status === 401) {
      // Handle token refresh or redirect to login
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

export default apiClient;
```

#### TanStack Query Setup
```typescript
// app/providers.tsx
'use client';

import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { ReactQueryDevtools } from '@tanstack/react-query-devtools';

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 60 * 1000, // 1 minute
      gcTime: 5 * 60 * 1000, // 5 minutes
      retry: 1,
      refetchOnWindowFocus: false,
    },
  },
});

export function Providers({ children }: { children: React.ReactNode }) {
  return (
    <QueryClientProvider client={queryClient}>
      {children}
      <ReactQueryDevtools initialIsOpen={false} />
    </QueryClientProvider>
  );
}
```

### Implementation Priorities

#### Phase 1: Foundation (Days 1-2)
1. ✅ Initialize Next.js with TypeScript
2. ✅ Configure Tailwind with PicoClinics colors
3. ✅ Install and setup shadcn/ui
4. ✅ Create layout components from v0.app
5. ✅ Setup API client with Axios

#### Phase 2: Core Features (Days 3-5)
1. [ ] Implement authentication flow
2. [ ] Build dashboard from v0.app design
3. [ ] Create CRUD templates for main entities
4. [ ] Connect to backend endpoints
5. [ ] Add loading and error states

#### Phase 3: Enhancement (Days 6-7)
1. [ ] Add data visualizations
2. [ ] Implement real-time updates
3. [ ] Optimize for mobile
4. [ ] Add PWA features
5. [ ] Performance optimization

#### Phase 4: Deployment (Day 8)
1. [ ] Configure Vercel project
2. [ ] Setup environment variables
3. [ ] Deploy to preview
4. [ ] Run lighthouse audit
5. [ ] Deploy to production

---

## Database Migration Patterns (Added 2025-08-30)

### SQLAlchemy Model Structure (PicoBrain)
- **Location**: `/backend/app/models/core.py`
- **Pattern**: All models in single file, re-exported via individual files
- **Inheritance**: Composition pattern using foreign keys (not true OOP inheritance)
- **Example**: Person → Employee relationship via person_id FK

### CSV to PostgreSQL Migration Strategy

#### 1. ID Mapping Pattern
```python
# Always create CSV ID → UUID mapping file
id_mapping = {}
for row in csv_data:
    new_id = uuid.uuid4()
    id_mapping[csv_row['id']] = new_id
    
# Save for dependent tables
import json
with open('id_mapping.json', 'w') as f:
    json.dump({k: str(v) for k, v in id_mapping.items()}, f)
```

#### 2. Data Transformation Functions
```python
def parse_address(address_string):
    """Extract city, country_code from full address"""
    parts = address_string.split(',')
    country_mapping = {
        'UK': 'GB', 'USA': 'US', 
        'Italy': 'IT', 'Canada': 'CA'
    }
    # Parse logic here
    return city, country_code

def parse_name(full_name):
    """Split full name into first and last"""
    parts = full_name.split()
    if len(parts) == 2:
        return parts[0], parts[1]
    elif len(parts) > 2:
        # Handle complex names
        return ' '.join(parts[:-1]), parts[-1]
    return full_name, ''
```

#### 3. Date Format Conversion
```python
from datetime import datetime

def convert_date(date_str):
    """Convert DD/MM/YYYY to Date object"""
    if not date_str:
        return None
    return datetime.strptime(date_str, '%d/%m/%Y').date()
```

#### 4. Enum Mapping Pattern
```python
# Create explicit mapping for mismatched enums
role_mapping = {
    'accountant': 'finance',
    'owner': 'admin',
    'staff': 'receptionist',  # or context-dependent
    'doctor': 'doctor'  # direct mapping
}

def map_role(csv_role):
    return role_mapping.get(csv_role.lower(), 'admin')
```

### Migration Script Template
```python
#!/usr/bin/env python3
import csv
import uuid
import sys
from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models.core import Model

# Database setup
DATABASE_URL = "postgresql://edo@localhost/picobraindb"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

def migrate_entity():
    session = SessionLocal()
    try:
        # 1. Clean existing data
        session.query(Model).delete()
        session.commit()
        
        # 2. Read CSV
        with open('data.csv', 'r', encoding='utf-8-sig') as f:
            data = list(csv.DictReader(f))
        
        # 3. Load ID mappings if needed
        with open('id_mapping.json') as f:
            id_mapping = json.load(f)
        
        # 4. Transform and insert
        for row in data:
            # Transform data
            new_record = Model(
                id=uuid.uuid4(),
                # mapped fields
            )
            session.add(new_record)
        
        session.commit()
        print(f"✓ Migrated {len(data)} records")
        
    except Exception as e:
        session.rollback()
        print(f"✗ Migration failed: {e}")
        raise
    finally:
        session.close()

if __name__ == "__main__":
    migrate_entity()
```

### Migration Order Strategy
1. **Respect Dependencies**: Parents before children
   - Clinics (no dependencies)
   - Persons (no dependencies) 
   - Employees (depends on Persons + Clinics)
   - Users (depends on Persons)
   - Clients (depends on Persons + Clinics)

2. **ID Mapping Persistence**: Save between migrations
   ```python
   # After each migration
   with open(f'{entity}_id_mapping.json', 'w') as f:
       json.dump(id_mapping, f)
   ```

3. **Validation After Migration**:
   ```python
   # Verify counts
   assert session.query(Model).count() == len(csv_data)
   # Verify relationships
   for record in session.query(Model).all():
       assert record.foreign_key_id is not None
   ```

### Common Migration Challenges & Solutions

| Challenge | Solution |
|-----------|----------|
| Missing fields in DB | Accept data loss or extend schema |
| Enum mismatches | Create mapping dictionary |
| Complex names | Smart parsing with fallbacks |
| Date formats | Use strptime with format string |
| Foreign key dependencies | Migrate in dependency order |
| NULL handling | Use `.get()` with defaults |
| Encoding issues | Use `encoding='utf-8-sig'` |
| Duplicate detection | Check unique constraints first |

### Database Access Pattern
```python
# Standard connection
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql://edo@localhost/picobraindb"
engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(bind=engine)

# Context manager pattern
from contextlib import contextmanager

@contextmanager
def get_db():
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except:
        db.rollback()
        raise
    finally:
        db.close()

# Usage
with get_db() as db:
    clinics = db.query(Clinic).all()
```

### Entity Relationship in PicoBrain
```
Person (Base Entity - 14 fields)
├── Employee (via person_id FK - 17 fields)
│   ├── role='doctor' → Doctor behavior
│   ├── role='nurse' → Nurse behavior  
│   ├── role='manager' → Manager behavior
│   └── role='finance' → Finance behavior
│   └── Links to:
│       ├── Clinic (via primary_clinic_id)
│       └── Currency (via salary_currency)
├── Client (via person_id FK)
│   └── Links to: Clinic (via preferred_clinic_id)
└── User (via person_id FK for authentication)

Clinic (Independent Entity - 17 fields)
├── employees (relationship)
├── clients (preferred_clinic relationship)
└── temp_id (migration helper)

Currencies (Reference Table - discovered via FK)
└── currency_code (referenced by employees.salary_currency)
```

### Migration Artifacts Created
- `/backend/migrate_clinics.py` - Initial clinic migration
- `/backend/remigrate_clinics_full.py` - Full address data migration
- `/backend/add_temp_id_column.py` - Schema modification script
- `/backend/clinic_id_mapping.json` - CSV ID to UUID mappings
- `/backend/verify_clinic_migration.py` - Data verification script
- `/backend/show_persons_employees_schema.py` - Schema inspection script
- `/backend/export_persons_employees_schema.py` - Schema export to JSON
- Pattern: Create similar scripts for Staff and Doctors

### Database Schema Updates (2025-08-30)

#### Persons Table - Complete Schema (14 fields)
```python
class Person(Base):
    __tablename__ = "persons"
    
    # Primary fields
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    middle_name = Column(String(100))
    
    # Contact fields
    email = Column(String(255), unique=True)
    phone_mobile = Column(String(50))
    phone_home = Column(String(50))
    
    # Personal details
    dob = Column(Date)
    gender = Column(ENUM('M', 'F', 'O', 'N', name='gender_type'))
    nationality = Column(String(2))  # Country code
    
    # Identification
    id_type = Column(String(20))  # passport, national ID, etc.
    id_number = Column(Text)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
```

#### Employees Table - Complete Schema (17 fields)
```python
class Employee(Base):
    __tablename__ = "employees"
    
    # Primary fields
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    person_id = Column(UUID(as_uuid=True), ForeignKey("persons.id"), nullable=False)
    employee_code = Column(String(20), unique=True)
    primary_clinic_id = Column(UUID(as_uuid=True), ForeignKey("clinics.id"), nullable=False)
    
    # Role and specialization
    role = Column(ENUM('doctor', 'nurse', 'receptionist', 'manager', 'finance', 'admin'))
    specialization = Column(String(100))
    
    # Professional licensing
    license_number = Column(String(50))
    license_expiry = Column(Date)
    
    # Employment dates
    hire_date = Column(Date, nullable=False)
    termination_date = Column(Date)
    
    # Compensation
    base_salary_minor = Column(BigInteger)  # Store in cents/pence
    salary_currency = Column(CHAR(3), ForeignKey("currencies.currency_code"))
    commission_rate = Column(Numeric)  # Decimal percentage
    
    # Status flags
    is_active = Column(Boolean, default=True)
    can_perform_treatments = Column(Boolean, default=False)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
```

#### Clinics Table - Complete Schema (17 fields)

```python
# Updated Clinic model with all database fields
class Clinic(Base):
    __tablename__ = "clinics"
    
    # Primary fields
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    code = Column(String(10), nullable=False, unique=True)
    name = Column(String(100), nullable=False)
    functional_currency = Column(CHAR(3))
    
    # Address fields (NEW)
    address_line_1 = Column(String(255))
    address_line_2 = Column(String(255))
    city = Column(String(100))
    state_province = Column(String(100))  # NEW
    postal_code = Column(String(20))      # NEW
    country_code = Column(CHAR(2))
    
    # Contact fields (NEW)
    phone = Column(String(50))
    email = Column(String(255))
    
    # Business fields (NEW)
    tax_id = Column(String(50))
    is_active = Column(Boolean, default=True)
    
    # Timestamps (NEW)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Migration helper (TEMPORARY)
    temp_id = Column(Integer)  # For CSV ID mapping during migration
```

### Two-Phase Migration Pattern

#### Phase 1: Basic Migration
- Create records with essential fields only
- Generate UUID mappings
- Handle data that exists in model

#### Phase 2: Full Data Migration
1. **Add missing columns to database** (if needed)
2. **Update SQLAlchemy models** to match database
3. **Re-migrate with UPDATE** (not DELETE/INSERT):
   ```python
   # Find existing record
   clinic = session.query(Clinic).filter_by(code=code).first()
   
   # Update all fields
   clinic.address_line_1 = row['address_line_1']
   clinic.address_line_2 = row['address_line_2']
   # ... update other fields
   
   # Preserve relationships
   clinic.updated_at = datetime.utcnow()
   ```

### Financial Data Storage Pattern

#### Salary Storage Best Practice
- Store salaries in **minor units** (cents/pence) using BigInteger
- Avoids floating-point precision issues
- Example: $5,000.00 stored as 500000 cents
- Formula: `display_amount = base_salary_minor / 100`

#### Currency Management
- Separate `currencies` table exists (discovered via FK)
- Each employee's salary has associated currency
- Clinics have functional_currency for operations
- Enables multi-currency support

#### Commission Storage
- Use Numeric type for precise decimal percentages
- Example: 15.5% stored as 0.155 or 15.5
- Calculation: `commission = (sale_amount * commission_rate)`

### Migration Best Practices Learned

1. **Always Check Database Schema First**
   - Database may have more fields than SQLAlchemy models
   - Use information_schema to discover all columns
   - Update models before migration

2. **Use temp_id for Mapping**
   - Add INTEGER temp_id column for CSV ID tracking
   - Preserves original ID relationships
   - Can be removed after all migrations complete

3. **Update vs Recreate**
   - UPDATE existing records to preserve UUIDs
   - Maintains foreign key relationships
   - Prevents orphaned records

4. **Data Quality Improvements**
   - Clean data during migration (fix typos, format issues)
   - Separate composite fields (address, name)
   - Convert data types (string to boolean)

5. **Verification Scripts**
   - Always create verification script
   - Check data completeness
   - Validate transformations

---

## Weekly Review: 2025-W35
- Commits: 3
- Files Changed: 19
- Top patterns: v0.app integration, Frontend architecture
- Key Achievement: Programmatic v0.app interaction established
---

## 🔄 Database Schema Update: Phone Number Splitting (2025-08-30)

### Complete Implementation Summary

#### Phase 1: Database Schema Changes ✅
**Rationale**: Improved UX with separate country code dropdowns, better validation, easier international formatting

**Tables Modified**:
1. **Persons**: Split `phone_mobile` and `phone_home` into country_code + number pairs
2. **Clinics**: Split `phone` into `phone_country_code` + `phone_number`
3. **Employees**: Added `temp_id` INTEGER for migration tracking
4. **Clients**: Added `temp_id` INTEGER (no phone fields to split)

**Migration Script**: `/backend/phone_splitting_migration.py` - Executed successfully

#### Phase 2: Pydantic Schemas & API Updates ✅

**Schema Updates** (`/backend/app/schemas/core.py`):
- Split all phone fields to match database
- Added validation patterns (country: `^\+\d{1,5}<!-- CLAUDE: ALWAYS READ THIS FIRST -->
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

## 📊 Database Migration Summary (2025-08-30)

### Completed
1. ✅ **Clinics**: Fully migrated with complete addresses (5 records)
2. ✅ **SQLAlchemy Models**: All 3 models updated to match database schema
   - Clinic: 7→17 fields
   - Person: 7→14 fields  
   - Employee: 8→17 fields
3. ✅ **temp_id**: Added to clinics for CSV ID mapping

### Ready for Migration
- **Staff.csv**: 44 records → Person + Employee tables
- **Doctors.csv**: 53 records → Person + Employee tables
- CSV fields now map to all database fields
- Employment dates, salaries, commissions can be stored

### Migration Order Plan
1. Clinics ✅ Complete
2. Persons (from Staff + Doctors)
3. Employees (link to Persons + Clinics)
4. Handle role mapping (accountant→finance, etc.)
5. Clean up temp_id column after migration

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
- Frontend: http://localhost:3000 (currently has build errors)
- Login Page: http://localhost:3000/login (requires frontend fix)
- Dashboard: http://localhost:3000/dashboard (requires frontend fix)
- Database Migrations: backend/alembic/versions/
- Test Scripts: backend/test_*.sh
- Admin User Creation: backend/app/seeds/create_admin.py

## 🔄 Authentication Integration Patterns

### Login Process (Verified)
1. User accesses http://localhost:3000/login
2. Enters credentials (admin@picobrain.com / admin123)
3. Frontend POSTs to /api/v1/auth/login
4. Backend validates with bcrypt password hash
5. Returns JWT token on success
6. Frontend stores token and redirects to /dashboard
7. All subsequent API calls include JWT in headers

### JWT Token Flow
**Pattern**: Middleware-based auth check with automatic refresh
**Implementation**: Store token in HTTP-only cookies or localStorage
**Benefits**: Seamless user experience, reduced auth errors

### Admin User Creation
**Script**: `backend/app/seeds/create_admin.py`
**Command**: `python manage.py create-admin`
**Creates**:
- Person record (System Administrator)
- User record with admin role
- Password hash using bcrypt
**Note**: Script checks if admin exists before creating

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

### Dashboard Layout Pattern (Implemented 2025-08-30)
**Learning**: Consistent layout wrapper reduces code duplication
**Pattern**: Single DashboardLayout component with slot-based content
**Status**: ✅ Successfully implemented in Phase 1

```typescript
// components/layout/dashboard-layout.tsx
export function DashboardLayout({ children, className }: DashboardLayoutProps) {
  return (
    <div className="min-h-screen bg-gray-50">
      <TopNavigation />
      <div className="flex h-[calc(100vh-4rem)]">
        <SideNavigation />
        <main className={cn(
          "flex-1 overflow-y-auto bg-gray-50",
          "lg:pl-64", // Account for fixed sidebar
          className
        )}>
          <div className="px-4 sm:px-6 lg:px-8 py-6">
            {children}
          </div>
        </main>
      </div>
    </div>
  )
}
```

**Implementation Success**:
- Mobile-responsive with slide-out menu
- Active route highlighting
- PicoClinics branding integrated
- Consistent padding and spacing

**Benefits**: 
- Eliminated layout inconsistencies between pages
- Single source of truth for navigation
- Easier maintenance and updates
- Guaranteed consistent UX across all dashboard pages

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

### Design Token System (Implemented 2025-08-30)
**Pattern**: Centralized design tokens for consistency
**Implementation**: JavaScript object with semantic naming

```typescript
// Used in dashboard refactoring
const tokens = {
  spacing: {
    page: '1.5rem',
    section: '1.5rem',
    card: '1rem',
  },
  typography: {
    pageTitle: 'text-3xl font-bold tracking-tight',
    sectionTitle: 'text-xl font-semibold',
    cardTitle: 'text-lg font-medium',
  }
}
```

**Result**: Consistent spacing and typography across all components

### StatCard Component Pattern
**Pattern**: Reusable metrics display component
**Implementation**: Self-contained with props for customization

```typescript
interface StatCardProps {
  title: string
  value: string | number
  description?: string
  icon: React.ElementType
  trend?: 'up' | 'down' | 'neutral'
  trendValue?: string
}
```

**Features**:
- Trend indicators with color coding
- Icon support for visual context
- Hover effects for interactivity
- Responsive grid layout

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

### Layout Inconsistency Across Pages
**Issue**: Different pages had different layouts and navigation
**Root Cause**: No shared layout component
**Solution**: Implemented DashboardLayout wrapper pattern
**Result**: All dashboard pages now have consistent look and feel

### className Utility for Tailwind
**Issue**: Complex conditional classes become unreadable
**Solution**: Implemented cn() utility function
```typescript
// lib/utils.ts
import { type ClassValue, clsx } from "clsx"
import { twMerge } from "tailwind-merge"

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}
```
**Benefits**: Cleaner conditional styling, proper class merging

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
```## Implementation Phases Documentation

### Phase 1: Dashboard Foundation (Completed 2025-08-30)
**Scope**: Main dashboard page only
**Files Created**: 4
- `components/layout/dashboard-layout.tsx` (210 lines)
- `app/dashboard/layout.tsx` (10 lines)
- `app/dashboard/page.tsx` (200 lines)
- `lib/utils.ts` (6 lines)

**Achievements**:
1. ✅ Established layout wrapper pattern
2. ✅ Integrated PicoClinics design system
3. ✅ Created reusable StatCard component
4. ✅ Implemented responsive navigation
5. ✅ Applied design tokens for consistency

**Key Decisions**:
- Used composition over inheritance
- Kept StatCard local (extract in Phase 2)
- Preserved all sub-pages unchanged
- Mobile-first responsive approach

**Lessons Learned**:
- Layout wrapper pattern immediately solves consistency issues
- Design tokens should be defined early
- cn() utility essential for complex Tailwind classes
- Incremental refactoring reduces risk

### Phase 2: Component Extraction (Planned)
**Scope**: Extract and share components
- [ ] Move StatCard to shared components
- [ ] Create shared DataTable component
- [ ] Extract form components
- [ ] Build loading skeletons

### Phase 3: Sub-Page Refactoring (Planned)
**Scope**: Apply patterns to all dashboard pages
- [ ] /dashboard/persons
- [ ] /dashboard/clinics
- [ ] /dashboard/clients
- [ ] /dashboard/employees
- [ ] /dashboard/users

## 🌨 v0.app Development Strategy (Updated 2025-08-30)

### Login Page Generation Plan

**Component Requirements**:
1. **Design Consistency**: Match dashboard and CRUD templates
2. **Color Scheme**: PicoClinics coral (#e67e5b) as primary
3. **Framework**: Next.js 14 App Router structure
4. **Form Handling**: React Hook Form with Zod validation
5. **Authentication**: JWT with /api/v1/auth/login endpoint
6. **Error Handling**: Inline validation messages
7. **Loading States**: Button spinner during authentication
8. **Responsive**: Mobile-first design approach

**File Structure for Login**:
```
app/
  (auth)/
    login/
      page.tsx       # Main login page
      layout.tsx     # Auth-specific layout
components/
  auth/
    LoginForm.tsx    # Form component
    SocialLogin.tsx  # OAuth buttons
lib/
  auth/
    validation.ts    # Zod schemas
    api.ts          # Auth API calls
```

### v0.app Templates Status
- **Dashboard**: `/Users/edo/PyProjects/picobrain-dashboard.zip` ✅
- **CRUD**: `/Users/edo/PyProjects/crud-template.zip` ✅
- **Login**: To be generated with Next.js 14 compatibility

## 🤖 v0.app Programmatic Interaction Guide (Discovered 2025-08-30)

### Key Discovery
**Breakthrough**: Successfully figured out how to programmatically interact with v0.app AI through browser automation.

### Technical Details

#### Editor Technology
- **Editor Type**: ProseMirror (rich text editor framework)
- **Text Input Method**: `document.execCommand('insertText', false, 'text')`
- **Key Requirement**: Must focus the editor before inserting text

#### Submit Button Identification
**Multiple Methods to Find Submit Button**:
1. **XPath**: `/html/body/div[3]/div[2]/div[2]/main/div/div/div[1]/div[1]/div/form/div[3]/div[2]/button[2]`
2. **JavaScript Path**: Complex selector with multiple classes
3. **Fallback Methods**: Search by text content ("Submit", "Send") or button styling

### Implementation Pattern

#### Core Class Structure
```javascript
class V0AppInteraction {
    constructor() {
        this.editorSelector = '.ProseMirror';
        this.submitButtonXPath = '...';
    }
    
    async insertTextViaExecCommand(text) {
        // Focus editor, insert text using execCommand
    }
    
    async submitPrompt() {
        // Find and click submit button
    }
    
    async sendPrompt(promptText) {
        // Complete workflow: insert + submit
    }
    
    async waitForResponse() {
        // Monitor for AI response
    }
}
```

#### Usage Examples
```javascript
// Simple usage
const v0 = new V0AppInteraction();
await v0.sendPrompt('Create a React component for a todo list');

// Step-by-step control
await v0.insertTextViaExecCommand('Create a dashboard');
await v0.submitPrompt();
const response = await v0.waitForResponse();
```

### Key Implementation Details

#### Text Insertion Strategy
1. **Primary Method**: `document.execCommand('insertText', false, text)`
   - Most reliable for ProseMirror
   - Maintains undo/redo stack
   - Triggers proper input events

2. **Alternative Methods**:
   - Input/beforeinput events (less reliable)
   - Direct DOM manipulation (not recommended)

#### Submit Button Detection
**Multi-fallback Approach**:
1. Try complex CSS selector first
2. Fall back to searching all buttons
3. Use XPath as last resort
4. Check for text content matches

#### Response Monitoring
- Poll for new content in response area
- Check for assistant message elements
- Compare content changes over time
- Implement timeout for safety

### Important Considerations

#### Timing and Delays
- **Focus delay**: 100ms after focusing editor
- **Submit delay**: 500ms between text insertion and submit
- **Response polling**: 500ms intervals
- **Response completion**: 2s after last change

#### Error Handling
- Editor not found errors
- Submit button detection failures
- Response timeout handling
- Network error recovery

#### Browser Compatibility
- Requires modern browser with execCommand support
- Works best in Chrome/Edge
- May need adjustments for Firefox/Safari

### Integration with PicoBrain

**Potential Use Cases**:
1. **Code Generation**: Generate components for PicoBrain UI
2. **Documentation**: Auto-generate API documentation
3. **Testing**: Generate test cases for endpoints
4. **Migration Scripts**: Create database migrations
5. **UI Components**: Generate consistent UI components

**Workflow Integration**:
```javascript
// Example: Generate a new component for PicoBrain
const v0 = new V0AppInteraction();
const prompt = `
Create a React component for PicoBrain that:
- Uses our coral color scheme (#e67e5b)
- Follows our DashboardLayout pattern
- Includes TypeScript types
- Uses Tailwind CSS
- Component: PatientAppointmentCard
`;
await v0.sendPrompt(prompt);
```

### Security and Best Practices

#### Rate Limiting
- Implement delays between requests
- Avoid overwhelming the service
- Respect v0.app's terms of service

#### Error Recovery
- Implement retry logic with exponential backoff
- Log all interactions for debugging
- Graceful degradation on failures

#### Content Validation
- Verify generated code before use
- Test in isolated environment first
- Review for security vulnerabilities

### Future Enhancements

**Planned Improvements**:
1. [ ] Add response parsing for code extraction
2. [ ] Implement conversation context management
3. [ ] Add support for file uploads
4. [ ] Create CLI wrapper for automation
5. [ ] Build integration tests

**Research Areas**:
- WebSocket connection for real-time updates
- API endpoint discovery
- Authentication token management
- Session persistence strategies

---

## 🎨 Frontend Development with v0.app (2025-08-30)

### v0.app Integration Results

#### Successfully Completed
1. **Programmatic Connection**: Established browser automation with v0.app
2. **Dashboard Prompt**: Submitted design request with PicoClinics colors
3. **CRUD Templates**: Requested reusable CRUD components
4. **Color Integration**: Applied exact picoclinics.com palette

#### Key Learnings
- **Context Limits**: v0.app has prompt size limitations - use focused prompts
- **Generation Time**: Complex components take 5-10 seconds to generate
- **Editor Type**: ProseMirror requires execCommand for text insertion
- **Best Results**: Provide specific requirements and color values

### Recommended Frontend Stack (Based on v0.app Best Practices)

```yaml
Framework: Next.js 14+ (App Router)
Language: TypeScript 5.x
Styling: Tailwind CSS 3.x
Components: shadcn/ui
State: Zustand or Context API
Data Fetching: TanStack Query v5
Forms: React Hook Form + Zod
Animations: Framer Motion
Icons: Lucide React
Deployment: Vercel
```

### File Structure for Vercel Deployment

```bash
frontend/
├── app/                       # Next.js App Router
│   ├── (auth)/               # Authentication routes group
│   │   ├── login/
│   │   ├── register/
│   │   └── forgot-password/
│   ├── (dashboard)/          # Dashboard routes group
│   │   ├── layout.tsx        # Shared dashboard layout
│   │   ├── page.tsx          # Dashboard home
│   │   ├── patients/
│   │   ├── appointments/
│   │   ├── clinics/
│   │   └── settings/
│   ├── api/                  # API routes (if needed)
│   ├── layout.tsx            # Root layout
│   └── page.tsx              # Landing page
├── components/
│   ├── ui/                   # shadcn/ui components
│   │   ├── button.tsx
│   │   ├── card.tsx
│   │   ├── dialog.tsx
│   │   └── ...
│   ├── dashboard/            # Dashboard components
│   │   ├── stat-card.tsx
│   │   ├── activity-feed.tsx
│   │   └── quick-actions.tsx
│   ├── forms/                # Form components
│   │   ├── patient-form.tsx
│   │   └── appointment-form.tsx
│   └── shared/               # Shared components
│       ├── header.tsx
│       ├── sidebar.tsx
│       └── footer.tsx
├── lib/
│   ├── api/                  # API client functions
│   │   ├── auth.ts
│   │   ├── patients.ts
│   │   └── appointments.ts
│   ├── hooks/                # Custom React hooks
│   │   ├── use-auth.ts
│   │   └── use-patients.ts
│   └── utils/                # Utility functions
│       ├── cn.ts            # Class name utility
│       └── format.ts        # Formatting utilities
├── styles/
│   └── globals.css          # Global styles + Tailwind
├── types/                    # TypeScript types
│   ├── api.ts
│   ├── models.ts
│   └── components.ts
└── public/                   # Static assets
    ├── images/
    └── fonts/
```

### PicoClinics Design System Implementation

#### Tailwind Configuration
```javascript
// tailwind.config.js
module.exports = {
  theme: {
    extend: {
      colors: {
        'pico': {
          coral: {
            DEFAULT: '#e67e5b',
            light: '#f2a085',
            dark: '#d4634a',
            subtle: '#fdf5f2',
          },
          gray: {
            50: '#fafafa',
            100: '#f5f5f5',
            200: '#e5e5e5',
            600: '#525252',
            900: '#171717',
          },
          success: '#10b981',
          warning: '#f59e0b',
          error: '#ef4444',
          info: '#3b82f6',
        }
      }
    }
  }
}
```

#### CSS Variables
```css
/* styles/globals.css */
@layer base {
  :root {
    --pico-coral: 231 126 91;      /* #e67e5b */
    --pico-coral-light: 242 160 133; /* #f2a085 */
    --pico-coral-dark: 212 99 74;   /* #d4634a */
    --pico-coral-subtle: 253 245 242; /* #fdf5f2 */
    
    --background: 0 0% 100%;
    --foreground: 0 0% 9%;          /* #171717 */
    --primary: var(--pico-coral);
    --primary-foreground: 0 0% 100%;
  }
}
```

### Dashboard Components Specification

#### Main Dashboard Requirements
1. **Header**: Logo placeholder + User menu with logout
2. **Sidebar**: Navigation with active state indicators
3. **Metric Cards**: 
   - Patients count
   - Appointments today
   - Monthly revenue
   - Pending tasks
4. **Recent Activity**: Timeline of recent actions
5. **Quick Actions**: Buttons for common tasks

#### CRUD Template Features
1. **List View**:
   - Search bar with debounce
   - Column filters
   - Pagination
   - Bulk actions
   
2. **Create/Edit Modal**:
   - Form validation with Zod
   - Field-level errors
   - Loading states
   - Success feedback
   
3. **Delete Confirmation**:
   - Modal dialog
   - Consequence warning
   - Undo option (soft delete)
   
4. **Notifications**:
   - Toast for success/error
   - Position: top-right
   - Auto-dismiss: 5 seconds

### Vercel Deployment Configuration

#### Environment Variables
```bash
# .env.local
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_APP_NAME=PicoBrain
NEXT_PUBLIC_APP_VERSION=1.0.0

# .env.production
NEXT_PUBLIC_API_URL=https://api.picobrain.com
```

#### vercel.json
```json
{
  "buildCommand": "npm run build",
  "outputDirectory": ".next",
  "devCommand": "npm run dev",
  "installCommand": "npm install",
  "framework": "nextjs",
  "regions": ["iad1"],
  "env": {
    "NEXT_PUBLIC_API_URL": "@picobrain-api-url",
    "NEXT_PUBLIC_APP_NAME": "PicoBrain"
  }
}
```

### API Integration Pattern

#### Axios Configuration
```typescript
// lib/api/client.ts
import axios from 'axios';

const apiClient = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor for auth
apiClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Response interceptor for error handling
apiClient.interceptors.response.use(
  (response) => response,
  async (error) => {
    if (error.response?.status === 401) {
      // Handle token refresh or redirect to login
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

export default apiClient;
```

#### TanStack Query Setup
```typescript
// app/providers.tsx
'use client';

import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { ReactQueryDevtools } from '@tanstack/react-query-devtools';

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 60 * 1000, // 1 minute
      gcTime: 5 * 60 * 1000, // 5 minutes
      retry: 1,
      refetchOnWindowFocus: false,
    },
  },
});

export function Providers({ children }: { children: React.ReactNode }) {
  return (
    <QueryClientProvider client={queryClient}>
      {children}
      <ReactQueryDevtools initialIsOpen={false} />
    </QueryClientProvider>
  );
}
```

### Implementation Priorities

#### Phase 1: Foundation (Days 1-2)
1. ✅ Initialize Next.js with TypeScript
2. ✅ Configure Tailwind with PicoClinics colors
3. ✅ Install and setup shadcn/ui
4. ✅ Create layout components from v0.app
5. ✅ Setup API client with Axios

#### Phase 2: Core Features (Days 3-5)
1. [ ] Implement authentication flow
2. [ ] Build dashboard from v0.app design
3. [ ] Create CRUD templates for main entities
4. [ ] Connect to backend endpoints
5. [ ] Add loading and error states

#### Phase 3: Enhancement (Days 6-7)
1. [ ] Add data visualizations
2. [ ] Implement real-time updates
3. [ ] Optimize for mobile
4. [ ] Add PWA features
5. [ ] Performance optimization

#### Phase 4: Deployment (Day 8)
1. [ ] Configure Vercel project
2. [ ] Setup environment variables
3. [ ] Deploy to preview
4. [ ] Run lighthouse audit
5. [ ] Deploy to production

---

## Database Migration Patterns (Added 2025-08-30)

### SQLAlchemy Model Structure (PicoBrain)
- **Location**: `/backend/app/models/core.py`
- **Pattern**: All models in single file, re-exported via individual files
- **Inheritance**: Composition pattern using foreign keys (not true OOP inheritance)
- **Example**: Person → Employee relationship via person_id FK

### CSV to PostgreSQL Migration Strategy

#### 1. ID Mapping Pattern
```python
# Always create CSV ID → UUID mapping file
id_mapping = {}
for row in csv_data:
    new_id = uuid.uuid4()
    id_mapping[csv_row['id']] = new_id
    
# Save for dependent tables
import json
with open('id_mapping.json', 'w') as f:
    json.dump({k: str(v) for k, v in id_mapping.items()}, f)
```

#### 2. Data Transformation Functions
```python
def parse_address(address_string):
    """Extract city, country_code from full address"""
    parts = address_string.split(',')
    country_mapping = {
        'UK': 'GB', 'USA': 'US', 
        'Italy': 'IT', 'Canada': 'CA'
    }
    # Parse logic here
    return city, country_code

def parse_name(full_name):
    """Split full name into first and last"""
    parts = full_name.split()
    if len(parts) == 2:
        return parts[0], parts[1]
    elif len(parts) > 2:
        # Handle complex names
        return ' '.join(parts[:-1]), parts[-1]
    return full_name, ''
```

#### 3. Date Format Conversion
```python
from datetime import datetime

def convert_date(date_str):
    """Convert DD/MM/YYYY to Date object"""
    if not date_str:
        return None
    return datetime.strptime(date_str, '%d/%m/%Y').date()
```

#### 4. Enum Mapping Pattern
```python
# Create explicit mapping for mismatched enums
role_mapping = {
    'accountant': 'finance',
    'owner': 'admin',
    'staff': 'receptionist',  # or context-dependent
    'doctor': 'doctor'  # direct mapping
}

def map_role(csv_role):
    return role_mapping.get(csv_role.lower(), 'admin')
```

### Migration Script Template
```python
#!/usr/bin/env python3
import csv
import uuid
import sys
from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models.core import Model

# Database setup
DATABASE_URL = "postgresql://edo@localhost/picobraindb"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

def migrate_entity():
    session = SessionLocal()
    try:
        # 1. Clean existing data
        session.query(Model).delete()
        session.commit()
        
        # 2. Read CSV
        with open('data.csv', 'r', encoding='utf-8-sig') as f:
            data = list(csv.DictReader(f))
        
        # 3. Load ID mappings if needed
        with open('id_mapping.json') as f:
            id_mapping = json.load(f)
        
        # 4. Transform and insert
        for row in data:
            # Transform data
            new_record = Model(
                id=uuid.uuid4(),
                # mapped fields
            )
            session.add(new_record)
        
        session.commit()
        print(f"✓ Migrated {len(data)} records")
        
    except Exception as e:
        session.rollback()
        print(f"✗ Migration failed: {e}")
        raise
    finally:
        session.close()

if __name__ == "__main__":
    migrate_entity()
```

### Migration Order Strategy
1. **Respect Dependencies**: Parents before children
   - Clinics (no dependencies)
   - Persons (no dependencies) 
   - Employees (depends on Persons + Clinics)
   - Users (depends on Persons)
   - Clients (depends on Persons + Clinics)

2. **ID Mapping Persistence**: Save between migrations
   ```python
   # After each migration
   with open(f'{entity}_id_mapping.json', 'w') as f:
       json.dump(id_mapping, f)
   ```

3. **Validation After Migration**:
   ```python
   # Verify counts
   assert session.query(Model).count() == len(csv_data)
   # Verify relationships
   for record in session.query(Model).all():
       assert record.foreign_key_id is not None
   ```

### Common Migration Challenges & Solutions

| Challenge | Solution |
|-----------|----------|
| Missing fields in DB | Accept data loss or extend schema |
| Enum mismatches | Create mapping dictionary |
| Complex names | Smart parsing with fallbacks |
| Date formats | Use strptime with format string |
| Foreign key dependencies | Migrate in dependency order |
| NULL handling | Use `.get()` with defaults |
| Encoding issues | Use `encoding='utf-8-sig'` |
| Duplicate detection | Check unique constraints first |

### Database Access Pattern
```python
# Standard connection
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql://edo@localhost/picobraindb"
engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(bind=engine)

# Context manager pattern
from contextlib import contextmanager

@contextmanager
def get_db():
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except:
        db.rollback()
        raise
    finally:
        db.close()

# Usage
with get_db() as db:
    clinics = db.query(Clinic).all()
```

### Entity Relationship in PicoBrain
```
Person (Base Entity - 14 fields)
├── Employee (via person_id FK - 17 fields)
│   ├── role='doctor' → Doctor behavior
│   ├── role='nurse' → Nurse behavior  
│   ├── role='manager' → Manager behavior
│   └── role='finance' → Finance behavior
│   └── Links to:
│       ├── Clinic (via primary_clinic_id)
│       └── Currency (via salary_currency)
├── Client (via person_id FK)
│   └── Links to: Clinic (via preferred_clinic_id)
└── User (via person_id FK for authentication)

Clinic (Independent Entity - 17 fields)
├── employees (relationship)
├── clients (preferred_clinic relationship)
└── temp_id (migration helper)

Currencies (Reference Table - discovered via FK)
└── currency_code (referenced by employees.salary_currency)
```

### Migration Artifacts Created
- `/backend/migrate_clinics.py` - Initial clinic migration
- `/backend/remigrate_clinics_full.py` - Full address data migration
- `/backend/add_temp_id_column.py` - Schema modification script
- `/backend/clinic_id_mapping.json` - CSV ID to UUID mappings
- `/backend/verify_clinic_migration.py` - Data verification script
- `/backend/show_persons_employees_schema.py` - Schema inspection script
- `/backend/export_persons_employees_schema.py` - Schema export to JSON
- Pattern: Create similar scripts for Staff and Doctors

### Database Schema Updates (2025-08-30)

#### Persons Table - Complete Schema (14 fields)
```python
class Person(Base):
    __tablename__ = "persons"
    
    # Primary fields
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    middle_name = Column(String(100))
    
    # Contact fields
    email = Column(String(255), unique=True)
    phone_mobile = Column(String(50))
    phone_home = Column(String(50))
    
    # Personal details
    dob = Column(Date)
    gender = Column(ENUM('M', 'F', 'O', 'N', name='gender_type'))
    nationality = Column(String(2))  # Country code
    
    # Identification
    id_type = Column(String(20))  # passport, national ID, etc.
    id_number = Column(Text)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
```

#### Employees Table - Complete Schema (17 fields)
```python
class Employee(Base):
    __tablename__ = "employees"
    
    # Primary fields
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    person_id = Column(UUID(as_uuid=True), ForeignKey("persons.id"), nullable=False)
    employee_code = Column(String(20), unique=True)
    primary_clinic_id = Column(UUID(as_uuid=True), ForeignKey("clinics.id"), nullable=False)
    
    # Role and specialization
    role = Column(ENUM('doctor', 'nurse', 'receptionist', 'manager', 'finance', 'admin'))
    specialization = Column(String(100))
    
    # Professional licensing
    license_number = Column(String(50))
    license_expiry = Column(Date)
    
    # Employment dates
    hire_date = Column(Date, nullable=False)
    termination_date = Column(Date)
    
    # Compensation
    base_salary_minor = Column(BigInteger)  # Store in cents/pence
    salary_currency = Column(CHAR(3), ForeignKey("currencies.currency_code"))
    commission_rate = Column(Numeric)  # Decimal percentage
    
    # Status flags
    is_active = Column(Boolean, default=True)
    can_perform_treatments = Column(Boolean, default=False)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
```

#### Clinics Table - Complete Schema (17 fields)

```python
# Updated Clinic model with all database fields
class Clinic(Base):
    __tablename__ = "clinics"
    
    # Primary fields
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    code = Column(String(10), nullable=False, unique=True)
    name = Column(String(100), nullable=False)
    functional_currency = Column(CHAR(3))
    
    # Address fields (NEW)
    address_line_1 = Column(String(255))
    address_line_2 = Column(String(255))
    city = Column(String(100))
    state_province = Column(String(100))  # NEW
    postal_code = Column(String(20))      # NEW
    country_code = Column(CHAR(2))
    
    # Contact fields (NEW)
    phone = Column(String(50))
    email = Column(String(255))
    
    # Business fields (NEW)
    tax_id = Column(String(50))
    is_active = Column(Boolean, default=True)
    
    # Timestamps (NEW)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Migration helper (TEMPORARY)
    temp_id = Column(Integer)  # For CSV ID mapping during migration
```

### Two-Phase Migration Pattern

#### Phase 1: Basic Migration
- Create records with essential fields only
- Generate UUID mappings
- Handle data that exists in model

#### Phase 2: Full Data Migration
1. **Add missing columns to database** (if needed)
2. **Update SQLAlchemy models** to match database
3. **Re-migrate with UPDATE** (not DELETE/INSERT):
   ```python
   # Find existing record
   clinic = session.query(Clinic).filter_by(code=code).first()
   
   # Update all fields
   clinic.address_line_1 = row['address_line_1']
   clinic.address_line_2 = row['address_line_2']
   # ... update other fields
   
   # Preserve relationships
   clinic.updated_at = datetime.utcnow()
   ```

### Financial Data Storage Pattern

#### Salary Storage Best Practice
- Store salaries in **minor units** (cents/pence) using BigInteger
- Avoids floating-point precision issues
- Example: $5,000.00 stored as 500000 cents
- Formula: `display_amount = base_salary_minor / 100`

#### Currency Management
- Separate `currencies` table exists (discovered via FK)
- Each employee's salary has associated currency
- Clinics have functional_currency for operations
- Enables multi-currency support

#### Commission Storage
- Use Numeric type for precise decimal percentages
- Example: 15.5% stored as 0.155 or 15.5
- Calculation: `commission = (sale_amount * commission_rate)`

### Migration Best Practices Learned

1. **Always Check Database Schema First**
   - Database may have more fields than SQLAlchemy models
   - Use information_schema to discover all columns
   - Update models before migration

2. **Use temp_id for Mapping**
   - Add INTEGER temp_id column for CSV ID tracking
   - Preserves original ID relationships
   - Can be removed after all migrations complete

3. **Update vs Recreate**
   - UPDATE existing records to preserve UUIDs
   - Maintains foreign key relationships
   - Prevents orphaned records

4. **Data Quality Improvements**
   - Clean data during migration (fix typos, format issues)
   - Separate composite fields (address, name)
   - Convert data types (string to boolean)

5. **Verification Scripts**
   - Always create verification script
   - Check data completeness
   - Validate transformations

---

## Weekly Review: 2025-W35
- Commits: 3
- Files Changed: 19
- Top patterns: v0.app integration, Frontend architecture
- Key Achievement: Programmatic v0.app interaction established
---

, number: `^\d{4,20}<!-- CLAUDE: ALWAYS READ THIS FIRST -->
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

## 📊 Database Migration Summary (2025-08-30)

### Completed
1. ✅ **Clinics**: Fully migrated with complete addresses (5 records)
2. ✅ **SQLAlchemy Models**: All 3 models updated to match database schema
   - Clinic: 7→17 fields
   - Person: 7→14 fields  
   - Employee: 8→17 fields
3. ✅ **temp_id**: Added to clinics for CSV ID mapping

### Ready for Migration
- **Staff.csv**: 44 records → Person + Employee tables
- **Doctors.csv**: 53 records → Person + Employee tables
- CSV fields now map to all database fields
- Employment dates, salaries, commissions can be stored

### Migration Order Plan
1. Clinics ✅ Complete
2. Persons (from Staff + Doctors)
3. Employees (link to Persons + Clinics)
4. Handle role mapping (accountant→finance, etc.)
5. Clean up temp_id column after migration

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
- Frontend: http://localhost:3000 (currently has build errors)
- Login Page: http://localhost:3000/login (requires frontend fix)
- Dashboard: http://localhost:3000/dashboard (requires frontend fix)
- Database Migrations: backend/alembic/versions/
- Test Scripts: backend/test_*.sh
- Admin User Creation: backend/app/seeds/create_admin.py

## 🔄 Authentication Integration Patterns

### Login Process (Verified)
1. User accesses http://localhost:3000/login
2. Enters credentials (admin@picobrain.com / admin123)
3. Frontend POSTs to /api/v1/auth/login
4. Backend validates with bcrypt password hash
5. Returns JWT token on success
6. Frontend stores token and redirects to /dashboard
7. All subsequent API calls include JWT in headers

### JWT Token Flow
**Pattern**: Middleware-based auth check with automatic refresh
**Implementation**: Store token in HTTP-only cookies or localStorage
**Benefits**: Seamless user experience, reduced auth errors

### Admin User Creation
**Script**: `backend/app/seeds/create_admin.py`
**Command**: `python manage.py create-admin`
**Creates**:
- Person record (System Administrator)
- User record with admin role
- Password hash using bcrypt
**Note**: Script checks if admin exists before creating

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

### Dashboard Layout Pattern (Implemented 2025-08-30)
**Learning**: Consistent layout wrapper reduces code duplication
**Pattern**: Single DashboardLayout component with slot-based content
**Status**: ✅ Successfully implemented in Phase 1

```typescript
// components/layout/dashboard-layout.tsx
export function DashboardLayout({ children, className }: DashboardLayoutProps) {
  return (
    <div className="min-h-screen bg-gray-50">
      <TopNavigation />
      <div className="flex h-[calc(100vh-4rem)]">
        <SideNavigation />
        <main className={cn(
          "flex-1 overflow-y-auto bg-gray-50",
          "lg:pl-64", // Account for fixed sidebar
          className
        )}>
          <div className="px-4 sm:px-6 lg:px-8 py-6">
            {children}
          </div>
        </main>
      </div>
    </div>
  )
}
```

**Implementation Success**:
- Mobile-responsive with slide-out menu
- Active route highlighting
- PicoClinics branding integrated
- Consistent padding and spacing

**Benefits**: 
- Eliminated layout inconsistencies between pages
- Single source of truth for navigation
- Easier maintenance and updates
- Guaranteed consistent UX across all dashboard pages

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

### Design Token System (Implemented 2025-08-30)
**Pattern**: Centralized design tokens for consistency
**Implementation**: JavaScript object with semantic naming

```typescript
// Used in dashboard refactoring
const tokens = {
  spacing: {
    page: '1.5rem',
    section: '1.5rem',
    card: '1rem',
  },
  typography: {
    pageTitle: 'text-3xl font-bold tracking-tight',
    sectionTitle: 'text-xl font-semibold',
    cardTitle: 'text-lg font-medium',
  }
}
```

**Result**: Consistent spacing and typography across all components

### StatCard Component Pattern
**Pattern**: Reusable metrics display component
**Implementation**: Self-contained with props for customization

```typescript
interface StatCardProps {
  title: string
  value: string | number
  description?: string
  icon: React.ElementType
  trend?: 'up' | 'down' | 'neutral'
  trendValue?: string
}
```

**Features**:
- Trend indicators with color coding
- Icon support for visual context
- Hover effects for interactivity
- Responsive grid layout

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

### Layout Inconsistency Across Pages
**Issue**: Different pages had different layouts and navigation
**Root Cause**: No shared layout component
**Solution**: Implemented DashboardLayout wrapper pattern
**Result**: All dashboard pages now have consistent look and feel

### className Utility for Tailwind
**Issue**: Complex conditional classes become unreadable
**Solution**: Implemented cn() utility function
```typescript
// lib/utils.ts
import { type ClassValue, clsx } from "clsx"
import { twMerge } from "tailwind-merge"

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}
```
**Benefits**: Cleaner conditional styling, proper class merging

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
```## Implementation Phases Documentation

### Phase 1: Dashboard Foundation (Completed 2025-08-30)
**Scope**: Main dashboard page only
**Files Created**: 4
- `components/layout/dashboard-layout.tsx` (210 lines)
- `app/dashboard/layout.tsx` (10 lines)
- `app/dashboard/page.tsx` (200 lines)
- `lib/utils.ts` (6 lines)

**Achievements**:
1. ✅ Established layout wrapper pattern
2. ✅ Integrated PicoClinics design system
3. ✅ Created reusable StatCard component
4. ✅ Implemented responsive navigation
5. ✅ Applied design tokens for consistency

**Key Decisions**:
- Used composition over inheritance
- Kept StatCard local (extract in Phase 2)
- Preserved all sub-pages unchanged
- Mobile-first responsive approach

**Lessons Learned**:
- Layout wrapper pattern immediately solves consistency issues
- Design tokens should be defined early
- cn() utility essential for complex Tailwind classes
- Incremental refactoring reduces risk

### Phase 2: Component Extraction (Planned)
**Scope**: Extract and share components
- [ ] Move StatCard to shared components
- [ ] Create shared DataTable component
- [ ] Extract form components
- [ ] Build loading skeletons

### Phase 3: Sub-Page Refactoring (Planned)
**Scope**: Apply patterns to all dashboard pages
- [ ] /dashboard/persons
- [ ] /dashboard/clinics
- [ ] /dashboard/clients
- [ ] /dashboard/employees
- [ ] /dashboard/users

## 🌨 v0.app Development Strategy (Updated 2025-08-30)

### Login Page Generation Plan

**Component Requirements**:
1. **Design Consistency**: Match dashboard and CRUD templates
2. **Color Scheme**: PicoClinics coral (#e67e5b) as primary
3. **Framework**: Next.js 14 App Router structure
4. **Form Handling**: React Hook Form with Zod validation
5. **Authentication**: JWT with /api/v1/auth/login endpoint
6. **Error Handling**: Inline validation messages
7. **Loading States**: Button spinner during authentication
8. **Responsive**: Mobile-first design approach

**File Structure for Login**:
```
app/
  (auth)/
    login/
      page.tsx       # Main login page
      layout.tsx     # Auth-specific layout
components/
  auth/
    LoginForm.tsx    # Form component
    SocialLogin.tsx  # OAuth buttons
lib/
  auth/
    validation.ts    # Zod schemas
    api.ts          # Auth API calls
```

### v0.app Templates Status
- **Dashboard**: `/Users/edo/PyProjects/picobrain-dashboard.zip` ✅
- **CRUD**: `/Users/edo/PyProjects/crud-template.zip` ✅
- **Login**: To be generated with Next.js 14 compatibility

## 🤖 v0.app Programmatic Interaction Guide (Discovered 2025-08-30)

### Key Discovery
**Breakthrough**: Successfully figured out how to programmatically interact with v0.app AI through browser automation.

### Technical Details

#### Editor Technology
- **Editor Type**: ProseMirror (rich text editor framework)
- **Text Input Method**: `document.execCommand('insertText', false, 'text')`
- **Key Requirement**: Must focus the editor before inserting text

#### Submit Button Identification
**Multiple Methods to Find Submit Button**:
1. **XPath**: `/html/body/div[3]/div[2]/div[2]/main/div/div/div[1]/div[1]/div/form/div[3]/div[2]/button[2]`
2. **JavaScript Path**: Complex selector with multiple classes
3. **Fallback Methods**: Search by text content ("Submit", "Send") or button styling

### Implementation Pattern

#### Core Class Structure
```javascript
class V0AppInteraction {
    constructor() {
        this.editorSelector = '.ProseMirror';
        this.submitButtonXPath = '...';
    }
    
    async insertTextViaExecCommand(text) {
        // Focus editor, insert text using execCommand
    }
    
    async submitPrompt() {
        // Find and click submit button
    }
    
    async sendPrompt(promptText) {
        // Complete workflow: insert + submit
    }
    
    async waitForResponse() {
        // Monitor for AI response
    }
}
```

#### Usage Examples
```javascript
// Simple usage
const v0 = new V0AppInteraction();
await v0.sendPrompt('Create a React component for a todo list');

// Step-by-step control
await v0.insertTextViaExecCommand('Create a dashboard');
await v0.submitPrompt();
const response = await v0.waitForResponse();
```

### Key Implementation Details

#### Text Insertion Strategy
1. **Primary Method**: `document.execCommand('insertText', false, text)`
   - Most reliable for ProseMirror
   - Maintains undo/redo stack
   - Triggers proper input events

2. **Alternative Methods**:
   - Input/beforeinput events (less reliable)
   - Direct DOM manipulation (not recommended)

#### Submit Button Detection
**Multi-fallback Approach**:
1. Try complex CSS selector first
2. Fall back to searching all buttons
3. Use XPath as last resort
4. Check for text content matches

#### Response Monitoring
- Poll for new content in response area
- Check for assistant message elements
- Compare content changes over time
- Implement timeout for safety

### Important Considerations

#### Timing and Delays
- **Focus delay**: 100ms after focusing editor
- **Submit delay**: 500ms between text insertion and submit
- **Response polling**: 500ms intervals
- **Response completion**: 2s after last change

#### Error Handling
- Editor not found errors
- Submit button detection failures
- Response timeout handling
- Network error recovery

#### Browser Compatibility
- Requires modern browser with execCommand support
- Works best in Chrome/Edge
- May need adjustments for Firefox/Safari

### Integration with PicoBrain

**Potential Use Cases**:
1. **Code Generation**: Generate components for PicoBrain UI
2. **Documentation**: Auto-generate API documentation
3. **Testing**: Generate test cases for endpoints
4. **Migration Scripts**: Create database migrations
5. **UI Components**: Generate consistent UI components

**Workflow Integration**:
```javascript
// Example: Generate a new component for PicoBrain
const v0 = new V0AppInteraction();
const prompt = `
Create a React component for PicoBrain that:
- Uses our coral color scheme (#e67e5b)
- Follows our DashboardLayout pattern
- Includes TypeScript types
- Uses Tailwind CSS
- Component: PatientAppointmentCard
`;
await v0.sendPrompt(prompt);
```

### Security and Best Practices

#### Rate Limiting
- Implement delays between requests
- Avoid overwhelming the service
- Respect v0.app's terms of service

#### Error Recovery
- Implement retry logic with exponential backoff
- Log all interactions for debugging
- Graceful degradation on failures

#### Content Validation
- Verify generated code before use
- Test in isolated environment first
- Review for security vulnerabilities

### Future Enhancements

**Planned Improvements**:
1. [ ] Add response parsing for code extraction
2. [ ] Implement conversation context management
3. [ ] Add support for file uploads
4. [ ] Create CLI wrapper for automation
5. [ ] Build integration tests

**Research Areas**:
- WebSocket connection for real-time updates
- API endpoint discovery
- Authentication token management
- Session persistence strategies

---

## 🎨 Frontend Development with v0.app (2025-08-30)

### v0.app Integration Results

#### Successfully Completed
1. **Programmatic Connection**: Established browser automation with v0.app
2. **Dashboard Prompt**: Submitted design request with PicoClinics colors
3. **CRUD Templates**: Requested reusable CRUD components
4. **Color Integration**: Applied exact picoclinics.com palette

#### Key Learnings
- **Context Limits**: v0.app has prompt size limitations - use focused prompts
- **Generation Time**: Complex components take 5-10 seconds to generate
- **Editor Type**: ProseMirror requires execCommand for text insertion
- **Best Results**: Provide specific requirements and color values

### Recommended Frontend Stack (Based on v0.app Best Practices)

```yaml
Framework: Next.js 14+ (App Router)
Language: TypeScript 5.x
Styling: Tailwind CSS 3.x
Components: shadcn/ui
State: Zustand or Context API
Data Fetching: TanStack Query v5
Forms: React Hook Form + Zod
Animations: Framer Motion
Icons: Lucide React
Deployment: Vercel
```

### File Structure for Vercel Deployment

```bash
frontend/
├── app/                       # Next.js App Router
│   ├── (auth)/               # Authentication routes group
│   │   ├── login/
│   │   ├── register/
│   │   └── forgot-password/
│   ├── (dashboard)/          # Dashboard routes group
│   │   ├── layout.tsx        # Shared dashboard layout
│   │   ├── page.tsx          # Dashboard home
│   │   ├── patients/
│   │   ├── appointments/
│   │   ├── clinics/
│   │   └── settings/
│   ├── api/                  # API routes (if needed)
│   ├── layout.tsx            # Root layout
│   └── page.tsx              # Landing page
├── components/
│   ├── ui/                   # shadcn/ui components
│   │   ├── button.tsx
│   │   ├── card.tsx
│   │   ├── dialog.tsx
│   │   └── ...
│   ├── dashboard/            # Dashboard components
│   │   ├── stat-card.tsx
│   │   ├── activity-feed.tsx
│   │   └── quick-actions.tsx
│   ├── forms/                # Form components
│   │   ├── patient-form.tsx
│   │   └── appointment-form.tsx
│   └── shared/               # Shared components
│       ├── header.tsx
│       ├── sidebar.tsx
│       └── footer.tsx
├── lib/
│   ├── api/                  # API client functions
│   │   ├── auth.ts
│   │   ├── patients.ts
│   │   └── appointments.ts
│   ├── hooks/                # Custom React hooks
│   │   ├── use-auth.ts
│   │   └── use-patients.ts
│   └── utils/                # Utility functions
│       ├── cn.ts            # Class name utility
│       └── format.ts        # Formatting utilities
├── styles/
│   └── globals.css          # Global styles + Tailwind
├── types/                    # TypeScript types
│   ├── api.ts
│   ├── models.ts
│   └── components.ts
└── public/                   # Static assets
    ├── images/
    └── fonts/
```

### PicoClinics Design System Implementation

#### Tailwind Configuration
```javascript
// tailwind.config.js
module.exports = {
  theme: {
    extend: {
      colors: {
        'pico': {
          coral: {
            DEFAULT: '#e67e5b',
            light: '#f2a085',
            dark: '#d4634a',
            subtle: '#fdf5f2',
          },
          gray: {
            50: '#fafafa',
            100: '#f5f5f5',
            200: '#e5e5e5',
            600: '#525252',
            900: '#171717',
          },
          success: '#10b981',
          warning: '#f59e0b',
          error: '#ef4444',
          info: '#3b82f6',
        }
      }
    }
  }
}
```

#### CSS Variables
```css
/* styles/globals.css */
@layer base {
  :root {
    --pico-coral: 231 126 91;      /* #e67e5b */
    --pico-coral-light: 242 160 133; /* #f2a085 */
    --pico-coral-dark: 212 99 74;   /* #d4634a */
    --pico-coral-subtle: 253 245 242; /* #fdf5f2 */
    
    --background: 0 0% 100%;
    --foreground: 0 0% 9%;          /* #171717 */
    --primary: var(--pico-coral);
    --primary-foreground: 0 0% 100%;
  }
}
```

### Dashboard Components Specification

#### Main Dashboard Requirements
1. **Header**: Logo placeholder + User menu with logout
2. **Sidebar**: Navigation with active state indicators
3. **Metric Cards**: 
   - Patients count
   - Appointments today
   - Monthly revenue
   - Pending tasks
4. **Recent Activity**: Timeline of recent actions
5. **Quick Actions**: Buttons for common tasks

#### CRUD Template Features
1. **List View**:
   - Search bar with debounce
   - Column filters
   - Pagination
   - Bulk actions
   
2. **Create/Edit Modal**:
   - Form validation with Zod
   - Field-level errors
   - Loading states
   - Success feedback
   
3. **Delete Confirmation**:
   - Modal dialog
   - Consequence warning
   - Undo option (soft delete)
   
4. **Notifications**:
   - Toast for success/error
   - Position: top-right
   - Auto-dismiss: 5 seconds

### Vercel Deployment Configuration

#### Environment Variables
```bash
# .env.local
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_APP_NAME=PicoBrain
NEXT_PUBLIC_APP_VERSION=1.0.0

# .env.production
NEXT_PUBLIC_API_URL=https://api.picobrain.com
```

#### vercel.json
```json
{
  "buildCommand": "npm run build",
  "outputDirectory": ".next",
  "devCommand": "npm run dev",
  "installCommand": "npm install",
  "framework": "nextjs",
  "regions": ["iad1"],
  "env": {
    "NEXT_PUBLIC_API_URL": "@picobrain-api-url",
    "NEXT_PUBLIC_APP_NAME": "PicoBrain"
  }
}
```

### API Integration Pattern

#### Axios Configuration
```typescript
// lib/api/client.ts
import axios from 'axios';

const apiClient = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor for auth
apiClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Response interceptor for error handling
apiClient.interceptors.response.use(
  (response) => response,
  async (error) => {
    if (error.response?.status === 401) {
      // Handle token refresh or redirect to login
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

export default apiClient;
```

#### TanStack Query Setup
```typescript
// app/providers.tsx
'use client';

import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { ReactQueryDevtools } from '@tanstack/react-query-devtools';

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 60 * 1000, // 1 minute
      gcTime: 5 * 60 * 1000, // 5 minutes
      retry: 1,
      refetchOnWindowFocus: false,
    },
  },
});

export function Providers({ children }: { children: React.ReactNode }) {
  return (
    <QueryClientProvider client={queryClient}>
      {children}
      <ReactQueryDevtools initialIsOpen={false} />
    </QueryClientProvider>
  );
}
```

### Implementation Priorities

#### Phase 1: Foundation (Days 1-2)
1. ✅ Initialize Next.js with TypeScript
2. ✅ Configure Tailwind with PicoClinics colors
3. ✅ Install and setup shadcn/ui
4. ✅ Create layout components from v0.app
5. ✅ Setup API client with Axios

#### Phase 2: Core Features (Days 3-5)
1. [ ] Implement authentication flow
2. [ ] Build dashboard from v0.app design
3. [ ] Create CRUD templates for main entities
4. [ ] Connect to backend endpoints
5. [ ] Add loading and error states

#### Phase 3: Enhancement (Days 6-7)
1. [ ] Add data visualizations
2. [ ] Implement real-time updates
3. [ ] Optimize for mobile
4. [ ] Add PWA features
5. [ ] Performance optimization

#### Phase 4: Deployment (Day 8)
1. [ ] Configure Vercel project
2. [ ] Setup environment variables
3. [ ] Deploy to preview
4. [ ] Run lighthouse audit
5. [ ] Deploy to production

---

## Database Migration Patterns (Added 2025-08-30)

### SQLAlchemy Model Structure (PicoBrain)
- **Location**: `/backend/app/models/core.py`
- **Pattern**: All models in single file, re-exported via individual files
- **Inheritance**: Composition pattern using foreign keys (not true OOP inheritance)
- **Example**: Person → Employee relationship via person_id FK

### CSV to PostgreSQL Migration Strategy

#### 1. ID Mapping Pattern
```python
# Always create CSV ID → UUID mapping file
id_mapping = {}
for row in csv_data:
    new_id = uuid.uuid4()
    id_mapping[csv_row['id']] = new_id
    
# Save for dependent tables
import json
with open('id_mapping.json', 'w') as f:
    json.dump({k: str(v) for k, v in id_mapping.items()}, f)
```

#### 2. Data Transformation Functions
```python
def parse_address(address_string):
    """Extract city, country_code from full address"""
    parts = address_string.split(',')
    country_mapping = {
        'UK': 'GB', 'USA': 'US', 
        'Italy': 'IT', 'Canada': 'CA'
    }
    # Parse logic here
    return city, country_code

def parse_name(full_name):
    """Split full name into first and last"""
    parts = full_name.split()
    if len(parts) == 2:
        return parts[0], parts[1]
    elif len(parts) > 2:
        # Handle complex names
        return ' '.join(parts[:-1]), parts[-1]
    return full_name, ''
```

#### 3. Date Format Conversion
```python
from datetime import datetime

def convert_date(date_str):
    """Convert DD/MM/YYYY to Date object"""
    if not date_str:
        return None
    return datetime.strptime(date_str, '%d/%m/%Y').date()
```

#### 4. Enum Mapping Pattern
```python
# Create explicit mapping for mismatched enums
role_mapping = {
    'accountant': 'finance',
    'owner': 'admin',
    'staff': 'receptionist',  # or context-dependent
    'doctor': 'doctor'  # direct mapping
}

def map_role(csv_role):
    return role_mapping.get(csv_role.lower(), 'admin')
```

### Migration Script Template
```python
#!/usr/bin/env python3
import csv
import uuid
import sys
from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models.core import Model

# Database setup
DATABASE_URL = "postgresql://edo@localhost/picobraindb"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

def migrate_entity():
    session = SessionLocal()
    try:
        # 1. Clean existing data
        session.query(Model).delete()
        session.commit()
        
        # 2. Read CSV
        with open('data.csv', 'r', encoding='utf-8-sig') as f:
            data = list(csv.DictReader(f))
        
        # 3. Load ID mappings if needed
        with open('id_mapping.json') as f:
            id_mapping = json.load(f)
        
        # 4. Transform and insert
        for row in data:
            # Transform data
            new_record = Model(
                id=uuid.uuid4(),
                # mapped fields
            )
            session.add(new_record)
        
        session.commit()
        print(f"✓ Migrated {len(data)} records")
        
    except Exception as e:
        session.rollback()
        print(f"✗ Migration failed: {e}")
        raise
    finally:
        session.close()

if __name__ == "__main__":
    migrate_entity()
```

### Migration Order Strategy
1. **Respect Dependencies**: Parents before children
   - Clinics (no dependencies)
   - Persons (no dependencies) 
   - Employees (depends on Persons + Clinics)
   - Users (depends on Persons)
   - Clients (depends on Persons + Clinics)

2. **ID Mapping Persistence**: Save between migrations
   ```python
   # After each migration
   with open(f'{entity}_id_mapping.json', 'w') as f:
       json.dump(id_mapping, f)
   ```

3. **Validation After Migration**:
   ```python
   # Verify counts
   assert session.query(Model).count() == len(csv_data)
   # Verify relationships
   for record in session.query(Model).all():
       assert record.foreign_key_id is not None
   ```

### Common Migration Challenges & Solutions

| Challenge | Solution |
|-----------|----------|
| Missing fields in DB | Accept data loss or extend schema |
| Enum mismatches | Create mapping dictionary |
| Complex names | Smart parsing with fallbacks |
| Date formats | Use strptime with format string |
| Foreign key dependencies | Migrate in dependency order |
| NULL handling | Use `.get()` with defaults |
| Encoding issues | Use `encoding='utf-8-sig'` |
| Duplicate detection | Check unique constraints first |

### Database Access Pattern
```python
# Standard connection
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql://edo@localhost/picobraindb"
engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(bind=engine)

# Context manager pattern
from contextlib import contextmanager

@contextmanager
def get_db():
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except:
        db.rollback()
        raise
    finally:
        db.close()

# Usage
with get_db() as db:
    clinics = db.query(Clinic).all()
```

### Entity Relationship in PicoBrain
```
Person (Base Entity - 14 fields)
├── Employee (via person_id FK - 17 fields)
│   ├── role='doctor' → Doctor behavior
│   ├── role='nurse' → Nurse behavior  
│   ├── role='manager' → Manager behavior
│   └── role='finance' → Finance behavior
│   └── Links to:
│       ├── Clinic (via primary_clinic_id)
│       └── Currency (via salary_currency)
├── Client (via person_id FK)
│   └── Links to: Clinic (via preferred_clinic_id)
└── User (via person_id FK for authentication)

Clinic (Independent Entity - 17 fields)
├── employees (relationship)
├── clients (preferred_clinic relationship)
└── temp_id (migration helper)

Currencies (Reference Table - discovered via FK)
└── currency_code (referenced by employees.salary_currency)
```

### Migration Artifacts Created
- `/backend/migrate_clinics.py` - Initial clinic migration
- `/backend/remigrate_clinics_full.py` - Full address data migration
- `/backend/add_temp_id_column.py` - Schema modification script
- `/backend/clinic_id_mapping.json` - CSV ID to UUID mappings
- `/backend/verify_clinic_migration.py` - Data verification script
- `/backend/show_persons_employees_schema.py` - Schema inspection script
- `/backend/export_persons_employees_schema.py` - Schema export to JSON
- Pattern: Create similar scripts for Staff and Doctors

### Database Schema Updates (2025-08-30)

#### Persons Table - Complete Schema (14 fields)
```python
class Person(Base):
    __tablename__ = "persons"
    
    # Primary fields
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    middle_name = Column(String(100))
    
    # Contact fields
    email = Column(String(255), unique=True)
    phone_mobile = Column(String(50))
    phone_home = Column(String(50))
    
    # Personal details
    dob = Column(Date)
    gender = Column(ENUM('M', 'F', 'O', 'N', name='gender_type'))
    nationality = Column(String(2))  # Country code
    
    # Identification
    id_type = Column(String(20))  # passport, national ID, etc.
    id_number = Column(Text)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
```

#### Employees Table - Complete Schema (17 fields)
```python
class Employee(Base):
    __tablename__ = "employees"
    
    # Primary fields
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    person_id = Column(UUID(as_uuid=True), ForeignKey("persons.id"), nullable=False)
    employee_code = Column(String(20), unique=True)
    primary_clinic_id = Column(UUID(as_uuid=True), ForeignKey("clinics.id"), nullable=False)
    
    # Role and specialization
    role = Column(ENUM('doctor', 'nurse', 'receptionist', 'manager', 'finance', 'admin'))
    specialization = Column(String(100))
    
    # Professional licensing
    license_number = Column(String(50))
    license_expiry = Column(Date)
    
    # Employment dates
    hire_date = Column(Date, nullable=False)
    termination_date = Column(Date)
    
    # Compensation
    base_salary_minor = Column(BigInteger)  # Store in cents/pence
    salary_currency = Column(CHAR(3), ForeignKey("currencies.currency_code"))
    commission_rate = Column(Numeric)  # Decimal percentage
    
    # Status flags
    is_active = Column(Boolean, default=True)
    can_perform_treatments = Column(Boolean, default=False)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
```

#### Clinics Table - Complete Schema (17 fields)

```python
# Updated Clinic model with all database fields
class Clinic(Base):
    __tablename__ = "clinics"
    
    # Primary fields
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    code = Column(String(10), nullable=False, unique=True)
    name = Column(String(100), nullable=False)
    functional_currency = Column(CHAR(3))
    
    # Address fields (NEW)
    address_line_1 = Column(String(255))
    address_line_2 = Column(String(255))
    city = Column(String(100))
    state_province = Column(String(100))  # NEW
    postal_code = Column(String(20))      # NEW
    country_code = Column(CHAR(2))
    
    # Contact fields (NEW)
    phone = Column(String(50))
    email = Column(String(255))
    
    # Business fields (NEW)
    tax_id = Column(String(50))
    is_active = Column(Boolean, default=True)
    
    # Timestamps (NEW)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Migration helper (TEMPORARY)
    temp_id = Column(Integer)  # For CSV ID mapping during migration
```

### Two-Phase Migration Pattern

#### Phase 1: Basic Migration
- Create records with essential fields only
- Generate UUID mappings
- Handle data that exists in model

#### Phase 2: Full Data Migration
1. **Add missing columns to database** (if needed)
2. **Update SQLAlchemy models** to match database
3. **Re-migrate with UPDATE** (not DELETE/INSERT):
   ```python
   # Find existing record
   clinic = session.query(Clinic).filter_by(code=code).first()
   
   # Update all fields
   clinic.address_line_1 = row['address_line_1']
   clinic.address_line_2 = row['address_line_2']
   # ... update other fields
   
   # Preserve relationships
   clinic.updated_at = datetime.utcnow()
   ```

### Financial Data Storage Pattern

#### Salary Storage Best Practice
- Store salaries in **minor units** (cents/pence) using BigInteger
- Avoids floating-point precision issues
- Example: $5,000.00 stored as 500000 cents
- Formula: `display_amount = base_salary_minor / 100`

#### Currency Management
- Separate `currencies` table exists (discovered via FK)
- Each employee's salary has associated currency
- Clinics have functional_currency for operations
- Enables multi-currency support

#### Commission Storage
- Use Numeric type for precise decimal percentages
- Example: 15.5% stored as 0.155 or 15.5
- Calculation: `commission = (sale_amount * commission_rate)`

### Migration Best Practices Learned

1. **Always Check Database Schema First**
   - Database may have more fields than SQLAlchemy models
   - Use information_schema to discover all columns
   - Update models before migration

2. **Use temp_id for Mapping**
   - Add INTEGER temp_id column for CSV ID tracking
   - Preserves original ID relationships
   - Can be removed after all migrations complete

3. **Update vs Recreate**
   - UPDATE existing records to preserve UUIDs
   - Maintains foreign key relationships
   - Prevents orphaned records

4. **Data Quality Improvements**
   - Clean data during migration (fix typos, format issues)
   - Separate composite fields (address, name)
   - Convert data types (string to boolean)

5. **Verification Scripts**
   - Always create verification script
   - Check data completeness
   - Validate transformations

---

## Weekly Review: 2025-W35
- Commits: 3
- Files Changed: 19
- Top patterns: v0.app integration, Frontend architecture
- Key Achievement: Programmatic v0.app interaction established
---

)
- Created utility schemas: `PhoneNumber`, `PhoneNumberUpdate`
- Added all missing database fields to schemas (timestamps, addresses, etc.)

**API Endpoint Enhancements**:
- **Validation Rule**: Phone parts must be provided as pairs or both null
- **New Endpoints**:
  - `POST /api/v1/persons/validate-phone` - Phone validation
  - `GET /api/v1/persons/{id}/formatted-phones` - Formatted display
  - `GET /api/v1/clinics/{id}/formatted-address` - Full address
  - `GET /api/v1/clinics/{id}/contact-info` - Structured contact data

### Lessons Learned

#### 1. Database Schema Evolution Pattern
**Best Practice**: Always check actual database schema before updating models
```python
# Use information_schema to discover columns
SELECT column_name, data_type, character_maximum_length
FROM information_schema.columns
WHERE table_name = 'table_name';
```

#### 2. Phone Number Storage Strategy
**Recommendation**: Split country code and number for:
- Better UX (country dropdown with flags)
- Easier validation (country-specific rules)
- E.164 compliance
- Analytics capabilities (group by country)

**Implementation**:
```python
phone_country_code = Column(String(6))   # '+1' to '+99999'
phone_number = Column(String(20))        # National portion
```

#### 3. API Validation Pattern
**Key Insight**: Validate phone field pairs at API layer
```python
if (phone_country_code and not phone_number) or \
   (phone_number and not phone_country_code):
    raise HTTPException(400, "Both parts required")
```

#### 4. Migration Helper Fields
**Pattern**: Use `temp_id` INTEGER for CSV→UUID mapping during migrations
- Add to all tables needing migration
- Preserve original relationships
- Remove after migration complete

#### 5. Comprehensive Schema Updates
**Lesson**: When updating schemas, include ALL database fields:
- Timestamps (created_at, updated_at)
- Business fields (tax_id, specialization)
- Migration helpers (temp_id)
- Prevents future inconsistencies

#### 6. Utility Endpoints Value
**Pattern**: Add helper endpoints for common operations:
- Formatted display (phones, addresses)
- Validation helpers
- Reduces frontend complexity

### Files Created/Modified
1. `/backend/phone_splitting_migration.py` - Database migration script
2. `/backend/app/models/core.py` - Updated SQLAlchemy models
3. `/backend/app/schemas/core.py` - Complete schema rewrite
4. `/backend/app/api/v1/endpoints/persons.py` - Phone validation logic
5. `/backend/app/api/v1/endpoints/clinics.py` - Contact utilities
6. `/backend/phone_number_api_update_summary.md` - Documentation

### Technical Decisions Made

| Decision | Rationale | Outcome |
|----------|-----------|----------|
| Split phone fields | Better UX, validation, international support | ✅ Implemented |
| VARCHAR(6) for country codes | Supports all ITU codes (+1 to +99999) | ✅ Flexible |
| VARCHAR(20) for numbers | Accommodates all national formats | ✅ Future-proof |
| Pair validation at API | Ensures data consistency | ✅ Prevents errors |
| Utility endpoints | Simplifies frontend development | ✅ Better DX |
| temp_id for migration | Preserves relationships during migration | ✅ Safe migration |

### Command Patterns Discovered

```bash
# Direct database access for schema inspection
cd /Users/edo/PyProjects/picobrain/backend
python3 << EOF
from sqlalchemy import create_engine, text
engine = create_engine("postgresql://edo@localhost/picobraindb")
with engine.connect() as conn:
    result = conn.execute(text("""SELECT * FROM information_schema.columns WHERE table_name = 'persons'"""))
    for row in result:
        print(row)
EOF

# Terminal automation for script execution
Control your Mac:osascript
tell application "Terminal"
    do script "cd /path && python script.py"
end tell
```

### Error Prevention Patterns

1. **Always validate field pairs**: Don't allow partial phone numbers
2. **Check existing records**: Prevent duplicate emails/codes
3. **Verify foreign keys**: Ensure referenced records exist
4. **Use transactions**: Rollback on any error
5. **Provide clear error messages**: Help developers understand issues

### Migration Workflow Template

```python
# Standard migration pattern for PicoBrain
1. Create migration script
2. Test on single record
3. Add validation checks
4. Run full migration in transaction
5. Verify with separate script
6. Update models and schemas
7. Update API endpoints
8. Test API with new structure
9. Document changes
```

---
