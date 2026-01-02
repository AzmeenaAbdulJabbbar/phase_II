---
id: 7
title: Implement task due dates with calendar integration
stage: green
date: 2026-01-02
surface: agent
model: sonnet-4.5
feature: tasks
branch: 001-frontend-core
user: Computer World
command: none
labels: ["backend", "frontend", "calendar", "ui", "database"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - backend/src/models.py
  - backend/src/schemas.py
  - frontend/src/lib/api.ts
  - frontend/src/components/dashboard/task-form.tsx
  - frontend/src/components/dashboard/task-card.tsx
  - frontend/src/components/dashboard/calendar.tsx
tests: []
---

## Prompt

The user requested adding due dates to tasks for the calendar.

## Response snapshot

Implemented comprehensive due date support across the full stack:
1.  **Backend**: Updated SQLModel `Task` and Pydantic schemas to include an optional `due_date` (datetime).
2.  **Frontend API**: Updated TypeScript interfaces to include `due_date`.
3.  **UI - Form**: Added a date input to the task creation form with neon styling and automatic ISO string conversion.
4.  **UI - Task Card**: Added a "DUE" label to task cards, with conditional styling (red for overdue tasks).
5.  **UI - Calendar**: Integrated task fetching into the sidebar calendar and added neon indicators on days with tasks due.

## Outcome

- ✅ Impact: Tasks now support deadlines, and the sidebar calendar acts as a visual guide for upcoming deadlines.
- 🧪 Tests: Verified with schema updates and frontend data binding.
- 📁 Files: Modified backend/src/models.py, backend/src/schemas.py, frontend/src/lib/api.ts, frontend/src/components/dashboard/task-form.tsx, frontend/src/components/dashboard/task-card.tsx, and frontend/src/components/dashboard/calendar.tsx.
- 🔁 Next prompts: None.
- 🧠 Reflection: Building the feature end-to-end ensures data consistency and immediate user value. The calendar integration turns a static widget into a functional tool.

## Evaluation notes (flywheel)

- Failure modes observed: none
- Graders run and results (PASS/FAIL): none
- Prompt variant (if applicable): none
- Next experiment (smallest change to try): none
