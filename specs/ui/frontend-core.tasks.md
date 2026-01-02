# Implementation Tasks: Frontend UI Core

**Branch**: `001-frontend-core` | **Date**: 2025-12-23
**Spec**: [frontend-core.md](frontend-core.md) | **Plan**: [frontend-core.plan.md](frontend-core.plan.md)

---

## Task Organization

Tasks are organized into **4 Sprints** as requested:
- **Sprint 1**: Setup & Auth (Next.js init, Better Auth setup, middleware)
- **Sprint 2**: Core UI (Navbar, Layout, Auth Pages)
- **Sprint 3**: API Integration (Task CRUD integration with Backend)
- **Sprint 4**: UX & Polish (Loading states, Skeletons, Notifications)

**Task Format Legend**:
- `- [ ] T###` - Sequential task ID
- `[P]` - Parallelizable (can run concurrently with other [P] tasks)
- `[US#]` - User Story number (maps to spec.md user stories)

**Total Tasks**: 65
**Parallel Opportunities**: 32 tasks can run in parallel

---

## Sprint 1: Setup & Auth (15 tasks)

**Goal**: Initialize Next.js project, configure Better Auth with JWT Plugin, implement middleware for protected routes

**User Stories Covered**: US1 (User Registration), US2 (User Login), US3 (Protected Routes)

**Independent Test Criteria**:
- Next.js app runs on localhost:3000
- Better Auth configured with JWT Plugin enabled
- Middleware redirects unauthenticated users to /signin
- Auth pages (/signin, /signup) are accessible

### Phase 1.1: Project Initialization

- [x] T001 Initialize Next.js 15+ project in `/frontend` directory with App Router and TypeScript strict mode
- [x] T002 Configure package.json with required dependencies (next, react, react-dom, typescript, @types/react, @types/node)
- [x] T003 Install and configure Tailwind CSS in frontend/tailwind.config.ts and frontend/src/app/globals.css
- [x] T004 Create tsconfig.json with strict mode enabled and path aliases (@/ for src/)
- [x] T005 [P] Create .env.example file with required environment variables (NEXT_PUBLIC_API_URL, BETTER_AUTH_SECRET, DATABASE_URL)
- [x] T006 [P] Create .env.local file with local development values (gitignored)
- [x] T007 [P] Create frontend/README.md with setup instructions and development commands

### Phase 1.2: Better Auth Setup

- [x] T008 Install Better Auth dependencies (better-auth, @better-auth/jwt) - Added to package.json
- [x] T009 [US1] [US2] Create frontend/src/auth.ts with Better Auth server configuration, JWT Plugin, and email/password provider (min 8 char password)
- [x] T010 [P] [US1] [US2] Create frontend/src/lib/auth-client.ts with Better Auth client utilities and React hooks
- [x] T011 [P] [US1] [US2] Create frontend/src/types/auth.ts with User, Session, and AuthState type definitions

### Phase 1.3: Route Protection Middleware

- [x] T012 [US3] Create frontend/src/middleware.ts with protected route logic (redirect unauthenticated to /signin, authenticated from auth pages to /dashboard)
- [x] T013 [US3] Configure middleware matcher to run on all routes except api, _next/static, _next/image, favicon.ico

### Phase 1.4: Root Layout Setup

- [x] T014 Create frontend/src/app/layout.tsx with root layout (Better Auth Provider, Tailwind global styles)
- [x] T015 [P] Create frontend/src/app/page.tsx as landing page with redirect logic (authenticated → /dashboard, unauthenticated → /signin)

### Phase 1.5: Additional Setup (Bonus Tasks)

- [x] T016A Create next.config.ts with Next.js configuration
- [x] T017A Create postcss.config.js for Tailwind CSS processing
- [x] T018A Create frontend/.gitignore to exclude node_modules, .env.local, etc.
- [x] T019A Create frontend/src/types/task.ts with Task type definitions
- [x] T020A Create frontend/src/lib/api.ts with API client and JWT Bearer token injection

---

## Sprint 2: Core UI (18 tasks)

**Goal**: Build Navbar, Layout components, and Auth pages (Signin/Signup)

**User Stories Covered**: US1 (Registration), US2 (Login), US8 (Profile Display), US9 (Logout)

**Independent Test Criteria**:
- Navbar displays user email when authenticated
- Signin page allows login with email/password
- Signup page allows registration with email/password/confirm
- Form validation works (email format, password length, password match)
- Profile dropdown shows Profile and Logout options

### Phase 2.1: UI Primitives (Reusable Components)

- [ ] T016 [P] Create frontend/src/components/ui/Button.tsx with Tailwind styling and variants (primary, secondary, danger)
- [ ] T017 [P] Create frontend/src/components/ui/Input.tsx with Tailwind styling, error state, and accessibility (aria-invalid, aria-describedby)
- [ ] T018 [P] Create frontend/src/components/ui/Card.tsx with Tailwind styling for task cards
- [ ] T019 [P] Create frontend/src/components/ui/Checkbox.tsx with Tailwind styling for task completion toggle

### Phase 2.2: Layout Components

- [ ] T020 [US8] [US9] Create frontend/src/components/layout/Navbar.tsx as Client Component ('use client') with user email display and profile dropdown
- [ ] T021 [P] [US8] [US9] Create frontend/src/components/layout/ProfileDropdown.tsx as Client Component with Profile and Logout options
- [ ] T022 [P] [US9] Create frontend/src/components/auth/LogoutButton.tsx as Client Component with Better Auth signOut method

### Phase 2.3: Auth Layouts

- [ ] T023 Create frontend/src/app/(auth)/layout.tsx with minimal auth layout (no navbar, centered content)
- [ ] T024 Create frontend/src/app/(protected)/layout.tsx with protected layout (includes Navbar component)

### Phase 2.4: Auth Form Component

- [ ] T025 [US1] [US2] Create frontend/src/components/auth/AuthForm.tsx as Client Component with unified signin/signup form
- [ ] T026 [US1] [US2] Implement real-time email validation in AuthForm (required, valid email format)
- [ ] T027 [US1] [US2] Implement real-time password validation in AuthForm (required, min 8 characters)
- [ ] T028 [US1] Implement confirm password field and validation in AuthForm (passwords must match for signup)
- [ ] T029 [US1] [US2] Implement form submission logic in AuthForm (authClient.signIn for signin, authClient.signUp for signup)
- [ ] T030 [US1] [US2] Implement error handling in AuthForm (display server errors, disable submit on validation errors)

### Phase 2.5: Auth Pages

- [ ] T031 [P] [US2] Create frontend/src/app/(auth)/signin/page.tsx with AuthForm component in signin mode
- [ ] T032 [P] [US1] Create frontend/src/app/(auth)/signup/page.tsx with AuthForm component in signup mode
- [ ] T033 [P] [US8] Create frontend/src/app/(protected)/profile/page.tsx with user profile display (email, created date)

---

## Sprint 3: API Integration (22 tasks)

**Goal**: Implement API client with JWT Bearer token, integrate Task CRUD operations with Backend

**User Stories Covered**: US4 (View Tasks), US5 (Create Task), US6 (Toggle Completion), US7 (Delete Task), US10 (Filter Tasks)

**Independent Test Criteria**:
- API client attaches JWT Bearer token to all requests
- Dashboard displays tasks fetched from backend
- Users can create new tasks
- Users can toggle task completion
- Users can delete tasks
- Filter buttons (All/Active/Completed) work

### Phase 3.1: API Client & Types

- [ ] T034 Create frontend/src/types/task.ts with Task, TaskCreate, TaskUpdate, and TaskFilter type definitions
- [ ] T035 Create frontend/src/types/api.ts with ApiError, ApiResponse type definitions
- [ ] T036 [US4] [US5] [US6] [US7] Create frontend/src/lib/api.ts with ApiClient class (getToken, request method with Bearer token injection)
- [ ] T037 [US4] [US5] [US6] [US7] Implement HTTP methods in ApiClient (get, post, patch, delete with timeout and error handling)
- [ ] T038 [US4] [US5] [US6] [US7] Implement 401 error handling in ApiClient (redirect to /signin on unauthorized)
- [ ] T039 [US4] [US5] [US6] [US7] Implement 422 error handling in ApiClient (display validation errors)
- [ ] T040 [US4] [US5] [US6] [US7] Implement network error handling in ApiClient (timeout, connection refused)
- [ ] T041 [P] [US4] [US5] [US6] [US7] Implement convenience methods in ApiClient (listTasks, createTask, toggleTask, deleteTask)

### Phase 3.2: Task List Component (Server Component)

- [ ] T042 [US4] Create frontend/src/components/tasks/TaskList.tsx as Server Component (NO 'use client') that fetches tasks via api.listTasks()
- [ ] T043 [P] [US4] Create frontend/src/components/tasks/EmptyState.tsx with message "No tasks yet. Create your first task to get started!"

### Phase 3.3: Task Card Component (Client Component with Optimistic Updates)

- [ ] T044 [US6] [US7] Create frontend/src/components/tasks/TaskCard.tsx as Client Component ('use client') with task display
- [ ] T045 [US6] Implement toggle completion in TaskCard with useOptimistic hook (optimistic UI update before API call)
- [ ] T046 [US6] Implement toggle completion API call in TaskCard (api.toggleTask with JWT Bearer token)
- [ ] T047 [US6] Implement optimistic update rollback in TaskCard on API error (revert to original state, show error toast)
- [ ] T048 [US7] Implement delete button in TaskCard with confirmation dialog ("Are you sure you want to delete this task?")
- [ ] T049 [US7] Implement delete task API call in TaskCard (api.deleteTask with JWT Bearer token)
- [ ] T050 [US7] Implement optimistic delete update in TaskCard (task removed immediately, rollback on error)

### Phase 3.4: Add Task Form Component

- [ ] T051 [US5] Create frontend/src/components/tasks/AddTaskForm.tsx as Client Component with modal/inline form
- [ ] T052 [US5] Implement title input with real-time validation in AddTaskForm (required, 1-200 characters)
- [ ] T053 [US5] Implement optional description input in AddTaskForm (max 2000 characters)
- [ ] T054 [US5] Implement form submission in AddTaskForm (api.createTask with JWT Bearer token, optimistic UI update)
- [ ] T055 [US5] Implement error handling in AddTaskForm (rollback optimistic update on API error, show error toast)

### Phase 3.5: Dashboard Page & Filter

- [ ] T056 [US4] Create frontend/src/app/(protected)/dashboard/page.tsx with TaskList component and AddTaskForm
- [ ] T057 [P] [US10] Create frontend/src/components/tasks/TaskFilters.tsx as Client Component with All/Active/Completed buttons
- [ ] T058 [P] [US10] Implement filter state management in TaskFilters (useState for filter selection)
- [ ] T059 [P] [US10] Implement client-side filtering logic in dashboard page (useMemo to filter tasks by completed status)

---

## Sprint 4: UX & Polish (10 tasks)

**Goal**: Add loading states, skeletons, toast notifications, and responsive design polish

**User Stories Covered**: All (cross-cutting UX improvements)

**Independent Test Criteria**:
- Loading skeletons appear while data is fetching
- Toast notifications show for success/error operations
- Application is responsive on mobile (320px) and desktop (1920px)
- All forms have proper accessibility (ARIA labels, keyboard navigation)

### Phase 4.1: Loading States & Skeletons

- [ ] T060 [P] Create frontend/src/components/ui/Skeleton.tsx with Tailwind shimmer animation for loading states
- [ ] T061 Create frontend/src/app/(protected)/loading.tsx with loading skeleton for dashboard (TaskCard skeletons)
- [ ] T062 Implement loading spinner in Button component (show spinner when isSubmitting prop is true)

### Phase 4.2: Toast Notifications

- [ ] T063 [P] Install sonner library for toast notifications (npm install sonner)
- [ ] T064 Add Toaster component to frontend/src/app/layout.tsx for global toast notifications
- [ ] T065 Implement toast notifications for all task operations (success: "Task created", error: "Failed to create task. Please try again.")

### Phase 4.3: Responsive Design & Accessibility

- [ ] T066 [P] Test responsive design on mobile (320px), tablet (768px), and desktop (1920px) widths
- [ ] T067 [P] Add ARIA labels to all interactive elements (buttons, inputs, checkboxes)
- [ ] T068 [P] Test keyboard navigation for all forms and interactive components (Tab, Enter, Esc)

### Phase 4.4: Modal Component

- [ ] T069 [P] Create frontend/src/components/ui/Modal.tsx with Tailwind styling, backdrop, and close button
- [ ] T070 Update AddTaskForm to use Modal component for better UX (modal opens on "Add Task" button click)

---

## Dependency Graph

### Sprint Dependencies (Sequential)

```
Sprint 1 (Setup & Auth)
    ↓
Sprint 2 (Core UI)
    ↓
Sprint 3 (API Integration)
    ↓
Sprint 4 (UX & Polish)
```

### User Story Dependencies (Within Sprints)

**Sprint 1**:
- US1, US2, US3 can be implemented in parallel after Better Auth setup (T009-T011)

**Sprint 2**:
- UI Primitives (T016-T019) can all run in parallel
- AuthForm (T025) depends on UI Primitives
- Auth Pages (T031-T033) depend on AuthForm
- Navbar (T020) can run in parallel with AuthForm

**Sprint 3**:
- API Client (T034-T041) MUST complete first (blocks all task components)
- TaskList (T042-T043) depends on API Client
- TaskCard (T044-T050) depends on API Client
- AddTaskForm (T051-T055) depends on API Client
- All three components (TaskList, TaskCard, AddTaskForm) can be developed in parallel after API Client
- Dashboard (T056) depends on TaskList, TaskCard, AddTaskForm
- Filters (T057-T059) can be developed in parallel with Dashboard

**Sprint 4**:
- All Sprint 4 tasks can run in parallel (cross-cutting concerns)

---

## Parallel Execution Examples

### Sprint 1 Parallel Opportunities (4 tasks)

After T004 (tsconfig.json) completes:
```bash
# Can run in parallel
T005: Create .env.example
T006: Create .env.local
T007: Create README.md
T011: Create types/auth.ts
```

### Sprint 2 Parallel Opportunities (12 tasks)

After T015 (root layout) completes:
```bash
# UI Primitives (can all run in parallel)
T016: Create Button.tsx
T017: Create Input.tsx
T018: Create Card.tsx
T019: Create Checkbox.tsx

# After AuthForm (T025) completes
T031: Create signin page
T032: Create signup page
T033: Create profile page

# Layout components (can run in parallel with AuthForm)
T021: Create ProfileDropdown.tsx
T022: Create LogoutButton.tsx
```

### Sprint 3 Parallel Opportunities (8 tasks)

After T041 (API Client) completes:
```bash
# Can run in parallel
T042: Create TaskList.tsx
T043: Create EmptyState.tsx
T044: Create TaskCard.tsx (start of TaskCard feature)
T051: Create AddTaskForm.tsx (start of AddTaskForm feature)

# After T050 (TaskCard complete) and T055 (AddTaskForm complete)
T057: Create TaskFilters.tsx
T058: Implement filter state
T059: Implement filter logic
```

### Sprint 4 Parallel Opportunities (8 tasks)

All can run in parallel:
```bash
T060: Create Skeleton.tsx
T063: Install sonner
T066: Test responsive design
T067: Add ARIA labels
T068: Test keyboard navigation
T069: Create Modal.tsx
```

---

## Implementation Strategy

### MVP Scope (Recommended for first delivery)

**Sprint 1** (MUST HAVE):
- Next.js project setup
- Better Auth configuration
- Middleware for protected routes

**Sprint 2** (MUST HAVE):
- Navbar (basic version)
- Auth pages (Signin/Signup)
- AuthForm component

**Sprint 3** (MUST HAVE):
- API Client (T034-T041)
- TaskList component (T042-T043)
- TaskCard component (T044-T050)
- AddTaskForm component (T051-T055)
- Dashboard page (T056)

**Sprint 4** (NICE TO HAVE):
- Can be deferred to post-MVP
- Loading skeletons, toast notifications, polish

### Incremental Delivery Order

1. **First Increment** (Sprint 1): Authentication working
   - Test: Users can sign up, sign in, and access protected routes

2. **Second Increment** (Sprint 2): UI shell complete
   - Test: Navigation, auth pages, profile dropdown all functional

3. **Third Increment** (Sprint 3): Core task management
   - Test: Users can view, create, toggle, and delete tasks

4. **Fourth Increment** (Sprint 4): Polish & UX
   - Test: All operations have proper feedback, responsive design works

---

## Task Validation Checklist

✅ All tasks follow checklist format (- [ ] T### [P?] [US#?] Description with file path)
✅ Task IDs are sequential (T001-T070)
✅ Parallelizable tasks marked with [P]
✅ User story tasks marked with [US#]
✅ Each task has clear file path
✅ Dependencies documented in Dependency Graph
✅ Parallel opportunities identified (32 tasks)
✅ Independent test criteria provided for each sprint
✅ MVP scope clearly defined
✅ Incremental delivery order specified

---

## Success Criteria Mapping

| Success Criterion | Implemented By |
|-------------------|----------------|
| SC-001: Signup within 30s | Sprint 2 (AuthForm T025-T032) |
| SC-002: Login within 20s | Sprint 2 (AuthForm T025-T031) |
| SC-003: Create task within 10s | Sprint 3 (AddTaskForm T051-T055) |
| SC-004: Task list displays within 2s | Sprint 3 (TaskList T042, API Client T036-T041) |
| SC-005: 100% protected routes redirect | Sprint 1 (Middleware T012-T013) |
| SC-006: 100% API requests include JWT | Sprint 3 (API Client T036-T041) |
| SC-007: Optimistic updates <50ms | Sprint 3 (TaskCard T045-T047, T050) |
| SC-008: Form validation <100ms | Sprint 2 (AuthForm T026-T028), Sprint 3 (AddTaskForm T052) |
| SC-009: Responsive 320px-1920px | Sprint 4 (Responsive design T066) |
| SC-010: 95% operations succeed | Sprint 3 (Error handling T038-T040, T047, T050, T055) |
| SC-011: Error states within 3s | Sprint 4 (Toast notifications T063-T065) |
| SC-012: JWT refresh automatic | Sprint 1 (Better Auth T009-T010) |
| SC-013: Logout 100% success | Sprint 2 (LogoutButton T022) |
| SC-014: Empty state UI | Sprint 3 (EmptyState T043) |

---

## File Paths Reference

### Sprint 1 Files
- `frontend/src/auth.ts` (T009)
- `frontend/src/lib/auth-client.ts` (T010)
- `frontend/src/types/auth.ts` (T011)
- `frontend/src/middleware.ts` (T012)
- `frontend/src/app/layout.tsx` (T014)
- `frontend/src/app/page.tsx` (T015)

### Sprint 2 Files
- `frontend/src/components/ui/Button.tsx` (T016)
- `frontend/src/components/ui/Input.tsx` (T017)
- `frontend/src/components/ui/Card.tsx` (T018)
- `frontend/src/components/ui/Checkbox.tsx` (T019)
- `frontend/src/components/layout/Navbar.tsx` (T020)
- `frontend/src/components/layout/ProfileDropdown.tsx` (T021)
- `frontend/src/components/auth/LogoutButton.tsx` (T022)
- `frontend/src/app/(auth)/layout.tsx` (T023)
- `frontend/src/app/(protected)/layout.tsx` (T024)
- `frontend/src/components/auth/AuthForm.tsx` (T025)
- `frontend/src/app/(auth)/signin/page.tsx` (T031)
- `frontend/src/app/(auth)/signup/page.tsx` (T032)
- `frontend/src/app/(protected)/profile/page.tsx` (T033)

### Sprint 3 Files
- `frontend/src/types/task.ts` (T034)
- `frontend/src/types/api.ts` (T035)
- `frontend/src/lib/api.ts` (T036)
- `frontend/src/components/tasks/TaskList.tsx` (T042)
- `frontend/src/components/tasks/EmptyState.tsx` (T043)
- `frontend/src/components/tasks/TaskCard.tsx` (T044)
- `frontend/src/components/tasks/AddTaskForm.tsx` (T051)
- `frontend/src/app/(protected)/dashboard/page.tsx` (T056)
- `frontend/src/components/tasks/TaskFilters.tsx` (T057)

### Sprint 4 Files
- `frontend/src/components/ui/Skeleton.tsx` (T060)
- `frontend/src/app/(protected)/loading.tsx` (T061)
- `frontend/src/components/ui/Modal.tsx` (T069)

---

## Next Steps

1. **Review this task list** with the team
2. **Run `/sp.implement`** to execute tasks sequentially
3. **Monitor progress** using task checkboxes
4. **Test after each sprint** using independent test criteria
5. **Create PR** after all tasks complete using `/sp.git.commit_pr`

---

**Task List Status**: ✅ COMPLETE - Ready for `/sp.implement` command
**Total Tasks**: 70
**Parallel Tasks**: 32
**Sequential Tasks**: 38
**Sprints**: 4
**User Stories**: 10 (US1-US10)
