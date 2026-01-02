# Implementation Plan: Phase II Backend API Core

**Branch**: `001-backend-api-core` | **Date**: 2025-12-21 | **Spec**: [backend-core.md](../backend-core.md)
**Input**: Feature specification from `specs/api/backend-core.md`

## Summary

Build a Python FastAPI service using SQLModel that handles multi-user Todo management with JWT authentication. The backend verifies JWT tokens from Better Auth, enforces strict user data isolation, and exposes a RESTful API for CRUD operations on tasks. All responses follow a standardized `{data, meta}` envelope format.

## Technical Context

**Language/Version**: Python 3.13+
**Primary Dependencies**: FastAPI, SQLModel, PyJWT, Pydantic, asyncpg
**Storage**: PostgreSQL (Neon Serverless) via asyncpg driver
**Testing**: pytest with pytest-asyncio
**Target Platform**: Linux/Docker server (also Windows for dev)
**Project Type**: Web API (backend-only, monorepo structure)
**Performance Goals**: <200ms p95 for single operations, <500ms for list operations
**Constraints**: Async-only database operations, strict user isolation
**Scale/Scope**: 100+ concurrent users, ~1000 tasks per user

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Status | Notes |
|-----------|--------|-------|
| I. Spec-Driven Development | ✅ PASS | Spec created via `/sp.specify`, plan via `/sp.plan` |
| II. Monorepo Architecture | ✅ PASS | Backend in `/backend/` per Constitution |
| III. Technology Stack | ✅ PASS | FastAPI + SQLModel + Python 3.13+ |
| IV. Security & Identity | ✅ PASS | JWT verification middleware planned |
| V. Database & API Patterns | ✅ PASS | SQLModel async, /api/ prefix, Pydantic validation |
| VI. Spec-Kit Plus Workflow | ✅ PASS | Following /sp.specify → /sp.plan → /sp.tasks flow |

### Data Isolation Verification

| Requirement | Status | Implementation |
|-------------|--------|----------------|
| Every query includes user_id WHERE clause | ✅ PLANNED | crud.py functions require user_id param |
| JWT middleware extracts user_id | ✅ PLANNED | auth.py get_current_user_id dependency |
| No endpoint returns cross-user data | ✅ PLANNED | All routes use Depends(get_current_user_id) |
| Cross-user access returns 403 | ✅ PLANNED | Ownership check in single-item operations |

## Project Structure

### Documentation (this feature)

```text
specs/api/
├── backend-core.md          # Feature specification
├── backend-core.tasks.md    # Task list (existing)
├── checklists/
│   └── requirements.md      # Spec quality checklist
└── plan/
    ├── plan.md              # This file
    ├── research.md          # Technology decisions
    ├── data-model.md        # Entity definitions
    ├── quickstart.md        # Development setup guide
    └── contracts/
        ├── openapi.yaml     # OpenAPI 3.1 specification
        └── cli-api.md       # Human-readable API contract
```

### Source Code (repository root)

```text
backend/
├── src/
│   ├── __init__.py          # Package marker
│   ├── main.py              # FastAPI app, CORS, exception handlers, routers
│   ├── config.py            # Pydantic settings (env vars)
│   ├── database.py          # Async engine, session factory
│   ├── models.py            # SQLModel table definitions (Task)
│   ├── schemas.py           # Pydantic request/response schemas
│   ├── auth.py              # JWT verification, get_current_user_id
│   ├── crud.py              # Database operations (user_id required)
│   ├── exceptions.py        # Custom exception classes
│   └── responses.py         # Standardized response envelope helpers
├── tests/
│   ├── __init__.py
│   ├── conftest.py          # Pytest fixtures (test DB, test client, mock JWT)
│   ├── test_auth.py         # JWT verification tests
│   ├── test_crud.py         # CRUD operation tests
│   └── test_api.py          # Integration tests
├── seed.py                  # Database seeding script
├── pyproject.toml           # Dependencies and project config
├── .env.example             # Environment variable template
└── .gitignore               # Python ignores
```

**Structure Decision**: Flat module structure in `/backend/src/` per user requirements and Constitution Section II.

## Complexity Tracking

No violations requiring justification. The design follows the simplest viable approach:

- Single database table (Task)
- Flat module structure (no deep nesting)
- No complex patterns (no Repository, no Unit of Work)
- Direct SQLModel usage (no additional ORM abstraction)

## Module Dependencies

```
main.py
├── config.py (settings)
├── database.py (get_session)
├── auth.py (get_current_user_id)
├── crud.py (database operations)
├── schemas.py (request/response models)
├── exceptions.py (custom errors)
└── responses.py (envelope wrappers)

models.py ← database.py (table creation)
         ← crud.py (query operations)

auth.py ← config.py (BETTER_AUTH_SECRET)
```

## Key Implementation Details

### JWT Verification (auth.py)

```python
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt
from uuid import UUID
from .config import settings

security = HTTPBearer()

async def get_current_user_id(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> UUID:
    """
    Extract and verify user_id from JWT token.
    Returns UUID of authenticated user.
    Raises 401 for invalid/expired tokens.
    """
    token = credentials.credentials
    try:
        payload = jwt.decode(
            token,
            settings.BETTER_AUTH_SECRET,
            algorithms=["HS256"]
        )
        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(status_code=401, detail="Invalid token")
        return UUID(user_id)
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except (jwt.InvalidTokenError, ValueError):
        raise HTTPException(status_code=401, detail="Invalid token")
```

### User Isolation (crud.py)

Every function signature enforces user_id requirement:

```python
async def get_tasks(session: AsyncSession, user_id: UUID) -> list[Task]:
    """List all tasks for a specific user. user_id is REQUIRED."""
    result = await session.execute(
        select(Task).where(Task.user_id == user_id).order_by(Task.created_at.desc())
    )
    return result.scalars().all()

async def get_task(session: AsyncSession, task_id: UUID, user_id: UUID) -> Task:
    """Get single task with ownership verification."""
    task = await session.get(Task, task_id)
    if not task:
        raise TaskNotFoundError(task_id)
    if task.user_id != user_id:
        raise AccessDeniedError()
    return task
```

### Response Envelope (responses.py)

```python
from datetime import datetime, timezone
from uuid import uuid4
from typing import Any

def success_response(data: Any, total: int | None = None) -> dict:
    """Wrap successful response in standard envelope."""
    meta = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "request_id": str(uuid4())
    }
    if total is not None:
        meta["total"] = total
    return {"data": data, "meta": meta}

def error_response(code: str, message: str, details: dict | None = None) -> dict:
    """Wrap error in standard envelope."""
    error = {"code": code, "message": message}
    if details:
        error["details"] = details
    return {
        "error": error,
        "meta": {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "request_id": str(uuid4())
        }
    }
```

## Seed Script (seed.py)

```python
"""
Database seeding script for development/testing.
Usage: python seed.py [--reset]
"""
import asyncio
from uuid import UUID

# Known test user IDs (matching Better Auth test tokens)
TEST_USER_A = UUID("11111111-1111-1111-1111-111111111111")
TEST_USER_B = UUID("22222222-2222-2222-2222-222222222222")

SEED_TASKS = [
    {"user_id": TEST_USER_A, "title": "User A Task 1", "completed": False},
    {"user_id": TEST_USER_A, "title": "User A Task 2", "completed": True},
    {"user_id": TEST_USER_A, "title": "User A Task 3", "completed": False},
    {"user_id": TEST_USER_B, "title": "User B Task 1", "completed": False},
    {"user_id": TEST_USER_B, "title": "User B Task 2", "completed": True},
]
```

## Risk Mitigation

| Risk | Mitigation |
|------|------------|
| JWT secret mismatch with frontend | Document in .env.example, validate on startup |
| SQL injection | SQLModel/SQLAlchemy parameterized queries |
| Cross-user data access | Mandatory user_id param in all CRUD functions |
| Connection pool exhaustion | Configure max pool size, use connection timeouts |

## Next Steps

1. Run `/sp.tasks` to generate atomic implementation tasks
2. Implement in order: config → database → models → schemas → auth → crud → responses → exceptions → main
3. Write tests alongside implementation
4. Test JWT integration with Better Auth frontend

## ADR Candidates

The following decisions may warrant Architecture Decision Records:

1. **JWT Verification Approach**: Using shared secret (HS256) vs. public key (RS256)
   - Current choice: HS256 with shared `BETTER_AUTH_SECRET`
   - Rationale: Simpler, sufficient for single-backend architecture

2. **User Isolation Strategy**: Query-level filtering vs. Row-Level Security
   - Current choice: Application-level filtering with mandatory user_id param
   - Rationale: Simpler to implement and test, PostgreSQL RLS adds complexity

If you want to document these decisions formally, run:
```
/sp.adr jwt-verification-strategy
/sp.adr user-isolation-approach
```
