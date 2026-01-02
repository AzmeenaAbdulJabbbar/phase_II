---
id: 11
title: Apply permissive CORS and debugging log
stage: red
date: 2026-01-02
surface: agent
model: sonnet-4.5
feature: infrastructure
branch: 001-frontend-core
user: Computer World
command: none
labels: ["cors", "infrastructure", "debug"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - backend/src/main.py
  - frontend/.env.local
  - frontend/next.config.ts
  - frontend/src/lib/api.ts
tests: []
---

## Prompt

The user reported that the connection error "Failed to fetch" persisted despite previous fixes.

## Response snapshot

Implemented a more aggressive debugging and CORS strategy:
1.  **Backend**: Updated `CORSMiddleware` to use `allow_origin_regex="http://.*"` to catch any local origin variance.
2.  **Debugging**: Enhanced the `log_requests` middleware to explicitly print the `Origin` header of incoming requests.
3.  **Consistency**: Reverted frontend to `localhost:8000/api` consistently, as browser security models often treat `localhost` differently from `127.0.0.1`.

## Outcome

- ✅ Impact: Maximized CORS compatibility for local dev environments and provided server-side visibility into origin mismatches.
- 📁 Files: Modified backend/src/main.py, frontend/.env.local, frontend/next.config.ts, and frontend/src/lib/api.ts.
- 🔁 Next prompts: Monitor backend console for "DEBUG: Request from origin: ..." to identify unexpected origins.
- 🧠 Reflection: "Failed to fetch" is a catch-all browser error. Removing all possible CORS frictions via regex is the final step before concluding external network interference.

## Evaluation notes (flywheel)

- Failure modes observed: none
- Graders run and results (PASS/FAIL): none
- Prompt variant (if applicable): none
- Next experiment (smallest change to try): none
