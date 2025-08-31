<!-- CLAUDE: ALWAYS READ THIS FIRST - ACTIVE PROJECT CONTEXT -->
<!-- Last Updated: 2025-08-31 02:31:14 -->
<!-- Session ID: 20250831_023114 -->

# 🧠 CLAUDE KNOWLEDGE BASE - PicoBrain

## 🚨 PRIORITY CONTEXT (Read First)
**Project**: PicoBrain Healthcare Management System
**Location**: /Users/edo/PyProjects/picobrain
**Status**: Backend complete, Frontend architecture planned
**Next Deliverable**: Clinics CRUD POC (Frontend Phase 3)

### Server URLs (Working ✅)
- **Backend API**: http://localhost:8000 ✅
- **API Docs**: http://localhost:8000/docs ✅ (NOT /api/v1/docs)  
- **Frontend**: http://localhost:3000 (Not yet implemented)
- **Dashboard**: http://localhost:3000/dashboard (Planned)
- **Login Page**: http://localhost:3000/login (Planned)

### 🔐 Authentication (Verified)
- **Admin Username**: admin@picobrain.com
- **Admin Password**: admin123
- **Type**: JWT with refresh tokens
- **Access Token**: 8 days expiry
- **Refresh Token**: Stored as httpOnly cookie

## 📊 CURRENT STATE (2025-08-31)

### Backend Status ✅ COMPLETE
```yaml
branch: main
database: picobraindb (PostgreSQL)
user: edo (NOT postgres!)
active_endpoints:
  - /api/v1/auth/* (login, refresh, me, logout)
  - /api/v1/persons/* (CRUD)
  - /api/v1/clinics/* (CRUD) 
  - /api/v1/employees/* (CRUD + bulk)
  - /api/v1/clients/* (CRUD)
  - /api/v1/users/* (CRUD, admin only)
migrated_data:
  - 5 clinics (complete with addresses)
  - 87 employees (all roles)
  - 91 persons (linked to employees)
```

### Frontend Status 🎯 PLANNING COMPLETE
```yaml
status: Architecture finalized, ready for implementation
tech_stack:
  framework: Next.js 14.x (App Router)
  ui_library: Ant Design 5.x
  state: TanStack Query v5 + Zustand
  http_client: Axios
  forms: React Hook Form + Zod
  deployment: Vercel
next_deliverable: Clinics POC
development_plan: /Users/edo/PyProjects/picobrain-frontend-plan.md
```

## 🏗️ Frontend Architecture (Finalized 2025-08-31)

### Technology Decisions
- **UI Framework**: Ant Design (chosen over shadcn/ui)
  - Reason: Enterprise-ready components, built-in virtualization for 100k+ records
- **State Management**: TanStack Query (server state) + Zustand (UI state)
  - Reason: Simple, no Redux complexity
- **Forms**: Single form with sections (not wizards)
- **Tables**: Server-side pagination (not infinite scroll)
- **Offline**: No PWA features (keep it simple)
- **Audit**: Edit tracking only (no view tracking)

### Component Architecture
```typescript
/components
├── shared/
│   ├── DataTable/      # ONE table for ALL entities
│   ├── EntityForm/     # ONE form for ALL CRUD
│   └── PageWrapper/    # Consistent page structure
└── features/
    └── [entity]/       # Entity-specific overrides only
```

### Implementation Phases
1. **Foundation (Days 1-2)**: Next.js setup, API client, auth
2. **Shared Components (Days 3-4)**: DataTable, EntityForm
3. **Clinics POC (Days 5-6)** 🎯 FIRST DELIVERABLE
4. **Complete CRUD (Days 7-10)**: All entities
5. **Polish (Days 11-12)**: Optimization, testing

## 🔌 API Structure (Complete Mapping)

### User Roles
```python
admin    # Full system access
manager  # Clinic management
staff    # General staff access
medical  # Doctors, nurses
finance  # Financial operations
readonly # View-only access
```

### Entity Relationships
```
Person (Base)
  ├── Employee (via person_id)
  │   └── role: doctor|nurse|receptionist|manager|finance|admin
  ├── Client (via person_id)
  └── User (via person_id for auth)

Clinic
  ├── Employees (via primary_clinic_id)
  └── Clients (via preferred_clinic_id)
```

### Database Fields Discovered
```python
# Person: 14 fields including phones split into country_code + number
# Employee: 17 fields including salary_minor, commission_rate, hire_date
# Clinic: 17 fields with full address fields
# Client: 6 fields
# User: 6 fields with role enum
```

## 🎯 SESSION OBJECTIVES (Updated)
- [x] Employee migration completed (87 records)
- [x] Frontend architecture planned
- [x] Technology stack finalized
- [x] Development plan documented
- [ ] Initialize Next.js 14 project
- [ ] Implement Phase 1 (Foundation)
- [ ] Build Clinics POC
- [ ] Define permission matrix

## 📄 KEY DOCUMENTS
- **Frontend Plan**: `/Users/edo/PyProjects/picobrain-frontend-plan.md`
- **Knowledge Base**: `/Users/edo/PyProjects/picobrain/knowledge.md`
- **Migration Report**: `/Users/edo/PyProjects/PICOBRAIN_MIGRATION_REPORT.md`

## 🚀 Quick Start Commands

### Start Development Environment
```bash
# Backend (Terminal Tab 1)
cd /Users/edo/PyProjects/picobrain/backend
source venv/bin/activate
python -m uvicorn app.main:app --reload --port 8000

# Frontend (Terminal Tab 2) - Once initialized
cd /Users/edo/PyProjects/picobrain/frontend
npm run dev
```

### Generate TypeScript Types
```bash
npx openapi-typescript http://localhost:8000/api/v1/openapi.json \
  --output ./types/generated/api.ts
```

## ⚠️ Critical Knowledge

### Database Connection
```python
# MUST use these exact parameters!
db_params = {
    'dbname': 'picobraindb',  # NOT edo_brain_4!
    'user': 'edo',             # NOT postgres!
    'password': '',
    'host': 'localhost',
    'port': '5432'
}
```

### Required Fields
- `primary_clinic_id`: CANNOT be NULL in employees
- `person_id`: Employee MUST have person record first
- Phone fields: Split into `country_code` and `number`
- Salaries: Stored in minor units (cents)

### Frontend Patterns (Planned)
```typescript
// Generic CRUD Hook
useCrud<T>(endpoint: string)

// Audit on mutations
const auditData = {
  ...data,
  _audit: { action, timestamp, user }
}

// Token refresh
apiClient.interceptors.response.use(...)
```

## 📋 TODO for Next Session

1. **Define Permission Matrix**:
   - Which roles can CRUD which entities?
   - Special permissions for medical/finance roles?

2. **Initialize Frontend**:
   ```bash
   npx create-next-app@14 frontend --typescript --tailwind --app
   npm install antd @tanstack/react-query axios react-hook-form zod
   ```

3. **Implement Clinics POC**:
   - List with pagination
   - Create/Edit forms
   - Delete confirmation
   - Search/filter
   - Test with 100k records

## 📝 Session Notes

### 2025-08-31 Frontend Planning Session
- Analyzed complete backend structure
- Discovered all API endpoints and models
- Chose Ant Design for enterprise features
- Created comprehensive development plan
- Documented in picobrain-frontend-plan.md

### Key Decisions Made
- Ant Design over shadcn/ui (better tables)
- Single forms with sections (not wizards)
- Server-side pagination (not infinite scroll)
- No offline support (simplicity)
- Edit audit only (not view tracking)

### Migration Complete ✅
- 5 clinics with full addresses
- 87 employees with all fields
- 91 persons linked properly
- Ready for frontend development

---

**Next Action**: Read picobrain-frontend-plan.md and start Phase 1 implementation
## Session Update: 2025-08-31 01:35
- **Changes**: 2887 additions, 19350 deletions
- **Files modified**: 66
- **Summary**:  .claude/cache.json                                 |    6 +-
 .claude/knowledge/patterns.json                    | 1481 +++-
 .claude/metrics/changes.csv                        |   13 +
 CLAUDE.md                                          | 1541 +---
 FRONTEND_IMPLEMENTATION_GUIDE.md                   |  669 --
 backend/app/api/v1/endpoints/clinics.py            |  145 +-
 backend/app/api/v1/endpoints/employees.py          |  420 +-
 backend/app/api/v1/endpoints/persons.py            |  115 +-
 backend/app/models/core.py                         |   70 +-
 backend/app/schemas/__init__.py                    |    7 +-
 backend/app/schemas/core.py                        |  129 +-
 frontend-setup.md                                  |   46 -
 frontend/.env.yaml                                 |   10 -
 frontend/DASHBOARD_STATUS.md                       |  129 -
 frontend/MODERN_UI_FRAMEWORK.md                    |  328 -
 frontend/README.md                                 |  186 -
 frontend/UI_STANDARDIZATION_STATUS.md              |  145 -
 frontend/next-env.d.ts                             |    6 -
 frontend/next.config.js                            |   52 -
 frontend/package-lock.json                         | 8023 --------------------
 frontend/package.json                              |   49 -
 frontend/postcss.config.js                         |    6 -
 frontend/public/abstract-geometric-shapes.png      |  Bin 675864 -> 0 bytes
 frontend/public/caring-doctor.png                  |  Bin 930303 -> 0 bytes
 frontend/src/app/dashboard/clients/page.tsx        |  484 --
 frontend/src/app/dashboard/clinics/page.tsx        |  463 --
 frontend/src/app/dashboard/employees/page.tsx      |  586 --
 frontend/src/app/dashboard/layout.tsx              |  329 -
 frontend/src/app/dashboard/page.tsx                |  696 --
 frontend/src/app/dashboard/persons/page.tsx        |  548 --
 frontend/src/app/dashboard/users/page.tsx          |  662 --
 frontend/src/app/globals.css                       |  415 -
 frontend/src/app/layout.tsx                        |   33 -
 frontend/src/app/login/page.tsx                    |  208 -
 frontend/src/app/page.tsx                          |    5 -
 frontend/src/app/providers.tsx                     |   30 -
 frontend/src/components/dashboard/StatsCard.tsx    |   72 -
 frontend/src/components/enhanced/CRMLayout.tsx     |   96 -
 .../src/components/enhanced/EnhancedStatsCard.tsx  |  172 -
 frontend/src/components/enhanced/EnhancedTable.tsx |  443 --
 frontend/src/components/enhanced/index.ts          |    8 -
 frontend/src/components/styled/index.tsx           |  320 -
 frontend/src/components/templates/PageTemplate.tsx |   49 -
 frontend/src/components/ui/avatar.tsx              |   53 -
 frontend/src/components/ui/badge.tsx               |   46 -
 frontend/src/components/ui/button.tsx              |   59 -
 frontend/src/components/ui/card.tsx                |   92 -
 frontend/src/components/ui/checkbox.tsx            |   32 -
 frontend/src/components/ui/dialog.tsx              |  143 -
 frontend/src/components/ui/dropdown-menu.tsx       |  257 -
 frontend/src/components/ui/input.tsx               |   21 -
 frontend/src/components/ui/label.tsx               |   24 -
 frontend/src/components/ui/select.tsx              |  185 -
 frontend/src/components/ui/textarea.tsx            |   18 -
 frontend/src/components/ui/toaster.tsx             |  129 -
 frontend/src/lib/api.ts                            |  136 -
 frontend/src/lib/theme.ts                          |   77 -
 frontend/src/lib/utils.ts                          |    6 -
 frontend/src/services/api.service.ts               |  381 -
 frontend/src/services/auth.service.ts              |  125 -
 frontend/src/styles/picoclinics-palette.css        |   90 -
 frontend/src/types/api.ts                          |  237 -
 frontend/tailwind.config.js                        |   58 -
 frontend/tsconfig.json                             |   35 -
 frontend/v0-prompt.md                              |   68 -
 knowledge.md                                       |  770 +-
 66 files changed, 2887 insertions(+), 19350 deletions(-)

### Patterns Observed
+      "pattern": "class Person",
+      "pattern": "class Clinic",
+      "pattern": "class Client",
+      "pattern": "class Employee",
+      "pattern": "class User",

---

## Session Update: 2025-08-31 02:28
- **Changes**: 4473 additions, 11526 deletions
- **Files modified**: 65
- **Summary**:  .claude/cache.json                                 |    6 +-
 .claude/knowledge/patterns.json                    | 1727 +++++++++-
 .claude/metrics/changes.csv                        |   14 +
 CLAUDE.md                                          |    4 +-
 FRONTEND_IMPLEMENTATION_GUIDE.md                   |  669 ----
 backend/app/api/v1/endpoints/clinics.py            |  145 +-
 backend/app/api/v1/endpoints/employees.py          |  420 ++-
 backend/app/api/v1/endpoints/persons.py            |  115 +-
 backend/app/models/core.py                         |   70 +-
 backend/app/schemas/__init__.py                    |    7 +-
 backend/app/schemas/core.py                        |  129 +-
 frontend-setup.md                                  |   46 -
 frontend/.env.yaml                                 |   10 -
 frontend/DASHBOARD_STATUS.md                       |  129 -
 frontend/MODERN_UI_FRAMEWORK.md                    |  328 --
 frontend/README.md                                 |  379 ++-
 frontend/UI_STANDARDIZATION_STATUS.md              |  145 -
 frontend/next-env.d.ts                             |    3 +-
 frontend/next.config.js                            |   41 +-
 frontend/package-lock.json                         | 3579 +++++++++-----------
 frontend/package.json                              |   60 +-
 frontend/public/abstract-geometric-shapes.png      |  Bin 675864 -> 0 bytes
 frontend/public/caring-doctor.png                  |  Bin 930303 -> 0 bytes
 frontend/src/app/dashboard/clients/page.tsx        |  484 ---
 frontend/src/app/dashboard/clinics/page.tsx        |  463 ---
 frontend/src/app/dashboard/employees/page.tsx      |  586 ----
 frontend/src/app/dashboard/layout.tsx              |  329 --
 frontend/src/app/dashboard/page.tsx                |  696 ----
 frontend/src/app/dashboard/persons/page.tsx        |  548 ---
 frontend/src/app/dashboard/users/page.tsx          |  662 ----
 frontend/src/app/globals.css                       |  427 +--
 frontend/src/app/layout.tsx                        |   22 +-
 frontend/src/app/login/page.tsx                    |  208 --
 frontend/src/app/page.tsx                          |    5 -
 frontend/src/app/providers.tsx                     |   30 -
 frontend/src/components/dashboard/StatsCard.tsx    |   72 -
 frontend/src/components/enhanced/CRMLayout.tsx     |   96 -
 .../src/components/enhanced/EnhancedStatsCard.tsx  |  172 -
 frontend/src/components/enhanced/EnhancedTable.tsx |  443 ---
 frontend/src/components/enhanced/index.ts          |    8 -
 frontend/src/components/styled/index.tsx           |  320 --
 frontend/src/components/templates/PageTemplate.tsx |   49 -
 frontend/src/components/ui/avatar.tsx              |   53 -
 frontend/src/components/ui/badge.tsx               |   46 -
 frontend/src/components/ui/button.tsx              |   59 -
 frontend/src/components/ui/card.tsx                |   92 -
 frontend/src/components/ui/checkbox.tsx            |   32 -
 frontend/src/components/ui/dialog.tsx              |  143 -
 frontend/src/components/ui/dropdown-menu.tsx       |  257 --
 frontend/src/components/ui/input.tsx               |   21 -
 frontend/src/components/ui/label.tsx               |   24 -
 frontend/src/components/ui/select.tsx              |  185 -
 frontend/src/components/ui/textarea.tsx            |   18 -
 frontend/src/components/ui/toaster.tsx             |  129 -
 frontend/src/lib/api.ts                            |  136 -
 frontend/src/lib/theme.ts                          |   77 -
 frontend/src/lib/utils.ts                          |    6 -
 frontend/src/services/api.service.ts               |  381 ---
 frontend/src/services/auth.service.ts              |  125 -
 frontend/src/styles/picoclinics-palette.css        |   90 -
 frontend/src/types/api.ts                          |  237 --
 frontend/tailwind.config.js                        |   58 -
 frontend/tsconfig.json                             |   11 +-
 frontend/v0-prompt.md                              |   68 -
 knowledge.md                                       |  105 +
 65 files changed, 4473 insertions(+), 11526 deletions(-)

### Patterns Observed
+      "pattern": "class Person",
+      "pattern": "class Clinic",
+      "pattern": "class Client",
+      "pattern": "class Employee",
+      "pattern": "class User",

---

## Session Update: 2025-08-31 05:05
- **Changes**: 4620 additions, 12094 deletions
- **Files modified**: 68
- **Summary**:  .claude/cache.json                                 |    6 +-
 .claude/knowledge/patterns.json                    | 1973 ++++++++++-
 .claude/metrics/changes.csv                        |   15 +
 CLAUDE.md                                          |    4 +-
 FRONTEND_IMPLEMENTATION_GUIDE.md                   |  669 ----
 backend/app/api/v1/endpoints/clinics.py            |  145 +-
 backend/app/api/v1/endpoints/employees.py          |  420 ++-
 backend/app/api/v1/endpoints/persons.py            |  115 +-
 backend/app/models/core.py                         |   70 +-
 backend/app/schemas/__init__.py                    |    7 +-
 backend/app/schemas/core.py                        |  129 +-
 backend/test_api.py                                |  227 --
 backend/test_api.sh                                |  300 --
 backend/test_connection.py                         |   40 -
 frontend-setup.md                                  |   46 -
 frontend/.env.yaml                                 |   10 -
 frontend/DASHBOARD_STATUS.md                       |  129 -
 frontend/MODERN_UI_FRAMEWORK.md                    |  328 --
 frontend/README.md                                 |  379 ++-
 frontend/UI_STANDARDIZATION_STATUS.md              |  145 -
 frontend/next-env.d.ts                             |    3 +-
 frontend/next.config.js                            |   41 +-
 frontend/package-lock.json                         | 3579 +++++++++-----------
 frontend/package.json                              |   60 +-
 frontend/public/abstract-geometric-shapes.png      |  Bin 675864 -> 0 bytes
 frontend/public/caring-doctor.png                  |  Bin 930303 -> 0 bytes
 frontend/src/app/dashboard/clients/page.tsx        |  484 ---
 frontend/src/app/dashboard/clinics/page.tsx        |  463 ---
 frontend/src/app/dashboard/employees/page.tsx      |  586 ----
 frontend/src/app/dashboard/layout.tsx              |  329 --
 frontend/src/app/dashboard/page.tsx                |  696 ----
 frontend/src/app/dashboard/persons/page.tsx        |  548 ---
 frontend/src/app/dashboard/users/page.tsx          |  662 ----
 frontend/src/app/globals.css                       |  427 +--
 frontend/src/app/layout.tsx                        |   22 +-
 frontend/src/app/login/page.tsx                    |  208 --
 frontend/src/app/page.tsx                          |    5 -
 frontend/src/app/providers.tsx                     |   30 -
 frontend/src/components/dashboard/StatsCard.tsx    |   72 -
 frontend/src/components/enhanced/CRMLayout.tsx     |   96 -
 .../src/components/enhanced/EnhancedStatsCard.tsx  |  172 -
 frontend/src/components/enhanced/EnhancedTable.tsx |  443 ---
 frontend/src/components/enhanced/index.ts          |    8 -
 frontend/src/components/styled/index.tsx           |  320 --
 frontend/src/components/templates/PageTemplate.tsx |   49 -
 frontend/src/components/ui/avatar.tsx              |   53 -
 frontend/src/components/ui/badge.tsx               |   46 -
 frontend/src/components/ui/button.tsx              |   59 -
 frontend/src/components/ui/card.tsx                |   92 -
 frontend/src/components/ui/checkbox.tsx            |   32 -
 frontend/src/components/ui/dialog.tsx              |  143 -
 frontend/src/components/ui/dropdown-menu.tsx       |  257 --
 frontend/src/components/ui/input.tsx               |   21 -
 frontend/src/components/ui/label.tsx               |   24 -
 frontend/src/components/ui/select.tsx              |  185 -
 frontend/src/components/ui/textarea.tsx            |   18 -
 frontend/src/components/ui/toaster.tsx             |  129 -
 frontend/src/lib/api.ts                            |  136 -
 frontend/src/lib/theme.ts                          |   77 -
 frontend/src/lib/utils.ts                          |    6 -
 frontend/src/services/api.service.ts               |  381 ---
 frontend/src/services/auth.service.ts              |  125 -
 frontend/src/styles/picoclinics-palette.css        |   90 -
 frontend/src/types/api.ts                          |  237 --
 frontend/tailwind.config.js                        |   58 -
 frontend/tsconfig.json                             |   11 +-
 frontend/v0-prompt.md                              |   68 -
 knowledge.md                                       |    6 +-
 68 files changed, 4620 insertions(+), 12094 deletions(-)

### Patterns Observed
+      "pattern": "class Person",
+      "pattern": "class Clinic",
+      "pattern": "class Client",
+      "pattern": "class Employee",
+      "pattern": "class User",

---
