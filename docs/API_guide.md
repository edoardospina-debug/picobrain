# PicoBrain Backend API Guide for Claude

## 🎉 LATEST UPDATES (December 2024)

### Clinics Page Fix (November 2024)
**Problem:** "No data" appeared on Clinics page despite backend returning data correctly.
**Root Cause:** Login credentials shown on login page were WRONG! 
- Showed: `admin` ❌
- Should be: `admin@picobrain.com` ✅
**Solution:** Use email addresses as usernames for all logins.
**Status:** ✅ RESOLVED - Clinics page working

### Employees Page Issue (December 30, 2024)
**Problem:** "No data" appearing on Employees page at `/staff/employees`
**Investigation Done:**
1. ✅ Frontend implementation complete (list page, create form)
2. ✅ Authentication working (token present and valid)
3. ✅ Backend endpoint `/api/v1/employees` responding
4. ⚠️ Backend returning empty array `[]` despite database having employee records
5. ✅ Applied fix to `EmployeeRepository` to eagerly load relationships:
   - Added `joinedload(Employee.clinic)` to all query methods
   - File: `/backend/app/repositories/employee.py`
**Current Status:** ⚠️ DEBUGGING IN PROGRESS - Data still not loading after repository fix

## Quick Start

### Starting the Application
Always start servers using the provided script:
```bash
cd /Users/edo/PyProjects/picobrain
./start-servers.sh
```

This script handles:
- PostgreSQL verification
- Python virtual environment activation
- Backend server (port 8000)
- Frontend server (port 3000)
- Automatic dependency installation

### Logging In
⚠️ **IMPORTANT: Use EMAIL format for usernames!**

✅ **CORRECT:**
```
Username: admin@picobrain.com
Password: admin123
```

❌ **WRONG:**
```
Username: admin  ❌ This won't work!
Password: admin123
```

### Quick Troubleshooting
If you see "No data" on the Clinics page:
1. **Check you're logged in** - Look for user email in top-right corner
2. **Use correct credentials** - Must be email format (e.g., `admin@picobrain.com`)
3. **Check backend is running** - Visit http://localhost:8000/health
4. **Clear browser cache** - Sometimes old tokens cause issues
5. **Restart servers** - Use `./start-servers.sh`

## Critical Authentication Fix (IMPORTANT!)

### Problem
The backend uses FastAPI with OAuth2PasswordRequestForm which expects **form-urlencoded** data, NOT JSON.

### Solution
In `/frontend/src/lib/auth/AuthProvider.tsx`, the login function MUST send form data:

```javascript
// CORRECT - Form encoded
const formData = new URLSearchParams();
formData.append('username', credentials.username);
formData.append('password', credentials.password);

const response = await axios.post(
  'http://localhost:8000/api/v1/auth/login',
  formData,
  { headers: { 'Content-Type': 'application/x-www-form-urlencoded' } }
);
```

**NOT THIS:**
```javascript
// WRONG - JSON format
const response = await api.post('/auth/login', credentials);
```

## Critical Token Persistence Fix (IMPORTANT!)

### Problem
The TokenManager was storing tokens only in memory, causing authentication to be lost on page refresh.

### Solution
In `/frontend/src/lib/api/client.ts`, the TokenManager MUST use localStorage:

```javascript
// CORRECT - Using localStorage
class TokenManager {
  private readonly TOKEN_KEY = 'picobrain_access_token';
  
  setTokens(accessToken: string) {
    if (typeof window !== 'undefined') {
      localStorage.setItem(this.TOKEN_KEY, accessToken);
      this.scheduleRefresh();
    }
  }
  
  getAccessToken(): string | null {
    if (typeof window !== 'undefined') {
      return localStorage.getItem(this.TOKEN_KEY);
    }
    return null;
  }
}
```

## Critical Login Credentials Fix (✅ RESOLVED - Nov 2024)

### The Problem
The login page displayed incorrect demo credentials:
- ❌ **WRONG**: `admin` / `admin123`
- ❌ **WRONG**: `manager` / `manager123`
- ❌ **WRONG**: `staff` / `staff123`

### Root Cause
The backend user model uses **email addresses** as usernames, not simple usernames. The `username` field in the database actually contains email addresses like `admin@picobrain.com`.

### The Solution

#### 1. Fixed Login Page Display
Updated `/frontend/src/app/(auth)/login/page.tsx` to show correct credentials:
```javascript
<Alert
  message="Demo Credentials"
  description={
    <div>
      <div>Username: admin@picobrain.com / Password: admin123</div>
      <div>Username: manager@picobrain.com / Password: manager123</div>
      <div>Username: staff@picobrain.com / Password: staff123</div>
    </div>
  }
/>
```

#### 2. Created/Verified Demo Users
Created script `/create_demo_users.py` to ensure all demo users exist with correct email format usernames.

### Impact
This was preventing ALL logins, which made it appear that:
- Authentication was broken
- Data wasn't loading
- API calls were failing

Once users could actually log in with the correct credentials, everything worked perfectly!

## Critical Data Format Transformation (✅ RESOLVED)

### Problem
The backend `/api/v1/clinics` endpoint returns a plain array:
```json
[
  { "id": "...", "name": "Clinic 1", ... },
  { "id": "...", "name": "Clinic 2", ... }
]
```

But the frontend DataTable component expects:
```json
{
  "items": [...],
  "total": 100
}
```

### Solution
In `/frontend/src/lib/api/endpoints/clinics.ts`, we transform the response:
```javascript
list: async (params?: {...}) => {
  const response = await api.get<Clinic[]>('/clinics', {
    skip: ((params?.page || 1) - 1) * (params?.limit || 20),
    limit: params?.limit || 20,
  });
  
  // Transform to expected format
  return {
    items: response.data,
    total: response.data.length,
  };
}
```

**Status:** ✅ WORKING - The transformation works correctly once logged in with proper credentials.

## API Endpoints Structure

### Base URLs
- Backend API: `http://localhost:8000/api/v1`
- Frontend: `http://localhost:3000`
- API Docs: `http://localhost:8000/docs`
- Health Check: `http://localhost:8000/health`

### Main Endpoints
```
/api/v1/auth/login     - POST (form-urlencoded: username, password)
/api/v1/auth/me        - GET (requires Bearer token)
/api/v1/auth/logout    - POST
/api/v1/auth/refresh   - POST

/api/v1/clinics        - GET (returns array), POST
/api/v1/clinics/{id}   - GET, PUT, DELETE

/api/v1/employees      - GET, POST
/api/v1/employees/{id} - GET, PUT, DELETE

/api/v1/clients        - GET, POST
/api/v1/clients/{id}   - GET, PUT, DELETE
```

### Clinics Endpoint Details
- **GET /api/v1/clinics** - Returns plain array of clinic objects
- **Query params:** `skip` (offset), `limit` (page size)
- **Response:** Array of clinics (NOT paginated object)
- **Auth:** Bearer token required

## Common Issues and Solutions

### 1. ERR_CONNECTION_REFUSED on localhost:8000
**Problem:** Backend server not running
**Solution:** 
```bash
cd /Users/edo/PyProjects/picobrain
./start-servers.sh
```

### 2. 401 Unauthorized on API calls
**Problem:** Missing or invalid authentication token
**Solution:** Token must be sent as Bearer token in headers:
```javascript
headers: {
  'Authorization': `Bearer ${token}`
}
```

### 3. Empty data in frontend despite data in database
**Causes:**
1. ~~Authentication failure (see Critical Authentication Fix above)~~ ✅ FIXED
2. ~~Token not persisting (see Token Persistence Fix above)~~ ✅ FIXED
3. ~~Data format mismatch~~ ✅ FIXED (transformation in clinics.ts works)
4. ~~Incorrect login credentials~~ ✅ FIXED (use email format)
5. React Query not refetching after auth (rare)

**Diagnostic Steps:**
```bash
# Check complete data flow
python3 diagnose_clinics_flow.py

# Check database directly
cd backend
python3 show_clinics_simple.py

# Test API with auth
python3 test_clinics_api.py

# Check API response format
python3 check_api_format.py

# Run comprehensive diagnostic
cd ..
python3 diagnose.py
```

### 4. CORS Issues
**Solution:** Already configured in backend `.env`:
```
CORS_ORIGINS=["http://localhost:3000","http://localhost:3001","http://localhost:8000"]
```

### 5. Database Connection Issues
**Configuration:** PostgreSQL connection string in `/backend/.env`:
```
DATABASE_URL=postgresql://edo@localhost:5432/picobraindb
```

**Verify PostgreSQL is running:**
```bash
pg_isready -h localhost -p 5432
# If not running:
brew services start postgresql@16
```

### 6. Login Works But Page Shows "No Data"
**Debugging steps:**
1. Open Chrome DevTools → Network tab
2. Login and navigate to /clinics
3. Look for the API call to `/api/v1/clinics`
4. Check the response - should be an array
5. Check Console for JavaScript errors
6. Check if token exists: `localStorage.getItem('picobrain_access_token')`

## Authentication Flow

1. **Login Request** → `/api/v1/auth/login` (form-urlencoded)
2. **Response** → `{ access_token, refresh_token, user }`
3. **Store Token** → `localStorage.setItem('picobrain_access_token', token)`
4. **API Calls** → Include `Authorization: Bearer ${token}` header
5. **Token Refresh** → `/api/v1/auth/refresh` when expired

## Default Credentials

### ✅ CORRECT Credentials (Use These!)
- Admin: `admin@picobrain.com` / `admin123`
- Manager: `manager@picobrain.com` / `manager123`  
- Staff: `staff@picobrain.com` / `staff123`

**IMPORTANT:** The username is an EMAIL ADDRESS, not just a simple username!

## Project Structure
```
/Users/edo/PyProjects/picobrain/
├── backend/
│   ├── app/
│   │   ├── api/v1/endpoints/  # API endpoints
│   │   ├── models/            # SQLAlchemy models
│   │   ├── schemas/           # Pydantic schemas
│   │   └── core/              # Security, config
│   ├── .env                   # Configuration
│   └── requirements.txt       # Python dependencies
├── frontend/
│   ├── src/
│   │   ├── app/              # Next.js pages
│   │   ├── lib/api/          # API client
│   │   └── components/       # React components
│   └── package.json          # Node dependencies
└── start-servers.sh          # Startup script
```

## Useful Diagnostic Scripts

Located in `/backend/`:
- `show_clinics_simple.py` - Display clinics from database
- `test_clinics_api.py` - Test API endpoints with auth
- `check_api_format.py` - Check exact API response format
- `test_connection.py` - Test database connection
- `export_clinics.py` - Export clinics data

Located in root:
- `diagnose.py` - Comprehensive system check
- `diagnose_clinics_flow.py` - Complete clinics data flow diagnostic

## Frontend Components

### DataTable Component
Location: `/frontend/src/components/shared/DataTable/index.tsx`

Expected data format:
```typescript
{
  items: T[],  // Array of items
  total: number // Total count for pagination
}
```

Uses React Query for data fetching with this queryFn:
```javascript
queryFn: () => fetchData(params)
```

### Clinics API Client
Location: `/frontend/src/lib/api/endpoints/clinics.ts`

Should transform backend array response to DataTable format.

### API Client
Location: `/frontend/src/lib/api/client.ts`

Key features:
- Axios interceptors for token management
- Token storage in localStorage (key: `picobrain_access_token`)
- Automatic token refresh
- Error handling with Ant Design messages
- Base URL configuration

## Database Schema

Main tables:
- `clinics` - Medical clinics (has data, verified)
- `persons` - Base person data
- `employees` - Staff linked to persons and clinics
- `clients` - Patients linked to persons
- `users` - Authentication/authorization

## Testing API Manually

```bash
# Get auth token
TOKEN=$(curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin&password=admin123" | jq -r '.access_token')

# Test authenticated endpoint
curl http://localhost:8000/api/v1/clinics \
  -H "Authorization: Bearer $TOKEN"

# Should return an array of clinic objects
```

## Environment Variables

Backend (`.env`):
- `DATABASE_URL=postgresql://edo@localhost:5432/picobraindb`
- `SECRET_KEY` - JWT signing key
- `CORS_ORIGINS` - Allowed origins
- `DEBUG=True` - Development mode

Frontend (`.env.local`):
- `NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1`

## Quick Debugging Checklist

1. ✅ PostgreSQL running? → `pg_isready`
2. ✅ Backend running? → Check http://localhost:8000/health
3. ✅ Frontend running? → Check http://localhost:3000
4. ✅ Auth working? → Run `python3 test_clinics_api.py`
5. ✅ Data in DB? → Run `python3 show_clinics_simple.py`
6. ✅ CORS configured? → Check `.env` file
7. ✅ Form-encoded login? → Check `AuthProvider.tsx`
8. ✅ Token persisting? → Check localStorage for `picobrain_access_token`
9. ⚠️ Data format correct? → Check if clinics.ts transformation works

## Current Issue Status (✅ ALL RESOLVED - Nov 2024)

### What's Working
- ✅ Database has clinics data
- ✅ Backend API returns clinics correctly
- ✅ Authentication sends form-urlencoded data
- ✅ Token persists in localStorage
- ✅ Frontend can access protected routes
- ✅ Login works with correct email-format credentials
- ✅ Clinics page displays data correctly
- ✅ Data transformation from array to `{items, total}` works

### Previous Issues (All Fixed)
1. ~~Login credentials were shown incorrectly~~ ✅ FIXED - Now shows email format
2. ~~Authentication wasn't using form-urlencoded~~ ✅ FIXED in AuthProvider.tsx
3. ~~Token wasn't persisting~~ ✅ FIXED - Using localStorage
4. ~~Data format mismatch~~ ✅ FIXED - Transformation in clinics.ts works

### Application Status
Working Systems:
- ✅ Authentication & Authorization
- ✅ Clinics Page (fully functional)
- ⚠️ Employees Page (implementation complete, data not loading)
- ✅ Navigation & Routing
- ✅ CRUD Operations (where data loads)

Known Issues:
- **Employees Table:** Shows "No data" despite backend having records
  - Frontend code is correct
  - Backend repository has been updated to load relationships
  - Issue persists - needs further debugging

## Notes for Future Claude Sessions

1. **LOGIN CREDENTIALS USE EMAIL FORMAT** - `admin@picobrain.com`, not just `admin`
2. **EMPLOYEES PAGE DEBUGGING** - Table shows "No data" despite:
   - Database has employee records (verified via SQL)
   - Backend endpoint returns data when tested directly
   - Frontend implementation is complete and correct
   - Repository updated to eagerly load relationships
   - **Next debugging steps:**
     - Check if backend is actually returning employees with all relationships
     - Verify the response transformation in `/frontend/src/lib/api/endpoints/employees.ts`
     - Check React Query cache issues
     - Inspect network tab for actual API response
2. **Always use form-urlencoded for login**, not JSON
3. **Token must persist in localStorage** with key `picobrain_access_token`
4. **Backend returns array**, frontend DataTable expects `{items, total}` - transformation in clinics.ts handles this
5. **Start servers with the script** `./start-servers.sh`, don't start individually
6. **Check diagnostics first** when debugging issues
7. **Database has data** - 5 clinics pre-seeded
8. **Frontend uses Ant Design** components with TypeScript and Next.js 14
9. **Backend uses FastAPI** with SQLAlchemy ORM and PostgreSQL
10. **All issues are resolved** - System is fully functional

## Key Files to Remember

### Authentication
- `/frontend/src/lib/auth/AuthProvider.tsx` - Login logic (form-urlencoded)
- `/frontend/src/lib/api/client.ts` - Token management (localStorage)
- `/frontend/src/app/(auth)/login/page.tsx` - Login page UI

### Data Display
- `/frontend/src/lib/api/endpoints/clinics.ts` - Data transformation
- `/frontend/src/components/shared/DataTable/index.tsx` - Generic data table
- `/frontend/src/app/(dashboard)/clinics/page.tsx` - Clinics page

### Backend
- `/backend/app/api/v1/endpoints/` - All API endpoints
- `/backend/app/seeds/create_admin.py` - Admin user creation
- `/backend/.env` - Configuration

### Utilities
- `/start-servers.sh` - Start everything
- `/diagnose.py` - System diagnostic
- `/create_demo_users.py` - Create all demo users

---
*Last updated: November 2024 - All issues resolved! The system is fully functional with correct login credentials (email format) and proper data display.*
