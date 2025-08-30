<!-- CLAUDE: ALWAYS READ THIS FIRST - ACTIVE PROJECT CONTEXT -->
<!-- Last Updated: 2025-08-30 16:50:15 -->
<!-- Session ID: 20250830_165015 -->

# 🧠 CLAUDE KNOWLEDGE BASE - PicoBrain

## 🚨 PRIORITY CONTEXT (Read First)
**Project**: PicoBrain
**Location**: /Users/edo/PyProjects/picobrain
**Session**: Active since 2025-08-30 14:24:17
**Context Usage**: ~6000 / 160000 tokens

### Server URLs (Verified)
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/api/v1/docs  
- **Frontend**: http://localhost:3000
- **Dashboard**: http://localhost:3000/dashboard (requires login)
- **Login Page**: http://localhost:3000/login

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
- [ ] Implement Claude KB v2.0 improvements
- [ ] Enhance automation and pattern extraction
- [ ] Validate setup completeness

## 📄 RECENT ACTIVITY
- **Latest Changes**: Backend config updates, Frontend dependencies added
- **Files Modified**: config.py, requirements.txt, package.json, package-lock.json
- **Patterns Added**: class-variance-authority integration

## Architecture Decisions (Verified)
### Backend Stack
- **Framework**: FastAPI 0.109.0 with Uvicorn 0.27.0
- **Database**: PostgreSQL with SQLAlchemy 2.0.25
- **Migrations**: Alembic 1.13.1
- **Auth**: JWT with python-jose 3.3.0, bcrypt 4.3.0

### Frontend Stack
- **Framework**: Next.js 15.5.2 with React 19.1.1
- **Styling**: Tailwind CSS 3.3.0
- **State**: Zustand 4.4.7
- **Data**: TanStack Query 5.17.9, Axios 1.6.5
- **UI**: Radix UI components, Framer Motion 11.0.0

## Active Patterns
- Conventional commits trigger automatic pattern extraction
- Virtual environment required for Python commands
- API requires authentication (default: admin@picobrain.com)

## Known Issues & Solutions
- **Mobile App**: Directory exists but React Native not configured
- **Backend**: No TypeScript, uses plain Python
- **Token Duplication**: Session updates were duplicating (now fixed)
- **Server Startup**: Need to start both backend (port 8000) and frontend (port 3000)
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
 frontend/package-lock.json | 2036 +++++++++++++++++++++++++++++++++++++++-----
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
