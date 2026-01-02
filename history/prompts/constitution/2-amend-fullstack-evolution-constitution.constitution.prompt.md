---
id: 2
title: Amend Full-Stack Evolution Constitution
stage: constitution
date: 2025-12-21
surface: agent
model: claude-sonnet-4-5-20250929
feature: none
branch: main
user: user
command: /sp.constitution
labels: ["constitution", "amendment", "jwt-bridge", "version-update", "methodology"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - .specify/memory/constitution.md
  - history/prompts/constitution/2-amend-fullstack-evolution-constitution.constitution.prompt.md
tests:
  - N/A (governance document)
---

## Prompt

"Act as a Lead System Architect to establish a strict Project Constitution for Phase II: Full-Stack Web Evolution.

1. NON-NEGOTIABLE DEVELOPMENT PARADIGM:
- STRICT Spec-Driven Development (SDD): Zero manual code edits. All logic must be updated via specs in /specs/ first.
- Methodology: /sp.specify (What/Why) → /sp.plan (How/Blueprint) → /sp.tasks (Atomic Units) → /sp.implement (Execution).

2. MONOREPO ARCHITECTURE:
- Folder Structure:
  - /frontend (Next.js 16+ App Router, TS, Tailwind)
  - /backend (FastAPI, Python 3.13+, SQLModel)
  - /specs (Organized: /features, /api, /database, /ui)
  - /.spec-kit/ (Config and templates)
- Instruction Context: Layered CLAUDE.md files in Root, Frontend, and Backend folders to maintain localized coding patterns.

3. TECH STACK & PERSISTENCE:
- Backend ORM: SQLModel for all schema definitions and queries.
- Database: Neon Serverless PostgreSQL (Production-grade).
- Deployment: Dockerized environment using root docker-compose.yml for local orchestration.

4. SECURITY & IDENTITY PROTOCOL (Better Auth + FastAPI JWT):
- Authentication: Implement Better Auth on the Frontend with the JWT Plugin enabled.
- JWT Bridge: Frontend must attach the JWT token in the 'Authorization: Bearer <token>' header for every API request.
- Backend Middleware: FastAPI must implement a custom security middleware to verify JWTs using the shared 'BETTER_AUTH_SECRET'.
- Data Isolation: Non-negotiable User Isolation."

## Response snapshot

Amended Constitution from v1.0.0 to v1.1.0 (MINOR) with the following changes:

**Modified Principles:**
- I. Spec-Driven Development: Added explicit methodology workflow diagram
- III. Technology Stack Compliance: Updated Next.js 15+ → 16+, Python 3.11+ → 3.13+
- IV. Security & Identity Protocol: Added explicit JWT Bridge pattern with code examples
- VI. Spec-Kit Plus Workflow: Added /specs/ui/ folder for UI specifications

**Added Sections:**
- Development Methodology section with visual workflow diagram and enforcement rules
- JWT Bridge Implementation section with frontend/backend code examples
- Enhanced authentication flow diagram showing the complete JWT bridge

**Key Enhancements:**
- Explicit `Authorization: Bearer <token>` header requirement for all API calls
- Complete FastAPI JWT verification middleware code example
- Updated technology versions to match current requirements
- Visual workflow: `/sp.specify → /sp.plan → /sp.tasks → /sp.implement`

## Outcome

- Impact: Strengthened governance with explicit JWT bridge and methodology workflow
- Tests: N/A (governance document)
- Files: .specify/memory/constitution.md amended
- Next prompts: Initialize monorepo structure per constitution, create layered CLAUDE.md files
- Reflection: Amendment provides clearer implementation guidance with code examples

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): Manual review - PASS
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Validate workflow with first feature implementation
