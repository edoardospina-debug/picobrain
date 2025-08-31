# PicoBrain Development Guide - Key Learnings & Solutions

## Project Overview
- **Location**: `/Users/edo/PyProjects/picobrain/`
- **Tech Stack**: 
  - Backend: FastAPI (Python) on port 8000
  - Frontend: Next.js 14 with TypeScript, Ant Design on port 3000
  - Database: PostgreSQL
- **Authentication**: JWT-based with admin/admin123 credentials

## Critical Server Startup Procedure

### ✅ ALWAYS Use the Unified Startup Script
```bash
cd /Users/edo/PyProjects/picobrain
./start-servers.sh
```
This script handles:
- PostgreSQL verification
- Backend API startup with dependencies
- Frontend startup with npm install
- Proper sequencing and health checks
- Clear status messages

### ⚠️ DO NOT start servers individually - causes issues with:
- Missing dependencies
- Authentication failures  
- Improper initialization order

## Frontend Issues & Solutions

### 1. React Server Components Error with Ant Design
**Problem**: "Could not find module in React Client Manifest" error
**Solution**: Separate server and client components properly
- Create `client-layout.tsx` marked with `'use client'`
- Keep `layout.tsx` as server component that imports client layout
- Never mix Ant Design imports in server components

### 2. TypeScript Compilation Errors
**Problem**: Interface syntax errors with `extends ColumnsType<T>[0]`
**Solution**: Use composition instead of extension:
```typescript
export interface DataTableColumn<T> {
  searchable?: boolean;
  exportable?: boolean;
  [key: string]: any; // Allow any column properties
}
```

### 3. Next.js Build Cache Issues
**Solution**: Clear and rebuild when encountering persistent errors:
```bash
cd frontend
rm -rf .next
npm run dev
```

## Chrome Automation Best Practices

### Page Content Detection
```javascript
// Wait for React/Next.js apps to fully render
setTimeout(() => {
  const pageInfo = {
    hasContent: document.body && document.body.innerText.length > 0,
    hasAntComponents: !!document.querySelector('[class*="ant-"]'),
    isReady: document.readyState === 'complete',
    // Check specific elements for your app
    hasLoginForm: !!document.querySelector('form[name="login"]'),
    hasTable: !!document.querySelector('.ant-table')
  };
  console.log(JSON.stringify(pageInfo, null, 2));
}, 3000); // Give React time to render
```

### Navigation Flow
1. **ALWAYS check if authentication is required first**
   - App redirects to `/clinics` when authenticated
   - Redirects to `/login` when not authenticated
2. **Use proper URL navigation**:
   - Root: `http://localhost:3000` → redirects based on auth
   - Login: `http://localhost:3000/login`
   - Main app: `http://localhost:3000/clinics`

## Authentication Requirements

### Login Flow
1. Frontend requires authentication for all dashboard routes
2. Use credentials: `admin` / `admin123`
3. JWT token stored in localStorage
4. Auto-refresh mechanism in place

### Permission Matrix
- Located at: `/Users/edo/PyProjects/picobrain/permission-matrix.md`
- Roles: admin, manager, staff, medical, finance, readonly
- Permissions use symbols: ✅ (yes), ❌ (no), 👁️ (view only), 🔒 (own records only)

## Project File Structure

### Key Configuration Files
- `.env.local` - Frontend environment variables
- `permission-matrix.md` - Role-based permissions
- `start-servers.sh` - Unified startup script
- `frontend/src/app/client-layout.tsx` - Client-side Ant Design config
- `frontend/src/lib/auth/AuthProvider.tsx` - Authentication context

### Component Organization
```
frontend/src/
├── app/
│   ├── (auth)/         # Public routes
│   │   └── login/
│   ├── (dashboard)/     # Protected routes
│   │   ├── clinics/
│   │   │   ├── page.tsx
│   │   │   ├── new/
│   │   │   └── [id]/
│   │   ├── staff/
│   │   │   ├── doctors/
│   │   │   │   ├── page.tsx      # List all doctors
│   │   │   │   ├── new/          # Create doctor form
│   │   │   │   └── [id]/         # Edit/view doctor
│   │   │   └── employees/
│   │   │       ├── page.tsx      # List all employees
│   │   │       ├── new/          # Create employee form
│   │   │       └── [id]/         # Edit/view employee
│   │   └── layout.tsx   # Dashboard layout
│   ├── layout.tsx       # Root layout (server)
│   └── client-layout.tsx # Client layout with Ant Design
├── components/
│   └── shared/
│       └── DataTable/   # Reusable table component
├── lib/
│   ├── api/
│   │   ├── client.ts
│   │   └── endpoints/
│   │       ├── clinics.ts
│   │       ├── employees.ts  # Handles doctors too
│   │       └── persons.ts
│   └── auth/           # Auth provider
└── types/
    └── index.ts        # All TypeScript interfaces
```

## Common Pitfalls to Avoid

1. **Don't use Ant Design imports in server components**
2. **Don't start servers without checking PostgreSQL first**
3. **Don't navigate to protected routes without authentication**
4. **Don't use complex TypeScript extends with Ant Design types**
5. **Don't expect immediate page rendering - React needs time**
6. **Don't forget to check both backend (port 8000) and frontend (port 3000)**

## Quick Debugging Commands

### Check Server Status
```bash
# Backend API docs
curl http://localhost:8000/docs

# Frontend
curl http://localhost:3000

# PostgreSQL
pg_isready -h localhost -p 5432
```

### Terminal Commands for Mac
```applescript
# Start servers
tell application "Terminal"
    do script "cd /Users/edo/PyProjects/picobrain && ./start-servers.sh"
end tell
```

### Chrome DevTools Checks
```javascript
// Quick diagnostic
{
  backend: await fetch('http://localhost:8000/health').then(r => r.ok).catch(() => false),
  frontend: window.location.hostname === 'localhost' && window.location.port === '3000',
  authenticated: !!localStorage.getItem('access_token'),
  antDesignLoaded: !!document.querySelector('.ant-layout')
}
```

## Complex Nested Forms Implementation

### Critical: Employee/Doctor Creation Pattern
**Challenge**: Creating employees requires simultaneous Person + Employee records
**Solution**: Use composite DTOs with transaction safety

#### The EmployeeCreateDTO Structure
```typescript
interface EmployeeCreateDTO {
  // Person fields (created first)
  first_name: string;
  last_name: string;
  middle_name?: string;
  email?: string;
  phone_mobile_country_code?: string;
  phone_mobile_number?: string;
  dob?: string;
  gender?: 'M' | 'F' | 'O' | 'N';
  nationality?: string;
  id_type?: string;
  id_number?: string;
  
  // Employee fields (linked to Person)
  employee_code?: string;
  primary_clinic_id: string;
  role: EmployeeRole; // doctor, nurse, receptionist, etc.
  specialization?: string;
  license_number?: string;
  license_expiry?: string;
  hire_date: string;
  base_salary_minor?: number; // Store in cents
  salary_currency?: string;
  commission_rate?: number;
  is_active?: boolean;
  can_perform_treatments?: boolean;
}
```

#### API Endpoint: POST /api/v1/employees/
- Creates BOTH Person and Employee in single transaction
- Rollback if either fails
- Returns both created entities
- Handles duplicate person detection by email

#### Frontend Implementation Pattern
1. Single form collects all data (Person + Employee)
2. Transform on submit (salary to cents, dates to YYYY-MM-DD)
3. Send as single DTO to backend
4. Backend service manages transaction
5. Handle errors at both entity levels

## Session Accomplishments
✅ Fixed React Server Components issue with Ant Design
✅ Resolved TypeScript compilation errors in DataTable
✅ Successfully started both backend and frontend servers
✅ Verified authentication flow
✅ Loaded Clinics management page
✅ Confirmed permission matrix implementation
✅ Established Chrome automation patterns for Next.js/React apps
✅ **Implemented Doctors page with complex nested forms**
✅ **Created modular API client for employees/doctors**
✅ **Established pattern for Person+Employee composite creation**

## Staff Module Implementation Status

### Completed
- ✅ `/staff/doctors` - List page with DataTable
- ✅ `/staff/doctors/new` - Create form with Person+Employee
- ✅ Type definitions for Employee, Doctor, DTOs
- ✅ API client with composite creation support

### In Progress
- 🔄 `/staff/employees` - All employees page
- 🔄 `/staff/employees/new` - Create any employee type

### Next Steps Ready
- Employee edit pages (update only Employee, not Person)
- Person management (separate CRUD for Person records)
- Clients module with medical records
- Role-based filtering and permissions
- Bulk operations and imports

---
*Generated from development session on 2024-12-30*
*This guide ensures smooth continuation without repeating solved issues*