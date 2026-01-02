# Feature Specification: Dashboard Molecules (Atomic Design Layer 2)

**Feature Branch**: `001-frontend-core` (Sprint 2 - Molecules)
**Created**: 2025-12-23
**Status**: Draft
**Input**: User description: "Define specifications for Dashboard Molecules in /specs/ui/molecules.md. 1. TaskCard Specification: Display: Task title, description (optional), and status. Actions: Checkbox for status toggle, Delete icon for removal. States: Active, Completed (strikethrough), and Loading (during API sync). 2. AddTaskForm Specification: Input: Text field for task title with validation (min 3 chars). Action: Submit button that triggers API call. Feedback: Clear input on success, show error message on failure."

---

## User Scenarios & Testing *(mandatory)*

### User Story 1 - View Task in TaskCard (Priority: P1)

As a user viewing my task list, I want to see each task displayed in a TaskCard so that I can quickly understand what needs to be done.

**Why this priority**: TaskCard is the primary unit of task display. Users must be able to see task details at a glance.

**Independent Test**: Can be tested by rendering TaskCard with mock task data and verifying title, description (if provided), and status are displayed correctly.

**Acceptance Scenarios**:

1. **Given** a task with title only, **When** TaskCard renders, **Then** I see the task title prominently displayed
2. **Given** a task with title and description, **When** TaskCard renders, **Then** I see both title and truncated description (2 lines max)
3. **Given** a completed task, **When** TaskCard renders, **Then** I see the title with strikethrough styling and muted color
4. **Given** an active (incomplete) task, **When** TaskCard renders, **Then** I see the title in normal text without strikethrough

---

### User Story 2 - Toggle Task Completion in TaskCard (Priority: P1)

As a user, I want to toggle task completion by clicking a checkbox so that I can mark tasks as done or undone.

**Why this priority**: Task completion toggling is the most frequent user action. Must be instant and intuitive.

**Independent Test**: Can be tested by clicking checkbox in TaskCard and verifying UI updates immediately with visual feedback (strikethrough appears/disappears).

**Acceptance Scenarios**:

1. **Given** an incomplete task, **When** I click the checkbox, **Then** the checkbox becomes checked and title gets strikethrough styling immediately
2. **Given** a completed task, **When** I click the checkbox, **Then** the checkbox becomes unchecked and strikethrough is removed immediately
3. **Given** I toggle completion, **When** API call is in progress, **Then** I see a loading indicator and checkbox is disabled
4. **Given** API call succeeds, **When** response received, **Then** loading indicator disappears and task state persists
5. **Given** API call fails, **When** error occurs, **Then** checkbox reverts to original state and I see error message

---

### User Story 3 - Delete Task from TaskCard (Priority: P1)

As a user, I want to delete tasks using a delete icon so that I can remove completed or unwanted tasks.

**Why this priority**: Task deletion is essential for list management and keeping tasks organized.

**Independent Test**: Can be tested by clicking delete icon in TaskCard and verifying confirmation prompt appears, then task is removed after confirmation.

**Acceptance Scenarios**:

1. **Given** I have a task in TaskCard, **When** I click the delete icon, **Then** I see a confirmation message "Are you sure you want to delete this task?"
2. **Given** confirmation prompt is shown, **When** I confirm deletion, **Then** TaskCard disappears immediately and I see success feedback
3. **Given** confirmation prompt is shown, **When** I cancel, **Then** prompt closes and TaskCard remains unchanged
4. **Given** I confirm deletion, **When** API call fails, **Then** TaskCard reappears and I see error message

---

### User Story 4 - Create Task using AddTaskForm (Priority: P1)

As a user, I want to create new tasks using a simple input form so that I can quickly capture tasks as they arise.

**Why this priority**: Task creation is fundamental to the application. Form must be fast and accessible.

**Independent Test**: Can be tested by typing a task title, pressing Enter or clicking submit, and verifying task appears in the list.

**Acceptance Scenarios**:

1. **Given** I am on the dashboard, **When** I see AddTaskForm, **Then** I see a text input field with placeholder "What needs to be done?"
2. **Given** I type a task title (min 3 chars), **When** I press Enter or click submit, **Then** task is created and appears in the list immediately
3. **Given** I submit a valid task, **When** creation succeeds, **Then** input field is cleared and I see success feedback
4. **Given** I type less than 3 characters, **When** I try to submit, **Then** submit button is disabled and I see validation error "Title must be at least 3 characters"
5. **Given** I type more than 200 characters, **When** validation runs, **Then** I see error "Title must be 200 characters or less"
6. **Given** I submit a task, **When** API call fails, **Then** I see error message "Failed to create task. Please try again."

---

### User Story 5 - Real-Time Validation in AddTaskForm (Priority: P2)

As a user filling the AddTaskForm, I want to see validation feedback as I type so that I know if my input is valid before submitting.

**Why this priority**: Real-time validation improves UX by preventing submission errors and providing immediate feedback.

**Independent Test**: Can be tested by typing in input field and verifying validation messages appear/disappear as input changes.

**Acceptance Scenarios**:

1. **Given** I start typing in AddTaskForm, **When** I type 1-2 characters, **Then** I see validation error "Title must be at least 3 characters" and submit is disabled
2. **Given** I have typed 3+ valid characters, **When** validation runs, **Then** error message disappears and submit button is enabled
3. **Given** I clear the input field, **When** field loses focus, **Then** I see error "Title is required"
4. **Given** I paste 250 characters, **When** validation runs, **Then** I see error "Title must be 200 characters or less"

---

### Edge Cases

- What happens when TaskCard checkbox is clicked multiple times rapidly?
  - Checkbox is disabled during API call (isPending state)
  - Subsequent clicks are ignored until first call completes
  - Prevents race conditions and duplicate requests

- What happens when AddTaskForm is submitted with only whitespace?
  - Validation trims whitespace before checking length
  - Empty/whitespace-only input shows "Title is required" error
  - Submit button remains disabled

- What happens when task description exceeds 2 lines in TaskCard?
  - Description is truncated with "line-clamp-2" Tailwind class
  - Ellipsis (...) appears at truncation point
  - Full description not shown in TaskCard (future: expand on click)

- What happens when delete API call is slow (>2 seconds)?
  - TaskCard shows "Deleting..." text
  - Delete button is disabled during call
  - User cannot interact with TaskCard until call completes

- What happens when TaskCard is in loading state and user navigates away?
  - API call is cancelled (AbortController in api.ts from Sprint 1)
  - No state leakage or memory issues
  - Clean component unmount

## Requirements *(mandatory)*

### Functional Requirements

#### TaskCard - Display Requirements

- **FR-001**: TaskCard MUST display task title prominently in readable font size (text-lg or larger)
- **FR-002**: TaskCard MUST display optional task description truncated to 2 lines maximum (line-clamp-2)
- **FR-003**: TaskCard MUST display task completion status via visual styling (strikethrough for completed, normal for active)
- **FR-004**: TaskCard MUST show task created date in human-readable format (e.g., "Dec 23, 2025" or "2 days ago")
- **FR-005**: TaskCard MUST use Card atom as container with proper spacing and shadow

#### TaskCard - Checkbox Toggle Requirements

- **FR-006**: TaskCard MUST include checkbox for completion toggle positioned at left side of card
- **FR-007**: Checkbox MUST reflect current task completion status (checked = completed, unchecked = active)
- **FR-008**: Clicking checkbox MUST trigger immediate visual update (strikethrough appears/disappears) before API call completes
- **FR-009**: Checkbox MUST be disabled during API call (prevent multiple simultaneous toggles)
- **FR-010**: TaskCard MUST display loading indicator text during toggle API call (e.g., "Updating...")
- **FR-011**: Failed toggle MUST revert visual state to original and display error message

#### TaskCard - Delete Action Requirements

- **FR-012**: TaskCard MUST include delete icon/button positioned at right side of card
- **FR-013**: Delete button MUST use danger styling (red color) to indicate destructive action
- **FR-014**: Clicking delete MUST show confirmation dialog with message "Are you sure you want to delete this task?"
- **FR-015**: Delete confirmation MUST have "Delete" and "Cancel" options clearly labeled
- **FR-016**: Confirming delete MUST trigger immediate TaskCard disappearance (optimistic removal)
- **FR-017**: Delete button MUST be disabled during API call showing "Deleting..." text
- **FR-018**: Failed delete MUST show error message and keep TaskCard visible

#### TaskCard - State Management

- **FR-019**: TaskCard MUST maintain three states: Active (default), Completed (strikethrough), Loading (during API sync)
- **FR-020**: Active state MUST show task title in normal text (text-gray-900), unchecked checkbox
- **FR-021**: Completed state MUST show task title with strikethrough (line-through text-gray-500), checked checkbox
- **FR-022**: Loading state MUST show disabled checkbox, loading indicator, and prevent user interactions
- **FR-023**: TaskCard MUST use optimistic updates pattern for both toggle and delete actions

#### AddTaskForm - Input Requirements

- **FR-024**: AddTaskForm MUST display text input field for task title with clear placeholder text
- **FR-025**: Input field placeholder MUST be helpful (e.g., "What needs to be done?" or "Add a new task...")
- **FR-026**: Input field MUST use Input atom with proper styling and accessibility
- **FR-027**: Input field MUST have associated label (visible or aria-label) for screen readers
- **FR-028**: Input field MUST support Enter key for form submission

#### AddTaskForm - Validation Requirements

- **FR-029**: AddTaskForm MUST validate title field: minimum 3 characters required
- **FR-030**: AddTaskForm MUST validate title field: maximum 200 characters allowed
- **FR-031**: AddTaskForm MUST show validation error "Title must be at least 3 characters" when length < 3
- **FR-032**: AddTaskForm MUST show validation error "Title must be 200 characters or less" when length > 200
- **FR-033**: AddTaskForm MUST show validation error "Title is required" when field is empty on blur
- **FR-034**: AddTaskForm MUST perform real-time validation as user types (not just on submit)
- **FR-035**: AddTaskForm MUST trim whitespace from title before validation and submission

#### AddTaskForm - Submit Action Requirements

- **FR-036**: AddTaskForm MUST include submit button labeled "Add Task" or similar clear call-to-action
- **FR-037**: Submit button MUST use Button atom with primary variant
- **FR-038**: Submit button MUST be disabled when validation errors exist or title is empty
- **FR-039**: Submit button MUST show loading spinner during API call with text "Adding..."
- **FR-040**: Clicking submit MUST trigger task creation via API with validated title
- **FR-041**: Successful submission MUST clear input field immediately
- **FR-042**: Successful submission MUST show success feedback (toast notification or inline message)

#### AddTaskForm - Error Handling Requirements

- **FR-043**: AddTaskForm MUST display validation errors below input field in red text
- **FR-044**: AddTaskForm MUST display API errors (network, server) as error messages
- **FR-045**: Failed submission MUST keep input value (do not clear on error) so user can retry
- **FR-046**: Failed submission MUST show specific error message "Failed to create task. Please try again."
- **FR-047**: AddTaskForm MUST handle network timeout errors gracefully with appropriate message

#### TaskCard & AddTaskForm - Accessibility Requirements

- **FR-048**: TaskCard checkbox MUST have aria-label describing action (e.g., "Mark task as complete")
- **FR-049**: TaskCard delete button MUST have aria-label with task context (e.g., "Delete task: {title}")
- **FR-050**: AddTaskForm input MUST have aria-invalid="true" when validation error exists
- **FR-051**: AddTaskForm validation errors MUST be associated with input via aria-describedby
- **FR-052**: All interactive elements (checkbox, buttons, input) MUST be keyboard accessible (Tab, Enter, Space)
- **FR-053**: Focus indicators MUST be visible on all interactive elements for keyboard users

#### TaskCard & AddTaskForm - Responsive Design Requirements

- **FR-054**: TaskCard MUST be responsive: full-width on mobile, comfortable width on desktop
- **FR-055**: TaskCard content MUST not overflow on small screens (320px width minimum)
- **FR-056**: AddTaskForm MUST be responsive: full-width input on mobile, constrained on desktop
- **FR-057**: AddTaskForm submit button MUST have minimum 44x44px touch target on mobile
- **FR-058**: TaskCard checkbox and delete button MUST have minimum 44x44px touch target on mobile

### Key Entities (Component Props)

#### TaskCard Props

| Prop | Type | Required | Notes |
|------|------|----------|-------|
| task | Task | Yes | Task object with id, title, description, completed, etc. |
| onUpdate | (task: Task) => void | No | Callback for parent to update task state |
| onDelete | (taskId: string) => void | No | Callback for parent to remove task |

#### Task Entity (from Sprint 1)

| Field | Type | Notes |
|-------|------|-------|
| id | string | Unique task identifier |
| user_id | string | Owner user ID |
| title | string | Task title (3-200 characters) |
| description | string | Optional task description |
| completed | boolean | Completion status |
| created_at | string | ISO 8601 datetime |
| updated_at | string | ISO 8601 datetime |

#### AddTaskForm Props

| Prop | Type | Required | Notes |
|------|------|----------|-------|
| onTaskCreated | () => void | No | Callback after successful creation (for parent refresh) |

#### TaskCreate Payload (from Sprint 1)

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| title | string | Yes | Task title (3-200 characters, trimmed) |
| description | string | No | Optional task description |

---

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: TaskCard renders task details within 50ms of receiving props
- **SC-002**: TaskCard checkbox toggle updates UI within 50ms of click (optimistic update)
- **SC-003**: TaskCard delete action shows confirmation within 100ms of button click
- **SC-004**: AddTaskForm validates input within 100ms of user typing (real-time feedback)
- **SC-005**: AddTaskForm clears input field within 200ms of successful submission
- **SC-006**: AddTaskForm submit button is disabled 100% of the time when validation fails
- **SC-007**: TaskCard completed state applies strikethrough to 100% of completed tasks
- **SC-008**: AddTaskForm shows validation error within 100ms when title length < 3 or > 200
- **SC-009**: TaskCard and AddTaskForm work correctly on mobile screens (320px width minimum)
- **SC-010**: All interactive elements (checkbox, buttons, input) are keyboard accessible (100% Tab navigation)
- **SC-011**: TaskCard optimistic updates rollback within 100ms of API failure
- **SC-012**: AddTaskForm allows task creation within 5 seconds from typing to submission

---

## Assumptions

1. Task type is defined in `frontend/src/types/task.ts` from Sprint 1
2. TaskCreate type is defined in `frontend/src/lib/api.ts` from Sprint 1
3. API client (`frontend/src/lib/api.ts`) is available with methods: toggleTask(), deleteTask(), createTask()
4. All API methods automatically attach JWT Bearer token (configured in Sprint 1)
5. UI atoms (Button, Input, Card, Checkbox) are available from Batch 1 (T001-T004)
6. Toast notification system (sonner) is available from Sprint 1
7. Validation rule: min 3 characters (user requirement), max 200 characters (backend constraint)
8. Backend API endpoints exist: PATCH /api/tasks/{id}, DELETE /api/tasks/{id}, POST /api/tasks
9. Backend returns updated Task object on successful PATCH
10. Backend returns 204 No Content or 200 OK on successful DELETE
11. Backend returns created Task object on successful POST
12. Optimistic updates provide better UX even with rollback risk
13. Users have modern browsers with JavaScript enabled
14. Network latency typically <200ms
15. Confirmation dialogs use browser native confirm() (future: custom modal)

---

## Out of Scope

- Task description editing in TaskCard (description is display-only)
- Task title inline editing in TaskCard (toggle and delete only)
- Expand description beyond 2 lines (no "show more" button)
- Custom modal for delete confirmation (using browser native confirm())
- Drag-and-drop reordering of TaskCards
- Bulk selection of multiple TaskCards
- Task priority or due date fields in AddTaskForm
- Multi-line description input in AddTaskForm (title only)
- Task categories or tags in TaskCard
- Task sharing or collaboration features
- Undo functionality for delete
- Task statistics in TaskCard (e.g., "3 days overdue")

---

## Dependencies

- **Sprint 1**: API client (lib/api.ts) with JWT Bearer token injection
- **Sprint 1**: Task and TaskCreate types
- **Sprint 1**: Better Auth session for authentication
- **Batch 1 (T001-T004)**: UI atoms (Button, Input, Card, Checkbox)
- **Batch 1 (T013-T015)**: TaskList component to render TaskCards
- **Sonner**: Toast notification library (from Sprint 1 package.json)
- **React Hooks**: useState, useOptimistic (or useState fallback), useTransition
- **Next.js Router**: useRouter for navigation and refresh
- **Backend API**: Task endpoints (GET, POST, PATCH, DELETE)
