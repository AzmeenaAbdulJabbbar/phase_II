# Implementation Plan: Phase II Frontend UI Core

**Feature**: Frontend UI Core
**Branch**: `002-frontend-ui-core`
**Spec**: [frontend-core.md](../frontend-core.md)
**Date**: 2025-12-21

---

## Plan Context

### Objective
Build a Next.js 15+ frontend for the Phase II Todo App that integrates with the FastAPI backend via JWT authentication, providing user registration, login, and complete task management functionality.

### Success Criteria
- Users can sign up, sign in, and sign out
- Authenticated users can create, view, update, and delete tasks
- All API requests include JWT Bearer token (Constitution mandate)
- Responsive UI with Tailwind CSS
- Optimistic updates for smooth UX

---

## 1. Scope

### In Scope
- Next.js 15+ App Router project structure
- Better Auth integration with JWT plugin
- API client with automatic token injection
- Authentication pages (sign-in, sign-up)
- Dashboard with task list
- Task CRUD UI components
- Client-side filtering (all/active/completed)
- Responsive layout with Tailwind CSS

### Out of Scope
- Server-side task filtering (client-side only for MVP)
- Task search functionality
- Task sharing between users
- Email verification flow
- Password reset flow
- Dark mode (future enhancement)

### Non-Goals
- Mobile native app
- Offline support
- Real-time sync (WebSocket)

---

## 2. Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                         Browser                                  │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                   Next.js Frontend                       │   │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────────┐  │   │
│  │  │   Better    │  │    API      │  │   React         │  │   │
│  │  │   Auth      │──│   Client    │──│   Components    │  │   │
│  │  │   Client    │  │  (lib/api)  │  │   (tasks, auth) │  │   │
│  │  └─────────────┘  └─────────────┘  └─────────────────┘  │   │
│  │         │                │                               │   │
│  │         └────────────────┼───────────────────────────────│   │
│  │                          │ Authorization: Bearer <jwt>   │   │
│  └──────────────────────────│───────────────────────────────┘   │
└─────────────────────────────│───────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    FastAPI Backend                               │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────────┐ │
│  │    JWT      │  │    CRUD     │  │      PostgreSQL         │ │
│  │    Auth     │──│   Routes    │──│      (Neon DB)          │ │
│  │  Middleware │  │  /api/tasks │  │                         │ │
│  └─────────────┘  └─────────────┘  └─────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
```

---

## 3. Key Technical Decisions

### 3.1 Authentication: Better Auth with JWT

**Decision**: Use Better Auth with JWT plugin for token-based authentication.

**Rationale**:
- Constitution-mandated library
- JWT enables stateless auth compatible with FastAPI backend
- Shared `BETTER_AUTH_SECRET` enables JWT Bridge pattern

**Implementation**:
- Server-side: `lib/auth.ts` - Better Auth configuration
- Client-side: `lib/auth-client.ts` - React hooks and utilities
- Token stored in httpOnly cookie for security

### 3.2 API Client: Custom Fetch Wrapper

**Decision**: Build custom API client instead of using axios/TanStack Query.

**Rationale**:
- No additional dependencies
- Full control over token injection
- Simple enough for MVP requirements
- Standardized error handling

**Implementation**: See `contracts/api-client.md`

### 3.3 Routing: App Router with Route Groups

**Decision**: Use route groups to separate auth and protected pages.

**Rationale**:
- Clean URL structure (no /auth prefix)
- Different layouts for auth vs dashboard
- Middleware-based route protection

**Structure**:
```
(auth)/          → Public auth pages, minimal layout
(dashboard)/     → Protected pages, full layout with navbar
```

### 3.4 State Management: Local State Only

**Decision**: Use React useState + useOptimistic, no global state library.

**Rationale**:
- App is server-driven (data from API)
- Local state limited to filters, forms, optimistic updates
- Reduces complexity for MVP

### 3.5 Styling: Tailwind CSS Utility-First

**Decision**: Pure Tailwind CSS without component library.

**Rationale**:
- Constitution mandate
- Fast prototyping
- Consistent design tokens
- No additional bundle size

---

## 4. Component Architecture

### Layout Components

| Component | Purpose | Location |
|-----------|---------|----------|
| `RootLayout` | HTML structure, providers | `app/layout.tsx` |
| `AuthLayout` | Minimal layout for auth pages | `app/(auth)/layout.tsx` |
| `DashboardLayout` | Full layout with navbar | `app/(dashboard)/layout.tsx` |
| `Navbar` | Navigation, user info, logout | `components/layout/Navbar.tsx` |

### Auth Components

| Component | Purpose | Location |
|-----------|---------|----------|
| `SignInForm` | Email/password login | `components/auth/SignInForm.tsx` |
| `SignUpForm` | Registration form | `components/auth/SignUpForm.tsx` |
| `LogoutButton` | Sign out action | `components/auth/LogoutButton.tsx` |

### Task Components

| Component | Purpose | Location |
|-----------|---------|----------|
| `TaskList` | Container for task cards | `components/tasks/TaskList.tsx` |
| `TaskCard` | Individual task display | `components/tasks/TaskCard.tsx` |
| `TaskForm` | Create/edit task modal | `components/tasks/TaskForm.tsx` |
| `TaskFilters` | Filter buttons | `components/tasks/TaskFilters.tsx` |
| `TaskActions` | Complete/edit/delete buttons | `components/tasks/TaskActions.tsx` |

### UI Primitives

| Component | Purpose |
|-----------|---------|
| `Button` | Styled button with variants |
| `Input` | Form input with error state |
| `Card` | Container with shadow/border |
| `Modal` | Dialog overlay |
| `Skeleton` | Loading placeholder |

---

## 5. Page Flow

### Authentication Flow

```
Landing (/)
    │
    ├── Not authenticated → /signin
    │                           │
    │                           ├── Sign in → Dashboard
    │                           │
    │                           └── "Create account" → /signup
    │                                                     │
    │                                                     └── Sign up → Dashboard
    │
    └── Authenticated → Dashboard (/)
```

### Task Management Flow

```
Dashboard (/)
    │
    ├── View task list (auto-load)
    │
    ├── Filter: all / active / completed
    │
    ├── "Add Task" button → TaskForm modal
    │       │
    │       └── Submit → Optimistic add → API create → Confirm/rollback
    │
    ├── Task card actions:
    │       ├── Checkbox → Toggle complete (optimistic)
    │       ├── Edit icon → TaskForm modal (prefilled)
    │       └── Delete icon → Confirm → Remove (optimistic)
    │
    └── Navbar → "Logout" → Sign out → /signin
```

---

## 6. Data Flow

### Task List Loading

```
1. DashboardLayout mounts
2. useEffect triggers task fetch
3. api.tasks.list() called with JWT
4. Backend returns { data: Task[], meta }
5. setTasks(response.data)
6. TaskList renders TaskCards
```

### Task Creation (Optimistic)

```
1. User submits TaskForm
2. Generate temp ID, create OptimisticTask
3. setTasks([...tasks, optimisticTask])
4. api.tasks.create(data) called
5. Success: Replace temp task with real task
   Failure: Remove temp task, show error
```

### Task Toggle (Optimistic)

```
1. User clicks checkbox
2. setTasks(tasks.map(t => t.id === id ? {...t, completed: !t.completed} : t))
3. api.tasks.update(id, { completed: !task.completed })
4. Success: Keep optimistic state
   Failure: Revert to previous state
```

---

## 7. Error Handling Strategy

### API Errors

| Error | User Message | Action |
|-------|--------------|--------|
| 401 | "Session expired" | Redirect to /signin |
| 403 | "Access denied" | Show error, no retry |
| 404 | "Task not found" | Remove from list |
| 422 | Field-specific errors | Show in form |
| 500 | "Something went wrong" | Show retry button |
| Network | "Connection failed" | Show retry button |

### Form Validation

- Client-side validation before submit
- Server errors mapped to form fields
- Generic errors shown in form alert

---

## 8. Security Considerations

### Authentication
- JWT stored in httpOnly cookie (not localStorage)
- Token refreshed before expiration
- Session validated on each API call

### CSRF Protection
- Same-origin requests only
- Better Auth handles CSRF tokens

### XSS Prevention
- React's automatic escaping
- No dangerouslySetInnerHTML usage
- User input sanitized in forms

---

## 9. Implementation Phases

### Phase 1: Project Foundation
- Initialize Next.js project
- Configure Tailwind CSS
- Set up TypeScript types
- Create directory structure

### Phase 2: Authentication
- Configure Better Auth
- Create auth client
- Build SignIn/SignUp forms
- Implement middleware

### Phase 3: API Integration
- Build API client
- Implement token injection
- Add error handling
- Create type definitions

### Phase 4: Task UI
- Build TaskList component
- Create TaskCard component
- Add TaskForm modal
- Implement filters

### Phase 5: Polish
- Add loading states
- Implement optimistic updates
- Error boundaries
- Responsive design

---

## 10. Dependencies

### Production
```json
{
  "next": "^15.0.0",
  "react": "^19.0.0",
  "react-dom": "^19.0.0",
  "better-auth": "^1.0.0",
  "tailwindcss": "^4.0.0"
}
```

### Development
```json
{
  "typescript": "^5.0.0",
  "@types/react": "^19.0.0",
  "@types/node": "^22.0.0",
  "eslint": "^9.0.0",
  "prettier": "^3.0.0"
}
```

---

## 11. Constitution Compliance Checklist

- [x] **FR-AUTH-01**: Better Auth with JWT plugin
- [x] **FR-API-01**: Custom API client with Bearer token injection
- [x] **FR-API-02**: All /api/* requests authenticated (except health)
- [x] **SEC-01**: User data isolation (via backend)
- [x] **TECH-01**: Next.js 15+ App Router
- [x] **TECH-02**: Tailwind CSS utility-first
- [x] **TECH-03**: TypeScript strict mode

---

## 12. Related Documents

- [Research](./research.md) - Technology decision rationale
- [Data Model](./data-model.md) - TypeScript type definitions
- [API Contract](./contracts/api-client.md) - Backend integration spec
- [Quickstart](./quickstart.md) - Developer setup guide
- [Feature Spec](../frontend-core.md) - Requirements and user stories

---

## 13. Risks and Mitigations

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Better Auth compatibility | Low | High | Test early, fallback to manual JWT |
| Token refresh timing | Medium | Medium | 5-min buffer before expiry |
| Optimistic update race conditions | Medium | Low | Queue updates, use request IDs |

---

## 14. Open Questions

1. **Session storage**: Database vs cookie-only for Better Auth sessions?
   - **Resolution**: Start with cookie-only for simplicity

2. **Form library**: Use react-hook-form or native forms?
   - **Resolution**: Native forms for MVP simplicity

3. **Testing**: Vitest vs Jest?
   - **Resolution**: Vitest (faster, ESM-native)
