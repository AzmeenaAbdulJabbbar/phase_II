---
id: 10
title: Generate Sprint 2 Dashboard Tasks with Atomic Design
stage: tasks
date: 2025-12-23
surface: agent
model: claude-sonnet-4-5
feature: frontend-ui-core
branch: 001-frontend-core
user: Computer World
command: /sp.tasks
labels: ["tasks", "sprint-2", "dashboard-ui", "atomic-design", "optimistic-updates"]
links:
  spec: specs/ui/dashboard-feature.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/ui/dashboard-feature.tasks.md
tests:
  - None (task generation - manual testing checklist in plan)
---

## Prompt

@specs/ui/dashboard-feature.plan.md "Generate atomic tasks for Sprint 2 implementation.

Include:
- Creating UI components (Atomic design).
- Integrating with the API client from Sprint 1.
- Handling loading and empty states."

## Response snapshot

Created atomic task list at `specs/ui/dashboard-feature.tasks.md` with 55 tasks organized by Atomic Design principles.

**Task Organization** (Atomic Design):

**Phase 1: UI Atoms** (4 tasks - all parallelizable):
- T001: Button.tsx (variants, loading, disabled, Tailwind)
- T002: Input.tsx (error state, ARIA, Tailwind)
- T003: Card.tsx (shadow, hover, Tailwind)
- T004: Checkbox.tsx (checked/unchecked, ARIA, Tailwind)

**Phase 2: Navbar Component** (5 tasks):
- T005: Create navbar.tsx (Client Component)
- T006: Integrate useAuth hook for user session
- T007: Implement logout with clientSignOut + toast
- T008: Add responsive styling (hide email mobile <768px)
- T009: Add loading skeleton for session loading

**Phase 3: Dashboard Page** (3 tasks):
- T010: Create (protected)/layout.tsx with Navbar
- T011: Create dashboard/page.tsx (Server Component with api.listTasks)
- T012: Add Tailwind layout styling (max-w-4xl, responsive)

**Phase 4: TaskList Component** (3 tasks):
- T013: Create task-list.tsx (Server Component, map to TaskCard)
- T014: Create EmptyState UI with SVG icon
- T015: Add task count display

**Phase 5: TaskCard Component** (17 tasks):
- T016-T017: Structure and styling
- T018-T024: Toggle completion with optimistic updates (7 tasks)
  - useOptimistic hook
  - handleToggle function
  - api.toggleTask integration
  - Success/error handlers
  - Visual distinction (strikethrough)
  - Loading indicator
- T025-T029: Delete with confirmation (5 tasks)
  - handleDelete with confirmation
  - api.deleteTask integration
  - Success/error handlers
  - Button styling
- T030-T032: Accessibility and details (3 tasks - parallelizable)
  - ARIA labels
  - Description preview
  - Created date display

**Phase 6: AddTaskForm Component** (15 tasks):
- T033-T034: Structure and styling
- T035-T038: Validation (4 tasks)
  - useState for title/titleError
  - validateTitle function
  - onChange handler
  - Disable submit on error
- T039-T045: Submission & optimistic creation (7 tasks)
  - handleSubmit with useTransition
  - api.createTask integration
  - Success/error handlers
  - router.refresh
  - Enter key handler
  - Loading spinner
- T046-T047: Accessibility (2 tasks - parallelizable)
  - ARIA attributes
  - maxLength validation

**Phase 7: Integration & Polish** (8 tasks):
- T048-T051: Dashboard integration (4 tasks)
  - Import and render Navbar
  - Import and render AddTaskForm
  - Import and render TaskList
  - Layout wrapper
- T052-T055: Loading & error states (4 tasks - parallelizable)
  - loading.tsx with skeletons
  - Skeleton.tsx component
  - Error handling in page
  - error.tsx boundary

**API Integration** (Sprint 1 dependency):

All tasks use centralized API client from Sprint 1:
- T011: api.listTasks() in Dashboard Page
- T020: api.toggleTask() in TaskCard toggle
- T026: api.deleteTask() in TaskCard delete
- T040: api.createTask() in AddTaskForm

JWT Bearer token automatically attached by API client - no additional work needed.

**Optimistic Updates Pattern** (detailed tasks):

Toggle pattern (T018-T024):
1. T018: Setup useOptimistic hook
2. T019: Apply optimistic update immediately
3. T020: API call with JWT
4. T021: Success handler (refresh)
5. T022: Error handler (rollback + toast)
6. T023: Visual distinction
7. T024: Loading indicator

Create pattern (T039-T045):
1. T039: handleSubmit with useTransition
2. T040: API call (POST)
3. T041: Success (clear form + toast)
4. T042: Error (toast)
5. T043: Refresh server data
6. T044: Enter key support
7. T045: Loading spinner

Delete pattern (T025-T029):
1. T025: Confirmation dialog
2. T026: API call (DELETE)
3. T027: Success (refresh + toast)
4. T028: Error (toast)
5. T029: Button styling

**Loading & Empty States**:

- T009: Navbar loading skeleton (while session loading)
- T014: TaskList empty state ("No tasks yet")
- T024: TaskCard toggle loading ("Updating...")
- T045: AddTaskForm submit loading ("Adding...")
- T052: Dashboard page loading (skeleton cards)
- T053: Reusable Skeleton component
- T054: Dashboard page error handling (try-catch)
- T055: Error boundary UI (error.tsx)

**Dependency Graph**:

Sequential phases with internal parallelization:
- Phase 1: All 4 atoms parallel
- Phase 2: T005 → (T006 || T007 || T008 || T009)
- Phase 3: Sequential
- Phase 4: T013 → (T014 || T015)
- Phase 5: Mostly sequential, T030-T032 parallel at end
- Phase 6: Mostly sequential, T046-T047 parallel at end
- Phase 7: T048-T051 sequential, then T052-T055 parallel

**Parallel Opportunities**: 14 of 55 tasks (25%)

**File Paths** (user-specified):
- ✓ /src/components/dashboard/task-list.tsx (T013)
- ✓ /src/components/dashboard/task-card.tsx (T016)
- ✓ /src/components/dashboard/add-task.tsx (T033)
- ✓ /src/app/dashboard/page.tsx (T011)

Plus atoms and organisms:
- /src/components/ui/* (T001-T004)
- /src/components/layout/navbar.tsx (T005)

**MVP Scope**:
- Phases 1-6: MUST HAVE (core functionality)
- Phase 7: NICE TO HAVE (loading/error polish)

## Outcome

- ✅ Impact: Created 55 atomic, executable tasks for Sprint 2 organized by Atomic Design layers (Atoms → Molecules → Organisms → Templates)
- 🧪 Tests: Manual testing checklist in plan; no automated tests in Sprint 2
- 📁 Files: 1 file created (dashboard-feature.tasks.md)
- 🔁 Next prompts: Run `/sp.implement` to execute Sprint 2 tasks following Atomic Design approach
- 🧠 Reflection: Tasks follow strict checklist format with 14 parallelizable tasks. API integration points clearly mapped to Sprint 1 client. Optimistic update pattern broken into granular steps (7 tasks for toggle, 7 for create, 5 for delete). Loading and empty states comprehensively covered.

## Evaluation notes (flywheel)

- Failure modes observed: None - task generation completed successfully
- Graders run and results (PASS/FAIL): Manual validation - PASS (all tasks follow format, Atomic Design respected)
- Prompt variant (if applicable): Atomic Design task organization with API integration focus
- Next experiment (smallest change to try): Execute tasks and validate Atomic Design approach improves maintainability
