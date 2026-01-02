# Feature Specification: Core Dashboard UI (Sprint 2)

**Feature Branch**: `001-frontend-core` (Sprint 2)
**Created**: 2025-12-23
**Status**: Draft
**Input**: User description: "Refine the UI specification for Sprint 2: Core Dashboard UI in /specs/ui/dashboard-feature.md. 1. COMPONENTS: Navbar: User Profile display aur Logout button. TaskList: List view for todos. TaskCard: Individual todo item with status toggle. AddTaskForm: Input field for new tasks. 2. DESIGN: Tailwind CSS based, mobile-responsive, and accessible. 3. DATA FLOW: Dashboard must fetch from GET /api/{user_id}/tasks. Support optimistic updates for toggling completion."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - View Dashboard with Task List (Priority: P1)

As an authenticated user, I want to see my dashboard with all my tasks displayed so that I have an overview of my work.

**Why this priority**: The dashboard is the primary interface users interact with daily. Essential for task visibility and management.

**Independent Test**: Can be tested by logging in and verifying the dashboard page loads with TaskList component fetching tasks from GET /api/{user_id}/tasks and displaying them in TaskCard components.

**Acceptance Scenarios**:

1. **Given** I am logged in with existing tasks, **When** I navigate to /dashboard, **Then** I see Navbar at top, TaskList in center displaying all my tasks as TaskCard components
2. **Given** I am logged in with zero tasks, **When** I view /dashboard, **Then** I see Navbar and empty state message in TaskList "No tasks yet. Create your first task!"
3. **Given** I am viewing /dashboard, **When** page loads, **Then** Navbar shows my email/profile, TaskList fetches from GET /api/{user_id}/tasks
4. **Given** tasks are loaded, **When** displayed, **Then** each TaskCard shows task title, completion checkbox, and delete button

---

### User Story 2 - User Profile Display in Navbar (Priority: P1)

As an authenticated user, I want to see my profile information in the Navbar so that I know which account I'm logged into.

**Why this priority**: User context is essential for multi-user applications. Navbar provides persistent profile visibility.

**Independent Test**: Can be tested by logging in and verifying Navbar displays user email extracted from JWT token and shows logout button.

**Acceptance Scenarios**:

1. **Given** I am logged in, **When** I view /dashboard, **Then** Navbar displays my email address at top-right
2. **Given** I am on /dashboard, **When** I look at Navbar, **Then** I see a logout button clearly labeled
3. **Given** I am viewing Navbar, **When** displayed, **Then** user profile section is visible on all screen sizes (mobile, tablet, desktop)

---

### User Story 3 - Logout from Navbar (Priority: P1)

As an authenticated user, I want to logout from the Navbar so that I can securely end my session.

**Why this priority**: Logout is critical for security, especially on shared devices. Must be easily accessible.

**Independent Test**: Can be tested by clicking logout button in Navbar and verifying Better Auth clears JWT token and redirects to /signin.

**Acceptance Scenarios**:

1. **Given** I am logged in on /dashboard, **When** I click logout button in Navbar, **Then** Better Auth clears my JWT token and I am redirected to /signin
2. **Given** I have logged out, **When** I try to access /dashboard, **Then** middleware redirects me to /signin
3. **Given** I click logout, **When** action completes, **Then** I see success message "Logged out successfully" (toast notification)

---

### User Story 4 - Toggle Task Completion with Optimistic Updates (Priority: P1)

As an authenticated user, I want to toggle task completion status instantly so that I get immediate feedback.

**Why this priority**: Task completion is the most frequent user action. Optimistic updates provide smooth UX.

**Independent Test**: Can be tested by clicking completion checkbox in TaskCard and verifying UI updates immediately before server confirmation, with rollback on error.

**Acceptance Scenarios**:

1. **Given** I have an incomplete task in TaskList, **When** I click completion checkbox in TaskCard, **Then** UI updates immediately (strikethrough, visual change) BEFORE API call completes
2. **Given** I toggle completion, **When** API call to PATCH /api/tasks/{task_id} succeeds, **Then** optimistic update is confirmed and persists
3. **Given** I toggle completion, **When** API call fails (network error, 500 error), **Then** optimistic update is rolled back to original state and I see error toast
4. **Given** I toggle completion, **When** optimistic update is active, **Then** I see subtle loading indicator on checkbox (spinner or opacity change)
5. **Given** server confirms toggle, **When** response received, **Then** TaskCard displays final completion state with correct timestamp

---

### User Story 5 - Create New Task from Dashboard (Priority: P1)

As an authenticated user, I want to create new tasks quickly from the dashboard so that I can capture tasks as they arise.

**Why this priority**: Task creation is fundamental to the application's purpose. Must be fast and accessible.

**Independent Test**: Can be tested by clicking "Add Task" button, entering title in AddTaskForm, submitting, and verifying task appears in TaskList with optimistic update.

**Acceptance Scenarios**:

1. **Given** I am on /dashboard, **When** I see AddTaskForm component, **Then** I see an input field for task title and "Add Task" submit button
2. **Given** I type a task title in AddTaskForm, **When** I press Enter or click "Add Task", **Then** task appears in TaskList immediately (optimistic update) and POST /api/tasks is sent with JWT Bearer token
3. **Given** I submit AddTaskForm with valid title (1-200 chars), **When** API call succeeds, **Then** optimistic task is replaced with server response (includes id, timestamps)
4. **Given** I submit AddTaskForm, **When** API call fails, **Then** optimistic task is removed from TaskList and I see error toast "Failed to create task. Please try again."
5. **Given** I submit AddTaskForm with empty title, **When** validation runs, **Then** submit button is disabled and I see error "Title is required"
6. **Given** I submit AddTaskForm with title over 200 characters, **When** validation runs, **Then** I see error "Title must be 200 characters or less"

---

### User Story 6 - Delete Task from TaskCard (Priority: P2)

As an authenticated user, I want to delete tasks from TaskCard so that I can remove completed or unwanted items.

**Why this priority**: Task deletion is important for list management but less frequent than viewing/creating tasks.

**Independent Test**: Can be tested by clicking delete button in TaskCard, confirming deletion, and verifying task is removed with optimistic update.

**Acceptance Scenarios**:

1. **Given** I have a task in TaskList, **When** I click delete button in TaskCard, **Then** I see confirmation dialog "Are you sure you want to delete this task?"
2. **Given** I confirm deletion, **When** I click "Delete" in dialog, **Then** TaskCard disappears immediately (optimistic update) and DELETE /api/tasks/{task_id} is sent
3. **Given** deletion API call succeeds, **When** response received, **Then** optimistic deletion is confirmed and task removed permanently
4. **Given** deletion API call fails, **When** error returned, **Then** TaskCard reappears (rollback) and I see error toast "Failed to delete task."
5. **Given** I click delete, **When** I click "Cancel" in dialog, **Then** dialog closes and TaskCard remains unchanged

---

### User Story 7 - Responsive Dashboard Layout (Priority: P2)

As a user on any device, I want the dashboard to adapt to my screen size so that I can manage tasks on mobile or desktop.

**Why this priority**: Responsive design ensures accessibility across devices, supporting users' varied contexts.

**Independent Test**: Can be tested by resizing browser from 320px to 1920px and verifying Navbar, TaskList, and TaskCard components adapt gracefully.

**Acceptance Scenarios**:

1. **Given** I am on /dashboard on mobile (320px-767px), **When** viewing, **Then** Navbar collapses user email and shows compact logout button, TaskList displays full-width TaskCards stacked vertically
2. **Given** I am on /dashboard on tablet (768px-1023px), **When** viewing, **Then** Navbar shows full user email, TaskList displays TaskCards in single column with comfortable spacing
3. **Given** I am on /dashboard on desktop (1024px+), **When** viewing, **Then** Navbar shows full user info, TaskList may display TaskCards in grid or single column with max-width constraint
4. **Given** I am on any screen size, **When** interacting with components, **Then** touch targets (buttons, checkboxes) are at least 44x44px for accessibility

---

### User Story 8 - Accessible Dashboard Components (Priority: P3)

As a user with accessibility needs, I want dashboard components to support keyboard navigation and screen readers so that I can manage tasks independently.

**Why this priority**: Accessibility is important for inclusivity but can be enhanced iteratively after core functionality works.

**Independent Test**: Can be tested by navigating dashboard with keyboard only (Tab, Enter, Escape) and verifying all interactions work without mouse.

**Acceptance Scenarios**:

1. **Given** I am on /dashboard with keyboard, **When** I press Tab, **Then** I can navigate through Navbar logout button, AddTaskForm input, and all TaskCard checkboxes/delete buttons
2. **Given** I have focus on TaskCard checkbox, **When** I press Space or Enter, **Then** completion toggles
3. **Given** I have focus on delete button, **When** I press Enter, **Then** delete confirmation dialog opens
4. **Given** I am using screen reader, **When** reading TaskCard, **Then** I hear task title, completion status, and available actions (toggle, delete)
5. **Given** I am using screen reader, **When** reading Navbar, **Then** I hear my email and logout button label

---

### Edge Cases

- What happens when GET /api/{user_id}/tasks returns empty array?
  - TaskList displays EmptyState component with message "No tasks yet. Create your first task!"
  - AddTaskForm remains visible and functional

- How does TaskCard handle rapid toggle clicks (double-click)?
  - Debounce toggle actions (ignore subsequent clicks while API call is pending)
  - Show loading indicator on checkbox during API call
  - Prevent race conditions with request cancellation

- What happens when optimistic update succeeds but page refreshes before confirmation?
  - On page refresh, TaskList fetches fresh data from GET /api/{user_id}/tasks
  - Optimistic state is discarded, server state is source of truth
  - No data loss (backend has the confirmed state)

- How does dashboard handle slow API responses (>2 seconds)?
  - TaskList shows loading skeleton while initial fetch is pending
  - Optimistic updates apply immediately regardless of API speed
  - Timeout after 10 seconds with error message and retry button

- What happens when user has 1000+ tasks?
  - TaskList renders all tasks (no pagination in Sprint 2)
  - Performance may degrade with very large lists
  - Future enhancement: virtual scrolling or pagination

- How does AddTaskForm handle Enter key in title input?
  - Enter key submits the form (creates task)
  - Shift+Enter inserts newline in description field (if multi-line)
  - Standard form submission behavior

- What happens when network connection is lost during toggle?
  - API client detects network error
  - Optimistic update rolls back
  - Error toast: "Network error. Please check your connection and try again."

## Requirements *(mandatory)*

### Functional Requirements

#### Dashboard Layout & Structure

- **FR-001**: Dashboard page MUST display Navbar component at the top of the page (full width, sticky optional)
- **FR-002**: Dashboard page MUST display TaskList component as main content area below Navbar
- **FR-003**: Dashboard page MUST display AddTaskForm component above TaskList for quick task creation
- **FR-004**: Dashboard layout MUST be responsive and adapt to screen sizes 320px-1920px width
- **FR-005**: Dashboard page MUST fetch tasks on load using GET /api/{user_id}/tasks endpoint

#### Navbar Component Requirements

- **FR-006**: Navbar MUST be a Client Component (requires 'use client' directive) for logout interactivity
- **FR-007**: Navbar MUST display current user's email address extracted from JWT token claims
- **FR-008**: Navbar MUST include logout button that calls Better Auth signOut method
- **FR-009**: Navbar MUST be positioned at top of page with distinct visual styling (background color, border/shadow)
- **FR-010**: Navbar MUST be responsive: collapse user email to icon on mobile (<768px), show full email on desktop
- **FR-011**: Logout button in Navbar MUST be clearly labeled and accessible (aria-label="Logout")
- **FR-012**: Navbar MUST maintain z-index to stay above TaskList content (if sticky positioning used)

#### TaskList Component Requirements

- **FR-013**: TaskList MUST fetch tasks from GET /api/{user_id}/tasks using API client with JWT Bearer token
- **FR-014**: TaskList MUST render TaskCard component for each task in the array
- **FR-015**: TaskList MUST display EmptyState component when tasks array is empty
- **FR-016**: TaskList MUST show loading skeleton while initial fetch is pending
- **FR-017**: TaskList MUST handle API errors gracefully with error message and retry button
- **FR-018**: TaskList MUST be scrollable when content exceeds viewport height
- **FR-019**: TaskList MUST display tasks in chronological order (newest first or oldest first)

#### TaskCard Component Requirements

- **FR-020**: TaskCard MUST be a Client Component (requires 'use client' directive) for interactive toggle/delete
- **FR-021**: TaskCard MUST display task title prominently
- **FR-022**: TaskCard MUST display task completion status with checkbox/toggle
- **FR-023**: TaskCard MUST display delete button (icon or text)
- **FR-024**: TaskCard MUST show task description preview if description exists (truncated to 2 lines)
- **FR-025**: TaskCard MUST show task created date/time in relative format (e.g., "2 hours ago")
- **FR-026**: TaskCard checkbox MUST toggle completion status on click
- **FR-027**: TaskCard MUST apply visual distinction for completed tasks (strikethrough text, muted color, or different background)
- **FR-028**: TaskCard delete button MUST show confirmation dialog before deletion

#### TaskCard Optimistic Updates

- **FR-029**: TaskCard toggle action MUST apply optimistic UI update immediately (before API call completes)
- **FR-030**: TaskCard optimistic update MUST use React useOptimistic hook or local state for immediate feedback
- **FR-031**: TaskCard optimistic update MUST send PATCH /api/tasks/{task_id} with JWT Bearer token
- **FR-032**: TaskCard MUST rollback optimistic update if API call fails (revert to original completion state)
- **FR-033**: TaskCard MUST show subtle loading indicator during API call (spinner on checkbox or opacity change)
- **FR-034**: TaskCard MUST display error toast if toggle fails with message "Failed to update task. Please try again."
- **FR-035**: TaskCard MUST disable further toggles while API call is pending (prevent race conditions)

#### TaskCard Delete Functionality

- **FR-036**: TaskCard delete button MUST show confirmation dialog with message "Are you sure you want to delete this task?"
- **FR-037**: TaskCard delete dialog MUST have "Delete" and "Cancel" buttons
- **FR-038**: TaskCard delete action MUST apply optimistic UI update (TaskCard disappears immediately)
- **FR-039**: TaskCard delete action MUST send DELETE /api/tasks/{task_id} with JWT Bearer token
- **FR-040**: TaskCard MUST rollback optimistic deletion if API call fails (TaskCard reappears)
- **FR-041**: TaskCard MUST display error toast if deletion fails with message "Failed to delete task."

#### AddTaskForm Component Requirements

- **FR-042**: AddTaskForm MUST be a Client Component (requires 'use client' directive) for form interactivity
- **FR-043**: AddTaskForm MUST display single-line input field for task title
- **FR-044**: AddTaskForm MUST display submit button labeled "Add Task" or similar
- **FR-045**: AddTaskForm MUST validate title field: required, 1-200 characters
- **FR-046**: AddTaskForm MUST show real-time validation feedback as user types
- **FR-047**: AddTaskForm MUST disable submit button when validation fails or title is empty
- **FR-048**: AddTaskForm MUST clear input field after successful task creation

#### AddTaskForm Optimistic Creation

- **FR-049**: AddTaskForm submit MUST apply optimistic UI update (new TaskCard appears immediately in TaskList)
- **FR-050**: AddTaskForm MUST send POST /api/tasks with JWT Bearer token and task data (title, description optional)
- **FR-051**: AddTaskForm optimistic task MUST be replaced with server response (includes id, timestamps, user_id)
- **FR-052**: AddTaskForm MUST rollback optimistic creation if API call fails (remove optimistic TaskCard)
- **FR-053**: AddTaskForm MUST display error toast if creation fails with message "Failed to create task. Please try again."
- **FR-054**: AddTaskForm MUST show loading spinner on submit button during API call

#### Responsive Design Requirements

- **FR-055**: All components MUST use Tailwind CSS utility classes for styling (no custom CSS files)
- **FR-056**: Navbar MUST be responsive: full-width on all screens, collapse user email on mobile (<768px)
- **FR-057**: TaskList MUST be responsive: full-width TaskCards on mobile, max-width constrained on desktop
- **FR-058**: TaskCard MUST be responsive: vertical stacking on mobile, horizontal layout on desktop (flex)
- **FR-059**: AddTaskForm MUST be responsive: full-width input on mobile, constrained width on desktop
- **FR-060**: All touch targets (buttons, checkboxes) MUST be minimum 44x44px for mobile accessibility

#### Accessibility Requirements

- **FR-061**: All interactive elements MUST have proper ARIA labels (aria-label, aria-describedby)
- **FR-062**: TaskCard checkbox MUST have aria-label describing action (e.g., "Mark task as complete")
- **FR-063**: TaskCard delete button MUST have aria-label "Delete task: {title}"
- **FR-064**: AddTaskForm input MUST have associated label element (for screen readers)
- **FR-065**: Navbar logout button MUST have aria-label "Logout"
- **FR-066**: All form errors MUST be associated with inputs via aria-describedby
- **FR-067**: Keyboard navigation MUST work: Tab through all interactive elements, Enter to activate

#### Data Flow Requirements

- **FR-068**: Dashboard MUST fetch tasks on initial load using GET /api/{user_id}/tasks
- **FR-069**: API client MUST extract user_id from JWT token (backend extracts from token, frontend uses /api/tasks endpoint)
- **FR-070**: All API calls (GET, POST, PATCH, DELETE) MUST include JWT Bearer token in Authorization header
- **FR-071**: TaskList MUST re-fetch tasks after successful mutations (create, toggle, delete) to ensure consistency
- **FR-072**: Dashboard MUST handle API errors (401, 422, 500, network) with appropriate user messages

### Key Entities (Client-Side Components)

#### Navbar Component

Client Component for user profile display and logout.

| Attribute | Type | Notes |
|-----------|------|-------|
| userEmail | String | Extracted from JWT token claims |
| onLogout | Function | Calls Better Auth signOut() method |

#### TaskList Component

Container for task display, can be Server or Client Component.

| Attribute | Type | Notes |
|-----------|------|-------|
| tasks | Task[] | Array of tasks from GET /api/{user_id}/tasks |
| isLoading | Boolean | Loading state during initial fetch |
| error | String \| null | Error message if fetch fails |

#### TaskCard Component

Client Component for individual task display and interaction.

| Attribute | Type | Notes |
|-----------|------|-------|
| task | Task | Task object with id, title, completed, etc. |
| optimisticCompleted | Boolean | Optimistic completion state (may differ from task.completed during API call) |
| isToggling | Boolean | Whether toggle API call is pending |
| isDeleting | Boolean | Whether delete API call is pending |
| onToggle | Function | Handles completion toggle with optimistic update |
| onDelete | Function | Handles deletion with confirmation and optimistic update |

#### AddTaskForm Component

Client Component for task creation.

| Attribute | Type | Notes |
|-----------|------|-------|
| title | String | Current input value |
| titleError | String \| null | Validation error message |
| isSubmitting | Boolean | Whether create API call is pending |
| onSubmit | Function | Handles task creation with optimistic update |

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Dashboard loads and displays tasks within 2 seconds of authentication
- **SC-002**: Navbar displays user email within 500ms of dashboard load
- **SC-003**: TaskCard optimistic toggle updates UI within 50ms of checkbox click
- **SC-004**: AddTaskForm optimistic creation shows new task in TaskList within 50ms of submit
- **SC-005**: All API calls include JWT Bearer token in Authorization header (100% coverage)
- **SC-006**: Optimistic updates rollback within 100ms of API error response
- **SC-007**: Error toast notifications appear within 500ms of error occurrence
- **SC-008**: Logout redirects to /signin within 1 second of button click
- **SC-009**: Dashboard is usable on mobile (320px width) without horizontal scroll
- **SC-010**: All interactive elements are keyboard-accessible (100% Tab navigation coverage)
- **SC-011**: TaskList displays up to 100 tasks without performance degradation (smooth scrolling)
- **SC-012**: AddTaskForm clears input and returns focus after successful creation within 200ms
- **SC-013**: Confirmation dialog for delete appears within 100ms of button click
- **SC-014**: GET /api/{user_id}/tasks request completes within 1 second under normal conditions

## Assumptions

1. Backend API is running on http://localhost:8000/api (or NEXT_PUBLIC_API_URL value)
2. Backend endpoint GET /api/{user_id}/tasks exists and returns Task[] array
3. Backend endpoint POST /api/tasks accepts {title, description?} and returns created Task
4. Backend endpoint PATCH /api/tasks/{task_id} accepts {completed} and returns updated Task
5. Backend endpoint DELETE /api/tasks/{task_id} returns 204 No Content or 200 OK
6. Backend extracts user_id from JWT token (frontend doesn't need to include user_id in URL)
7. JWT token is available in Better Auth session and valid (not expired)
8. All API endpoints require JWT Bearer token in Authorization header
9. Backend returns 401 Unauthorized for invalid/expired tokens
10. Backend returns 422 Unprocessable Entity for validation errors
11. Task title validation (1-200 chars) matches backend validation exactly
12. Users have modern browsers with JavaScript enabled
13. Network latency is typically <200ms for API calls
14. Maximum 1000 tasks per user (no pagination in Sprint 2)
15. Optimistic updates provide better UX despite rollback risk

## Out of Scope (Not in Sprint 2)

- Task edit functionality (inline editing of title/description)
- Task filtering (All/Active/Completed filters) - Sprint 3 or 4
- Task search functionality
- Task sorting options (by date, title, completion)
- Bulk task operations (select multiple, bulk delete)
- Task categories, tags, or labels
- Task due dates or reminders
- Drag-and-drop reordering
- Task description expansion (TaskCard shows preview only)
- Profile page (separate from Navbar profile display)
- Dark mode toggle
- Keyboard shortcuts beyond basic navigation
- Real-time updates (websockets, polling)
- Offline support or caching
- Undo/redo functionality
- Task statistics or analytics

## Dependencies

- **Sprint 1**: MUST be complete (Better Auth, API client, middleware all set up)
- **Backend API**: FastAPI backend running with task endpoints (GET, POST, PATCH, DELETE /api/tasks)
- **Better Auth Session**: Valid JWT token in session for API calls
- **API Client**: `frontend/src/lib/api.ts` with JWT Bearer token injection
- **Type Definitions**: `frontend/src/types/task.ts` with Task interface
- **Tailwind CSS**: Configured and working for component styling
- **Sonner Library**: Installed for toast notifications (added in Sprint 1 package.json)
- **React Hooks**: useOptimistic (React 19) or useState for optimistic updates
