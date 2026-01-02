# Research: Phase II Backend API Core

**Date**: 2025-12-21
**Feature**: Backend API Core
**Branch**: `001-backend-api-core`

## Research Topics

This document consolidates research findings for all technical decisions required by the backend implementation.

---

## 1. JWT Library Selection

### Decision: PyJWT

**Rationale**: PyJWT is the most widely adopted JWT library for Python with excellent async compatibility, straightforward API, and active maintenance. It directly supports HS256 algorithm required by Better Auth.

**Alternatives Considered**:

| Library | Pros | Cons | Rejected Because |
|---------|------|------|------------------|
| python-jose | More algorithms, JWK support | Heavier dependencies, more complex | Over-engineered for HS256-only use case |
| authlib | Full OAuth2 suite | Much larger scope | We only need JWT verification, not OAuth |
| PyJWT | Lightweight, well-documented | Fewer features | Best fit for single-algorithm verification |

**Implementation Pattern**:
```python
import jwt
from datetime import datetime, timezone

def verify_token(token: str, secret: str) -> dict:
    return jwt.decode(token, secret, algorithms=["HS256"])
```

---

## 2. Async Database Driver for Neon PostgreSQL

### Decision: asyncpg via SQLAlchemy async

**Rationale**: asyncpg is the fastest async PostgreSQL driver for Python, natively supported by SQLAlchemy's async engine. Neon Serverless PostgreSQL is wire-compatible with standard PostgreSQL, so asyncpg works seamlessly.

**Alternatives Considered**:

| Driver | Pros | Cons | Rejected Because |
|--------|------|------|------------------|
| asyncpg | Fastest, native async | Requires SQLAlchemy async setup | Best performance for async FastAPI |
| psycopg3 (async) | Modern, good async support | Newer, less ecosystem adoption | asyncpg more mature for async use |
| aiopg | Established | Based on older psycopg2 | asyncpg significantly faster |

**Connection String Format**:
```
postgresql+asyncpg://user:password@host/database?ssl=require
```

---

## 3. SQLModel vs Pure SQLAlchemy

### Decision: SQLModel (Constitution Mandate)

**Rationale**: Constitution v1.1.0 mandates SQLModel as the ORM. SQLModel combines Pydantic validation with SQLAlchemy ORM, reducing boilerplate and ensuring type safety.

**Key Pattern**: SQLModel models serve dual purpose as both database models and Pydantic schemas with careful separation:
- Table models: `table=True` for database operations
- Schema models: No `table` flag for request/response validation

**Important Considerations**:
- SQLModel's async support requires SQLAlchemy 2.0+ patterns
- Use `AsyncSession` from `sqlalchemy.ext.asyncio`
- Avoid circular imports by separating models from database engine

---

## 4. FastAPI Security Dependencies

### Decision: HTTPBearer with Custom Dependency

**Rationale**: FastAPI's `HTTPBearer` security scheme provides automatic OpenAPI documentation and extracts Bearer tokens. Combined with a custom `Depends` function, this creates a reusable authentication layer.

**Pattern**:
```python
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

security = HTTPBearer()

async def get_current_user_id(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> str:
    # Verify JWT and extract user_id
    pass
```

**Why Not OAuth2PasswordBearer**: We're not implementing OAuth2 password flow; Better Auth handles authentication. We only need to verify tokens.

---

## 5. Global Exception Handling Strategy

### Decision: Custom Exception Handlers + Response Middleware

**Rationale**: FastAPI's exception handlers allow consistent error formatting. A combination of specific exception handlers and a catch-all ensures all responses follow the `{data, meta}` / `{error, meta}` format.

**Implementation Approach**:
1. Define custom exception classes (e.g., `TaskNotFoundError`, `AccessDeniedError`)
2. Register exception handlers for each custom exception
3. Register handlers for `HTTPException` and generic `Exception`
4. Wrap all responses with `meta` (timestamp, request_id)

**Request ID Generation**: Use `uuid.uuid4()` per request, stored in request state for correlation.

---

## 6. Project Structure Decision

### Decision: Flat Module Structure in `/backend/src/`

**Rationale**: Per user requirements, organize code into focused modules without deep nesting. This keeps imports simple and aligns with the monorepo structure defined in Constitution.

**Final Structure**:
```
backend/
├── src/
│   ├── __init__.py
│   ├── main.py          # FastAPI app, routers, middleware
│   ├── config.py        # Pydantic settings
│   ├── database.py      # Async engine, session factory
│   ├── models.py        # SQLModel table definitions
│   ├── schemas.py       # Pydantic request/response schemas
│   ├── auth.py          # JWT verification, dependencies
│   ├── crud.py          # Database operations with user_id
│   ├── exceptions.py    # Custom exceptions
│   └── responses.py     # Standardized response wrappers
├── tests/
│   ├── conftest.py
│   ├── test_auth.py
│   ├── test_crud.py
│   └── test_api.py
├── seed.py              # Database seeding script
├── pyproject.toml
└── .env.example
```

---

## 7. User Isolation Enforcement Pattern

### Decision: Mandatory `user_id` Parameter in All CRUD Functions

**Rationale**: The Constitution mandates that every database query includes `WHERE user_id = :current_user_id`. By making `user_id` a required parameter in all CRUD functions (not optional, not defaulted), the code enforces this invariant at the function signature level.

**Pattern**:
```python
# CORRECT: user_id is required
async def get_tasks(session: AsyncSession, user_id: UUID) -> list[Task]:
    result = await session.execute(
        select(Task).where(Task.user_id == user_id)
    )
    return result.scalars().all()

# WRONG: user_id optional or missing - NEVER DO THIS
async def get_tasks(session: AsyncSession, user_id: UUID | None = None):
    ...
```

**Ownership Check for Single-Item Operations**:
```python
async def get_task(session: AsyncSession, task_id: UUID, user_id: UUID) -> Task:
    task = await session.get(Task, task_id)
    if task is None:
        raise TaskNotFoundError(task_id)
    if task.user_id != user_id:
        raise AccessDeniedError()
    return task
```

---

## 8. Seed Script Requirements

### Decision: Standalone `seed.py` with Test Fixtures

**Rationale**: A dedicated seed script enables reproducible test data for development and integration testing. Uses direct database operations, not API calls.

**Seed Data Structure**:
- 2 test users (UUIDs matching Better Auth test tokens)
- 5 tasks per user with varied completion states
- Known UUIDs for predictable test assertions

**Execution**:
```bash
python seed.py --reset  # Drop and recreate all data
python seed.py          # Add seed data (idempotent)
```

---

## Summary of Technology Decisions

| Decision Area | Choice | Key Reason |
|--------------|--------|------------|
| JWT Library | PyJWT | Lightweight, HS256 support |
| Async DB Driver | asyncpg | Fastest, Neon-compatible |
| ORM | SQLModel | Constitution mandate |
| Auth Security | HTTPBearer + Depends | Clean FastAPI integration |
| Error Handling | Custom exception handlers | Consistent response format |
| Project Layout | Flat modules in /backend/src/ | Simplicity, user requirement |
| User Isolation | Required user_id param | Compile-time enforcement |
| Dev Seeding | Standalone seed.py | Reproducible test data |
