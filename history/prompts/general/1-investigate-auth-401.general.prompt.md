---
id: 1
title: Investigate frontend 401 authentication error
stage: general
date: 2026-01-02
surface: agent
model: sonnet-4.5
feature: none
branch: 001-frontend-core
user: Computer World
command: none
labels: ["auth", "debug", "api"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - frontend/src/lib/api.ts
  - frontend/src/lib/mock-auth.ts
  - backend/src/auth.py
  - backend/src/main.py
  - backend/.env
tests: []
---

## Prompt

The user encountered a 401 Not Authenticated error in the frontend API and opened api.ts for investigation.

## Response snapshot

I investigated the authentication flow between the frontend and backend.
- Frontend uses `mock-auth.ts` to generate JWT tokens with a hardcoded secret.
- Backend uses `auth.py` with `HTTPBearer` to verify tokens using a secret from `.env`.
- I verified that the secrets match: `hackathon-2-phase-ii-todo-app-secret-key-2025-dev`.
- Identified that 401 "Not authenticated" is the default FastAPI response when the Authorization header is missing or invalid.
- Noted a discrepancy in `frontend/.env.local` where `BETTER_AUTH_SECRET` is different, though `mock-auth.ts` currently hardcodes it.

## Outcome

- ✅ Impact: Identified match in JWT secrets; narrowed down to header injection or CORS.
- 🧪 Tests: None run yet.
- 📁 Files: Read frontend/src/lib/api.ts, mock-auth.ts, backend/src/auth.py, main.py, config.py, and .env.
- 🔁 Next prompts: Verify if the browser is sending the Authorization header and check CORS settings.
- 🧠 Reflection: The backend's standard error response confirms we are hitting the backend, but the Generic FastAPI 401 suggests the security dependency is failing before our custom logic.

## Evaluation notes (flywheel)

- Failure modes observed: none
- Graders run and results (PASS/FAIL): none
- Prompt variant (if applicable): none
- Next experiment (smallest change to try): Check CORS configurations in backend/src/main.py and verify if Authorization is allowed.
