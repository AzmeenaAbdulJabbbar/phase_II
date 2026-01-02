# Phase II Todo App - Frontend

Multi-user task management web application built with Next.js 15+ App Router, Better Auth, and Tailwind CSS.

## Tech Stack

- **Framework**: Next.js 15+ (App Router)
- **Language**: TypeScript (strict mode)
- **Styling**: Tailwind CSS
- **Authentication**: Better Auth with JWT Plugin
- **UI Components**: React 18+
- **Notifications**: Sonner (toast notifications)

## Prerequisites

- Node.js 20+ LTS
- npm or pnpm
- PostgreSQL database (for Better Auth session storage)
- Backend API running on port 8000

## Setup Instructions

### 1. Install Dependencies

```bash
npm install
# or
pnpm install
```

### 2. Environment Configuration

Copy `.env.example` to `.env.local` and update the values:

```bash
cp .env.example .env.local
```

Required environment variables:

- `NEXT_PUBLIC_API_URL`: Backend API URL (default: http://localhost:8000/api)
- `BETTER_AUTH_SECRET`: Shared secret with backend (MUST match backend secret)
- `DATABASE_URL`: PostgreSQL connection string

**CRITICAL**: Ensure `BETTER_AUTH_SECRET` matches the backend secret exactly.

### 3. Start Development Server

```bash
npm run dev
```

The app will be available at http://localhost:3000

## Project Structure

```
frontend/
├── src/
│   ├── app/                 # Next.js App Router pages
│   │   ├── layout.tsx       # Root layout with Tailwind
│   │   ├── page.tsx         # Landing page (redirects)
│   │   └── globals.css      # Tailwind imports
│   ├── components/          # React components
│   │   ├── ui/              # Reusable UI primitives
│   │   ├── layout/          # Layout components (Navbar, etc.)
│   │   ├── tasks/           # Task-related components
│   │   └── auth/            # Auth components
│   ├── lib/                 # Utilities and libraries
│   │   ├── api.ts           # API client with JWT Bearer token
│   │   └── auth-client.ts   # Better Auth client utilities
│   ├── types/               # TypeScript type definitions
│   │   ├── auth.ts          # Auth types
│   │   └── task.ts          # Task types
│   ├── auth.ts              # Better Auth server configuration
│   └── middleware.ts        # Route protection middleware
├── public/                  # Static assets
├── .env.example             # Environment variable template
├── .env.local               # Local environment (gitignored)
├── next.config.ts           # Next.js configuration
├── tailwind.config.ts       # Tailwind CSS configuration
├── tsconfig.json            # TypeScript configuration
└── package.json             # Dependencies and scripts
```

## Key Features

- **Authentication**: Email/password with Better Auth and JWT
- **Protected Routes**: Middleware redirects unauthenticated users
- **API Client**: Automatic JWT Bearer token attachment to all requests
- **Task Management**: View, create, toggle, and delete tasks
- **Responsive Design**: Mobile-first design (320px - 1920px)
- **Optimistic Updates**: Instant UI feedback with rollback on error

## Development Commands

- `npm run dev` - Start development server (port 3000)
- `npm run build` - Build for production
- `npm run start` - Start production server
- `npm run lint` - Run ESLint
- `npm run type-check` - Run TypeScript type checking

## Authentication Flow

1. User visits protected route (e.g., /dashboard)
2. Middleware checks for session token
3. If no token → redirect to /signin
4. User logs in → Better Auth issues JWT
5. JWT stored in httpOnly cookie
6. API client automatically attaches JWT to all requests
7. Backend verifies JWT and extracts user_id

## API Integration

The API client (`src/lib/api.ts`) automatically:
- Attaches JWT Bearer token to all requests
- Handles 401 (redirects to /signin)
- Handles 422 (displays validation errors)
- Handles network errors (shows friendly messages)
- Sets 10-second timeout for all requests

## Sprint Status

**Sprint 1: Setup & Auth** - ✅ COMPLETE
- Next.js 15 project initialized
- Better Auth configured with JWT Plugin
- API client with Bearer token injection
- Middleware for protected routes
- Environment files configured

**Sprint 2: Core UI** - PENDING
**Sprint 3: API Integration** - PENDING
**Sprint 4: UX & Polish** - PENDING

## Notes

- This frontend requires the FastAPI backend to be running on port 8000
- Ensure `BETTER_AUTH_SECRET` matches between frontend and backend
- Session tokens are stored in httpOnly cookies for security
- All protected routes automatically redirect to /signin if unauthenticated
