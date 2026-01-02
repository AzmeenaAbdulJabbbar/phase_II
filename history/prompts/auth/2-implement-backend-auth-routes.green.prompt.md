---
id: 2
title: Implement backend auth routes for JWT Bridge
stage: green
date: 2026-01-02
surface: agent
model: sonnet-4.5
feature: auth
branch: 001-frontend-core
user: Computer World
command: none
labels: ["auth", "backend", "fastapi", "jwt"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - backend/src/schemas.py
  - backend/src/auth.py
  - backend/src/main.py
tests:
  - Verify JWT encoding/decoding with PyJWT
---

## Prompt

The user requested adding auth routes on the backend to solve a 401 Not Authenticated error occurring during frontend-backend testing.

## Response snapshot

Implemented authentication routes in the backend to support the JWT Bridge pattern:
1.  **Schemas**: Added `UserLogin`, `UserRegister`, and `AuthResponse` to `backend/src/schemas.py`.
2.  **Auth helper**: Added `create_jwt_token` to `backend/src/auth.py` and updated imports.
3.  **Routes**: Added `/api/auth/signin` and `/api/auth/signup` to `backend/src/main.py`.
4.  **Deterministic IDs**: Added `generate_user_id` to `main.py` mirroring the frontend's deterministic UUID generation from email addresses.
5.  **Verification**: Confirmed that the backend's JWT verification using `BETTER_AUTH_SECRET` is compatible with tokens containing a `sub` claim.

## Outcome

- ✅ Impact: Resolved the missing backend auth routes and ensured consistent user ID generation between frontend and backend.
- 🧪 Tests: Verified JWT encoding/decoding with a standalone Python script in the venv.
- 📁 Files: Modified backend/src/schemas.py, backend/src/auth.py, and backend/src/main.py.
- 🔁 Next prompts: Test the full auth flow from the frontend UI or verify with `curl`.
- 🧠 Reflection: Using deterministic IDs bridged the state between the mock frontend auth and the backend without requiring a full user table synchronization for testing.

## Evaluation notes (flywheel)

- Failure modes observed: none
- Graders run and results (PASS/FAIL): none
- Prompt variant (if applicable): none
- Next experiment (smallest change to try): Update frontend mockAuth to call backend endpoints.
