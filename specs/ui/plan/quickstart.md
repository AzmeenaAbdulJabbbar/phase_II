# Quickstart: Phase II Frontend UI Core

**Date**: 2025-12-21
**Feature**: Frontend UI Core
**Branch**: `002-frontend-ui-core`

## Prerequisites

- Node.js 20+ LTS
- pnpm (preferred) or npm
- Backend running at `http://localhost:8000`
- Environment variables configured

---

## 1. Project Setup

```bash
# From project root
cd frontend

# Install dependencies
pnpm install

# Copy environment file
cp .env.example .env.local
```

---

## 2. Environment Variables

Create `frontend/.env.local`:

```env
# Backend API URL
NEXT_PUBLIC_API_URL=http://localhost:8000

# Better Auth Configuration
BETTER_AUTH_SECRET=your-shared-secret-with-backend
NEXT_PUBLIC_AUTH_URL=http://localhost:3000

# Optional: Database for Better Auth (if storing sessions)
DATABASE_URL=postgresql://user:pass@host/db
```

**IMPORTANT**: `BETTER_AUTH_SECRET` must match the backend's secret for JWT verification to work.

---

## 3. Directory Structure

```
frontend/
├── src/
│   ├── app/                    # Next.js App Router
│   │   ├── (auth)/            # Auth route group
│   │   │   ├── signin/page.tsx
│   │   │   ├── signup/page.tsx
│   │   │   └── layout.tsx
│   │   ├── (dashboard)/       # Protected route group
│   │   │   ├── page.tsx       # Main task list
│   │   │   ├── layout.tsx
│   │   │   └── loading.tsx
│   │   ├── layout.tsx         # Root layout
│   │   ├── page.tsx           # Landing/redirect
│   │   └── globals.css
│   ├── components/
│   │   ├── ui/                # Reusable primitives
│   │   ├── layout/            # Navbar, Sidebar
│   │   ├── tasks/             # Task components
│   │   └── auth/              # Auth forms
│   ├── lib/
│   │   ├── api.ts             # API client
│   │   ├── auth.ts            # Better Auth server config
│   │   └── auth-client.ts     # Better Auth client
│   └── types/
│       ├── task.ts
│       ├── api.ts
│       ├── auth.ts
│       └── ui.ts
├── public/
├── tailwind.config.ts
├── next.config.ts
├── tsconfig.json
├── package.json
└── .env.example
```

---

## 4. Key Files to Create

### 4.1 Better Auth Server (`lib/auth.ts`)

```typescript
import { betterAuth } from "better-auth";
import { jwt } from "better-auth/plugins";

export const auth = betterAuth({
  secret: process.env.BETTER_AUTH_SECRET!,
  plugins: [jwt()],
  // Add database adapter if persisting sessions
});

export type Auth = typeof auth;
```

### 4.2 Better Auth Client (`lib/auth-client.ts`)

```typescript
import { createAuthClient } from "better-auth/react";

export const authClient = createAuthClient({
  baseURL: process.env.NEXT_PUBLIC_AUTH_URL,
});

export const { useSession, signIn, signUp, signOut } = authClient;
```

### 4.3 API Client (`lib/api.ts`)

See `contracts/api-client.md` for full implementation.

### 4.4 Middleware (`middleware.ts`)

```typescript
import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';

export function middleware(request: NextRequest) {
  const { pathname } = request.nextUrl;

  // Check for session cookie/token
  const token = request.cookies.get('better-auth.session_token');

  // Protect dashboard routes
  if (pathname.startsWith('/dashboard') && !token) {
    return NextResponse.redirect(new URL('/signin', request.url));
  }

  // Redirect authenticated users from auth pages
  if ((pathname === '/signin' || pathname === '/signup') && token) {
    return NextResponse.redirect(new URL('/dashboard', request.url));
  }

  return NextResponse.next();
}

export const config = {
  matcher: ['/dashboard/:path*', '/signin', '/signup'],
};
```

---

## 5. Development Commands

```bash
# Start development server
pnpm dev

# Build for production
pnpm build

# Run production build
pnpm start

# Type checking
pnpm type-check

# Linting
pnpm lint

# Format code
pnpm format
```

---

## 6. Testing Strategy

### Unit Tests (Vitest)

```bash
pnpm test           # Run tests
pnpm test:watch     # Watch mode
pnpm test:coverage  # With coverage
```

### E2E Tests (Playwright - future)

```bash
pnpm test:e2e
```

---

## 7. Development Workflow

1. **Start backend first**:
   ```bash
   cd backend
   uvicorn src.main:app --reload
   ```

2. **Start frontend**:
   ```bash
   cd frontend
   pnpm dev
   ```

3. **Access application**:
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Docs: http://localhost:8000/docs

---

## 8. Common Issues

### CORS Errors

Ensure backend has CORS configured for `http://localhost:3000`:

```python
# backend/src/main.py
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### JWT Token Issues

1. Check that `BETTER_AUTH_SECRET` matches between frontend and backend
2. Verify token is being sent in Authorization header
3. Check token expiration

### Authentication Redirect Loop

Check middleware is correctly reading the session cookie name.

---

## 9. Next Steps After Setup

1. Run `pnpm dev` and verify http://localhost:3000 loads
2. Test authentication flow (signup → signin → dashboard)
3. Verify task CRUD operations work
4. Check optimistic updates are smooth
5. Test error handling (network errors, 401/403/404)
