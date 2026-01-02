<!--
SYNC IMPACT REPORT
==================
Version Change: 1.0.0 → 1.1.0 (MINOR - expanded guidance and version updates)
Modified Principles:
  - I. Spec-Driven Development: Added explicit methodology workflow
  - III. Technology Stack Compliance: Updated Next.js 15+ → 16+, Python 3.11+ → 3.13+
  - IV. Security & Authentication Protocol: Added explicit JWT Bridge pattern
  - VI. Spec-Kit Plus Workflow: Added /specs/ui/ folder
Added Sections:
  - Development Methodology section (explicit workflow sequence)
  - JWT Bridge specification in Security section
Removed Sections: None
Templates Requiring Updates:
  - .specify/templates/plan-template.md: ✅ No changes required
  - .specify/templates/spec-template.md: ✅ No changes required
  - .specify/templates/tasks-template.md: ✅ No changes required
Follow-up TODOs: None
==================
-->

# Phase II: Full-Stack Web Evolution Constitution

## Core Principles

### I. Spec-Driven Development (NON-NEGOTIABLE)

**STRICT Spec-Driven Development (SDD)**: Zero manual code edits are permitted. All logic
MUST be updated via specifications in `/specs/` first. This is the foundational paradigm.

**Mandatory Methodology**:
```
/sp.specify (What/Why) → /sp.plan (How/Blueprint) → /sp.tasks (Atomic Units) → /sp.implement (Execution)
```

This workflow ensures:
- Every implementation has a traceable specification
- Changes are documented before execution
- Code reviews verify spec compliance, not just code quality
- AI agents read specs before writing any code
- No step may be skipped or reordered

**Rationale**: Specifications serve as the single source of truth. Manual coding bypasses
the audit trail and creates undocumented behavior that cannot be reliably maintained.

### II. Monorepo Architecture

We are building a modern, multi-user web application using a MONOREPO structure. All
architectural decisions MUST support:

- Multiple concurrent users with isolated data
- Scalable frontend and backend separation
- Docker-based deployment for consistency
- Unified dependency management at the monorepo level

**Mandatory Folder Structure**:
- `/frontend` - Next.js 16+ App Router, TypeScript, Tailwind
- `/backend` - FastAPI, Python 3.13+, SQLModel
- `/specs` - Organized: `/features`, `/api`, `/database`, `/ui`
- `/.spec-kit/` - Config and templates

**Instruction Context**: Layered CLAUDE.md files MUST be maintained in Root, Frontend,
and Backend folders to preserve localized coding patterns.

**Rationale**: Monorepo structure enables atomic cross-stack changes, shared tooling,
and consistent versioning across frontend and backend.

### III. Technology Stack Compliance

All implementations MUST use the following technology stack exclusively:

**Frontend**:
- Next.js 16+ with App Router (NOT Pages Router)
- TypeScript (strict mode)
- Tailwind CSS for styling
- Better Auth for authentication (with JWT Plugin)

**Backend**:
- Python 3.13+
- FastAPI (latest stable)
- SQLModel as the ORM
- Neon Serverless PostgreSQL for database

**Deployment**:
- Docker-ready architecture
- Root `docker-compose.yml` for local orchestration

**Rationale**: Technology stack is fixed to ensure consistency, reduce decision fatigue,
and enable deep expertise within the chosen tools.

### IV. Security & Identity Protocol (NON-NEGOTIABLE)

Implement a 'Stateless Auth' architecture using Better Auth + FastAPI JWT Bridge.

**Frontend Requirements (Better Auth)**:
- Better Auth MUST be configured with the JWT Plugin enabled
- Tokens MUST be securely stored (httpOnly cookies or secure storage)
- Token refresh logic MUST be implemented

**JWT Bridge (CRITICAL)**:
- Frontend MUST attach the JWT token in the `Authorization: Bearer <token>` header
  for EVERY API request to the backend
- No API request to protected endpoints may omit this header

**Backend Requirements (FastAPI JWT Middleware)**:
- FastAPI MUST implement a custom security middleware to verify JWTs
- Middleware MUST use the shared `BETTER_AUTH_SECRET` for verification
- Secret MUST be stored in environment variables, NEVER hardcoded
- Invalid/expired tokens MUST return 401 Unauthorized

**Data Isolation (NON-NEGOTIABLE)**:
- All API endpoints MUST filter data by `user_id` extracted from JWT
- No user MUST ever access another user's data
- Database queries MUST include `user_id` in WHERE clauses
- Endpoint authorization MUST be tested for each route
- Cross-user data access attempts MUST be logged as security events

**Rationale**: Security is non-negotiable. Data isolation failures expose user data
and create legal/compliance liability.

### V. Database & API Patterns

All database and API implementations MUST follow these patterns:

**Database (SQLModel)**:
- SQLModel for ALL schema definitions and queries
- Async database operations preferred
- Migrations MUST be versioned and reversible
- Foreign key constraints MUST be enforced
- All models MUST include `user_id` foreign key for multi-tenancy

**API**:
- All backend routes MUST reside under the `/api/` prefix
- Pydantic models for strict request/response validation
- Consistent error response format across all endpoints
- HTTP status codes MUST follow REST conventions

**Rationale**: Consistent patterns reduce cognitive load and make the codebase
predictable for both human developers and AI agents.

### VI. Spec-Kit Plus Workflow (MANDATORY)

All feature implementations MUST follow the Spec-Kit Plus workflow:

**Specification Storage**:
- All specs MUST be stored in subfolders of `/specs/`
- Feature specs: `/specs/features/`
- API specs: `/specs/api/`
- Database specs: `/specs/database/`
- UI specs: `/specs/ui/`

**Implementation Requirements**:
- AI agents MUST read the relevant spec (`@specs/...`) before implementation
- Every feature MUST have a `/sp.plan` step before implementation
- Every feature MUST have a `/sp.tasks` step before implementation
- Implementation without prior planning is PROHIBITED

**Rationale**: The spec-driven workflow ensures all changes are planned, reviewed,
and traceable. Skipping steps leads to undocumented technical debt.

## Development Methodology

### Mandatory Workflow Sequence

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│ /sp.specify │ →  │  /sp.plan   │ →  │  /sp.tasks  │ →  │/sp.implement│
│  (What/Why) │    │(How/Blueprint)   │(Atomic Units)│    │ (Execution) │
└─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘
```

| Step | Command | Purpose | Output |
|------|---------|---------|--------|
| 1 | `/sp.specify` | Define WHAT and WHY | `specs/<feature>/spec.md` |
| 2 | `/sp.clarify` | Resolve ambiguities | Updated spec.md |
| 3 | `/sp.plan` | Design HOW (Blueprint) | `specs/<feature>/plan.md` |
| 4 | `/sp.tasks` | Break into atomic units | `specs/<feature>/tasks.md` |
| 5 | `/sp.implement` | Execute tasks | Code changes |
| 6 | `/sp.git.commit_pr` | Commit and PR | Git commit + PR |

**Enforcement**: Skipping any step is a governance violation and MUST be rejected.

## Technology Stack

| Layer | Technology | Version/Notes |
|-------|------------|---------------|
| Frontend Framework | Next.js | 16+ with App Router |
| Frontend Language | TypeScript | Strict mode enabled |
| Frontend Styling | Tailwind CSS | Latest stable |
| Frontend Auth | Better Auth | With JWT Plugin |
| Backend Framework | FastAPI | Latest stable |
| Backend Language | Python | 3.13+ |
| Backend ORM | SQLModel | Latest stable |
| Database | PostgreSQL | Neon Serverless |
| Containerization | Docker | With docker-compose |

## Architecture & Monorepo Rules

### Directory Structure

```text
/
├── frontend/                 # Next.js 16+ application
│   ├── src/
│   │   ├── app/             # App Router pages
│   │   ├── components/      # React components
│   │   ├── lib/             # Utilities and helpers
│   │   └── services/        # API client services
│   ├── CLAUDE.md            # Frontend-specific agent rules
│   └── package.json
│
├── backend/                  # FastAPI application (Python 3.13+)
│   ├── src/
│   │   ├── api/             # Route handlers
│   │   ├── models/          # SQLModel definitions
│   │   ├── services/        # Business logic
│   │   └── middleware/      # Auth and other middleware
│   ├── CLAUDE.md            # Backend-specific agent rules
│   └── pyproject.toml
│
├── specs/                    # All specifications
│   ├── features/            # Feature specifications
│   ├── api/                 # API contract specs
│   ├── database/            # Schema specifications
│   └── ui/                  # UI/UX specifications
│
├── docker-compose.yml        # Root orchestration
├── CLAUDE.md                 # Root orchestration rules
└── .spec-kit/                # Spec-Kit Plus configuration
    └── config.yaml
```

### Layered CLAUDE.md Strategy

- **Root CLAUDE.md**: Orchestration rules, cross-cutting concerns, workflow enforcement
- **frontend/CLAUDE.md**: Next.js patterns, component conventions, Better Auth client setup
- **backend/CLAUDE.md**: FastAPI patterns, SQLModel conventions, JWT middleware rules

## Security & Authentication Protocol

### Authentication Flow (JWT Bridge)

```
┌──────────┐     ┌─────────────────┐     ┌─────────────┐     ┌──────────────────┐
│   User   │ →   │ Frontend        │ →   │ JWT Token   │ →   │ Backend FastAPI  │
│          │     │ (Better Auth)   │     │ (Bearer)    │     │ (JWT Middleware) │
└──────────┘     └─────────────────┘     └─────────────┘     └──────────────────┘
                        │                       │                      │
                        │  Login/Register       │  Authorization:      │  Verify JWT
                        │  ←──────────────→     │  Bearer <token>      │  Extract user_id
                        │                       │  ────────────────→   │  Filter by user
```

### JWT Bridge Implementation

**Frontend (Every API Call)**:
```typescript
// All API requests MUST include this header
headers: {
  'Authorization': `Bearer ${token}`,
  'Content-Type': 'application/json'
}
```

**Backend (JWT Verification Middleware)**:
```python
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt

security = HTTPBearer()

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> User:
    token = credentials.credentials
    try:
        payload = jwt.decode(
            token,
            settings.BETTER_AUTH_SECRET,
            algorithms=["HS256"]
        )
        user_id = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return await get_user_by_id(user_id)
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
```

### Environment Variables Required

```env
# Shared secret between frontend and backend (MUST MATCH)
BETTER_AUTH_SECRET=<secure-random-string-min-32-chars>

# Database connection
DATABASE_URL=postgres://<user>:<password>@<host>/<database>

# Frontend
NEXT_PUBLIC_API_URL=http://localhost:8000/api
```

### Data Isolation Checklist

- [ ] Every database query includes `WHERE user_id = :current_user_id`
- [ ] JWT middleware extracts and validates `user_id` on every request
- [ ] No endpoint returns data without user_id filtering
- [ ] Integration tests verify cross-user data access is blocked
- [ ] Security events logged for unauthorized access attempts

## Database & API Patterns

### SQLModel Pattern

```python
from sqlmodel import SQLModel, Field
from uuid import UUID, uuid4
from datetime import datetime

class Task(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    user_id: UUID = Field(index=True, foreign_key="user.id")  # MANDATORY
    title: str
    completed: bool = False
    created_at: datetime = Field(default_factory=datetime.utcnow)
```

### API Route Pattern

```python
from fastapi import APIRouter, Depends
from app.middleware.auth import get_current_user

router = APIRouter(prefix="/api/tasks")

@router.get("/")
async def list_tasks(current_user: User = Depends(get_current_user)):
    # user_id filtering is MANDATORY - NO EXCEPTIONS
    return await TaskService.get_by_user(current_user.id)

@router.post("/")
async def create_task(
    task: TaskCreate,
    current_user: User = Depends(get_current_user)
):
    # user_id assignment is MANDATORY
    return await TaskService.create(task, user_id=current_user.id)
```

## Spec-Kit Plus Conventions

### Workflow Sequence

1. **Specify**: `/sp.specify` - Define What/Why (feature specification)
2. **Clarify**: `/sp.clarify` - Resolve ambiguities
3. **Plan**: `/sp.plan` - Design How/Blueprint (implementation approach)
4. **Tasks**: `/sp.tasks` - Generate atomic task list
5. **Implement**: `/sp.implement` - Execute tasks from tasks.md
6. **Commit**: `/sp.git.commit_pr` - Create PR with changes

### Specification Requirements

Every spec MUST include:
- User scenarios with acceptance criteria
- Functional requirements (FR-XXX format)
- Success criteria (measurable)
- Edge cases and error handling

## Governance

### Amendment Process

1. Amendments MUST be documented with rationale
2. Breaking changes require MAJOR version bump
3. All changes MUST update `LAST_AMENDED_DATE`
4. Constitution changes require review of dependent templates

### Compliance Verification

- All PRs MUST verify compliance with this constitution
- Non-compliant code MUST be rejected
- Exceptions require explicit documentation and approval
- AI agents MUST reference constitution before implementation

### Version Policy

- **MAJOR**: Breaking governance changes, principle removals, incompatible workflow changes
- **MINOR**: New principles, expanded guidance, version updates
- **PATCH**: Clarifications, typo fixes

**Version**: 1.1.0 | **Ratified**: 2025-12-21 | **Last Amended**: 2025-12-21
