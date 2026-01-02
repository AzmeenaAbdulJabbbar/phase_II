---
id: 1
title: Establish Phase II Constitution
stage: constitution
date: 2025-12-21
surface: agent
model: claude-sonnet-4-5-20250929
feature: none
branch: main
user: user
command: /sp.constitution
labels: ["constitution", "spec-driven-development", "phase-ii", "monorepo", "jwt-auth"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - .specify/memory/constitution.md
  - history/prompts/constitution/1-establish-phase-ii-constitution.constitution.prompt.md
tests:
  - N/A (governance document)
---

## Prompt

"Establish a strict Spec-Driven Development constitution for the 'Evolution of Todo' Phase II.

1. CORE DIRECTIVE:
- Zero manual coding is permitted. All code changes must be driven by updating specifications in /specs/ and using @reference commands.
- We are building a modern, multi-user web application using a MONOREPO structure.

2. TECHNOLOGY STACK:
- Frontend: Next.js 15+ (App Router), TypeScript, Tailwind CSS, Better Auth.
- Backend: Python FastAPI, SQLModel (ORM), Neon Serverless PostgreSQL.
- Deployment: Docker-ready with a root docker-compose.yml.

3. ARCHITECTURE & MONOREPO RULES:
- Project structure must strictly follow: /frontend (Next.js), /backend (FastAPI), /specs (Organized by type), and /.spec-kit/config.yaml.
- Use layered CLAUDE.md files: a Root CLAUDE.md for orchestration, and specialized CLAUDE.md files in /frontend and /backend for layer-specific patterns.

4. SECURITY & AUTHENTICATION PROTOCOL:
- Implement a 'Stateless Auth' architecture using JWT.
- Frontend: Better Auth must be configured with the JWT plugin.
- Backend: Must implement JWT verification middleware using the shared BETTER_AUTH_SECRET.
- Data Isolation: All API endpoints MUST filter tasks by the user_id extracted from the JWT. No user should ever access another user's data.

5. DATABASE & API PATTERNS:
- Use SQLModel for all backend DB operations.
- All backend routes must reside under the /api/ prefix.
- Use Pydantic models for strict request/response validation.

6. SPEC-KIT PLUS CONVENTIONS:
- All specifications must be stored in subfolders of /specs/ (e.g., /specs/features/, /specs/api/, /specs/database/).
- Claude Code must always read the relevant spec (@specs/...) before implementation.
- Every feature implementation requires a prior /sp.plan and /sp.tasks step."

## Response snapshot

Created Evolution of Todo Phase II Constitution v1.0.0 with 6 core principles:

1. **Spec-Driven Development (NON-NEGOTIABLE)** - Zero manual coding; all changes via specs
2. **Modern Multi-User Web Application** - Monorepo structure for scalable full-stack app
3. **Technology Stack Compliance** - Fixed stack: Next.js 15+, FastAPI, SQLModel, Neon PostgreSQL
4. **Security & Authentication Protocol (NON-NEGOTIABLE)** - JWT-based stateless auth with strict data isolation
5. **Database & API Patterns** - SQLModel ORM, /api/ prefix, Pydantic validation
6. **Spec-Kit Plus Workflow (MANDATORY)** - Required /sp.plan and /sp.tasks before implementation

Additional sections include:
- Technology stack reference table
- Complete monorepo directory structure
- Authentication flow diagram
- Data isolation checklist
- Code patterns for SQLModel and FastAPI routes
- Governance rules and version policy

## Outcome

- Impact: Established foundational governance for Phase II development
- Tests: N/A (governance document)
- Files: .specify/memory/constitution.md created
- Next prompts: /sp.specify for first feature, create layered CLAUDE.md files
- Reflection: Constitution provides comprehensive guardrails for spec-driven development

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): Manual review - PASS
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Test workflow with first feature spec
