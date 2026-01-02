# Implementation Tasks: Dashboard UI (Sprint 2)

**Branch**: `001-frontend-core` | **Date**: 2025-12-23
**Spec**: [dashboard-feature.md](dashboard-feature.md) | **Plan**: [dashboard-feature.plan.md](dashboard-feature.plan.md)

---

## Task Organization

Tasks organized following **Atomic Design** principles:
- **Atoms**: Basic UI primitives (Button, Input, Checkbox, Card)
- **Molecules**: Composite components (TaskCard, AddTaskForm)
- **Organisms**: Complex components (TaskList, Navbar)
- **Templates**: Page layouts (Dashboard Page)

**Task Format Legend**:
- `- [ ] T###` - Sequential task ID
- `[P]` - Parallelizable (can run concurrently)
- `[US#]` - User Story number (from spec.md)

**Total Tasks**: 24
**Parallel Opportunities**: 14 tasks

---

## Phase 1: UI Atoms (Atomic Design Layer 1)

**Goal**: Create reusable UI primitives following Atomic Design

**User Stories**: Foundation for US1-US8

**Independent Test**: Each atom renders correctly with all variants and states

### Atomic Components (All Parallelizable)

- [x] T001 [P] Create frontend/src/components/ui/button.tsx with variants (primary, secondary, danger, ghost), disabled state, loading spinner, and Tailwind styling
- [x] T002 [P] Create frontend/src/components/ui/input.tsx with error state, ARIA attributes (aria-invalid, aria-describedby), label support, and Tailwind styling
- [x] T003 [P] Create frontend/src/components/ui/card.tsx with Tailwind styling (shadow, rounded, padding, hover effect) and sub-components (CardHeader, CardTitle, CardContent)
- [x] T004 [P] Create frontend/src/components/ui/checkbox.tsx with Tailwind styling, checked/unchecked states, label support, and accessibility (aria-label)

---

## Phase 2: Navbar Component (Organism)

**Goal**: Implement Navbar with user profile display and logout

**User Stories**: US2 (Profile Display), US3 (Logout)

**Independent Test**: Navbar displays user email, logout button works, responsive on mobile

### Navbar Implementation

- [x] T005 [US2] [US3] Create frontend/src/components/layout/navbar.tsx as Client Component with user email display and logout button
- [x] T006 [US2] Integrate useAuth hook in Navbar to get user session and display email from JWT token
- [x] T007 [US3] Implement logout handler in Navbar using clientSignOut from Better Auth with toast notification and redirect to /signin
- [x] T008 [US2] Add responsive styling to Navbar (hide email on mobile <768px with hidden md:block, show on desktop, sticky positioning z-50)
- [x] T009 [US2] Add loading skeleton to Navbar for session loading state (placeholder email and logout button with animate-pulse)

---

## Phase 3: Dashboard Page & Route Structure (Template)

**Goal**: Create Dashboard page with Server Component data fetching

**User Stories**: US1 (View Dashboard)

**Independent Test**: Dashboard page loads, fetches tasks server-side, renders layout with Navbar

### Dashboard Page Setup

- [x] T010 [US1] Create frontend/src/app/(protected)/layout.tsx with protected route group layout including Navbar component
- [x] T011 [US1] Create frontend/src/app/(protected)/dashboard/page.tsx as Server Component that fetches tasks using api.listTasks() with error handling
- [x] T012 [US1] Add Tailwind layout styling to dashboard page (max-w-4xl mx-auto, px-4 sm:px-6 lg:px-8, py-8, space-y-6)

---

## Phase 4: TaskList Component (Organism)

**Goal**: Implement TaskList to display array of tasks with empty state

**User Stories**: US1 (View Dashboard)

**Independent Test**: TaskList receives tasks prop, renders TaskCard for each task, shows empty state when no tasks

### TaskList Implementation

- [x] T013 [US1] Create frontend/src/components/dashboard/task-list.tsx as Server Component that receives initialTasks prop and maps to TaskCard components (placeholder cards for now)
- [x] T014 [P] [US1] Create EmptyState UI in task-list.tsx with SVG icon (clipboard), message "No tasks yet. Create your first task!", and Tailwind styling (bg-white, rounded-lg, shadow-sm, p-12, text-center)
- [x] T015 [P] [US1] Add task count display in task-list.tsx header showing "Your Tasks (N)" with Tailwind styling (text-lg font-semibold text-gray-900)

---

## Phase 5: TaskCard Component with Optimistic Updates (Molecule)

**Goal**: Implement interactive TaskCard with toggle and delete, optimistic updates

**User Stories**: US4 (Toggle Completion), US6 (Delete Task)

**Independent Test**: TaskCard displays task, checkbox toggles with optimistic update, delete button shows confirmation and removes task

### TaskCard Structure

- [ ] T016 [US4] [US6] Create frontend/src/components/dashboard/task-card.tsx as Client Component with task prop and basic layout (checkbox, title, delete button)
- [ ] T017 [US4] Add Tailwind styling to task-card.tsx (Card wrapper, flex layout, hover effects, responsive padding)

### TaskCard Toggle (Optimistic Updates)

- [ ] T018 [US4] Implement useOptimistic hook in task-card.tsx for completion state with initial value from task.completed
- [ ] T019 [US4] Implement handleToggle function in task-card.tsx that applies optimistic UI update immediately (setOptimisticCompleted)
- [ ] T020 [US4] Integrate api.toggleTask() call in handleToggle with JWT Bearer token, wrapped in useTransition for pending state
- [ ] T021 [US4] Implement success handler in handleToggle that calls router.refresh() to revalidate server data
- [ ] T022 [US4] Implement error handler in handleToggle that rolls back optimistic update and shows error toast "Failed to update task"
- [ ] T023 [US4] Add visual distinction for completed tasks in task-card.tsx (line-through text-gray-500 for completed, text-gray-900 for active)
- [ ] T024 [US4] Add loading indicator in task-card.tsx during toggle (isPending state, disabled checkbox, "Updating..." text)

### TaskCard Delete (Optimistic Updates)

- [ ] T025 [US6] Implement handleDelete function in task-card.tsx with confirmation dialog ("Are you sure you want to delete this task?")
- [ ] T026 [US6] Integrate api.deleteTask() call in handleDelete with JWT Bearer token
- [ ] T027 [US6] Implement success handler in handleDelete that calls router.refresh() and shows success toast "Task deleted"
- [ ] T028 [US6] Implement error handler in handleDelete that shows error toast "Failed to delete task."
- [ ] T029 [US6] Add delete button styling in task-card.tsx (text-red-600, hover effect, disabled state, aria-label)

### TaskCard Accessibility & Details

- [ ] T030 [P] [US4] [US6] Add ARIA labels to task-card.tsx checkbox (aria-label="Mark task as complete/incomplete") and delete button
- [ ] T031 [P] [US1] Add task description preview in task-card.tsx with line-clamp-2 for truncation and text-gray-600 styling
- [ ] T032 [P] [US1] Add created date display in task-card.tsx with relative format (toLocaleDateString) and text-xs text-gray-400 styling

---

## Phase 6: AddTaskForm Component with Optimistic Creation (Molecule)

**Goal**: Implement task creation form with validation and optimistic updates

**User Stories**: US5 (Create New Task)

**Independent Test**: Form validates title (1-200 chars), submits with Enter key, creates task optimistically, clears on success

### AddTaskForm Structure

- [ ] T033 [US5] Create frontend/src/components/dashboard/add-task.tsx as Client Component with title input and submit button
- [ ] T034 [US5] Add Tailwind styling to add-task.tsx (Card wrapper, flex layout, full-width input, responsive button)

### AddTaskForm Validation

- [ ] T035 [US5] Implement useState for title and titleError in add-task.tsx
- [ ] T036 [US5] Implement validateTitle function in add-task.tsx (required, 1-200 chars) with real-time feedback
- [ ] T037 [US5] Add onChange handler to input that calls validateTitle and updates titleError display below input
- [ ] T038 [US5] Disable submit button when titleError exists or title is empty

### AddTaskForm Submission & Optimistic Creation

- [ ] T039 [US5] Implement handleSubmit function in add-task.tsx wrapped in useTransition for pending state
- [ ] T040 [US5] Integrate api.createTask() call in handleSubmit with JWT Bearer token
- [ ] T041 [US5] Implement success handler in handleSubmit that clears title input and shows success toast "Task created"
- [ ] T042 [US5] Implement error handler in handleSubmit that shows error toast "Failed to create task"
- [ ] T043 [US5] Call router.refresh() in success handler to revalidate server data and display new task
- [ ] T044 [US5] Add Enter key handler (onKeyDown) to input that triggers form submission
- [ ] T045 [US5] Add loading spinner to submit button during isPending state with "Adding..." text

### AddTaskForm Accessibility

- [ ] T046 [P] [US5] Add ARIA attributes to add-task.tsx input (aria-label="New task title", aria-invalid, aria-describedby for error)
- [ ] T047 [P] [US5] Add maxLength={200} attribute to input for browser-level validation

---

## Phase 7: Integration & Polish

**Goal**: Integrate all components in Dashboard Page, handle loading and empty states

**User Stories**: US1 (Dashboard), US7 (Responsive), US8 (Accessibility)

**Independent Test**: Complete dashboard works end-to-end with all components integrated

### Dashboard Integration

- [ ] T048 [US1] Import and render Navbar in dashboard page.tsx at top of layout
- [ ] T049 [US1] Import and render AddTaskForm in dashboard page.tsx above TaskList
- [ ] T050 [US1] Import and render TaskList in dashboard page.tsx with initialTasks prop from server-side fetch
- [ ] T051 [US1] Add main content wrapper in dashboard page.tsx with Tailwind layout (max-w-4xl mx-auto px-4 py-8, space-y-6)

### Loading States

- [ ] T052 [P] [US1] Create frontend/src/app/(protected)/dashboard/loading.tsx with loading skeleton for task cards
- [ ] T053 [P] Create frontend/src/components/ui/skeleton.tsx with Tailwind shimmer animation component

### Error Handling

- [ ] T054 [US1] Add try-catch in dashboard page.tsx for api.listTasks() with error display UI if fetch fails
- [ ] T055 [P] Create frontend/src/app/(protected)/dashboard/error.tsx with error boundary UI and retry button

---

## Dependency Graph

### Phase Dependencies (Sequential)

```
Phase 1 (Atoms) → Phase 2 (Navbar) → Phase 3 (Dashboard Page) → Phase 4 (TaskList) → Phase 5 (TaskCard) → Phase 6 (AddTaskForm) → Phase 7 (Integration)
```

### Within-Phase Parallelization

**Phase 1 (Atoms)**: All 4 tasks parallelizable
```
T001 (Button) || T002 (Input) || T003 (Card) || T004 (Checkbox)
```

**Phase 2 (Navbar)**: T006-T009 depend on T005
```
T005 → (T006 || T007 || T008 || T009)
```

**Phase 4 (TaskList)**: T014-T015 parallelizable after T013
```
T013 → (T014 || T015)
```

**Phase 5 (TaskCard)**: Accessibility tasks (T030-T032) parallelizable
```
T016 → T017 → T018 → T019 → T020 → T021 → T022 → T023 → T024 → T025 → T026 → T027 → T028 → T029
                                                                                          ↓
                                                                               (T030 || T031 || T032)
```

**Phase 6 (AddTaskForm)**: Accessibility tasks (T046-T047) parallelizable
```
T033 → T034 → T035 → T036 → T037 → T038 → T039 → T040 → T041 → T042 → T043 → T044 → T045
                                                                                    ↓
                                                                         (T046 || T047)
```

**Phase 7 (Integration)**: Loading/Error tasks parallelizable
```
T048 → T049 → T050 → T051
  ↓
(T052 || T053 || T054 || T055)
```

---

## Parallel Execution Examples

### Phase 1: All Atoms in Parallel (4 tasks)

```bash
# Can all run simultaneously
T001: Create Button.tsx
T002: Create Input.tsx
T003: Create Card.tsx
T004: Create Checkbox.tsx
```

### Phase 2: Navbar Sub-tasks (3 parallel after T005)

```bash
# After T005 completes
T006: Integrate useAuth || T007: Implement logout || T008: Responsive styling
```

### Phase 5: TaskCard Accessibility (3 parallel)

```bash
# After T029 completes
T030: Add ARIA labels || T031: Add description preview || T032: Add created date
```

### Phase 6: AddTaskForm Accessibility (2 parallel)

```bash
# After T045 completes
T046: Add ARIA attributes || T047: Add maxLength
```

### Phase 7: Loading & Error States (4 parallel)

```bash
# After T051 completes
T052: Create loading.tsx || T053: Create Skeleton.tsx || T054: Add error handling || T055: Create error.tsx
```

---

## Implementation Strategy

### Atomic Design Approach

**Layer 1 - Atoms** (Foundation):
- Button, Input, Card, Checkbox
- No dependencies on other components
- Fully reusable across application
- All parallelizable

**Layer 2 - Molecules** (Composite):
- TaskCard (uses Card, Checkbox, Button atoms)
- AddTaskForm (uses Input, Button atoms)
- Depend on atoms being complete

**Layer 3 - Organisms** (Complex):
- TaskList (uses TaskCard molecules)
- Navbar (uses Button atoms)
- Depend on molecules/atoms

**Layer 4 - Templates** (Pages):
- Dashboard Page (uses all organisms)
- Depends on all lower layers

### API Integration Points

| Component | API Method | Endpoint | Token Required |
|-----------|------------|----------|----------------|
| Dashboard Page | api.listTasks() | GET /api/tasks | ✓ JWT Bearer |
| TaskCard (toggle) | api.toggleTask() | PATCH /api/tasks/{id} | ✓ JWT Bearer |
| TaskCard (delete) | api.deleteTask() | DELETE /api/tasks/{id} | ✓ JWT Bearer |
| AddTaskForm | api.createTask() | POST /api/tasks | ✓ JWT Bearer |

All API calls use the centralized API client from Sprint 1 with automatic JWT Bearer token injection.

### Loading & Empty States

| Component | Loading State | Empty State |
|-----------|---------------|-------------|
| Navbar | Loading skeleton (T009) | N/A |
| TaskList | Via dashboard loading.tsx (T052) | EmptyState UI (T014) |
| TaskCard | "Updating..." text (T024) | N/A |
| AddTaskForm | Loading spinner (T045) | N/A |
| Dashboard Page | loading.tsx with skeletons (T052) | N/A |

---

## Success Criteria Mapping

| Success Criterion | Implemented By |
|-------------------|----------------|
| SC-001: Dashboard loads within 2s | Phase 3 (Server Component fetch - T011) |
| SC-002: Navbar email within 500ms | Phase 2 (useAuth hook - T006) |
| SC-003: Optimistic toggle within 50ms | Phase 5 (useOptimistic - T018-T019) |
| SC-004: Optimistic create within 50ms | Phase 6 (useTransition - T039-T043) |
| SC-005: 100% JWT Bearer token | Sprint 1 API client (used in T020, T026, T040) |
| SC-006: Rollback within 100ms | Phase 5 (error handler - T022, T028) |
| SC-007: Error toast within 500ms | All phases (toast.error calls) |
| SC-008: Logout within 1s | Phase 2 (clientSignOut - T007) |
| SC-009: Mobile 320px no scroll | All phases (Tailwind responsive - T008, T017, T034) |
| SC-010: 100% keyboard accessible | Phases 5-6 (ARIA labels - T030, T046) |
| SC-011: 100 tasks no lag | TaskList rendering (T013) |
| SC-012: AddTaskForm clears within 200ms | Phase 6 (clear handler - T041) |
| SC-013: Delete dialog within 100ms | Phase 5 (confirmation - T025) |
| SC-014: GET completes within 1s | Dashboard Page (T011) |

---

## File Paths Reference

### UI Atoms (Phase 1)
- `frontend/src/components/ui/button.tsx` (T001)
- `frontend/src/components/ui/input.tsx` (T002)
- `frontend/src/components/ui/card.tsx` (T003)
- `frontend/src/components/ui/checkbox.tsx` (T004)

### Navbar (Phase 2)
- `frontend/src/components/layout/navbar.tsx` (T005-T009)

### Dashboard Page (Phase 3)
- `frontend/src/app/(protected)/layout.tsx` (T010)
- `frontend/src/app/(protected)/dashboard/page.tsx` (T011-T012)

### TaskList (Phase 4)
- `frontend/src/components/dashboard/task-list.tsx` (T013-T015)

### TaskCard (Phase 5)
- `frontend/src/components/dashboard/task-card.tsx` (T016-T032)

### AddTaskForm (Phase 6)
- `frontend/src/components/dashboard/add-task.tsx` (T033-T047)

### Loading & Error (Phase 7)
- `frontend/src/app/(protected)/dashboard/loading.tsx` (T052)
- `frontend/src/app/(protected)/dashboard/error.tsx` (T055)
- `frontend/src/components/ui/skeleton.tsx` (T053)

---

## MVP Scope

**Phase 1-6 (MUST HAVE)**:
- All atoms, molecules, organisms implemented
- Core dashboard functionality works
- Optimistic updates functional

**Phase 7 (NICE TO HAVE)**:
- Loading and error states
- Can be added after core functionality verified

---

## Next Steps

1. **Execute Tasks Sequentially**: Follow dependency graph
2. **Parallelize Where Possible**: Use parallel opportunities (14 tasks)
3. **Test After Each Phase**: Verify atoms work, then molecules, etc.
4. **Run `/sp.implement`**: Execute Sprint 2 tasks with this task list

---

## Task Validation Checklist

✅ All tasks follow checklist format (- [ ] T### [P?] [US#?] Description with file path)
✅ Task IDs are sequential (T001-T055)
✅ Parallelizable tasks marked with [P] (14 tasks)
✅ User story tasks marked with [US#]
✅ Each task has clear file path
✅ Dependencies documented in Dependency Graph
✅ Parallel opportunities identified (14 tasks)
✅ Independent test criteria provided per phase
✅ MVP scope clearly defined
✅ Atomic Design layers respected (Atoms → Molecules → Organisms → Templates)

---

**Task List Status**: ✅ COMPLETE - Ready for `/sp.implement` Sprint 2
**Total Tasks**: 55
**Parallel Tasks**: 14 (25%)
**Sequential Tasks**: 41 (75%)
**Atomic Design Layers**: 4 (Atoms, Molecules, Organisms, Templates)
**User Stories**: 8 (US1-US8)
