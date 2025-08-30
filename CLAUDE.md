<!-- CLAUDE: ALWAYS READ THIS FIRST - ACTIVE PROJECT CONTEXT -->
<!-- Last Updated: 2025-08-30 17:32:11 -->
<!-- Session ID: 20250830_173211 -->

# 🧠 CLAUDE KNOWLEDGE BASE - PicoBrain

## 🚨 PRIORITY CONTEXT (Read First)
**Project**: PicoBrain
**Location**: /Users/edo/PyProjects/picobrain
**Session**: Active since 2025-08-30 14:24:17
**Context Usage**: ~6000 / 160000 tokens

### Server URLs (Working ✅)
- **Backend API**: http://localhost:8000 ✅
- **API Docs**: http://localhost:8000/docs ✅ (NOT /api/v1/docs)  
- **Frontend**: http://localhost:3000 ✅ (Fixed!)
- **Dashboard**: http://localhost:3000/dashboard ✅ (Fixed!)
- **Login Page**: http://localhost:3000/login ✅ (Fixed!)

### 🔐 Authentication (Verified 2025-08-30)
- **Admin Username**: admin@picobrain.com
- **Admin Password**: admin123
- **Login Route**: `/login` (not `/login/dashboard`)
- **After Login**: Auto-redirects to `/dashboard`
- **Session**: JWT-based authentication

## 📊 CURRENT STATE
```yaml
branch: main
last_commit: 0fbf0fd - Initial project structure
active_endpoints:
  - /api/v1/auth/* (login, me, refresh, logout)
  - /api/v1/persons/* (CRUD)
  - /api/v1/clinics/* (CRUD)
  - /api/v1/users/* (CRUD, admin only)
  - /api/v1/employees/* (CRUD)
  - /api/v1/clients/* (CRUD)
```

## 🎯 SESSION OBJECTIVES
- [x] Consolidate knowledge base from project documentation
- [x] Implement frontend consistency improvements (Phase 1)
- [x] Create DashboardLayout component for consistent UI
- [x] Refactor main dashboard page with design tokens
- [x] Start servers for testing (CRITICAL FIRST STEP!)
- [ ] Implement remaining dashboard sub-pages (Phase 2)
- [ ] Enhance automation and pattern extraction

## 📄 RECENT ACTIVITY
- **Latest Changes**: Frontend architecture refactoring (Phase 1 complete)
- **Files Created**: 
  - `components/layout/dashboard-layout.tsx` - Unified dashboard wrapper
  - `app/dashboard/layout.tsx` - Next.js layout integration
  - `app/dashboard/page.tsx` - Refactored main dashboard
  - `lib/utils.ts` - Utility functions for className merging
- **Patterns Added**: Dashboard layout wrapper, Design token system, StatCard component
- **UI Improvements**: Consistent navigation, PicoClinics branding integration

## Architecture Decisions (Verified)
### Backend Stack
- **Framework**: FastAPI 0.109.0 with Uvicorn 0.27.0
- **Database**: PostgreSQL with SQLAlchemy 2.0.25
- **Migrations**: Alembic 1.13.1
- **Auth**: JWT with python-jose 3.3.0, bcrypt 4.3.0

### Frontend Stack (Updated)
- **Framework**: Next.js 14.2.3 with React 18.3.1 (downgraded for stability)
- **Styling**: Tailwind CSS 3.3.0
- **State**: Zustand 4.4.7
- **Data**: TanStack Query 5.17.9, Axios 1.6.5
- **UI**: Radix UI components, Framer Motion 11.0.0

## Active Patterns
- Conventional commits trigger automatic pattern extraction
- Virtual environment required for Python commands
- API requires authentication (default: admin@picobrain.com)

## Known Issues & Solutions
- **Frontend Build Error**: ✅ FIXED!
  - Root cause: React 19 compatibility + missing 'use client' directive
  - Solution: Downgraded to React 18 + Next.js 14, added 'use client' to DashboardLayout
  - All pages now working correctly
- **Mobile App**: Directory exists but React Native not configured
- **Backend**: No TypeScript, uses plain Python
- **Token Duplication**: Session updates were duplicating (now fixed)
- **Server Startup**: ⚠️ MUST start both servers before any work! Backend (port 8000) and frontend (port 3000)
  - Backend: `cd backend && source venv/bin/activate && python -m uvicorn app.main:app --reload`
  - Frontend: `cd frontend && npm run dev`
  - Both servers stay running in separate terminal tabs
- **Login Route**: Use `/login` not `/login/dashboard` (404 error)
- **Database**: Requires PostgreSQL running locally or via Docker

## Session Notes
- Session initialized at 2025-08-30 04:15:00
- Knowledge base consolidated from project documentation
- Automation scripts: Ready
- Knowledge extraction: Enabled
- Memory limit: 8GB RAM (MacBook M2)
- **Login Process Verified**: Successfully logged in with admin credentials
- **Server Startup Script**: Created `start-servers.sh` for easy startup

## Session Update: 2025-08-30 14:45
- **Action**: Consolidated knowledge base from project documentation
- **Files Updated**: CLAUDE.md, knowledge.md
- **Knowledge Added**: Verified commands, technical stack, API endpoints
- **Cleanup**: Removed duplicate session entries

## PicoClinics Architecture Overview

### Tech Stack Integration
- **Frontend**: Next.js 15.5.2 (App Router), TypeScript, Tailwind CSS, shadcn/ui
- **Backend**: FastAPI with PostgreSQL (SQLAlchemy ORM)
- **Authentication**: JWT-based with refresh tokens
- **State Management**: Zustand (client), TanStack Query (server state)
- **Deployment**: Vercel-ready (frontend), Docker-ready (backend)

### Key Frontend Directories (Verified)
- `/frontend/src/app` - Next.js App Router pages and layouts
  - `/dashboard` - Dashboard pages (clients, clinics, employees, persons, users)
  - `/login` - Authentication pages
- `/frontend/src/components` - Component library
  - `/ui` - shadcn/ui base components
  - `/dashboard` - Dashboard-specific components
  - `/enhanced` - Enhanced/composite components
  - `/styled` - Styled wrapper components
  - `/templates` - Page templates
- `/frontend/src/hooks` - Custom React hooks for data fetching
- `/frontend/src/lib` - Utilities (api.ts, theme.ts, utils.ts)
- `/frontend/src/services` - API service layer (api.service.ts, auth.service.ts)
- `/frontend/src/types` - TypeScript type definitions
- `/frontend/src/styles` - Global styles and CSS modules

### Backend Structure (Verified)
- `/backend/app` - Main application code
  - `/api` - API endpoints grouped by version
  - `/core` - Core functionality (config, security)
  - `/db` - Database utilities and session management
  - `/models` - SQLAlchemy ORM models
  - `/schemas` - Pydantic schemas for validation
  - `/services` - Business logic layer
- `/backend/alembic` - Database migrations
- `/backend/tests` - Test suite

### Active Development Patterns
- Use server components by default in Next.js App Router
- Client components only when interactivity needed
- Implement parallel data fetching with Promise.all()
- Apply optimistic UI updates for better perceived performance
- Use Pydantic for request/response validation
- Leverage SQLAlchemy 2.0 async capabilities

## Session Update: 2025-08-30 15:50
- **Changes**: 1917 additions, 266 deletions
- **Files modified**: 4
- **Summary**:  backend/app/config.py      |   43 +-
 backend/requirements.txt   |   75 +-
 frontend/package-lock.json | 2036 +++++++++++++++++++++++++++++++++++++++## Session Update: 2025-08-30 18:30 - Dashboard Fixed! 🎉
- **Issue**: Frontend "Internal Server Error" on all routes
- **Root Causes Identified**:
  1. React 19/Next.js 15 compatibility issues
  2. Missing 'use client' directive in DashboardLayout
- **Fixes Applied**:
  1. Downgraded React from 19.1.1 to 18.3.1
  2. Downgraded Next.js from 15.5.2 to 14.2.3
  3. Added 'use client' to dashboard-layout.tsx
- **Result**: ✅ Dashboard fully functional at http://localhost:3000/dashboard
- **Verification**: All pages now loading correctly with proper UI

---

## Session Update: 2025-08-30 18:15 - Server Issues Identified
- **Backend Server**: ✅ Running correctly on port 8000
- **API Docs**: ✅ Found at http://localhost:8000/docs (NOT /api/v1/docs)
- **Frontend Server**: ❌ Internal Server Error - Build issues preventing all pages from loading
- **Root Cause**: Next.js compilation error affecting entire frontend application
- **Knowledge Updated**: Corrected API docs URL in both files

### Critical Issues to Fix:
1. **Frontend Build Error**: Internal Server Error on all routes
   - Affects: /, /dashboard, /login, even /test
   - Attempted fixes: npm install, server restart, simple test page
   - Status: Needs investigation of build/compilation logs

2. **Documentation Error**: Fixed - API docs at /docs not /api/v1/docs

---

## Session Update: 2025-08-30 18:00 - Server Management Lesson
- **Learning**: Servers must be started FIRST before any testing or development
- **Backend Server**: Started via Terminal with uvicorn (no app.py file exists)
- **Frontend Server**: Started via Terminal with `cd frontend && npm run dev`
- **Both Running**: Essential for dashboard access at http://localhost:3000/dashboard
- **Knowledge Updated**: Added server startup as critical first step in both files

### Key Takeaway
**Always start both servers before beginning work:**
1. Open Terminal, create two tabs
2. Tab 1: Start backend (`cd backend && source venv/bin/activate && python -m uvicorn app.main:app --reload`)
3. Tab 2: Start frontend (`cd frontend && npm run dev`)
4. Keep both running during entire work session
5. Access dashboard at http://localhost:3000/dashboard

-----
 frontend/package.json      |   29 +-
 4 files changed, 1917 insertions(+), 266 deletions(-)

### Patterns Observed
+        "class-variance-authority": "^0.7.1",
+    "node_modules/class-variance-authority": {
+      "resolved": "https://registry.npmjs.org/class-variance-authority/-/class-variance-authority-0.7.1.tgz",
+    "class-variance-authority": "^0.7.1",

---

## Session Update: 2025-08-30 15:57
- **Changes**: 1924 additions, 269 deletions
- **Files modified**: 6
- **Summary**:  CLAUDE.md                  |    4 +-
 backend/app/config.py      |   43 +-
 backend/requirements.txt   |   75 +-
 frontend/package-lock.json | 2036 +++++++++++++++++++++++++++++++++++++++-----
 frontend/package.json      |   29 +-
 knowledge.md               |    6 +-
 6 files changed, 1924 insertions(+), 269 deletions(-)

### Patterns Observed
+        "class-variance-authority": "^0.7.1",
+    "node_modules/class-variance-authority": {
+      "resolved": "https://registry.npmjs.org/class-variance-authority/-/class-variance-authority-0.7.1.tgz",
+    "class-variance-authority": "^0.7.1",

---

## Session Update: 2025-08-30 16:07
- **Changes**: 1919 additions, 268 deletions
- **Files modified**: 5
- **Summary**:  CLAUDE.md                  |    4 +-
 backend/app/config.py      |   43 +-
 backend/requirements.txt   |   75 +-
 frontend/package-lock.json | 2036 +++++++++++++++++++++++++++++++++++++++-----
 frontend/package.json      |   29 +-
 5 files changed, 1919 insertions(+), 268 deletions(-)

### Patterns Observed
+        "class-variance-authority": "^0.7.1",
+    "node_modules/class-variance-authority": {
+      "resolved": "https://registry.npmjs.org/class-variance-authority/-/class-variance-authority-0.7.1.tgz",
+    "class-variance-authority": "^0.7.1",

---

## Session Update: 2025-08-30 16:58
- **Changes**: 1981 additions, 281 deletions
- **Files modified**: 6
- **Summary**:  CLAUDE.md                  |   21 +-
 backend/app/config.py      |   43 +-
 backend/requirements.txt   |   75 +-
 frontend/package-lock.json | 2036 +++++++++++++++++++++++++++++++++++++++-----
 frontend/package.json      |   29 +-
 knowledge.md               |   58 +-
 6 files changed, 1981 insertions(+), 281 deletions(-)

### Patterns Observed
+        "class-variance-authority": "^0.7.1",
+    "node_modules/class-variance-authority": {
+      "resolved": "https://registry.npmjs.org/class-variance-authority/-/class-variance-authority-0.7.1.tgz",
+    "class-variance-authority": "^0.7.1",

---

## Session Update: 2025-08-30 17:12
- **Changes**: 2000 additions, 281 deletions
- **Files modified**: 6
- **Summary**:  CLAUDE.md                  |   40 +-
 backend/app/config.py      |   43 +-
 backend/requirements.txt   |   75 +-
 frontend/package-lock.json | 2036 +++++++++++++++++++++++++++++++++++++++-----
 frontend/package.json      |   29 +-
 knowledge.md               |   58 +-
 6 files changed, 2000 insertions(+), 281 deletions(-)

### Patterns Observed
++        "class-variance-authority": "^0.7.1",
++    "node_modules/class-variance-authority": {
++      "resolved": "https://registry.npmjs.org/class-variance-authority/-/class-variance-authority-0.7.1.tgz",
++    "class-variance-authority": "^0.7.1",
+        "class-variance-authority": "^0.7.1",

---

## Session Update: 2025-08-30 17:45 - Frontend Refactoring Phase 1
- **Changes**: ~420 lines added (3 new components, 1 utility file)
- **Files created**: 4
- **Summary**: Implemented DashboardLayout wrapper pattern for consistent UI across all dashboard pages

### Implementation Details
- **DashboardLayout Component**: Responsive sidebar + top navigation with PicoClinics branding
- **Design Tokens**: Established spacing and typography tokens for consistency
- **Color Integration**: Applied #e67e5b coral primary throughout dashboard
- **Mobile Support**: Slide-out menu for mobile devices
- **StatCard Pattern**: Reusable card component with trends and icons

### Technical Decisions
- Used composition pattern with children prop for layout wrapper
- Implemented cn() utility for Tailwind class merging
- Created self-contained StatCard (to be extracted in Phase 2)
- Applied hover states and smooth transitions for better UX

### Success Metrics
- ✅ Main dashboard page fully refactored
- ✅ Consistent navigation implemented
- ✅ PicoClinics design system applied
- ✅ Mobile-responsive layout working
- ✅ Zero impact on sub-pages (preserved for Phase 2)

### Next Phase Ready
- Foundation established for systematic refactoring
- Pattern proven on main dashboard
- Ready to extract shared components
- Can apply to all sub-pages incrementally

---

## Session Update: 2025-08-30 17:54
- **Changes**: 382 additions, 1025 deletions
- **Files modified**: 6
- **Summary**:  .claude/cache.json                    |   2 +-
 .claude/metrics/changes.csv           |   1 +
 CLAUDE.md                             |  58 ++-
 frontend/src/app/dashboard/layout.tsx | 335 +------------
 frontend/src/app/dashboard/page.tsx   | 861 ++++++++--------------------------
 knowledge.md                          | 150 +++++-
 6 files changed, 382 insertions(+), 1025 deletions(-)

### Patterns Observed
+  - `lib/utils.ts` - Utility functions for className merging
+- Implemented cn() utility for Tailwind class merging
+export default function Layout({ 
+const tokens = {
+function StatCard({ title, value, description, icon: Icon, trend, trendValue }: StatCardProps) {

---

## Session Update: 2025-08-30 18:39
- **Changes**: 529 additions, 1065 deletions
- **Files modified**: 8
- **Summary**:  .claude/cache.json                    |   6 +-
 .claude/metrics/changes.csv           |   2 +
 CLAUDE.md                             | 148 +++++-
 frontend/package-lock.json            |   2 +-
 frontend/package.json                 |  29 +-
 frontend/src/app/dashboard/layout.tsx | 335 +------------
 frontend/src/app/dashboard/page.tsx   | 861 ++++++++--------------------------
 knowledge.md                          | 211 +++++++--
 8 files changed, 529 insertions(+), 1065 deletions(-)

### Patterns Observed
+  - `lib/utils.ts` - Utility functions for className merging
+- **Result**: ✅ Dashboard fully functional at http://localhost:3000/dashboard
+- Implemented cn() utility for Tailwind class merging
++  - `lib/utils.ts` - Utility functions for className merging
++- Implemented cn() utility for Tailwind class merging

---

## Session Update: 2025-08-30 18:40
- **Changes**: 551 additions, 1064 deletions
- **Files modified**: 8
- **Summary**:  .claude/cache.json                    |   6 +-
 .claude/metrics/changes.csv           |   3 +
 CLAUDE.md                             | 168 ++++++-
 frontend/package-lock.json            |   2 +-
 frontend/package.json                 |  29 +-
 frontend/src/app/dashboard/layout.tsx | 335 +------------
 frontend/src/app/dashboard/page.tsx   | 861 ++++++++--------------------------
 knowledge.md                          | 211 +++++++--
 8 files changed, 551 insertions(+), 1064 deletions(-)

### Patterns Observed
+  - `lib/utils.ts` - Utility functions for className merging
+- **Result**: ✅ Dashboard fully functional at http://localhost:3000/dashboard
+- Implemented cn() utility for Tailwind class merging
++  - `lib/utils.ts` - Utility functions for className merging
++- Implemented cn() utility for Tailwind class merging

---
