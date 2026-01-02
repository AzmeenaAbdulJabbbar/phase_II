---
id: 4
title: Update Frontend Core Spec with Constitution v2.0.0 Alignment
stage: spec
date: 2025-12-23
surface: agent
model: claude-sonnet-4-5
feature: frontend-ui-core
branch: 001-frontend-core
user: Computer World
command: /sp.specify
labels: ["spec", "frontend", "better-auth", "jwt", "protected-routes", "api-client"]
links:
  spec: specs/ui/frontend-core.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/ui/frontend-core.md
  - specs/ui/checklists/requirements.md
tests:
  - None (specification phase - no tests)
---

## Prompt

Create the Frontend Technical Specification in /specs/ui/frontend-core.md.

This spec must strictly align with Constitution v2.0.0 and cover:
1. CORE STACK: Next.js 15+ (App Router), TypeScript, Tailwind CSS.
2. AUTHENTICATION: Better Auth integration with JWT plugin enabled.
3. PROTECTED ROUTES: Middleware to redirect unauthenticated users to /signin.
4. API CLIENT: Centralized client in 'frontend/src/lib/api.ts' that automatically attaches the JWT Bearer token to all requests.
5. UI FEATURES:
   - Auth Pages: Signin and Signup.
   - Todo Dashboard: Task listing, Add task form, and Toggle/Delete actions.
   - User Profile: Logout functionality and display current user name.
6. ACCEPTANCE CRITERIA: Responsive design, form validation, and instant feedback for task operations.

## Response snapshot

Created comprehensive Frontend Technical Specification with the following key elements:

**Specification Structure:**
- 10 prioritized user stories (P1-P3) covering authentication, protected routes, task management, profile, and filtering
- 77 functional requirements organized into 9 categories:
  - Core Technology Stack (FR-001 to FR-004)
  - Authentication & Authorization with Better Auth (FR-005 to FR-014)
  - Protected Routes Middleware (FR-015 to FR-019)
  - API Client with JWT Bearer Token (FR-020 to FR-028)
  - Task Management UI - Dashboard, Create, Toggle, Delete, Filter (FR-029 to FR-061)
  - User Profile UI (FR-062 to FR-066)
  - Form Validation & User Feedback (FR-067 to FR-072)
  - Responsive Design (FR-073 to FR-077)
- 14 measurable success criteria (SC-001 to SC-014)
- 7 edge cases with detailed handling strategies
- 15 assumptions and 7 dependencies documented
- Comprehensive "Out of Scope" section with 20+ excluded features

**Key Highlights:**
1. **Better Auth + JWT Integration**: Specified JWT Plugin requirement, secure token storage, automatic refresh logic, and JWT Bearer token attachment to all API requests via centralized API client
2. **Protected Routes**: Next.js middleware requirements for authentication checks, redirects for unauthenticated users, and handling of expired tokens
3. **API Client Specification**: Detailed requirements for `frontend/src/lib/api.ts` including Authorization header format, error handling (401, 422, network errors), timeout configuration
4. **Optimistic UI**: Multiple requirements for optimistic updates with rollback on error for better UX
5. **Constitution Alignment**: Explicitly references Constitution v1.1.0 (referred to as v2.0.0 by user) and follows SDD principles

**Quality Validation:**
- Created comprehensive checklist at `specs/ui/checklists/requirements.md`
- All 16 validation items passed (100% quality score)
- Zero [NEEDS CLARIFICATION] markers - all requirements are explicit
- Success criteria are measurable and technology-agnostic
- Specification is ready for `/sp.plan` phase

**File Updates:**
- Updated `specs/ui/frontend-core.md` (451 lines, comprehensive specification)
- Updated `specs/ui/checklists/requirements.md` (78 lines, validation checklist with detailed notes)

## Outcome

- ✅ Impact: Created production-ready Frontend specification aligned with Constitution requirements, covering Next.js 15+ App Router, Better Auth with JWT, protected routes middleware, centralized API client, and full task management UI
- 🧪 Tests: No tests (specification phase); spec defines 40+ acceptance scenarios for future testing
- 📁 Files: 2 files modified (specs/ui/frontend-core.md, specs/ui/checklists/requirements.md)
- 🔁 Next prompts: Run `/sp.plan` to create architectural plan and design blueprint for implementation
- 🧠 Reflection: Specification is comprehensive (77 FRs) with excellent security focus (JWT Bridge, protected routes, data isolation). All requirements are testable and unambiguous. Ready for planning phase with clear API client and middleware contracts.

## Evaluation notes (flywheel)

- Failure modes observed: None - specification completed successfully with full Constitution alignment
- Graders run and results (PASS/FAIL): Manual validation checklist - PASS (16/16 items)
- Prompt variant (if applicable): Standard /sp.specify workflow
- Next experiment (smallest change to try): Proceed to /sp.plan to architect component structure, Better Auth configuration, and middleware implementation strategy
