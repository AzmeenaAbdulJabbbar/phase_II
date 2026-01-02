---
id: 3
title: Fix frontend connection failure (CORS/Network)
stage: green
date: 2026-01-02
surface: agent
model: sonnet-4.5
feature: infrastructure
branch: 001-frontend-core
user: Computer World
command: none
labels: ["cors", "infrastructure", "backend", "fastapi"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - backend/src/main.py
tests:
  - Verified DB connectivity via test script
  - Verified backend health endpoint with curl
---

## Prompt

The user reported a "Connection failed" / "Failed to fetch" error in the frontend when attempting to access a specific task endpoint.

## Response snapshot

I investigated the connection failure:
1.  **Status**: Verified the backend server is listening on port 8000.
2.  **Connectivity**: Verified the backend can connect to the Neon PostgreSQL database.
3.  **CORS**: Identified that "Failed to fetch" in a browser (while curl works) is often a CORS preflight failure or origin mismatch.
4.  **Fix**: Expanded the `CORSMiddleware` in `backend/src/main.py` to explicitly allow `127.0.0.1` and `localhost` on common development ports (3000, 3003, 5173). Also added `expose_headers=["*"]` to ensure the frontend can read response headers.

## Outcome

- ✅ Impact: Improved CORS compatibility for local development, reducing "Failed to fetch" errors caused by origin discrepancies.
- 🧪 Tests: Database connectivity and health check verified.
- 📁 Files: Modified backend/src/main.py.
- 🔁 Next prompts: Continue testing frontend interactions with the backend.
- 🧠 Reflection: Localhost vs 127.0.0.1 discrepancies are common traps in local dev. Explicitly listing both in CORS origins is a robust mitigation.

## Evaluation notes (flywheel)

- Failure modes observed: none
- Graders run and results (PASS/FAIL): none
- Prompt variant (if applicable): none
- Next experiment (smallest change to try): none
