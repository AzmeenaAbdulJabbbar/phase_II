---
id: 12
title: Revert Task section UI to original state
stage: refactor
date: 2026-01-02
surface: agent
model: sonnet-4.5
feature: frontend-core
branch: 001-frontend-core
user: Computer World
command: none
labels: ["ui", "refactor", "reversion"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - frontend/src/components/dashboard/task-list.tsx
  - frontend/src/components/dashboard/task-card.tsx
  - frontend/src/components/dashboard/task-form.tsx
tests: []
---

## Prompt

The user requested to revert the "My Tasks" section UI to its original state: "my task phle jesa th wese hi krdo ui".

## Response snapshot

Reverted the Task section components to their original simpler styling:
1.  **TaskList**: Restored original layout for search, filters, and task grid.
2.  **TaskCard**: Removed due date indicators and simplified the card layout.
3.  **TaskForm**: Removed the "Due Date" input field and associated state management logic.

## Outcome

- ✅ Impact: Restored UI consistency with the user's preferred original design while maintaining backend compatibility for due dates (data remains but is not displayed).
- 📁 Files: Modified frontend/src/components/dashboard/task-list.tsx, task-card.tsx, and task-form.tsx.

## Evaluation notes (flywheel)

- Failure modes observed: none
- Graders run and results (PASS/FAIL): none
- Prompt variant (if applicable): none
- Next experiment (smallest change to try): none
