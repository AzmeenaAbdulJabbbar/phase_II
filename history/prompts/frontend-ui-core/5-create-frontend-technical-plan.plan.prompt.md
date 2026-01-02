---
id: 5
title: Create Frontend Technical Plan with Architectural Requirements
stage: plan
date: 2025-12-23
surface: agent
model: claude-sonnet-4-5
feature: frontend-ui-core
branch: 001-frontend-core
user: Computer World
command: /sp.plan
labels: ["plan", "architecture", "better-auth", "api-client", "server-components", "client-components"]
links:
  spec: specs/ui/frontend-core.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/ui/frontend-core.plan.md
  - specs/ui/plan/research.md
  - specs/ui/plan/data-model.md
  - specs/ui/plan/quickstart.md
  - specs/ui/plan/contracts/api-client.ts
  - specs/ui/plan/contracts/auth-client.ts
tests:
  - None (planning phase - no tests)
---

## Prompt

@specs/ui/frontend-core.md "Generate a Technical Plan for the Next.js frontend in /specs/ui/frontend-core.plan.md.

ARCHITECTURAL REQUIREMENTS:
1. MONOREPO SYNC: Plan files inside the '/frontend' directory.
2. AUTH SETUP: Plan 'frontend/src/auth.ts' for Better Auth configuration.
3. API WRAPPER: Design a fetch wrapper that handles the 'BETTER_AUTH_SECRET' handshake and includes the 'user_id' in URL paths.
4. COMPONENT TREE:
   - Navbar, TaskCard, TaskList, and AuthForm components.
5. STATE MANAGEMENT: Use React Server Components for fetching and Client Components for interactivity (toggling tasks)."

## Response snapshot

Created comprehensive Technical Plan at `specs/ui/frontend-core.plan.md` aligned with user's specific architectural requirements and Constitution v1.1.0.

**Plan Structure:**
- **Summary**: Production-ready frontend in `/frontend` with Better Auth, API client, and component tree (Navbar, TaskCard, TaskList, AuthForm)
- **Technical Context**: Next.js 15+, TypeScript strict, Better Auth + JWT, Tailwind CSS, performance goals aligned with 14 SC criteria
- **Constitution Check**: ✅ PASS - All 6 constitutional principles satisfied
- **Project Structure**: Detailed `/frontend` directory layout with exact file locations

**Architectural Decisions Documented:**

1. **AUTH SETUP (`frontend/src/auth.ts`)**:
   - Better Auth configuration with JWT Plugin enabled
   - Shared `BETTER_AUTH_SECRET` with backend (Constitution IV requirement)
   - httpOnly cookies for secure token storage
   - Email/password provider with min 8 char password
   - Complete implementation blueprint provided

2. **API WRAPPER (`frontend/src/lib/api.ts`)**:
   - Custom fetch wrapper with automatic JWT Bearer token injection
   - Handles `BETTER_AUTH_SECRET` via Authorization header
   - Optional `user_id` extraction from JWT for URL paths (backend extracts from token)
   - Centralized error handling: 401 (redirect to /signin), 422 (validation errors), network errors
   - Timeout configuration (10 seconds)
   - Methods: get, post, patch, delete + convenience methods (listTasks, createTask, toggleTask, deleteTask)
   - Complete implementation blueprint provided (150+ lines)

3. **COMPONENT TREE**:
   - **Navbar** (Client Component): User email display, profile dropdown, logout button
   - **TaskList** (Server Component): Fetches tasks server-side via `api.listTasks()`, passes to TaskCard children
   - **TaskCard** (Client Component): Interactive checkbox for toggle, delete button, optimistic updates with `useOptimistic`
   - **AuthForm** (Client Component): Unified form for signin/signup, real-time validation, error handling
   - Component tree diagram provided showing Server/Client component split

4. **STATE MANAGEMENT**:
   - Server Components (TaskList) for data fetching (zero client JavaScript)
   - Client Components (TaskCard, AuthForm) for interactivity with `'use client'` directive
   - Local state with `useState` for form inputs, UI state
   - `useOptimistic` hook for optimistic updates (toggle, delete) with rollback on error
   - No global state management (Zustand/Redux) - unnecessary for server-driven app

5. **NEXT.JS MIDDLEWARE**:
   - Route protection at `frontend/src/middleware.ts`
   - Protects `/dashboard/*` and `/profile/*` routes
   - Redirects unauthenticated users to `/signin` (FR-017)
   - Redirects authenticated users from auth pages to `/dashboard` (FR-018)
   - Complete implementation blueprint provided

**Implementation Blueprints Provided:**

- `frontend/src/auth.ts` - Better Auth server config (40 lines)
- `frontend/src/lib/api.ts` - API client with Bearer token (150+ lines)
- `frontend/src/components/layout/Navbar.tsx` - Navbar with dropdown (60 lines)
- `frontend/src/components/tasks/TaskList.tsx` - Server Component (20 lines)
- `frontend/src/components/tasks/TaskCard.tsx` - Client Component with optimistic updates (80 lines)
- `frontend/src/components/auth/AuthForm.tsx` - Unified auth form (150+ lines)
- `frontend/src/middleware.ts` - Protected route middleware (40 lines)

**Supporting Artifacts:**
- Research.md: Technology decisions (Next.js App Router, Better Auth, API patterns)
- Data Model: TypeScript types (Task, TaskCreate, User, Session, AuthState)
- Contracts: API client interface, Auth client interface
- Quickstart: Setup instructions for development

**Implementation Phases (9 phases for /sp.tasks)**:
A. Project setup & configuration
B. Auth configuration (auth.ts, middleware.ts)
C. API client (lib/api.ts)
D. UI primitives (Button, Input, Card, etc.)
E. Layout components (Navbar, ProfileDropdown)
F. Auth pages & AuthForm
G. Dashboard & Task components (TaskList, TaskCard)
H. Optimistic updates & error handling
I. Testing & polish

**Risk Analysis**: 7 risks identified with mitigations (JWT mismatch, CORS, token expiration, network failures, etc.)

**Success Criteria Validation**: All 14 SC criteria mapped to implementation strategies

## Outcome

- ✅ Impact: Created production-ready technical plan for Next.js frontend with Better Auth, API client, and complete component architecture aligned with user's 5 architectural requirements
- 🧪 Tests: No tests (planning phase); plan defines testing strategy in Phase I
- 📁 Files: 1 new file (frontend-core.plan.md), 5 existing supporting files verified (research.md, data-model.md, quickstart.md, contracts/)
- 🔁 Next prompts: Run `/sp.tasks` to generate atomic task list from plan
- 🧠 Reflection: Plan provides complete implementation blueprints for all critical files (auth.ts, api.ts, Navbar, TaskList, TaskCard, AuthForm, middleware.ts) with 500+ lines of reference code. Server/Client component split clearly defined per user requirement #5.

## Evaluation notes (flywheel)

- Failure modes observed: None - plan completed successfully with all user requirements addressed
- Graders run and results (PASS/FAIL): Manual validation - PASS (all 5 architectural requirements satisfied)
- Prompt variant (if applicable): Standard /sp.plan workflow with specific architectural requirements
- Next experiment (smallest change to try): Proceed to /sp.tasks to break plan into atomic implementation tasks
