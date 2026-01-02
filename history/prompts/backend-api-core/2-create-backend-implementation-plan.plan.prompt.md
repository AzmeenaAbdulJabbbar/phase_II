---
id: 2
title: Create Backend Implementation Plan
stage: plan
date: 2025-12-21
surface: agent
model: claude-sonnet-4.5
feature: backend-api-core
branch: 001-backend-api-core
user: system
command: /sp.plan
labels: ["backend", "api", "fastapi", "jwt", "sqlmodel", "planning", "architecture"]
links:
  spec: specs/api/backend-core.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/api/plan/plan.md
  - specs/api/plan/research.md
  - specs/api/plan/data-model.md
  - specs/api/plan/quickstart.md
  - specs/api/plan/contracts/openapi.yaml
  - specs/api/plan/contracts/cli-api.md
tests:
  - null
---

## Prompt

@specs/api/backend-core.md "Generate a detailed Technical Plan for the FastAPI backend following the Monorepo structure defined in our Constitution.

KEY ARCHITECTURAL REQUIREMENTS FOR THIS PLAN:
1. FILE STRUCTURE: Organize into /backend/src/ with separate modules for:
   - models.py (SQLModel definitions)
   - database.py (Async engine & session management for Neon)
   - auth.py (JWT middleware & security dependencies)
   - main.py (FastAPI app & router inclusion)
   - crud.py (Service layer with enforced user_id filtering)

2. JWT HANDSHAKE:
   - Detail the 'HTTPBearer' dependency in FastAPI to secure routes.
   - Plan the verification logic for the Better Auth JWT using the 'python-jose' or 'pyjwt' library.

3. DATABASE ARCHITECTURE:
   - Define the 'get_session' async generator.
   - Outline the Task model with proper SQLAlchemy relationships if needed.

4. USER ISOLATION INVARIANT:
   - The plan MUST explicitly show that every CRUD function in 'crud.py' accepts a 'user_id' argument derived from the token.

5. ERROR HANDLING:
   - Plan for global exception handlers to wrap responses in the 'data/meta' format required by the Constitution.

6. DEV ENVIRONMENT:
   - Include a plan for a 'seed.py' script to populate the Neon DB for testing."

## Response snapshot

Created comprehensive Implementation Plan with Phase 0 and Phase 1 artifacts:

**Phase 0 - Research** (`research.md`):
- JWT Library: PyJWT selected (lightweight, HS256 support)
- Async DB Driver: asyncpg via SQLAlchemy async
- ORM: SQLModel (Constitution mandate)
- Auth: HTTPBearer with custom dependency
- Error Handling: Custom exception handlers
- Project Layout: Flat modules in /backend/src/
- User Isolation: Mandatory user_id param in all CRUD functions
- Dev Seeding: Standalone seed.py

**Phase 1 - Design** (`data-model.md`, `contracts/`):
- Task entity with user_id FK and indexes
- OpenAPI 3.1 specification
- Human-readable API contract

**Implementation Plan** (`plan.md`):
- Full project structure for /backend/
- Module dependency graph
- Key implementation patterns (auth, crud, responses)
- Constitution compliance verification (all gates PASS)
- Risk mitigation strategies
- ADR candidates identified

## Outcome

- ✅ Impact: High - Complete implementation blueprint for backend API
- 🧪 Tests: Not applicable (planning phase)
- 📁 Files: 6 files created (plan + research + data-model + quickstart + 2 contracts)
- 🔁 Next prompts: /sp.tasks (generate atomic implementation tasks)
- 🧠 Reflection: Plan explicitly enforces user isolation at function signature level. All Constitution gates pass. Architecture is minimal viable (flat structure, no over-engineering).

## Evaluation notes (flywheel)

- Failure modes observed: None - clear requirements from spec and Constitution
- Graders run and results (PASS/FAIL): Constitution Check PASS (all 6 principles verified)
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): None - plan complete and ready for /sp.tasks
