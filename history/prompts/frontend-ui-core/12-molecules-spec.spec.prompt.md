---
id: 12
title: Dashboard Molecules Specification (TaskCard and AddTaskForm)
stage: spec
date: 2025-12-23
surface: agent
model: claude-sonnet-4-5
feature: frontend-ui-core
branch: 001-frontend-core
user: Computer World
command: /sp.specify
labels: ["spec", "molecules", "taskcard", "addtaskform", "atomic-design", "validation"]
links:
  spec: specs/ui/molecules.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/ui/molecules.md
  - specs/ui/molecules-checklists/requirements.md
tests:
  - None (specification phase)
---

## Prompt

"Define specifications for Dashboard Molecules in /specs/ui/molecules.md.

1. TaskCard Specification:
   - Display: Task title, description (optional), and status.
   - Actions: Checkbox for status toggle, Delete icon for removal.
   - States: Active, Completed (strikethrough), and Loading (during API sync).

2. AddTaskForm Specification:
   - Input: Text field for task title with validation (min 3 chars).
   - Action: Submit button that triggers API call.
   - Feedback: Clear input on success, show error message on failure."

## Response snapshot

Created focused specification for Dashboard Molecules (Atomic Design Layer 2) at `specs/ui/molecules.md`.

**Specification Structure:**

**5 User Stories** (P1-P2):
- P1: View Task in TaskCard (US1)
- P1: Toggle Task Completion in TaskCard (US2)
- P1: Delete Task from TaskCard (US3)
- P1: Create Task using AddTaskForm (US4)
- P2: Real-Time Validation in AddTaskForm (US5)

**58 Functional Requirements** organized by component:

**TaskCard Component** (FR-001 to FR-023):
1. **Display** (5 requirements):
   - FR-001: Display title prominently (text-lg)
   - FR-002: Display description truncated to 2 lines (line-clamp-2)
   - FR-003: Display completion status via visual styling
   - FR-004: Show created date (human-readable)
   - FR-005: Use Card atom as container

2. **Checkbox Toggle** (6 requirements):
   - FR-006: Include checkbox at left side
   - FR-007: Reflect current completion status
   - FR-008: Immediate visual update (optimistic)
   - FR-009: Disable during API call
   - FR-010: Show loading indicator ("Updating...")
   - FR-011: Revert on failure

3. **Delete Action** (7 requirements):
   - FR-012: Include delete icon/button at right side
   - FR-013: Use danger styling (red)
   - FR-014: Show confirmation dialog
   - FR-015: Confirmation has Delete/Cancel options
   - FR-016: Immediate removal (optimistic)
   - FR-017: Disable during API call ("Deleting...")
   - FR-018: Show error on failure

4. **State Management** (5 requirements):
   - FR-019: Three states (Active, Completed, Loading)
   - FR-020: Active state styling (text-gray-900, unchecked)
   - FR-021: Completed state styling (line-through text-gray-500, checked)
   - FR-022: Loading state (disabled, indicator)
   - FR-023: Optimistic updates for toggle and delete

**AddTaskForm Component** (FR-024 to FR-047):
1. **Input** (5 requirements):
   - FR-024: Text input for title
   - FR-025: Helpful placeholder
   - FR-026: Use Input atom
   - FR-027: Associated label (aria-label)
   - FR-028: Enter key support

2. **Validation** (7 requirements):
   - FR-029: Min 3 characters (**user requirement**)
   - FR-030: Max 200 characters
   - FR-031: Error message for min length
   - FR-032: Error message for max length
   - FR-033: Error message for empty (on blur)
   - FR-034: Real-time validation (as user types)
   - FR-035: Trim whitespace

3. **Submit Action** (7 requirements):
   - FR-036: Submit button labeled "Add Task"
   - FR-037: Use Button atom (primary variant)
   - FR-038: Disable when validation fails
   - FR-039: Loading spinner ("Adding...")
   - FR-040: Trigger API createTask
   - FR-041: Clear input on success
   - FR-042: Show success feedback (toast)

4. **Error Handling** (5 requirements):
   - FR-043: Display validation errors below input (red)
   - FR-044: Display API errors
   - FR-045: Keep input value on error (for retry)
   - FR-046: Specific error message
   - FR-047: Handle network timeout

**Accessibility** (FR-048 to FR-053):
- TaskCard checkbox: aria-label
- TaskCard delete: aria-label with context
- AddTaskForm input: aria-invalid, aria-describedby
- Keyboard accessible (Tab, Enter, Space)
- Visible focus indicators

**Responsive Design** (FR-054 to FR-058):
- TaskCard: Full-width mobile, comfortable desktop
- AddTaskForm: Full-width input mobile
- Minimum 44x44px touch targets

**12 Success Criteria**:
- SC-001: TaskCard renders within 50ms
- SC-002: Checkbox toggle updates within 50ms (optimistic)
- SC-003: Delete confirmation within 100ms
- SC-004: Validation feedback within 100ms (real-time)
- SC-005: Clear input within 200ms on success
- SC-006: Submit disabled 100% when invalid
- SC-007: Strikethrough on 100% of completed tasks
- SC-008: Validation error within 100ms
- SC-009: Works on 320px mobile
- SC-010: 100% keyboard accessible
- SC-011: Rollback within 100ms on failure
- SC-012: Create task within 5 seconds

**Key Specifications:**

1. **TaskCard States**:
   - Active: Normal text, unchecked checkbox
   - Completed: Strikethrough, muted color, checked checkbox
   - Loading: Disabled checkbox, loading indicator

2. **AddTaskForm Validation**:
   - **Min 3 characters** (user requirement - different from earlier 1 char)
   - Max 200 characters
   - Trim whitespace
   - Real-time feedback

3. **Optimistic Updates**:
   - Immediate UI change (<50ms)
   - API call with JWT Bearer
   - Rollback on error + toast
   - Loading indicators during pending

4. **Dependencies**:
   - Sprint 1: API client, types, Better Auth
   - Batch 1: Button, Input, Card, Checkbox atoms
   - TaskList component (renders TaskCards)

**Quality Validation**: 16/16 checklist items passed (100%)

**Important Note**: Validation requirement changed from min 1 char (earlier specs) to **min 3 chars** (user requirement in this spec). This is the authoritative requirement for molecules implementation.

## Outcome

- ✅ Impact: Created focused molecule specification for TaskCard and AddTaskForm with 58 functional requirements covering display, actions, states, validation, and feedback
- 🧪 Tests: No tests (spec phase); 19 acceptance scenarios defined for testing
- 📁 Files: 2 files created (molecules.md, molecules-checklists/requirements.md)
- 🔁 Next prompts: Implement TaskCard (T016-T032) and AddTaskForm (T033-T047) using this spec
- 🧠 Reflection: Specification provides clear component contracts with validation rules (min 3 chars), state machine (Active/Completed/Loading), and optimistic update patterns. Ready for Batch 2-3 implementation.

## Evaluation notes (flywheel)

- Failure modes observed: None - specification completed successfully
- Graders run and results (PASS/FAIL): Manual validation - PASS (16/16 items)
- Prompt variant (if applicable): Molecule-focused specification (Atomic Design Layer 2)
- Next experiment (smallest change to try): Implement molecules and verify atoms compose correctly, validate min 3 char requirement works
