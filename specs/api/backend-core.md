# Feature Specification: Phase II Backend API Core

**Feature Branch**: `001-backend-api-core`
**Created**: 2025-12-21
**Status**: Draft
**Input**: User description: "Create a comprehensive Technical Specification for the Phase II Backend - Python FastAPI service using SQLModel for multi-user Todo management with JWT authentication"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Authenticated Task Creation (Priority: P1)

As an authenticated user, I want to create new tasks in my personal task list so that I can track my work items securely.

**Why this priority**: Task creation is the foundational CRUD operation. Without the ability to create tasks, no other task operations are meaningful. This also establishes the JWT authentication flow that all other operations depend on.

**Independent Test**: Can be fully tested by sending a POST request with a valid JWT token and task payload, then verifying the task is created and associated with the correct user_id.

**Acceptance Scenarios**:

1. **Given** a valid JWT token in the Authorization header, **When** I POST to `/api/tasks/` with a valid task payload (title, description), **Then** the system creates a task with `user_id` from the JWT and returns status 201 with the created task data
2. **Given** no Authorization header, **When** I POST to `/api/tasks/`, **Then** the system returns 401 Unauthorized
3. **Given** an expired JWT token, **When** I POST to `/api/tasks/`, **Then** the system returns 401 with message "Token expired"
4. **Given** a valid JWT token, **When** I POST with missing required `title` field, **Then** the system returns 422 Unprocessable Entity with validation error details

---

### User Story 2 - Task Retrieval with User Isolation (Priority: P1)

As an authenticated user, I want to retrieve only my own tasks so that I can view my personal task list without seeing other users' data.

**Why this priority**: User data isolation is a NON-NEGOTIABLE security requirement per the Constitution. This story validates that the system enforces strict multi-tenant boundaries.

**Independent Test**: Can be tested by creating tasks for two different users, then verifying each user can only retrieve their own tasks.

**Acceptance Scenarios**:

1. **Given** I am authenticated as User A with 3 tasks, **When** I GET `/api/tasks/`, **Then** I receive exactly my 3 tasks and no tasks from other users
2. **Given** I am authenticated as User A, **When** User B creates a task, **Then** User A's task list remains unchanged
3. **Given** I am authenticated, **When** I GET `/api/tasks/`, **Then** the response includes standardized JSON format with `data` array and `meta` object
4. **Given** I am authenticated with no tasks, **When** I GET `/api/tasks/`, **Then** I receive an empty `data` array with `meta.total: 0`

---

### User Story 3 - Task Update with Ownership Validation (Priority: P2)

As an authenticated user, I want to update my existing tasks so that I can modify task details and mark tasks as completed.

**Why this priority**: Update operations are essential for task lifecycle management but depend on task retrieval working correctly.

**Independent Test**: Can be tested by creating a task, then sending PATCH requests to modify title, description, and completed status.

**Acceptance Scenarios**:

1. **Given** I own task with ID `123`, **When** I PATCH `/api/tasks/123` with `{"completed": true}`, **Then** the task is updated and returned with status 200
2. **Given** User A owns task `123`, **When** User B attempts to PATCH `/api/tasks/123`, **Then** the system returns 403 Forbidden
3. **Given** I am authenticated, **When** I PATCH a non-existent task ID, **Then** the system returns 404 Not Found
4. **Given** I own a task, **When** I PATCH with invalid data types, **Then** the system returns 422 Unprocessable Entity

---

### User Story 4 - Task Deletion with Authorization (Priority: P2)

As an authenticated user, I want to delete my own tasks so that I can remove completed or irrelevant items from my list.

**Why this priority**: Delete is destructive and requires robust authorization checks to prevent data loss across user boundaries.

**Independent Test**: Can be tested by creating a task, deleting it, then verifying it no longer appears in the user's task list.

**Acceptance Scenarios**:

1. **Given** I own task `123`, **When** I DELETE `/api/tasks/123`, **Then** the task is removed and status 204 is returned
2. **Given** User A owns task `123`, **When** User B attempts to DELETE `/api/tasks/123`, **Then** the system returns 403 Forbidden and the task remains intact
3. **Given** I am authenticated, **When** I DELETE a non-existent task ID, **Then** the system returns 404 Not Found
4. **Given** I delete a task, **When** I subsequently GET my tasks, **Then** the deleted task is not present

---

### User Story 5 - Single Task Retrieval (Priority: P3)

As an authenticated user, I want to retrieve a specific task by ID so that I can view detailed information about a single task.

**Why this priority**: Detail view is useful but not essential for core functionality.

**Independent Test**: Can be tested by creating a task, then retrieving it by ID.

**Acceptance Scenarios**:

1. **Given** I own task `123`, **When** I GET `/api/tasks/123`, **Then** I receive the full task details with status 200
2. **Given** User A owns task `123`, **When** User B attempts to GET `/api/tasks/123`, **Then** the system returns 403 Forbidden
3. **Given** I am authenticated, **When** I GET a non-existent task ID, **Then** the system returns 404 Not Found

---

### Edge Cases

- What happens when JWT token is malformed (not valid base64)?
  - System returns 401 Unauthorized with message "Invalid token"
- How does system handle concurrent updates to the same task?
  - Last-write-wins with optimistic concurrency (no locking)
- What happens when database connection fails?
  - System returns 503 Service Unavailable with retry guidance
- How are UUIDs validated in path parameters?
  - Invalid UUID format returns 422 Unprocessable Entity
- What happens when user_id in token doesn't exist in database?
  - System returns 401 Unauthorized (token considered invalid)

## Requirements *(mandatory)*

### Functional Requirements

#### Authentication & Security

- **FR-001**: System MUST reject any request to protected endpoints without a valid `Authorization: Bearer <token>` header
- **FR-002**: System MUST verify JWT tokens using the `BETTER_AUTH_SECRET` environment variable with HS256 algorithm
- **FR-003**: System MUST extract `user_id` from the JWT `sub` claim for user identification
- **FR-004**: System MUST return 401 Unauthorized for expired tokens with message "Token expired"
- **FR-005**: System MUST return 401 Unauthorized for invalid/malformed tokens with message "Invalid token"

#### Data Isolation (NON-NEGOTIABLE)

- **FR-006**: System MUST include `WHERE user_id = :current_user_id` in every database query for task operations
- **FR-007**: System MUST return 403 Forbidden when a user attempts to access a task owned by another user
- **FR-008**: System MUST never return task data belonging to a user other than the authenticated user
- **FR-009**: System MUST assign `user_id` from the authenticated user when creating new tasks

#### CRUD Operations

- **FR-010**: System MUST provide `POST /api/tasks/` endpoint to create new tasks
- **FR-011**: System MUST provide `GET /api/tasks/` endpoint to list all tasks for the authenticated user
- **FR-012**: System MUST provide `GET /api/tasks/{task_id}` endpoint to retrieve a single task
- **FR-013**: System MUST provide `PATCH /api/tasks/{task_id}` endpoint to update task fields
- **FR-014**: System MUST provide `DELETE /api/tasks/{task_id}` endpoint to remove a task

#### Response Format

- **FR-015**: System MUST return all successful responses in standardized JSON format:
  ```json
  {
    "data": <resource or array of resources>,
    "meta": {
      "timestamp": "<ISO8601>",
      "request_id": "<uuid>",
      "total": <count for list operations>
    }
  }
  ```
- **FR-016**: System MUST return all error responses in standardized format:
  ```json
  {
    "error": {
      "code": "<HTTP_STATUS_CODE>",
      "message": "<human-readable message>",
      "details": <optional validation errors>
    },
    "meta": {
      "timestamp": "<ISO8601>",
      "request_id": "<uuid>"
    }
  }
  ```

#### Database Operations

- **FR-017**: System MUST use async database sessions for all database operations
- **FR-018**: System MUST index the `user_id` column on the Task table for query performance
- **FR-019**: System MUST use UUID type for `id` and `user_id` fields

### Key Entities

#### Task Entity

Represents a single todo item belonging to a specific user.

| Attribute   | Type      | Constraints                        |
|-------------|-----------|-----------------------------------|
| id          | UUID      | Primary key, auto-generated       |
| user_id     | UUID      | Foreign key to User, indexed, NOT NULL |
| title       | String    | Required, max 255 characters      |
| description | String    | Optional, max 2000 characters     |
| completed   | Boolean   | Default: false                    |
| created_at  | DateTime  | Auto-set on creation              |
| updated_at  | DateTime  | Auto-set on update                |

#### User Entity (Reference Only - Managed by Better Auth)

Users are managed by the Better Auth system on the frontend. The backend references users via `user_id` extracted from JWT tokens.

| Attribute   | Type      | Notes                             |
|-------------|-----------|-----------------------------------|
| id          | UUID      | Referenced in JWT `sub` claim     |

### Data Contracts (Pydantic Schemas)

#### TaskCreate (Request Body for POST)

```
{
  "title": string (required, 1-255 chars),
  "description": string (optional, max 2000 chars)
}
```

#### TaskUpdate (Request Body for PATCH)

```
{
  "title": string (optional, 1-255 chars),
  "description": string (optional, max 2000 chars),
  "completed": boolean (optional)
}
```
All fields are optional; only provided fields are updated.

#### TaskRead (Response Body)

```
{
  "id": UUID,
  "user_id": UUID,
  "title": string,
  "description": string | null,
  "completed": boolean,
  "created_at": ISO8601 datetime,
  "updated_at": ISO8601 datetime
}
```

### Error Taxonomy

| HTTP Status | Error Code | Condition                                    | Message                          |
|-------------|------------|----------------------------------------------|----------------------------------|
| 401         | UNAUTHORIZED | Missing Authorization header               | "Authorization header required"  |
| 401         | UNAUTHORIZED | Malformed/invalid JWT token                | "Invalid token"                  |
| 401         | UNAUTHORIZED | Expired JWT token                          | "Token expired"                  |
| 401         | UNAUTHORIZED | User ID from token not found               | "Invalid token"                  |
| 403         | FORBIDDEN    | User attempting to access another's task   | "Access denied"                  |
| 404         | NOT_FOUND    | Task ID does not exist                     | "Task not found"                 |
| 422         | VALIDATION_ERROR | Invalid request body or parameters      | "Validation failed"              |
| 500         | INTERNAL_ERROR | Unexpected server error                   | "Internal server error"          |
| 503         | SERVICE_UNAVAILABLE | Database connection failure           | "Service temporarily unavailable"|

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 100% of API requests without valid JWT tokens are rejected with 401 status
- **SC-002**: 100% of cross-user data access attempts are blocked with 403 status
- **SC-003**: API response time for single task operations is under 200ms at p95 under normal load
- **SC-004**: API response time for task list operations (up to 100 tasks) is under 500ms at p95
- **SC-005**: Zero data leakage incidents where User A can access User B's tasks
- **SC-006**: All database operations complete using async sessions (no blocking I/O)
- **SC-007**: Task creation assigns correct `user_id` from JWT in 100% of cases
- **SC-008**: All API responses conform to the standardized JSON envelope format
- **SC-009**: System handles 100 concurrent authenticated users without error rate exceeding 0.1%

## Assumptions

1. Better Auth on the frontend issues JWT tokens with `sub` claim containing the user's UUID
2. The `BETTER_AUTH_SECRET` is a shared secret between frontend and backend, stored securely in environment variables
3. JWT tokens use HS256 algorithm for signing
4. Database is PostgreSQL (Neon Serverless) with async driver support
5. Task IDs and User IDs are UUID v4 format
6. Frontend handles token refresh; backend only validates tokens
7. No pagination is required for initial implementation (future enhancement)
8. No sorting/filtering query parameters are required for initial implementation

## Out of Scope

- User registration/authentication (handled by Better Auth on frontend)
- Task categories, tags, or labels
- Task due dates or reminders
- Task sharing between users
- Batch operations (bulk create/update/delete)
- Real-time updates (WebSockets)
- Rate limiting (future enhancement)
- API versioning (future enhancement)

## Dependencies

- **Better Auth (Frontend)**: JWT token issuance and refresh
- **Neon PostgreSQL**: Database hosting
- **PyJWT**: JWT token verification library
- **SQLModel**: ORM for database operations
- **FastAPI**: Web framework with async support
- **Pydantic**: Request/response validation
