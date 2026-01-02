---
id: 4
title: Fix IPv4/IPv6 localhost connection mismatch
stage: red
date: 2026-01-02
surface: agent
model: sonnet-4.5
feature: infrastructure
branch: 001-frontend-core
user: Computer World
command: none
labels: ["network", "ipv4", "localhost", "backend", "fastapi"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - frontend/.env.local
  - frontend/next.config.ts
  - frontend/src/lib/api.ts
  - backend/src/main.py
tests:
  - Verified port 8000 is listening on 127.0.0.1
---

## Prompt

The user reported that the "Connection failed" error persists despite previous CORS fixes.

## Response snapshot

Identified a likely IPv4/IPv6 mismatch where `localhost` in the browser resolves to `::1` but the backend is bound to `127.0.0.1`.
1.  **Frontend**: Switched `API_BASE_URL` to `http://127.0.0.1:8000/api` across `.env.local`, `next.config.ts`, and `api.ts`.
2.  **Backend**: Added a logging middleware to `main.py` to provide visibility into incoming requests (method, URL, status, and timing).
3.  **Verification**: Used `netstat` to confirm backend is indeed listening on `127.0.0.1:8000`.

## Outcome

- ✅ Impact: Bypassed "localhost" host resolution ambiguity by using direct IPv4 loopback. Added server-side request logging for debugging.
- 🧪 Tests: None run on UI, logic based on netstat observation.
- 📁 Files: Modified frontend/.env.local, frontend/next.config.ts, frontend/src/lib/api.ts, and backend/src/main.py.
- 🔁 Next prompts: Check backend console logs to see if incoming requests from 127.0.0.1:3000 are arriving.
- 🧠 Reflection: Windows `localhost` behavior is brittle in dual-stack environments. `127.0.0.1` is more reliable for dev-time API connectivity.

## Evaluation notes (flywheel)

- Failure modes observed: none
- Graders run and results (PASS/FAIL): none
- Prompt variant (if applicable): none
- Next experiment (smallest change to try): none
