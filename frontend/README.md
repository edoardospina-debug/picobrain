# PicoBrain Frontend

## Overview

PicoBrain is a medical practice management system built with Next.js 14, TypeScript, and Ant Design. This frontend application integrates with a FastAPI backend to provide comprehensive clinic management capabilities.

## Tech Stack

- **Framework**: Next.js 14 (App Router)
- **Language**: TypeScript 5.x
- **UI Library**: Ant Design 5.x
- **State Management**: TanStack Query v5
- **Form Handling**: React Hook Form + Zod
- **HTTP Client**: Axios
- **Styling**: Tailwind CSS (utilities) + Ant Design (components)

## Prerequisites

- Node.js 18+ and npm/yarn
- Backend API running at `http://localhost:8000`

## Installation

1. Navigate to the frontend directory:
```bash
cd /Users/edo/PyProjects/picobrain/frontend
```

2. Install dependencies:
```bash
npm install
# or
yarn install
```

3. Set up environment variables:
```bash
# Copy the .env.local file (already created)
# Modify if needed for your environment
```

## Running the Application

### Development Mode
```bash
npm run dev
# or
yarn dev
```

The application will be available at `http://localhost:3000`

### Production Build
```bash
npm run build
npm start
# or
yarn build
yarn start
```

## Features Implemented

### Phase 1: Foundation ✅
- Next.js 14 project setup with TypeScript
- Ant Design configuration with light theme
- API client with JWT authentication
- Token refresh mechanism
- Layout components (Sidebar, TopBar)
- Routing structure

### Phase 2: Shared Components ✅
- Generic DataTable component with:
  - Server-side pagination
  - Column sorting
  - Advanced filtering
  - Search functionality
  - Row actions (edit, delete, view)
  - Bulk operations
  - Export to CSV
- Dynamic form components
- Loading states and error boundaries

### Phase 3: Clinics POC ✅
- **List Page** (`/clinics`)
  - Paginated table with 20 items per page
  - Sortable columns (name, code, city, status)
  - Search by name or code
  - Filter by active status
  - Quick actions (edit, view, deactivate)
  - Bulk export and deactivate

- **Create Page** (`/clinics/new`)
  - Multi-section form (Basic, Address, Contact)
  - Real-time validation with Zod
  - Currency dropdown
  - Country code selector
  - Phone number formatting

- **Edit Page** (`/clinics/[id]`)
  - Pre-populated form with existing data
  - Update validation
  - Unsaved changes warning

## Project Structure

```
frontend/
├── src/
│   ├── app/                    # Next.js app directory
│   │   ├── (auth)/             # Auth group (login)
│   │   ├── (dashboard)/        # Dashboard group (protected routes)
│   │   │   ├── clinics/        # Clinics module
│   │   │   ├── staff/          # Staff module (future)
│   │   │   ├── clients/        # Clients module (future)
│   │   │   └── users/          # Users module (future)
│   │   ├── layout.tsx          # Root layout
│   │   └── globals.css         # Global styles
│   ├── components/
│   │   ├── shared/             # Reusable components
│   │   │   └── DataTable/      # Generic data table
│   │   └── features/           # Feature-specific components
│   │       └── clinics/        # Clinic components
│   ├── lib/
│   │   ├── api/                # API client and endpoints
│   │   ├── auth/               # Authentication logic
│   │   └── validators/         # Zod schemas
│   └── types/                  # TypeScript type definitions
├── public/                     # Static assets
├── .env.local                  # Environment variables
├── next.config.js              # Next.js configuration
├── tailwind.config.ts          # Tailwind configuration
└── package.json                # Dependencies
```

## User Roles & Permissions

The system supports 6 user roles with different permission levels:

- **admin**: Full system access
- **manager**: Clinic management access
- **staff**: General staff access
- **medical**: Medical staff (doctors, nurses)
- **finance**: Financial operations
- **readonly**: View-only access

## API Integration

The frontend integrates with the backend API at `http://localhost:8000/api/v1`

### Authentication Flow
1. User logs in with credentials
2. Receives JWT access token
3. Token stored in memory (not localStorage for security)
4. Auto-refresh 5 minutes before expiry
5. Refresh token stored as httpOnly cookie

### Available Endpoints
- `/auth/*` - Authentication
- `/clinics/*` - Clinic CRUD operations
- `/employees/*` - Employee management (coming soon)
- `/clients/*` - Client management (coming soon)
- `/users/*` - User management (coming soon)

## Configuration

### Theme Settings
- **Theme**: Light (configurable in layout.tsx)
- **Date Format**: MM/DD/YYYY
- **Table Density**: Comfortable (16px padding)

### Environment Variables
```env
NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1
NEXT_PUBLIC_APP_URL=http://localhost:3000
NEXT_PUBLIC_APP_NAME=PicoBrain
NEXT_PUBLIC_THEME=light
NEXT_PUBLIC_DATE_FORMAT=MM/DD/YYYY
NEXT_PUBLIC_TABLE_DENSITY=comfortable
```

## Testing the Application

### Login Credentials (Development)
- **Admin**: username: `admin`, password: `admin123`
- **Manager**: username: `manager`, password: `manager123`
- **Staff**: username: `staff`, password: `staff123`

### Test Scenarios
1. **Login Flow**
   - Navigate to `/login`
   - Enter credentials
   - Should redirect to `/clinics`

2. **Clinic CRUD**
   - View clinic list
   - Search for clinics
   - Create new clinic
   - Edit existing clinic
   - Delete/deactivate clinic
   - Export clinic data

3. **Permission Testing**
   - Login with different roles
   - Verify menu items visibility
   - Check action buttons based on permissions

## Troubleshooting

### Backend Connection Issues
- Ensure backend is running at `http://localhost:8000`
- Check CORS settings in backend
- Verify API endpoints are accessible

### Authentication Issues
- Clear browser cookies
- Check token expiration settings
- Verify backend JWT configuration

### Build Errors
```bash
# Clear Next.js cache
rm -rf .next
npm run build
```

## Next Steps

### Phase 4: Complete CRUD Pages
- [ ] Implement Staff management (Persons + Employees)
- [ ] Add Clients management
- [ ] Create Users management with role assignment
- [ ] Handle complex Person relationships

### Phase 5: Polish & Optimization
- [ ] Add comprehensive error handling
- [ ] Implement success/error notifications
- [ ] Add keyboard shortcuts
- [ ] Performance testing
- [ ] Accessibility audit (WCAG 2.1 AA)

### Phase 6: Deployment
- [ ] Configure production environment variables
- [ ] Set up Vercel deployment
- [ ] Configure custom domain
- [ ] Set up monitoring

## Contributing

1. Create a feature branch
2. Make your changes
3. Test thoroughly
4. Submit a pull request

## License

Private - All rights reserved

---

**Version**: 0.1.0  
**Last Updated**: December 2024  
**Status**: Development - Clinics POC Complete
