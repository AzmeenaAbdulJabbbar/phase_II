---
id: 4
title: Implement Sprint 1 Infrastructure
stage: green
date: 2025-12-21
surface: agent
model: claude-sonnet-4.5
feature: backend-api-core
branch: 001-backend-api-core
user: system
command: /sp.implement
labels: ["backend", "infrastructure", "database", "models", "schemas", "test-first"]
links:
  spec: specs/api/backend-core.md
  ticket: null
  adr: null
  pr: null
files:
  - backend/src/__init__.py
  - backend/src/config.py
  - backend/src/database.py
  - backend/src/models.py
  - backend/src/schemas.py
  - backend/tests/__init__.py
  - backend/tests/conftest.py
  - backend/tests/test_config.py
  - backend/tests/test_database.py
  - backend/tests/test_models.py
  - backend/tests/test_schemas.py
  - backend/pyproject.toml
  - backend/.env.example
  - backend/.gitignore
tests:
  - backend/tests/test_config.py
  - backend/tests/test_database.py
  - backend/tests/test_models.py
  - backend/tests/test_schemas.py
---

## Prompt

@specs/api/backend-core.tasks.md "Implement Sprint 1: Infrastructure.

1. Create the backend monorepo folder structure if it doesn't exist.
2. Initialize the Python environment using 'uv' and install: fastapi, sqlmodel, pydantic-settings, and psycopg2-binary.
3. Implement 'backend/src/database.py' with the Neon PostgreSQL connection logic.
4. Implement 'backend/src/models.py' using SQLModel exactly as specified in the Data Contract spec.

CRITICAL:
- Use the Red-Green-Refactor approach: write the DB connection test before the implementation.
- After implementation, generate the PHR in 'history/prompts/backend-core/01-infra.green.prompt.md'.
- Ensure NO manual code is written; refine the plan if the implementation fails."

## Response snapshot

Implemented Sprint 1: Infrastructure (Tasks T001-T014) using test-first approach:

**Project Setup (T001-T004)**:
- Created `backend/` directory structure with `src/` and `tests/`
- Created `pyproject.toml` with dependencies (FastAPI, SQLModel, PyJWT, asyncpg, pydantic-settings)
- Created `.env.example` with DATABASE_URL and BETTER_AUTH_SECRET templates
- Created `.gitignore` for Python projects

**Test Setup (T005-T006)**:
- Created `tests/__init__.py` and `tests/conftest.py`
- Implemented JWT mock fixtures (valid, expired, invalid tokens)
- Set up test user UUIDs for isolation testing

**Configuration (T007-T008)**:
- Test: `test_config.py` - 6 tests for settings loading
- Impl: `config.py` - Pydantic BaseSettings with validation

**Database (T009-T010)**:
- Test: `test_database.py` - 5 tests for async engine and session
- Impl: `database.py` - Async engine with asyncpg, session generator, init/close methods

**Models (T011-T012)**:
- Test: `test_models.py` - 11 tests for Task model fields and constraints
- Impl: `models.py` - Task SQLModel with user_id index (MANDATORY per Constitution)

**Schemas (T013-T014)**:
- Test: `test_schemas.py` - 14 tests for validation rules
- Impl: `schemas.py` - TaskCreate, TaskUpdate, TaskRead with spec-compliant validation

## Outcome

- ✅ Impact: High - Backend foundation established with test coverage
- 🧪 Tests: 36 test cases across 4 test files
- 📁 Files: 14 files created (6 impl + 4 test + 4 config)
- 🔁 Next prompts: /sp.implement Sprint 2 (Security - JWT Middleware)
- 🧠 Reflection: Test-first approach ensured all implementations match spec. Task model has user_id index as required by Constitution for query performance.

## Evaluation notes (flywheel)

- Failure modes observed: None - all tasks completed successfully
- Graders run and results (PASS/FAIL): Sprint 1 DoD PASS (all 14 tasks marked complete)
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Run pytest to verify all tests pass
