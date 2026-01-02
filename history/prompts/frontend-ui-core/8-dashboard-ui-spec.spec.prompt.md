---
id: 8
title: Dashboard UI Specification for Sprint 2
stage: spec
date: 2025-12-23
surface: agent
model: claude-sonnet-4-5
feature: frontend-ui-core
branch: 001-frontend-core
user: Computer World
command: /sp.specify
labels: ["spec", "dashboard", "ui-components", "optimistic-updates", "responsive-design"]
links:
  spec: specs/ui/dashboard-feature.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/ui/dashboard-feature.md
  - specs/ui/dashboard-checklists/requirements.md
tests:
  - None (specification phase - no tests)
---

## Prompt

"Refine the UI specification for Sprint 2: Core Dashboard UI in /specs/ui/dashboard-feature.md.

1. COMPONENTS:
   - Navbar: User Profile display aur Logout button.
   - TaskList: List view for todos.
   - TaskCard: Individual todo item with status toggle.
   - AddTaskForm: Input field for new tasks.
2. DESIGN:
   - Tailwind CSS based, mobile-responsive, and accessible.
3. DATA FLOW:
   - Dashboard must fetch from GET /api/{user_id}/tasks.
   - Support optimistic updates for toggling completion."

## Response snapshot

Created refined Dashboard UI specification at `specs/ui/dashboard-feature.md` with detailed requirements for Sprint 2 components.

**Specification Structure:**

**8 User Stories** (P1-P3 prioritized):
- P1: View Dashboard with TaskList (US1)
- P1: User Profile Display in Navbar (US2)
- P1: Logout from Navbar (US3)
- P1: Toggle Task Completion with Optimistic Updates (US4)
- P1: Create New Task from Dashboard (US5)
- P2: Delete Task from TaskCard (US6)
- P2: Responsive Dashboard Layout (US7)
- P3: Accessible Dashboard Components (US8)

**72 Functional Requirements** organized by component:

1. **Dashboard Layout & Structure** (FR-001 to FR-005):
   - Navbar at top, TaskList as main content, AddTaskForm above list
   - Responsive 320px-1920px
   - Fetch tasks on load from GET /api/{user_id}/tasks

2. **Navbar Component** (FR-006 to FR-012):
   - Client Component with user email display
   - Logout button with Better Auth signOut
   - Responsive (collapse email on mobile <768px)
   - Accessible with ARIA labels

3. **TaskList Component** (FR-013 to FR-019):
   - Fetch from GET /api/{user_id}/tasks with JWT Bearer token
   - Render TaskCard for each task
   - EmptyState when tasks array is empty
   - Loading skeleton during fetch
   - Error handling with retry button

4. **TaskCard Component** (FR-020 to FR-028):
   - Client Component with title, checkbox, delete button
   - Display description preview (2 lines)
   - Show relative timestamp ("2 hours ago")
   - Visual distinction for completed tasks (strikethrough, muted color)
   - Delete confirmation dialog

5. **TaskCard Optimistic Updates** (FR-029 to FR-035):
   - Immediate UI update before API call (useOptimistic hook)
   - PATCH /api/tasks/{id} with JWT Bearer token
   - Rollback on API failure
   - Loading indicator during API call
   - Error toast on failure
   - Disable during pending (prevent race conditions)

6. **TaskCard Delete Functionality** (FR-036 to FR-041):
   - Confirmation dialog ("Are you sure?")
   - Optimistic deletion (disappears immediately)
   - DELETE /api/tasks/{id} with JWT Bearer token
   - Rollback on failure (reappears)
   - Error toast

7. **AddTaskForm Component** (FR-042 to FR-048):
   - Client Component with title input and submit button
   - Validation: required, 1-200 characters
   - Real-time validation feedback
   - Disable submit on validation failure
   - Clear input after success

8. **AddTaskForm Optimistic Creation** (FR-049 to FR-054):
   - Optimistic TaskCard appears immediately
   - POST /api/tasks with JWT Bearer token
   - Replace optimistic with server response
   - Rollback on failure
   - Error toast
   - Loading spinner on submit button

9. **Responsive Design** (FR-055 to FR-060):
   - Tailwind CSS utility classes only
   - Navbar, TaskList, TaskCard, AddTaskForm all responsive
   - Minimum 44x44px touch targets

10. **Accessibility** (FR-061 to FR-067):
    - ARIA labels on all interactive elements
    - Keyboard navigation (Tab, Enter)
    - Form errors with aria-describedby

11. **Data Flow** (FR-068 to FR-072):
    - GET /api/{user_id}/tasks on dashboard load
    - JWT Bearer token on ALL requests
    - Re-fetch after mutations
    - Error handling (401, 422, 500, network)

**14 Success Criteria**:
- SC-001: Dashboard loads within 2 seconds
- SC-002: Navbar displays email within 500ms
- SC-003: Optimistic toggle within 50ms
- SC-004: Optimistic create within 50ms
- SC-005: 100% API calls include JWT Bearer token
- SC-006: Optimistic rollback within 100ms on error
- SC-007: Error toasts within 500ms
- SC-008: Logout redirects within 1 second
- SC-009: Mobile usable at 320px without horizontal scroll
- SC-010: 100% keyboard-accessible
- SC-011: 100 tasks without performance degradation
- SC-012: AddTaskForm clears within 200ms after success
- SC-013: Delete dialog within 100ms
- SC-014: GET request completes within 1 second

**Key Specifications:**

1. **Component Architecture**:
   - Navbar: Client Component (logout interactivity)
   - TaskList: Server or Client Component (fetch tasks)
   - TaskCard: Client Component (toggle, delete interactivity)
   - AddTaskForm: Client Component (form submission)

2. **Optimistic Updates Pattern**:
   - Immediate UI update using useOptimistic hook or local state
   - API call sent with JWT Bearer token
   - On success: confirm update
   - On failure: rollback + error toast
   - Loading indicator during pending state

3. **Data Flow**:
   - Dashboard fetches: GET /api/{user_id}/tasks (Note: backend may use /api/tasks and extract user_id from JWT)
   - Create task: POST /api/tasks
   - Toggle completion: PATCH /api/tasks/{id}
   - Delete task: DELETE /api/tasks/{id}
   - All requests include Authorization: Bearer <token>

4. **Responsive Design**:
   - Mobile (<768px): Full-width cards, collapsed Navbar
   - Tablet (768px-1023px): Single column, full Navbar
   - Desktop (1024px+): Max-width constrained, full Navbar
   - Min touch target: 44x44px

5. **Accessibility**:
   - ARIA labels on buttons, checkboxes
   - Keyboard navigation (Tab, Enter, Escape)
   - Screen reader support
   - Form error associations (aria-describedby)

**Edge Cases Addressed**:
- Empty task list → EmptyState component
- Rapid toggle clicks → Debounce/disable during pending
- Page refresh during optimistic update → Server state is source of truth
- Slow API (>2s) → Loading skeleton + timeout
- 1000+ tasks → Performance consideration (no pagination in Sprint 2)
- Enter key in form → Submit task
- Network loss → Rollback + error toast

**Assumptions** (15 total):
- Backend API running on port 8000
- Backend endpoints exist (GET, POST, PATCH, DELETE /api/tasks)
- Backend extracts user_id from JWT (frontend doesn't include in URL)
- JWT token valid and available in Better Auth session
- Title validation (1-200 chars) matches backend exactly
- Modern browsers with JavaScript enabled

**Dependencies**:
- Sprint 1 MUST be complete (Better Auth, API client, middleware)
- Backend API with task endpoints
- API client with JWT Bearer token injection (lib/api.ts)
- Type definitions (Task, TaskCreate)
- Tailwind CSS configured
- Sonner library for toasts

**Quality Validation**: 16/16 checklist items passed (100%)

## Outcome

- ✅ Impact: Created focused Sprint 2 specification for Core Dashboard UI with 4 components (Navbar, TaskList, TaskCard, AddTaskForm), optimistic updates, responsive design, and accessibility
- 🧪 Tests: No tests (specification phase); spec defines 30+ acceptance scenarios for testing
- 📁 Files: 2 files created (dashboard-feature.md, dashboard-checklists/requirements.md)
- 🔁 Next prompts: Continue Sprint 2 implementation with refined component requirements or run `/sp.plan` if architectural decisions needed
- 🧠 Reflection: Specification provides comprehensive component requirements (72 FRs) with detailed optimistic update patterns, responsive design (320px-1920px), and accessibility. Ready for immediate Sprint 2 implementation.

## Evaluation notes (flywheel)

- Failure modes observed: None - specification completed successfully with all component requirements
- Graders run and results (PASS/FAIL): Manual validation checklist - PASS (16/16 items)
- Prompt variant (if applicable): Refinement specification (focused on Sprint 2 dashboard components)
- Next experiment (smallest change to try): Proceed with Sprint 2 implementation using this refined spec for component details
