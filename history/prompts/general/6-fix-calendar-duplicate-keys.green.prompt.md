---
id: 6
title: Fix duplicate keys in Calendar grid
stage: green
date: 2026-01-02
surface: agent
model: sonnet-4.5
feature: ui
branch: 001-frontend-core
user: Computer World
command: none
labels: ["ui", "bugfix", "react", "calendar"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - frontend/src/components/dashboard/calendar.tsx
tests: []
---

## Prompt

The user reported a React key duplication error in the Calendar component header.

## Response snapshot

Fixed the duplicate key console error in `Calendar.tsx`:
- Changed the key generation logic for the day-of-week header.
- Switched from using the day letter (e.g., "S", "M") as a key to using the index (`header-${i}`).
- This resolves the conflict where two "S" (Sunday/Saturday) and two "T" (Tuesday/Thursday) keys existed in the same fragment.

## Outcome

- ✅ Impact: Resolved React warning/error for duplicate keys in the calendar UI grid.
- 🧪 Tests: None (UI fix).
- 📁 Files: Modified frontend/src/components/dashboard/calendar.tsx.
- 🔁 Next prompts: None.
- 🧠 Reflection: Always use indexes or unique identifiers for keys when mapping over static arrays with potentially duplicate values.

## Evaluation notes (flywheel)

- Failure modes observed: none
- Graders run and results (PASS/FAIL): none
- Prompt variant (if applicable): none
- Next experiment (smallest change to try): none
