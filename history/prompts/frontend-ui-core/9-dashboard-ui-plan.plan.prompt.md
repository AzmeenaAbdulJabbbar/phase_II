---
id: 9
title: Dashboard UI Technical Plan for Sprint 2
stage: plan
date: 2025-12-23
surface: agent
model: claude-sonnet-4-5
feature: frontend-ui-core
branch: 001-frontend-core
user: Computer World
command: /sp.plan
labels: ["plan", "dashboard-ui", "server-components", "client-components", "optimistic-updates"]
links:
  spec: specs/ui/dashboard-feature.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/ui/dashboard-feature.plan.md
tests:
  - None (planning phase - manual testing checklist provided)
---

## Prompt

@specs/ui/dashboard-feature.md "Generate a Technical Plan for the Dashboard UI.

1. FILE MAPPING:
   - /src/components/dashboard/task-list.tsx
   - /src/components/dashboard/task-card.tsx
   - /src/components/dashboard/add-task.tsx
   - /src/app/dashboard/page.tsx
2. DATA HANDLING:
   - Plan Server Components for initial fetch.
   - Plan Client Components for checkbox toggle and delete actions."

## Response snapshot

Created comprehensive Technical Plan at `specs/ui/dashboard-feature.plan.md` with detailed component architecture and implementation blueprints.

**Plan Structure:**

**Component Architecture Decision Matrix**:

| Component | Type | Reason |
|-----------|------|--------|
| Dashboard Page | Server Component | Initial data fetch with api.listTasks() server-side |
| TaskList | Server Component | Pure rendering, receives tasks as props |
| TaskCard | Client Component | Interactive (checkbox toggle, delete button) |
| AddTaskForm | Client Component | Form input, validation, submission |
| Navbar | Client Component | Logout button interactivity |

**File Mapping** (user-specified paths):
1. `frontend/src/app/dashboard/page.tsx` - Server Component (fetches tasks)
2. `frontend/src/components/dashboard/task-list.tsx` - Server Component (renders TaskCards)
3. `frontend/src/components/dashboard/task-card.tsx` - Client Component (toggle/delete with optimistic updates)
4. `frontend/src/components/dashboard/add-task.tsx` - Client Component (create form with optimistic updates)
5. `frontend/src/components/layout/navbar.tsx` - Client Component (user profile + logout)

**Implementation Blueprints Provided** (5 complete components):

1. **Dashboard Page** (Server Component):
   - Fetches tasks server-side: `const tasks = await api.listTasks()`
   - Renders Navbar, AddTaskForm, TaskList
   - Passes `initialTasks` prop to TaskList
   - 30 lines of complete code

2. **TaskList Component** (Server Component):
   - Receives `initialTasks` prop from Dashboard Page
   - Maps tasks to TaskCard components
   - EmptyState UI when tasks.length === 0
   - Pure rendering, no state management
   - 40 lines of complete code with SVG empty state icon

3. **TaskCard Component** (Client Component):
   - useOptimistic hook for completion toggle
   - useTransition for pending state
   - Optimistic toggle pattern:
     - Immediate UI update
     - PATCH /api/tasks/{id}
     - Rollback on error + toast
   - Optimistic delete pattern:
     - Confirmation dialog
     - Immediate removal
     - DELETE /api/tasks/{id}
     - router.refresh() for re-fetch
   - 80+ lines of complete code with visual distinction for completed tasks

4. **AddTaskForm Component** (Client Component):
   - Real-time validation (1-200 chars)
   - Enter key submission
   - useTransition for pending state
   - Optimistic creation:
     - POST /api/tasks
     - Clear form on success
     - Toast notifications
   - Loading spinner during submission
   - 90+ lines of complete code

5. **Navbar Component** (Client Component):
   - useAuth hook for user session
   - clientSignOut from Better Auth
   - Responsive (hide email on mobile <768px)
   - Sticky positioning (z-50)
   - Loading skeleton while session loading
   - 50+ lines of complete code

**Optimistic Update Pattern Documented**:

Detailed 5-step pattern for all mutations:
1. Setup: `useOptimistic(initialValue, updater)`
2. Apply: `setOptimisticValue(newValue)` - <50ms
3. API Call: `await api.method()` with JWT Bearer token
4. Success: Confirm (router.refresh() or parent callback)
5. Failure: Rollback + toast.error()

**Data Flow Architecture**:

```
Dashboard Page (Server) → api.listTasks() → tasks[]
    ↓
TaskList (Server) → receives initialTasks prop → maps to TaskCard
    ↓
TaskCard (Client) → user clicks checkbox → optimistic update → PATCH → refresh
    ↓
AddTaskForm (Client) → user submits → optimistic update → POST → refresh
```

**Responsive Design Strategy**:

Breakpoints with Tailwind classes:
- Mobile (<768px): Full-width, collapsed Navbar, stacked cards
- Tablet (768px-1023px): Single column, full Navbar
- Desktop (1024px+): Max-width constrained (max-w-4xl)

Classes documented for each component:
- Container: `max-w-4xl mx-auto px-4 sm:px-6 lg:px-8`
- Navbar: `hidden md:block` for responsive email
- TaskCard: Responsive padding `p-4 sm:p-6`

**Implementation Phases** (Sprint 2 breakdown):
- Phase 2.1: UI Primitives (Button, Input, Card, Checkbox)
- Phase 2.2: Navbar Component
- Phase 2.3: Dashboard Page with route group
- Phase 2.4: Task Components (TaskList, TaskCard, AddTaskForm)

**Risk Analysis**:
- Server Component mutation handling → Use router.refresh()
- useOptimistic availability (React 18) → Fallback to useState
- Slow router.refresh() → Use parent callback pattern
- Large task lists (1000+) → Future pagination
- Confirmation dialog UX → Use proper modal component

**Testing Strategy**:
Manual testing checklist with 7 categories:
1. Dashboard Load
2. Navbar functionality
3. TaskCard Toggle
4. AddTaskForm
5. TaskCard Delete
6. Responsive Design
7. Accessibility

## Outcome

- ✅ Impact: Created production-ready technical plan for Sprint 2 Dashboard UI with complete implementation blueprints for 5 components (290+ lines of reference code)
- 🧪 Tests: Manual testing checklist with 20+ test scenarios provided
- 📁 Files: 1 file created (dashboard-feature.plan.md)
- 🔁 Next prompts: Proceed with Sprint 2 implementation using provided component blueprints
- 🧠 Reflection: Plan provides complete, copy-paste-ready code for all components with optimistic update patterns, responsive design, and accessibility. Server/Client component split clearly defined per user requirement. Ready for immediate implementation.

## Evaluation notes (flywheel)

- Failure modes observed: None - plan completed with all component blueprints
- Graders run and results (PASS/FAIL): Manual validation - PASS (all user requirements addressed)
- Prompt variant (if applicable): Focused dashboard UI plan (Sprint 2 specific)
- Next experiment (smallest change to try): Implement components using provided blueprints and validate optimistic update pattern works
