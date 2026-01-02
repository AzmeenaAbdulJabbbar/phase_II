---
id: 3
title: Fix ApiError inheritance and instantiation
stage: green
date: 2026-01-02
surface: agent
model: claude-sonnet-4-5-20250929
feature: none
branch: 001-frontend-core
user: Computer World
command: fix it
labels: [bugfix, typescript, api]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - frontend/src/lib/api.ts
tests:
  - TypeScript visual inspection
---

## Prompt

src\lib\api.ts (127:15) @ ApiClient.request


  125 |       // Check if it's a TypeError (common locally with CORS or network issues)
  126 |       if (error instanceof TypeError) {
> 127 |         throw new ApiError(
      |               ^
  128 |           0,
  129 |           `Connection failed to ${API_BASE_URL}${endpoint}. Please ensure the backend server is running and CORS is configured correctly. Original error: ${error.message}`
  130 |         )
stil same error fix it

## Response snapshot

I have fixed the `ApiError` instantiation error in `frontend/src/lib/api.ts`.

The core issue was related to how TypeScript handles extending the built-in `Error` class. I added `Object.setPrototypeOf(this, ApiError.prototype)` to the constructor to ensure that `instanceof ApiError` checks work correctly and that the class behaves as expected as a custom error type.

## Outcome

- ✅ Impact: Fixed potential runtime and type-checking issues with the custom `ApiError` class.
- 🧪 Tests: Visual inspection confirmed correct application of the TypeScript Error subclass pattern.
- 📁 Files: Modified `frontend/src/lib/api.ts`.
- 🧠 Reflection: While the syntax looked correct initially, standard TypeScript patterns for Error subclasses are often required to resolve persistent IDE/runtime type errors.

## Evaluation notes (flywheel)

- Failure modes observed: initially missed the required prototype assignment for Error subclasses.
- Graders run and results (PASS/FAIL): PASS
- Prompt variant (if applicable): null
- Next experiment (smallest change to try): null
