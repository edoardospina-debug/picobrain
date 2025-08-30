# PicoBrain Frontend

Modern React/Next.js frontend for the PicoBrain Healthcare Management System.

## 🚀 Quick Start

### Prerequisites
- Node.js 18+ installed
- Backend API running at `http://localhost:8000`
- npm or yarn package manager

### Installation

1. **Install dependencies:**
```bash
cd frontend
npm install
```

2. **Configure environment:**
```bash
# Copy the environment template
cp .env.local .env.local

# Edit .env.local if needed (default settings should work for local development)
```

3. **Run development server:**
```bash
npm run dev
```

The application will be available at `http://localhost:3000`

## 📁 Project Structure

```
frontend/
├── src/
│   ├── app/              # Next.js App Router pages
│   │   ├── login/        # Login page
│   │   ├── dashboard/    # Dashboard and protected routes
│   │   └── layout.tsx    # Root layout
│   ├── components/       # Reusable React components
│   │   └── ui/          # UI components (buttons, forms, etc.)
│   ├── services/        # API service layer
│   │   ├── auth.service.ts
│   │   └── api.service.ts
│   ├── lib/             # Utilities and configurations
│   │   └── api.ts       # Axios configuration
│   ├── types/           # TypeScript type definitions
│   │   └── api.ts       # API types matching backend schemas
│   ├── hooks/           # Custom React hooks
│   └── stores/          # State management (Zustand)
├── public/              # Static assets
├── next.config.js       # Next.js configuration
├── tailwind.config.js   # Tailwind CSS configuration
└── tsconfig.json        # TypeScript configuration
```

## 🔑 Authentication

Default admin credentials for development:
- **Username:** admin@picobrain.com
- **Password:** admin123

## 🛠️ Available Scripts

```bash
# Development
npm run dev          # Start development server

# Production
npm run build        # Build for production
npm run start        # Start production server

# Code Quality
npm run lint         # Run ESLint
npm run type-check   # Run TypeScript compiler check
```

## 🎨 Key Features

### Implemented
- ✅ JWT Authentication with token management
- ✅ Protected routes with auth guards
- ✅ Dashboard with statistics overview
- ✅ Responsive sidebar navigation
- ✅ Toast notifications system
- ✅ TypeScript with strict typing
- ✅ Tailwind CSS for styling
- ✅ API service layer with interceptors
- ✅ Error handling and loading states

### Ready for Implementation
- 📋 CRUD interfaces for all entities (persons, clinics, clients, employees, users)
- 📊 Data tables with sorting, filtering, and pagination
- 📝 Forms with validation
- 🔍 Search functionality
- 📈 Charts and analytics
- 🖼️ File upload to AWS S3
- 👤 User profile management
- ⚙️ System settings

## 🚢 Deployment to Vercel

### Method 1: Using Vercel CLI

1. **Install Vercel CLI:**
```bash
npm i -g vercel
```

2. **Deploy:**
```bash
vercel
```

3. **Set environment variables in Vercel:**
```
NEXT_PUBLIC_API_URL=https://your-backend-url.onrender.com
```

### Method 2: GitHub Integration

1. Push code to GitHub
2. Import project in Vercel Dashboard
3. Configure environment variables
4. Deploy automatically on push

## 🔧 Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `NEXT_PUBLIC_API_URL` | Backend API URL | `http://localhost:8000` |
| `NEXT_PUBLIC_APP_NAME` | Application name | `PicoBrain` |
| `NEXT_PUBLIC_APP_VERSION` | App version | `1.0.0` |
| `NEXT_PUBLIC_S3_BUCKET` | AWS S3 bucket name | - |
| `NEXT_PUBLIC_AWS_REGION` | AWS region | - |

## 🎯 Next Steps

1. **Complete CRUD Pages:**
   - Create list, create, edit, and delete pages for each entity
   - Implement data tables with react-table or similar
   - Add form validation with react-hook-form

2. **Enhance UI/UX:**
   - Add loading skeletons
   - Implement error boundaries
   - Add confirmation dialogs
   - Improve mobile responsiveness

3. **Add Features:**
   - Real-time notifications
   - File upload functionality
   - Export to CSV/PDF
   - Advanced search and filters

4. **Performance:**
   - Implement code splitting
   - Add image optimization
   - Configure caching strategies
   - Set up monitoring

## 📚 Technologies Used

- **Framework:** Next.js 15.5.2
- **UI Library:** React 19.1.1
- **Styling:** Tailwind CSS 3.3.0
- **State Management:** Zustand 4.4.7
- **Data Fetching:** React Query 5.17.9
- **HTTP Client:** Axios 1.6.5
- **Language:** TypeScript 5.x
- **Package Manager:** npm/yarn

## 🤝 Contributing

1. Create feature branch: `git checkout -b feature/your-feature`
2. Commit changes: `git commit -m 'Add your feature'`
3. Push to branch: `git push origin feature/your-feature`
4. Submit pull request

## 📝 License

Private and confidential - PicoBrain Healthcare System
