---
id: 6
title: Generate Frontend Task List in 4 Sprints
stage: tasks
date: 2025-12-23
surface: agent
model: claude-sonnet-4-5
feature: frontend-ui-core
branch: 001-frontend-core
user: Computer World
command: /sp.tasks
labels: ["tasks", "sprint-planning", "setup-auth", "core-ui", "api-integration", "ux-polish"]
links:
  spec: specs/ui/frontend-core.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/ui/frontend-core.tasks.md
tests:
  - None (task generation phase - tests defined in tasks)
---

## Prompt

@specs/ui/frontend-core.plan.md "Generate a task list in /specs/ui/frontend-core.tasks.md.

Break it down into:
- Sprint 1: Setup & Auth (Next.js init, Better Auth setup, middleware).
- Sprint 2: Core UI (Navbar, Layout, Auth Pages).
- Sprint 3: API Integration (Task CRUD integration with the Backend).
- Sprint 4: UX & Polish (Loading states, Skeletons, Notifications)."

## Response snapshot

Created comprehensive task list at `specs/ui/frontend-core.tasks.md` with 70 atomic, executable tasks organized into 4 sprints as requested.

**Task Organization**:

**Sprint 1: Setup & Auth** (15 tasks)
- T001-T007: Project initialization (Next.js, TypeScript, Tailwind, env files)
- T008-T011: Better Auth setup (JWT Plugin, auth.ts, auth-client.ts, types)
- T012-T013: Middleware for protected routes
- T014-T015: Root layout setup
- **User Stories**: US1 (Registration), US2 (Login), US3 (Protected Routes)
- **Parallel Opportunities**: 4 tasks (env files, README, auth types)

**Sprint 2: Core UI** (18 tasks)
- T016-T019: UI Primitives (Button, Input, Card, Checkbox)
- T020-T022: Layout components (Navbar, ProfileDropdown, LogoutButton)
- T023-T024: Auth and protected layouts
- T025-T030: AuthForm component with validation
- T031-T033: Auth pages (signin, signup, profile)
- **User Stories**: US1 (Registration), US2 (Login), US8 (Profile Display), US9 (Logout)
- **Parallel Opportunities**: 12 tasks (UI primitives, pages, layout components)

**Sprint 3: API Integration** (22 tasks)
- T034-T041: API Client with JWT Bearer token (types, client class, HTTP methods, error handling)
- T042-T043: TaskList component (Server Component with EmptyState)
- T044-T050: TaskCard component (Client Component with optimistic updates for toggle/delete)
- T051-T055: AddTaskForm component (Client Component with validation and optimistic create)
- T056-T059: Dashboard page and TaskFilters
- **User Stories**: US4 (View Tasks), US5 (Create Task), US6 (Toggle Completion), US7 (Delete Task), US10 (Filter Tasks)
- **Parallel Opportunities**: 8 tasks (after API Client completes, components can be built in parallel)

**Sprint 4: UX & Polish** (10 tasks)
- T060-T062: Loading states and skeletons
- T063-T065: Toast notifications (sonner integration)
- T066-T068: Responsive design and accessibility
- T069-T070: Modal component for AddTaskForm
- **User Stories**: All (cross-cutting UX improvements)
- **Parallel Opportunities**: 8 tasks (all can run in parallel)

**Task Format Compliance**:
- All 70 tasks follow strict checklist format: `- [ ] T### [P?] [US#?] Description with file path`
- Task IDs sequential (T001-T070)
- 32 tasks marked `[P]` for parallel execution
- 52 tasks marked with `[US#]` labels mapping to spec.md user stories
- All tasks include exact file paths

**Dependency Graph**:
- Sprint dependencies are sequential (Sprint 1 → 2 → 3 → 4)
- Within-sprint dependencies documented (e.g., API Client MUST complete before task components)
- Parallel execution examples provided for each sprint
- Clear blocking relationships (Setup blocks UI, UI blocks API Integration, API Integration blocks Polish)

**MVP Scope Definition**:
- Sprint 1 (MUST HAVE): Setup and auth working
- Sprint 2 (MUST HAVE): UI shell complete
- Sprint 3 (MUST HAVE): Core task management (view, create, toggle, delete)
- Sprint 4 (NICE TO HAVE): Can be deferred post-MVP

**Independent Test Criteria** (per sprint):
- Sprint 1: Next.js runs, Better Auth configured, middleware redirects work
- Sprint 2: Navbar shows user email, auth pages functional, form validation works
- Sprint 3: Tasks display, users can CRUD tasks, filter buttons work
- Sprint 4: Loading skeletons appear, toasts show, responsive design verified

**Success Criteria Mapping**:
- All 14 SC criteria mapped to specific tasks
- Example: SC-005 (100% protected routes) → Sprint 1 Middleware (T012-T013)
- Example: SC-007 (Optimistic updates <50ms) → Sprint 3 TaskCard (T045-T047, T050)

**File Paths Reference**:
- Sprint 1: 6 files (auth.ts, middleware.ts, layouts, etc.)
- Sprint 2: 13 files (UI components, auth pages, Navbar, etc.)
- Sprint 3: 9 files (API client, task components, dashboard)
- Sprint 4: 3 files (Skeleton, Modal, loading.tsx)
- Total: 31 files to create/modify

**Incremental Delivery Strategy**:
1. First Increment (Sprint 1): Authentication working
2. Second Increment (Sprint 2): UI shell complete
3. Third Increment (Sprint 3): Core task management
4. Fourth Increment (Sprint 4): Polish & UX

## Outcome

- ✅ Impact: Created immediately executable task list with 70 atomic tasks organized into 4 sprints covering all 10 user stories and 77 functional requirements
- 🧪 Tests: No tests in this phase; independent test criteria defined for each sprint
- 📁 Files: 1 file created (frontend-core.tasks.md with 650+ lines)
- 🔁 Next prompts: Run `/sp.implement` to execute tasks sequentially with automatic checklist updates
- 🧠 Reflection: Task list enables both sequential and parallel execution (32 of 70 tasks parallelizable). Clear MVP scope (Sprints 1-3) vs. nice-to-have (Sprint 4). Each task maps to specific file path and user story for traceability.

## Evaluation notes (flywheel)

- Failure modes observed: None - task generation completed successfully with all 4 sprints defined
- Graders run and results (PASS/FAIL): Manual validation - PASS (all tasks follow checklist format, dependencies clear, parallel opportunities identified)
- Prompt variant (if applicable): Standard /sp.tasks workflow with sprint-based organization
- Next experiment (smallest change to try): Proceed to /sp.implement to execute tasks and validate task granularity is appropriate
