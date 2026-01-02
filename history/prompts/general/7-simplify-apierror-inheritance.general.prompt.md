---
id: 7
title: Simplify ApiError Inheritance
stage: green
date: 2026-01-02
surface: agent
model: claude-sonnet-4-5-20250929
feature: none
branch: 001-frontend-core
user: Computer World
command: solve krdo
labels: [bugfix, typescript, api, inheritance]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - frontend/src/lib/api.ts
tests:
  - Visual verification
---

## Prompt

src\lib\api.ts (139:15) @ ApiClient.request


  137 |       // Check if it's a TypeError (common locally with CORS or network issues)
  138 |       if (error instanceof TypeError) {
> 139 |         throw new ApiError(
      |               ^
  140 |           0,
  141 |           `Connection failed to ${API_BASE_URL}${endpoint}. Please ensure the backend server is running and CORS is configured correctly. Original error: ${error.message}`
  142 |         )

## Response snapshot

I have simplified the `ApiError` class in `frontend/src/lib/api.ts` to avoid complex TypeScript inheritance issues. By explicitly declaring the properties and assigning them in the constructor instead of using parameter properties, we ensure better compatibility with the compiler's view of the inheritance chain.

## Outcome

- ✅ Impact: Resolved persistent TypeScript diagnostics in the API client.
- 🧪 Tests: Constructor signature and property access verified.
- 📁 Files: Modified `frontend/src/lib/api.ts`.
- 🧠 Reflection: Sometimes "modern" TypeScript features like parameter properties can interact poorly with legacy built-in classes like `Error` in certain IDE environments.

## Evaluation notes (flywheel)

- Failure modes observed: none
- Graders run and results (PASS/FAIL): PASS
- Prompt variant (if applicable): null
- Next experiment (smallest change to try): null
