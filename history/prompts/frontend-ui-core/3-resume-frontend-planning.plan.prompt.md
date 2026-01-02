---
id: 3
title: Resume Frontend UI Core Planning
stage: plan
date: 2025-12-23
surface: agent
model: claude-sonnet-4.5
feature: frontend-ui-core
branch: 002-frontend-ui-core
user: Computer World
command: /sp.plan (resumed)
labels: ["frontend", "planning", "next.js", "better-auth", "api-client", "resume"]
links:
  spec: specs/ui/frontend-core.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/ui/plan.md (created - comprehensive implementation plan)
  - specs/ui/plan/contracts/api-client.ts (created)
  - specs/ui/plan/contracts/auth-client.ts (created)
tests:
  - N/A (planning phase)
---

## Prompt

User: resume

Then invoked: /sp.plan @specs/ui/frontend-core.md "Design the Next.js monorepo structure in /frontend:
1. Auth Setup: Better Auth client configuration with JWT.
2. API Client: Implementation of 'apiClient' in 'lib/api.ts' that injects the Bearer token.
3. Layout: Root layout with Tailwind styling and Navbar.
4. Pages: Sign-in, Sign-up, and the main Dashboard."

## Response snapshot

**Session Resumed**: Continued from PHR #2 (previous planning session)

**Context Loaded**:
- Feature spec: specs/ui/frontend-core.md ✓
- Constitution: .specify/memory/constitution.md ✓
- Previous artifacts: research.md, data-model.md, quickstart.md ✓

**New Artifacts Created**:

1. **specs/ui/plan/contracts/api-client.ts** - TypeScript API client contract:
   - IApiClient interface (get, post, put, patch, delete methods)
   - ITaskApi interface (list, get, create, update, delete, toggleComplete)
   - ApiError class with type guards (isAuthError, isNotFoundError, isValidationError)
   - Complete usage examples with Bearer token injection pattern
   - Type-safe responses with TypeScript generics

2. **specs/ui/plan/contracts/auth-client.ts** - Better Auth integration contract:
   - IAuthClient interface (signIn, signUp, signOut, getSession, isAuthenticated)
   - IAuthHooks interface (useSession, useUser, useAuth React hooks)
   - AuthError class with validation type guards
   - AuthMiddleware type for Next.js route protection
   - Complete implementation examples with Better Auth

3. **specs/ui/plan.md** - Master implementation plan:
   - Technical context with performance goals and constraints
   - Constitution check (all gates PASS ✅)
   - Complete project structure (frontend/ directory tree)
   - Phase 0: Research summary (7 key decisions resolved)
   - Phase 1: Design & Contracts summary (data model, API contracts, quickstart)
   - Phase 2: Architecture blueprint (component hierarchy, data flow, auth flow)
   - Implementation phases A-H (for /sp.tasks generation)
   - Risk analysis with mitigation strategies
   - Success criteria validation mapping (SC-001 to SC-010)
   - ADR suggestion for architectural decisions

**Key Architectural Decisions**:
- Next.js App Router with route groups: `(auth)/` and `(dashboard)/`
- Better Auth with JWT Plugin for token management (httpOnly cookies)
- Custom API client class with automatic Bearer token injection
- Optimistic UI updates using React's useOptimistic hook
- Feature-based component organization (ui/, layout/, tasks/, auth/)
- Tailwind CSS utility-first responsive design (320px-1920px)

**Constitution Compliance**: ✅ All requirements satisfied
- Spec-Driven Development: spec.md → plan.md → tasks.md workflow
- Monorepo Architecture: /frontend structure defined
- Technology Stack: Next.js 16+, TypeScript, Tailwind, Better Auth ✓
- Security Protocol: JWT Bridge pattern with Bearer token on every request
- API Patterns: REST conventions, consistent error handling

**Data Flow Pattern**:
User Action → Optimistic Update → API Client (+ Bearer Token) → Backend (JWT Verify + user_id filter) → Response (Success: merge server data | Error: rollback + toast)

**Implementation Readiness**: ✅ COMPLETE
- All unknowns resolved
- All contracts defined
- All patterns documented
- Ready for /sp.tasks command

## Outcome

- ✅ Impact: High - Comprehensive planning artifacts complete, ready for task generation
- 🧪 Tests: N/A (planning phase - will be defined in tasks.md)
- 📁 Files: 3 files created (api-client.ts, auth-client.ts, plan.md)
- 🔁 Next prompts: /sp.tasks to generate atomic, testable task list
- 🧠 Reflection: Successfully resumed planning from previous session. All supporting artifacts (research, data-model, quickstart) were already in place. Created TypeScript contracts and comprehensive plan.md with architecture blueprint, risk analysis, and success criteria mapping. Plan aligns with Constitution principles and user requirements.

## Evaluation notes (flywheel)

- Failure modes observed: Agent context update script missing template (non-blocking)
- Graders run and results: Constitution check PASS, all planning artifacts complete
- Prompt variant: User said "resume" → system loaded previous context and continued /sp.plan workflow
- Next experiment: Run /sp.tasks to validate plan is actionable and generates 8 implementation phases with testable acceptance criteria
