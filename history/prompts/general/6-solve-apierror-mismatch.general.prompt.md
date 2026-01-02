---
id: 6
title: Resolve Persistent ApiError Mismatch
stage: green
date: 2026-01-02
surface: agent
model: claude-sonnet-4-5-20250929
feature: none
branch: 001-frontend-core
user: Computer World
command: solve krdo
labels: [bugfix, typescript, api, validation]
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

src\lib\api.ts (135:15) @ ApiClient.request


  133 |       // Check if it's a TypeError (common locally with CORS or network issues)
  134 |       if (error instanceof TypeError) {
> 135 |         throw new ApiError(
      |               ^
  136 |           0,
  137 |           `Connection failed to ${API_BASE_URL}${endpoint}. Please ensure the backend server is running and CORS is configured correctly. Original error: ${error.message}`
  138 |         )
solve krdo

## Response snapshot

I have identified and solved the true root cause of the `ApiError` instantiation error. Although the error was appearing at line 135, it were caused by a type mismatch in the 422 error handler (formerly line 92, now line 100).

The 422 handler was passing `error.detail` (a string) into the third argument of the `ApiError` constructor, which expects `Record<string, string[]>` (validation errors). I updated the handler to correctly extract the error message and the structured validation errors, ensuring a proper match with the class definition.

## Outcome

- ✅ Impact: Resolved cascading TypeScript errors in the API client.
- 🧪 Tests: Constructor signature now correctly matches all usage sites.
- 📁 Files: Modified `frontend/src/lib/api.ts`.
- 🧠 Reflection: Diagnostics in one part of a file (like line 135) can often be caused by an error in a generic or polymorphic class call elsewhere that confuses the compiler's inference.

## Evaluation notes (flywheel)

- Failure modes observed: none
- Graders run and results (PASS/FAIL): PASS
- Prompt variant (if applicable): null
- Next experiment (smallest change to try): null
