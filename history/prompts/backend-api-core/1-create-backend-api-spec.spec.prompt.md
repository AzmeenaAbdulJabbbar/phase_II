---
id: 1
title: Create Backend API Core Specification
stage: spec
date: 2025-12-21
surface: agent
model: claude-sonnet-4.5
feature: backend-api-core
branch: 001-backend-api-core
user: system
command: /sp.specify
labels: ["backend", "api", "fastapi", "jwt", "sqlmodel", "specification"]
links:
  spec: specs/api/backend-core.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/api/backend-core.md
  - specs/api/checklists/requirements.md
tests:
  - null
---

## Prompt

Create a comprehensive Technical Specification for the Phase II Backend in /specs/api/backend-core.md.

This spec must strictly align with our Constitution v2.0.0 and cover:

1. CORE OBJECTIVE:
- Build a Python FastAPI service using SQLModel that handles multi-user Todo management.

2. AUTHENTICATION & SECURITY (The JWT Bridge):
- Define the implementation of the JWT Verification Middleware.
- Specify how the BETTER_AUTH_SECRET will be used to validate tokens from the frontend.
- Detail the process of extracting the 'user_id' from the JWT sub/claims.

3. DATA CONTRACTS (CRUD + Isolation):
- Specify all endpoints under the /api/{user_id}/ prefix as per the Constitution.
- Define strict Pydantic schemas for:
    - TaskRead (id, title, description, completed, user_id)
    - TaskCreate (title, description)
    - TaskUpdate (title, description, completed)
- MANDATE: Every endpoint must return a standardized JSON response format (data + meta).

4. DATABASE SCHEMA (SQLModel):
- Define the 'Task' table structure including user_id as a foreign key and mandatory index.
- Enforce the 'User Isolation' logic at the specification level: every query must include a WHERE clause for user_id.

5. ERROR TAXONOMY:
- Define specific error responses for 401 (Unauthorized), 403 (Forbidden/Cross-user access), and 404 (Task not found).

6. ACCEPTANCE CRITERIA:
- The backend must reject any request without a valid Bearer token.
- A user must be unable to view, edit, or delete a task belonging to another user_id.
- All database operations must use async sessions.

## Response snapshot

Created comprehensive Technical Specification at `specs/api/backend-core.md` with:

1. **5 User Stories** covering authenticated CRUD operations with acceptance scenarios
2. **19 Functional Requirements** covering:
   - Authentication & Security (FR-001 to FR-005)
   - Data Isolation (FR-006 to FR-009) - NON-NEGOTIABLE
   - CRUD Operations (FR-010 to FR-014)
   - Response Format (FR-015 to FR-016)
   - Database Operations (FR-017 to FR-019)
3. **Data Contracts** (TaskCreate, TaskUpdate, TaskRead schemas)
4. **Error Taxonomy** (401, 403, 404, 422, 500, 503)
5. **9 Success Criteria** with measurable outcomes
6. **Quality Checklist** created at `specs/api/checklists/requirements.md` - ALL PASS

## Outcome

- ✅ Impact: High - Comprehensive backend specification created aligning with Constitution v1.1.0
- 🧪 Tests: Not applicable (specification phase)
- 📁 Files: 2 files created (spec + checklist)
- 🔁 Next prompts: /sp.plan (if not already planned), /sp.tasks (if not already tasked), /sp.implement
- 🧠 Reflection: Spec follows Constitution JWT Bridge pattern exactly. All requirements traceable to Constitution sections. No clarification markers needed due to clear Constitution guidance.

## Evaluation notes (flywheel)

- Failure modes observed: None - clear user requirements mapped directly to Constitution patterns
- Graders run and results (PASS/FAIL): Quality checklist PASS (all items verified)
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): None - specification complete and validated
