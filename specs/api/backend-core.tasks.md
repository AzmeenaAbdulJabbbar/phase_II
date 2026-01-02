# Tasks: Phase II Backend API Core

**Feature**: Backend API Core
**Branch**: `001-backend-api-core`
**Spec**: [backend-core.md](./backend-core.md)
**Plan**: [plan/plan.md](./plan/plan.md)
**Date**: 2025-12-21

## Overview

This task list implements a FastAPI backend with JWT authentication and strict user data isolation per the Constitution v1.1.0. Tasks are organized into sprints following test-first development.

**User Stories** (from spec.md):
- US1: Authenticated Task Creation (P1)
- US2: Task Retrieval with User Isolation (P1)
- US3: Task Update with Ownership Validation (P2)
- US4: Task Deletion with Authorization (P2)
- US5: Single Task Retrieval (P3)

---

## Sprint 1: Infrastructure (Environment, DB Connection, Models)

**Goal**: Establish project foundation with working database connection and models.

### Setup Tasks

- [x] T001 Create backend directory structure per plan in `backend/`
- [x] T002 [P] Create `backend/pyproject.toml` with dependencies (FastAPI, SQLModel, PyJWT, asyncpg, pydantic-settings)
- [x] T003 [P] Create `backend/.env.example` with required environment variables
- [x] T004 [P] Create `backend/.gitignore` for Python projects

### Test Setup

- [x] T005 Create `backend/tests/__init__.py` package marker
- [x] T006 Create `backend/tests/conftest.py` with pytest fixtures (test DB, mock JWT)

### Configuration

- [x] T007 Write failing test for config loading in `backend/tests/test_config.py`
- [x] T008 Implement `backend/src/config.py` with pydantic-settings (BETTER_AUTH_SECRET, DATABASE_URL)

### Database Connection

- [x] T009 Write failing test for database session in `backend/tests/test_database.py`
- [x] T010 Implement `backend/src/database.py` with async engine and `get_session` generator
  - **Depends on**: T008

### Models

- [x] T011 Write failing test for Task model in `backend/tests/test_models.py`
- [x] T012 Implement `backend/src/models.py` with Task SQLModel (per data-model.md)
  - **Depends on**: T010
  - **DoD**: Task has id, user_id (indexed), title, description, completed, created_at, updated_at

### Schemas

- [x] T013 [P] Write failing test for Pydantic schemas in `backend/tests/test_schemas.py`
- [x] T014 [P] Implement `backend/src/schemas.py` with TaskCreate, TaskUpdate, TaskRead
  - **DoD**: Validation rules match spec (title 1-255 chars, description max 2000)

**Sprint 1 Definition of Done**:
- [x] All tests pass
- [x] Database connects to Neon PostgreSQL
- [x] Task model creates table with correct indexes
- [x] Schemas validate per spec requirements

---

## Sprint 2: Security (JWT Middleware, Auth Dependency)

**Goal**: Implement JWT verification and establish authentication foundation.

### Custom Exceptions

- [x] T015 Write failing test for custom exceptions in `backend/tests/test_exceptions.py`
- [x] T016 Implement `backend/src/exceptions.py` with TaskNotFoundError, AccessDeniedError
  - **Depends on**: T006

### Response Helpers

- [x] T017 Write failing test for response envelope in `backend/tests/test_responses.py`
- [x] T018 Implement `backend/src/responses.py` with success_response, error_response
  - **DoD**: Returns `{data, meta}` format per FR-015, FR-016

### JWT Authentication

- [x] T019 Write failing test for JWT verification (valid token) in `backend/tests/test_auth.py`
- [x] T020 Write failing test for JWT verification (missing token) in `backend/tests/test_auth.py`
- [x] T021 Write failing test for JWT verification (expired token) in `backend/tests/test_auth.py`
- [x] T022 Write failing test for JWT verification (invalid token) in `backend/tests/test_auth.py`
- [x] T023 Implement `backend/src/auth.py` with HTTPBearer and `get_current_user_id` dependency
  - **Depends on**: T008, T016
  - **DoD**:
    - Uses `BETTER_AUTH_SECRET` with HS256 algorithm
    - Extracts `user_id` from JWT `sub` claim
    - Returns 401 for missing/invalid/expired tokens
    - All auth tests pass

**Sprint 2 Definition of Done**:
- [x] JWT verification works with Better Auth tokens
- [x] 401 returned for all invalid auth scenarios
- [x] Response envelope helpers produce correct format

---

## Sprint 3: Core CRUD (5 Features with User Isolation)

**Goal**: Implement all CRUD operations with strict user isolation.

### CRUD Layer

- [ ] T024 [US1] Write failing test for `create_task` with user_id in `backend/tests/test_crud.py`
- [ ] T025 [US2] Write failing test for `get_tasks` (list) filtering by user_id in `backend/tests/test_crud.py`
- [ ] T026 [US5] Write failing test for `get_task` (single) with ownership check in `backend/tests/test_crud.py`
- [ ] T027 [US3] Write failing test for `update_task` with ownership check in `backend/tests/test_crud.py`
- [ ] T028 [US4] Write failing test for `delete_task` with ownership check in `backend/tests/test_crud.py`

- [ ] T029 Implement `backend/src/crud.py` with all CRUD functions
  - **Depends on**: T010, T012, T016
  - **CRITICAL**: Every function MUST require `user_id` parameter (NON-NEGOTIABLE)
  - **DoD**:
    - `create_task(session, user_id, task_data)` → assigns user_id
    - `get_tasks(session, user_id)` → filters by user_id
    - `get_task(session, task_id, user_id)` → checks ownership, raises AccessDeniedError if not owner
    - `update_task(session, task_id, user_id, task_data)` → checks ownership before update
    - `delete_task(session, task_id, user_id)` → checks ownership before delete

### User Isolation Tests (MANDATORY)

- [ ] T030 Write test for 403 when User B accesses User A's task in `backend/tests/test_crud.py`
  - **DoD**: Proves `get_task` raises AccessDeniedError for cross-user access
- [ ] T031 Write test for 403 when User B updates User A's task in `backend/tests/test_crud.py`
- [ ] T032 Write test for 403 when User B deletes User A's task in `backend/tests/test_crud.py`

### API Endpoints - Create (US1)

- [ ] T033 [US1] Write failing integration test for POST /api/tasks/ in `backend/tests/test_api.py`
- [ ] T034 [US1] Write failing test for POST /api/tasks/ without auth (401) in `backend/tests/test_api.py`
- [ ] T035 [US1] Write failing test for POST /api/tasks/ with invalid payload (422) in `backend/tests/test_api.py`

### API Endpoints - List (US2)

- [ ] T036 [US2] Write failing integration test for GET /api/tasks/ in `backend/tests/test_api.py`
- [ ] T037 [US2] Write failing test for user isolation in GET /api/tasks/ in `backend/tests/test_api.py`
  - **DoD**: User A sees only User A's tasks, not User B's

### API Endpoints - Get Single (US5)

- [ ] T038 [US5] Write failing integration test for GET /api/tasks/{id} in `backend/tests/test_api.py`
- [ ] T039 [US5] Write failing test for 403 on cross-user GET /api/tasks/{id} in `backend/tests/test_api.py`
- [ ] T040 [US5] Write failing test for 404 on non-existent task in `backend/tests/test_api.py`

### API Endpoints - Update (US3)

- [ ] T041 [US3] Write failing integration test for PATCH /api/tasks/{id} in `backend/tests/test_api.py`
- [ ] T042 [US3] Write failing test for 403 on cross-user PATCH in `backend/tests/test_api.py`
- [ ] T043 [US3] Write failing test for 404 on non-existent task PATCH in `backend/tests/test_api.py`

### API Endpoints - Delete (US4)

- [ ] T044 [US4] Write failing integration test for DELETE /api/tasks/{id} in `backend/tests/test_api.py`
- [ ] T045 [US4] Write failing test for 403 on cross-user DELETE in `backend/tests/test_api.py`
- [ ] T046 [US4] Write failing test for 404 on non-existent task DELETE in `backend/tests/test_api.py`

### Main Application

- [ ] T047 Implement `backend/src/main.py` with FastAPI app, CORS, routers, exception handlers
  - **Depends on**: T023, T029, T014, T018, T016
  - **DoD**:
    - App at `http://localhost:8000`
    - All routes under `/api/` prefix
    - Health check at `/api/health` (no auth)
    - Exception handlers wrap errors in standard format
    - CORS configured for frontend

**Sprint 3 Definition of Done**:
- [ ] All CRUD operations work correctly
- [ ] All 5 user stories have passing tests
- [ ] User isolation verified with 403 tests (T030, T031, T032, T039, T042, T045)
- [ ] API returns correct status codes (201, 200, 204, 401, 403, 404, 422)

---

## Sprint 4: Integration & Validation

**Goal**: Refine responses, add dev tooling, and validate end-to-end.

### Standardized JSON Responses

- [ ] T048 Write test verifying all success responses have `{data, meta}` format in `backend/tests/test_api.py`
- [ ] T049 Write test verifying all error responses have `{error, meta}` format in `backend/tests/test_api.py`
- [ ] T050 Verify `meta.timestamp` is ISO8601 format
- [ ] T051 Verify `meta.request_id` is valid UUID
- [ ] T052 Verify `meta.total` present in list responses

### Global Exception Handlers

- [ ] T053 Write test for 500 error response format in `backend/tests/test_api.py`
- [ ] T054 Write test for 503 response on database failure in `backend/tests/test_api.py`
- [ ] T055 Ensure global handlers in `main.py` catch all exceptions

### Development Tooling

- [ ] T056 [P] Create `backend/seed.py` for database seeding
  - **DoD**:
    - Two test users (known UUIDs)
    - 5 tasks per user
    - `--reset` flag to clear and reseed
- [ ] T057 [P] Verify OpenAPI docs at `/docs` and `/redoc`

### End-to-End Validation

- [ ] T058 Run full test suite with `pytest --cov=src`
- [ ] T059 Verify all Success Criteria from spec.md:
  - SC-001: 100% unauthenticated requests rejected (401)
  - SC-002: 100% cross-user access blocked (403)
  - SC-005: Zero data leakage
  - SC-007: Task creation assigns correct user_id
  - SC-008: All responses use standard envelope

**Sprint 4 Definition of Done**:
- [ ] All tests pass with coverage report
- [ ] Response format 100% compliant with spec
- [ ] Seed script works for dev testing
- [ ] PHR created for implementation

---

## Dependencies Graph

```
T001 (structure)
  └── T002, T003, T004 [parallel]
      └── T005, T006 (test setup)
          └── T007 → T008 (config)
              └── T009 → T010 (database)
                  └── T011 → T012 (models)
                      └── T015 → T016 (exceptions)
                          └── T019-T022 → T023 (auth)
                              └── T024-T028 → T029 (crud)
                                  └── T030-T032 (isolation tests)
                                      └── T033-T046 (api tests) → T047 (main)
                                          └── T048-T059 (integration)
```

## Parallel Execution Opportunities

**Within Sprint 1**:
- T002, T003, T004 can run in parallel (no dependencies)
- T013, T014 can run in parallel with T011, T012

**Within Sprint 2**:
- T017, T018 can run in parallel with T019-T023

**Within Sprint 3**:
- All test-writing tasks for different user stories can parallelize
- T056, T057 in Sprint 4 can parallelize

## Task Summary

| Sprint | Tasks | Focus |
|--------|-------|-------|
| Sprint 1 | T001-T014 | Infrastructure |
| Sprint 2 | T015-T023 | Security |
| Sprint 3 | T024-T047 | Core CRUD |
| Sprint 4 | T048-T059 | Integration |

**Total Tasks**: 59
**Test Tasks**: 35 (test-first approach)
**Implementation Tasks**: 24
**User Isolation Tests**: 6 (T030-T032, T039, T042, T045)

## MVP Scope

**Minimum Viable Product**: Complete Sprint 1-3
- US1 (Create) + US2 (List) are P1 priorities
- Full user isolation enforcement
- Standard response format

**Full Feature**: Complete all 4 sprints

---

## Implementation Order

Recommended sequence:
1. `config.py` - Environment setup
2. `database.py` - DB connection
3. `models.py` - Task entity
4. `schemas.py` - Request/response validation
5. `exceptions.py` - Custom errors
6. `responses.py` - Envelope helpers
7. `auth.py` - JWT middleware
8. `crud.py` - Database operations
9. `main.py` - FastAPI application
10. `seed.py` - Dev tooling

Each step follows test-first: write failing test → implement → verify pass.
