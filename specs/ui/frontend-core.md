# Feature Specification: Phase II Frontend UI Core

**Feature Branch**: `001-frontend-core`
**Created**: 2025-12-23
**Status**: Draft
**Input**: User description: "Create the Frontend Technical Specification in /specs/ui/frontend-core.md. This spec must strictly align with Constitution v2.0.0 and cover: 1. CORE STACK: Next.js 15+ (App Router), TypeScript, Tailwind CSS. 2. AUTHENTICATION: Better Auth integration with JWT plugin enabled. 3. PROTECTED ROUTES: Middleware to redirect unauthenticated users to /signin. 4. API CLIENT: Centralized client in 'frontend/src/lib/api.ts' that automatically attaches the JWT Bearer token to all requests. 5. UI FEATURES: Auth Pages: Signin and Signup. Todo Dashboard: Task listing, Add task form, and Toggle/Delete actions. User Profile: Logout functionality and display current user name. 6. ACCEPTANCE CRITERIA: Responsive design, form validation, and instant feedback for task operations."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - User Registration (Priority: P1)

As a new user, I want to create an account so that I can have a personal, secure space to manage my tasks.

**Why this priority**: Registration is the entry point for all new users. Without account creation, the application has no user base.

**Independent Test**: Can be tested by visiting /signup, entering valid credentials (email, password, confirm password), and verifying successful account creation with redirect to /dashboard and JWT token stored securely.

**Acceptance Scenarios**:

1. **Given** I am on /signup page, **When** I enter a valid email and matching password (min 8 chars), **Then** my account is created, JWT token is issued, and I am redirected to /dashboard
2. **Given** I am on /signup page, **When** I enter an email that already exists, **Then** I see error message "Email already registered"
3. **Given** I am on /signup page, **When** I enter a password under 8 characters, **Then** I see validation feedback "Password must be at least 8 characters"
4. **Given** I am on /signup page, **When** password and confirm password don't match, **Then** I see error message "Passwords do not match"
5. **Given** I am on /signup page, **When** I submit without email, **Then** I see validation error "Email is required"

---

### User Story 2 - User Login (Priority: P1)

As a registered user, I want to log in to my account so that I can access my personal task list securely.

**Why this priority**: Login is essential for returning users to access their data. Core authentication flow with JWT token issuance.

**Independent Test**: Can be tested by visiting /signin, entering valid credentials, and verifying successful authentication with JWT token stored and redirect to /dashboard.

**Acceptance Scenarios**:

1. **Given** I am on /signin page, **When** I enter valid credentials, **Then** JWT token is issued, stored securely, and I am redirected to /dashboard
2. **Given** I am on /signin page, **When** I enter invalid credentials, **Then** I see error message "Invalid email or password"
3. **Given** I am logged in with valid JWT, **When** I navigate to protected routes, **Then** I can access them without re-authentication
4. **Given** I am not logged in, **When** I try to access /dashboard or any protected route, **Then** middleware intercepts and redirects me to /signin
5. **Given** I am logged in, **When** my JWT token expires, **Then** I am redirected to /signin with message "Session expired, please log in again"

---

### User Story 3 - Protected Route Access Control (Priority: P1)

As the system, I must protect all dashboard routes from unauthenticated access to ensure data security.

**Why this priority**: Security is non-negotiable. Unauthorized access to user data creates legal and compliance liability.

**Independent Test**: Can be tested by attempting to access /dashboard, /profile, or any protected route without authentication and verifying redirect to /signin.

**Acceptance Scenarios**:

1. **Given** I am not authenticated, **When** I navigate to /dashboard, **Then** Next.js middleware redirects me to /signin
2. **Given** I am not authenticated, **When** I navigate to /profile, **Then** Next.js middleware redirects me to /signin
3. **Given** I have an expired JWT token, **When** I access a protected route, **Then** middleware detects expiration and redirects to /signin
4. **Given** I am authenticated, **When** I access /signin or /signup, **Then** I am redirected to /dashboard

---

### User Story 4 - View Task List (Priority: P1)

As an authenticated user, I want to see all my tasks on the dashboard so that I have an overview of my work.

**Why this priority**: The task list is the core feature users interact with daily. Essential for task management.

**Independent Test**: Can be tested by logging in and verifying the task list fetches from backend API with JWT Bearer token and displays correctly.

**Acceptance Scenarios**:

1. **Given** I am logged in with existing tasks, **When** I view /dashboard, **Then** API client attaches JWT Bearer token and fetches my tasks, displaying them in a list
2. **Given** I am logged in with no tasks, **When** I view /dashboard, **Then** I see empty state message "No tasks yet. Create your first task to get started!"
3. **Given** I am viewing /dashboard, **When** page loads, **Then** I see loading skeleton while data is being fetched
4. **Given** tasks are loaded, **When** displayed, **Then** each task shows title, description preview, completion status, and action buttons (toggle, delete)
5. **Given** API call fails (network error), **When** fetching tasks, **Then** I see error message "Failed to load tasks. Please try again." with retry button

---

### User Story 5 - Create New Task (Priority: P1)

As an authenticated user, I want to create new tasks so that I can track items I need to complete.

**Why this priority**: Task creation is fundamental to the application's purpose. Users must be able to add tasks.

**Independent Test**: Can be tested by clicking "Add Task" button, filling form with valid data, and verifying task is sent to backend API with JWT token and appears in list.

**Acceptance Scenarios**:

1. **Given** I am on /dashboard, **When** I click "Add Task" button, **Then** a form/modal appears with fields for title and description
2. **Given** I am filling add task form, **When** I enter valid title (1-200 chars) and optional description, **Then** form validates in real-time
3. **Given** I submit valid task, **When** API client sends POST request with JWT Bearer token, **Then** task is created and appears in my list with optimistic UI update
4. **Given** I submit task with empty title, **When** validation runs, **Then** I see error "Title is required" and submit is disabled
5. **Given** I submit task with title over 200 characters, **When** validation runs, **Then** I see error "Title must be 200 characters or less"
6. **Given** task creation API call fails, **When** error is returned, **Then** optimistic update is rolled back and I see error toast "Failed to create task. Please try again."

---

### User Story 6 - Mark Task Complete/Incomplete (Priority: P1)

As an authenticated user, I want to toggle task completion status so that I can track my progress.

**Why this priority**: Task completion is a core interaction that users perform frequently throughout their day.

**Independent Test**: Can be tested by clicking completion checkbox on a task and verifying API client sends PATCH request with JWT token to update status.

**Acceptance Scenarios**:

1. **Given** I have an incomplete task, **When** I click the checkbox, **Then** task is marked as complete with visual indication (strikethrough, different color) and API client sends PATCH with JWT Bearer token
2. **Given** I have a complete task, **When** I click the checkbox, **Then** task is marked as incomplete and API client sends PATCH with JWT Bearer token
3. **Given** I toggle completion, **When** action is performed, **Then** UI updates optimistically before server confirmation
4. **Given** server confirms success, **When** response received, **Then** completion state persists on page refresh
5. **Given** API call fails, **When** toggling completion, **Then** optimistic update is rolled back and I see error toast

---

### User Story 7 - Delete Task (Priority: P1)

As an authenticated user, I want to delete tasks I no longer need so that I can keep my list organized.

**Why this priority**: Users need to remove completed or irrelevant tasks to maintain a clean workspace.

**Independent Test**: Can be tested by clicking delete button on a task, confirming in modal, and verifying API client sends DELETE request with JWT token.

**Acceptance Scenarios**:

1. **Given** I have an existing task, **When** I click delete button, **Then** I see confirmation dialog "Are you sure you want to delete this task?"
2. **Given** I confirm deletion, **When** I click "Delete", **Then** API client sends DELETE request with JWT Bearer token and task is removed from list with optimistic UI update
3. **Given** I click delete, **When** I click "Cancel" in confirmation, **Then** dialog closes and task remains unchanged
4. **Given** deletion API call fails, **When** error is returned, **Then** optimistic update is rolled back and I see error toast "Failed to delete task. Please try again."

---

### User Story 8 - User Profile Display (Priority: P2)

As an authenticated user, I want to see my profile information (name, email) so that I know which account I'm logged into.

**Why this priority**: User profile provides context and personalization but isn't essential for core task management.

**Independent Test**: Can be tested by logging in and verifying user name/email is displayed in navigation bar, fetched from JWT token claims.

**Acceptance Scenarios**:

1. **Given** I am logged in, **When** I view any page, **Then** navigation bar displays my email address extracted from JWT token
2. **Given** I am on /dashboard, **When** I click my profile icon/name, **Then** I see a dropdown with "Profile" and "Logout" options
3. **Given** I click "Profile" option, **When** navigating, **Then** I am taken to /profile page showing my full user details

---

### User Story 9 - User Logout (Priority: P2)

As an authenticated user, I want to log out of my account so that I can secure my session when done.

**Why this priority**: Logout is important for security but users interact with it less frequently than core task operations.

**Independent Test**: Can be tested by clicking logout button and verifying JWT token is cleared, session is terminated, and redirect to /signin occurs.

**Acceptance Scenarios**:

1. **Given** I am logged in, **When** I click logout button in profile dropdown, **Then** Better Auth clears JWT token, session is terminated, and I am redirected to /signin
2. **Given** I have logged out, **When** I try to access /dashboard or protected routes, **Then** middleware redirects me to /signin
3. **Given** I log out, **When** I click browser back button, **Then** I cannot access protected pages and am redirected to /signin

---

### User Story 10 - Filter Tasks by Status (Priority: P3)

As an authenticated user, I want to filter my tasks by status (All, Active, Completed) so that I can focus on specific items.

**Why this priority**: Filtering helps users manage larger task lists but isn't essential for basic functionality.

**Independent Test**: Can be tested by selecting different filter options (All, Active, Completed) and verifying the displayed list updates with client-side filtering.

**Acceptance Scenarios**:

1. **Given** I have both complete and incomplete tasks, **When** I filter by "Active", **Then** I see only incomplete tasks
2. **Given** I have both complete and incomplete tasks, **When** I filter by "Completed", **Then** I see only completed tasks
3. **Given** I am filtering tasks, **When** I select "All", **Then** I see all tasks regardless of status
4. **Given** I apply a filter, **When** I refresh the page, **Then** filter selection is preserved via URL query params or local state

---

### Edge Cases

- What happens when the backend API is unavailable?
  - API client detects network error, user sees toast notification "Unable to connect to server. Please check your connection and try again." with retry button
  - Cached/existing task data remains visible, mutations are queued or fail gracefully

- How does the system handle concurrent edits from multiple sessions?
  - Last-write-wins with timestamp-based conflict detection on backend
  - Frontend refetches data after mutations to ensure consistency

- What happens when JWT token expires mid-use?
  - API client detects 401 Unauthorized response from backend
  - Better Auth attempts token refresh automatically
  - If refresh fails, user is redirected to /signin with message "Session expired, please log in again"
  - Unsaved form data is lost (no automatic persistence)

- How are network failures during task operations handled?
  - Optimistic updates are applied immediately for better UX
  - On API error, optimistic updates are rolled back
  - Error toast notification appears with retry option
  - User can retry the operation manually

- What happens when user tries to access /signin while already authenticated?
  - Middleware detects valid JWT token and redirects to /dashboard

- What happens when form validation fails on the frontend but passes on backend (or vice versa)?
  - Frontend validation MUST match backend validation rules exactly (1-200 chars for title)
  - If backend returns 422 Unprocessable Entity, frontend displays server-side validation errors
  - Mismatch indicates a bug and must be logged for investigation

- What happens on mobile devices with slow connections?
  - Loading skeletons provide immediate feedback
  - Optimistic updates ensure UI remains responsive
  - Timeout for API calls set to 10 seconds before showing error

## Requirements *(mandatory)*

### Functional Requirements

#### Core Technology Stack

- **FR-001**: Frontend MUST be built using Next.js 15+ (or 16+ per Constitution) with App Router architecture (NOT Pages Router)
- **FR-002**: All frontend code MUST be written in TypeScript with strict mode enabled
- **FR-003**: All styling MUST use Tailwind CSS utility classes (no inline styles or CSS modules)
- **FR-004**: Application MUST be responsive and function on screen sizes from 320px (mobile) to 1920px+ (desktop)

#### Authentication & Authorization (Better Auth)

- **FR-005**: Frontend MUST integrate Better Auth library with JWT Plugin enabled
- **FR-006**: Better Auth MUST be configured to issue JWT tokens upon successful signup/login
- **FR-007**: JWT tokens MUST be stored securely (httpOnly cookies or secure storage as per Better Auth best practices)
- **FR-008**: Frontend MUST provide /signup page for new user registration with fields: email (required), password (required, min 8 chars), confirm password (required)
- **FR-009**: Frontend MUST provide /signin page for existing user authentication with fields: email (required), password (required)
- **FR-010**: Frontend MUST validate password requirements: minimum 8 characters
- **FR-011**: Frontend MUST validate email format using standard email regex
- **FR-012**: Frontend MUST compare password and confirm password fields and show error if they don't match
- **FR-013**: Frontend MUST provide logout functionality that clears JWT token and terminates session via Better Auth
- **FR-014**: Frontend MUST handle JWT token refresh automatically before expiration using Better Auth built-in refresh logic

#### Protected Routes Middleware

- **FR-015**: Frontend MUST implement Next.js middleware to protect all routes except /signin and /signup
- **FR-016**: Middleware MUST check for valid JWT token on every protected route access
- **FR-017**: Middleware MUST redirect unauthenticated users to /signin when accessing protected routes
- **FR-018**: Middleware MUST redirect authenticated users from /signin and /signup to /dashboard
- **FR-019**: Middleware MUST check JWT token expiration and redirect to /signin if expired (after refresh attempt fails)

#### API Client with JWT Bearer Token

- **FR-020**: Frontend MUST implement centralized API client in frontend/src/lib/api.ts
- **FR-021**: API client MUST automatically attach JWT Bearer token to Authorization header for ALL requests
- **FR-022**: API client MUST extract JWT token from Better Auth session/storage
- **FR-023**: API client MUST format Authorization header as: "Authorization: Bearer <token>"
- **FR-024**: API client MUST handle 401 Unauthorized responses by triggering logout and redirecting to /signin
- **FR-025**: API client MUST handle 422 Unprocessable Entity by displaying server-side validation errors
- **FR-026**: API client MUST handle network errors (timeout, connection refused) with user-friendly error messages
- **FR-027**: API client MUST set timeout for all requests (recommended 10 seconds)
- **FR-028**: API client MUST support GET, POST, PATCH, DELETE methods for task operations

#### Task Management UI - Dashboard

- **FR-029**: Frontend MUST provide /dashboard route as main task management interface
- **FR-030**: /dashboard MUST display all tasks belonging to authenticated user (fetched via API client with JWT)
- **FR-031**: /dashboard MUST show loading skeleton while tasks are being fetched
- **FR-032**: /dashboard MUST display empty state UI when user has zero tasks with message and call-to-action
- **FR-033**: Each task in list MUST display: title, description preview (truncated), completion status, created date
- **FR-034**: Each task MUST have action buttons: toggle completion (checkbox), delete (button/icon)

#### Task Management UI - Create Task

- **FR-035**: /dashboard MUST have "Add Task" button prominently displayed
- **FR-036**: Clicking "Add Task" MUST open a form (inline or modal) with fields: title (required), description (optional)
- **FR-037**: Add task form MUST validate title: required, 1-200 characters
- **FR-038**: Add task form MUST show real-time validation feedback as user types
- **FR-039**: Add task form MUST have "Submit" and "Cancel" buttons
- **FR-040**: On valid submit, frontend MUST send POST request to backend API with JWT Bearer token
- **FR-041**: Frontend MUST apply optimistic UI update: new task appears in list immediately before API confirmation
- **FR-042**: On API success (201 Created), optimistic update is confirmed
- **FR-043**: On API error, optimistic update is rolled back and error toast is shown

#### Task Management UI - Toggle Completion

- **FR-044**: Each task MUST have completion checkbox/toggle button
- **FR-045**: Clicking checkbox MUST toggle task completion status (complete ↔ incomplete)
- **FR-046**: Frontend MUST send PATCH request to backend API with JWT Bearer token to update completion status
- **FR-047**: Frontend MUST apply optimistic UI update: visual state changes immediately (strikethrough, color change)
- **FR-048**: On API success, optimistic update is confirmed and persists
- **FR-049**: On API error, optimistic update is rolled back and error toast is shown

#### Task Management UI - Delete Task

- **FR-050**: Each task MUST have delete button (icon or text button)
- **FR-051**: Clicking delete MUST show confirmation dialog with message "Are you sure you want to delete this task?"
- **FR-052**: Confirmation dialog MUST have "Delete" and "Cancel" buttons
- **FR-053**: On "Delete" confirmation, frontend MUST send DELETE request to backend API with JWT Bearer token
- **FR-054**: Frontend MUST apply optimistic UI update: task is removed from list immediately
- **FR-055**: On API success (204 No Content or 200 OK), optimistic update is confirmed
- **FR-056**: On API error, optimistic update is rolled back (task reappears) and error toast is shown

#### Task Management UI - Filter Tasks

- **FR-057**: /dashboard MUST have filter buttons/tabs: "All", "Active" (incomplete), "Completed"
- **FR-058**: Clicking "All" MUST display all tasks regardless of completion status
- **FR-059**: Clicking "Active" MUST display only incomplete tasks (client-side filtering)
- **FR-060**: Clicking "Completed" MUST display only completed tasks (client-side filtering)
- **FR-061**: Active filter MUST be visually indicated (highlighted, underlined, or different color)

#### User Profile UI

- **FR-062**: Frontend MUST display current user's email in navigation bar (extracted from JWT token claims)
- **FR-063**: Frontend MUST provide profile icon/button in navigation bar
- **FR-064**: Clicking profile icon MUST show dropdown menu with options: "Profile", "Logout"
- **FR-065**: Clicking "Logout" MUST trigger Better Auth logout, clear JWT token, and redirect to /signin
- **FR-066**: (Optional) Clicking "Profile" MAY navigate to /profile page showing full user details

#### Form Validation & User Feedback

- **FR-067**: All form fields MUST show validation errors immediately below the field
- **FR-068**: Submit buttons MUST be disabled when form has validation errors
- **FR-069**: Frontend MUST show loading spinner on submit buttons during API calls
- **FR-070**: Frontend MUST display success toast notifications for successful operations (task created, deleted, updated)
- **FR-071**: Frontend MUST display error toast notifications for failed operations with user-friendly messages
- **FR-072**: Error messages MUST NOT expose sensitive system information (no stack traces, internal error codes)

#### Responsive Design

- **FR-073**: Application MUST be usable on mobile devices (320px width minimum)
- **FR-074**: Navigation bar MUST collapse to hamburger menu on mobile screens (< 768px)
- **FR-075**: Task list MUST stack vertically on mobile with full-width cards
- **FR-076**: Forms and modals MUST be responsive and not break on small screens
- **FR-077**: Touch targets (buttons, checkboxes) MUST be at least 44x44px for mobile accessibility

### Key Entities (Client-Side State)

#### User Session (Client-Side)

Represents the authenticated user's session state managed by Better Auth.

| Attribute   | Type      | Notes                                          |
|-------------|-----------|------------------------------------------------|
| user_id     | UUID      | Unique identifier extracted from JWT claims    |
| email       | String    | User's email address from JWT claims           |
| token       | String    | JWT access token (stored securely)             |
| refresh_token | String  | JWT refresh token (httpOnly cookie)            |
| expires_at  | DateTime  | Token expiration timestamp from JWT            |

#### Task (Client-Side View Model)

Represents a task as displayed in the UI, fetched from backend API.

| Attribute   | Type      | Notes                                          |
|-------------|-----------|------------------------------------------------|
| id          | UUID      | Unique task identifier (from backend)          |
| title       | String    | Task title (1-200 chars, validated)            |
| description | String    | Optional task description                      |
| completed   | Boolean   | Completion status                              |
| created_at  | DateTime  | When task was created (ISO 8601 string)        |
| updated_at  | DateTime  | When task was last modified (ISO 8601 string)  |
| user_id     | UUID      | Owner of the task (for verification)           |

#### Filter State (Client-Side UI State)

Represents the current task filter selection in the UI.

| Attribute   | Type      | Notes                                          |
|-------------|-----------|------------------------------------------------|
| filter      | Enum      | "all" \| "active" \| "completed"               |

#### Form State (Client-Side UI State)

Represents form data and validation state for task creation/editing.

| Attribute      | Type      | Notes                                       |
|----------------|-----------|---------------------------------------------|
| title          | String    | Task title being entered                    |
| description    | String    | Task description being entered              |
| titleError     | String    | Validation error message for title          |
| isSubmitting   | Boolean   | Whether form is currently being submitted   |

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Users can complete signup flow within 30 seconds from landing on /signup to reaching /dashboard
- **SC-002**: Users can complete login flow within 20 seconds from landing on /signin to reaching /dashboard
- **SC-003**: Users can create a new task within 10 seconds from clicking "Add Task" to seeing task in list
- **SC-004**: Task list displays within 2 seconds of /dashboard page load
- **SC-005**: 100% of protected routes redirect unauthenticated users to /signin (zero unauthorized access)
- **SC-006**: 100% of API requests include JWT Bearer token in Authorization header (verified via backend logs)
- **SC-007**: Optimistic UI updates are reflected within 50ms of user action (toggle, delete)
- **SC-008**: Form validation provides instant feedback within 100ms of field blur or input
- **SC-009**: Application renders correctly on screens from 320px to 1920px width without horizontal scroll
- **SC-010**: 95% of task operations (create, toggle, delete) complete successfully on first attempt (measured over 100 operations)
- **SC-011**: Error states are communicated to users within 3 seconds of occurrence with actionable error messages
- **SC-012**: JWT token refresh happens automatically without user intervention (no sudden logouts mid-session)
- **SC-013**: Users can logout successfully 100% of the time with immediate redirect to /signin
- **SC-014**: Empty state UI appears when user has zero tasks with clear call-to-action

## Assumptions

1. Backend API is available at a configurable URL (e.g., http://localhost:8000/api or production URL)
2. Backend API follows the contract defined in specs/api/backend-core.md
3. Backend API requires JWT Bearer token in Authorization header for all protected endpoints
4. Backend API validates JWT using shared BETTER_AUTH_SECRET environment variable
5. Backend API returns consistent error response format (JSON with "detail" field)
6. Better Auth library handles JWT token storage, refresh, and session management automatically
7. Better Auth is configured with JWT Plugin and shares BETTER_AUTH_SECRET with backend
8. Users have modern browsers (Chrome, Firefox, Safari, Edge - last 2 versions)
9. Network latency is typically under 200ms for API calls in production
10. Task title validation (1-200 chars) matches backend validation exactly
11. Users access the application via web browser (no native mobile app in this phase)
12. Email/password authentication is the only method (no social login in v1)
13. Maximum of 1000 tasks per user for reasonable UI performance (no pagination in v1)
14. JWT token expiration is set to reasonable duration (e.g., 1 hour access token, 7 days refresh token)
15. Optimistic updates are acceptable for better UX (with rollback on error)

## Out of Scope (Not in Phase II Frontend Core)

- Social authentication (Google, GitHub, OAuth providers)
- Task due dates, reminders, or push notifications
- Task categories, tags, labels, or color coding
- Drag-and-drop task reordering or priority management
- Real-time collaboration or task sharing between users
- Offline mode, service workers, or PWA features
- Keyboard shortcuts or accessibility beyond basic ARIA
- Dark mode toggle (UI is light mode only in v1)
- Task search functionality or advanced filtering
- Bulk task operations (select multiple, bulk delete)
- Export/import functionality (CSV, JSON)
- Task edit functionality (create/toggle/delete only in v1)
- User profile editing (name, password change)
- Email verification or password reset flows
- Rate limiting or throttling on frontend
- Internationalization (i18n) or multiple languages
- Analytics or usage tracking
- Admin panel or user management
- Task assignment to other users

## Dependencies

- **Backend API**: FastAPI backend (specs/api/backend-core.md) for all data operations (GET, POST, PATCH, DELETE tasks; user auth)
- **Better Auth Library**: npm package for authentication, JWT handling, and session management
- **Next.js Framework**: Version 15+ (or 16+ per Constitution) with App Router
- **TypeScript**: Strict mode enabled for type safety
- **Tailwind CSS**: For all styling and responsive design
- **Internet Connectivity**: Required for all operations (no offline support)
- **Environment Variables**: NEXT_PUBLIC_API_URL (backend URL), BETTER_AUTH_SECRET (shared secret)
- **Backend Availability**: Frontend is non-functional if backend is down (no fallback or cached operations)
