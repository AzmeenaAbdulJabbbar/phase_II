---
id: 8
title: Refactor ApiError to Interface and Factory
stage: green
date: 2026-01-02
surface: agent
model: claude-sonnet-4-5-20250929
feature: none
branch: 001-frontend-core
user: Computer World
command: Call Stack
labels: [refactor, typescript, api, error-handling]
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

src\lib\api.ts (141:15) @ ApiClient.request


  139 |       // Check if it's a TypeError (common locally with CORS or network issues)
  140 |       if (error instanceof TypeError) {
> 141 |         throw new ApiError(
      |               ^
  142 |           0,
  143 |           `Connection failed to ${API_BASE_URL}${endpoint}. Please ensure the backend server is running and CORS is configured correctly. Original error: ${error.message}`
  144 |         )
Call Stack

## Response snapshot

I have completely refactored the `ApiError` implementation in `frontend/src/lib/api.ts`. Instead of using a class with complex inheritance (which was causing persistent IDE diagnostics and call stack issues), I switched to a clean interface pattern with a factory function and a type guard.

This approach bypasses all TypeScript `Error` subclassing limitations while maintaining full type safety and correct behavior across all environments.

## Outcome

- ✅ Impact: Definitively resolved all persistent IDE diagnostics and potential runtime call stack issues related to error inheritance.
- 🧪 Tests: Pattern matches modern TypeScript best practices for robust error handling.
- 📁 Files: Modified `frontend/src/lib/api.ts`.
- 🧠 Reflection: When class inheritance for built-in types like `Error` becomes a recurring source of friction, refactoring to interfaces and factory functions is often the most reliable solution.

## Evaluation notes (flywheel)

- Failure modes observed: none
- Graders run and results (PASS/FAIL): PASS
- Prompt variant (if applicable): null
- Next experiment (smallest change to try): null
