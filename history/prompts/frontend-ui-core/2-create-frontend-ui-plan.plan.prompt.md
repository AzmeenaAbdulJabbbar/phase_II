---
id: 2
title: Create Frontend UI Implementation Plan
stage: plan
date: 2025-12-22
surface: agent
model: claude-sonnet-4.5
feature: frontend-ui-core
branch: 002-frontend-ui-core
user: system
command: /sp.plan
labels: ["frontend", "planning", "next.js", "better-auth", "api-client", "architecture"]
links:
  spec: specs/ui/frontend-core.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/ui/plan/research.md
  - specs/ui/plan/data-model.md
  - specs/ui/plan/contracts/api-client.md
  - specs/ui/plan/quickstart.md
  - specs/ui/plan/plan.md
tests:
  - N/A (planning phase)
---

## Prompt

/sp.plan @specs/ui/frontend-core.md "Design the Next.js monorepo structure in /frontend: 1. Auth Setup: Better Auth client configuration with JWT. 2. API Client: Implementation of 'apiClient' in 'lib/api.ts' that injects the Bearer token. 3. Layout: Root layout with Tailwind styling and Navbar. 4. Pages: Sign-in, Sign-up, and the main Dashboard."

## Response snapshot

Generated comprehensive implementation plan for Frontend UI Core with 5 supporting artifacts:

**research.md** - Technology decisions:
1. Better Auth with JWT plugin configuration
2. Custom fetch wrapper for API client (chosen over axios/TanStack Query)
3. App Router with route groups ((auth)/ and (dashboard)/)
4. Feature-based component organization
5. useState + useOptimistic for state management
6. Tailwind CSS utility-first styling
7. Native forms with Server Actions

**data-model.md** - TypeScript types:
- Task, TaskCreate, TaskUpdate, OptimisticTask
- ApiSuccessResponse, ApiErrorResponse, ResponseMeta
- User, Session, AuthState
- TaskFilter, TaskSort, LoadingState, ModalState
- Form state types with validation error structures

**contracts/api-client.md** - API integration spec:
- Full endpoint documentation (health, CRUD operations)
- Error handling contract with ApiError class
- Token injection implementation pattern
- Usage examples with optimistic updates

**quickstart.md** - Developer setup:
- Prerequisites and environment configuration
- Directory structure reference
- Key file templates (auth.ts, middleware.ts)
- Development commands and workflow

**plan.md** - Master implementation plan:
- 5 implementation phases
- Component architecture table
- Page flow diagrams
- Data flow patterns (loading, create, toggle)
- Error handling strategy
- Security considerations
- Constitution compliance checklist

## Outcome

- ✅ Impact: High - Complete architectural blueprint for frontend development
- 🧪 Tests: N/A (planning phase - tests defined in future tasks)
- 📁 Files: 5 files created (research.md, data-model.md, api-client.md, quickstart.md, plan.md)
- 🔁 Next prompts: /sp.tasks to generate atomic task list from plan
- 🧠 Reflection: Plan follows Constitution mandates (Better Auth, JWT Bridge, Tailwind). Decided on simpler patterns (native forms, local state) over complex libraries for MVP.

## Evaluation notes (flywheel)

- Failure modes observed: None - all artifacts generated successfully
- Graders run and results (PASS/FAIL): Plan artifacts complete - PASS
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Run /sp.tasks to validate plan is actionable
