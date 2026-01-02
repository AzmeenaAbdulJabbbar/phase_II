# Implementation Plan: Dashboard UI (Sprint 2)

**Branch**: `001-frontend-core` | **Date**: 2025-12-23 | **Spec**: [dashboard-feature.md](dashboard-feature.md)

**Input**: User requirements:
1. FILE MAPPING: /src/components/dashboard/task-list.tsx, task-card.tsx, add-task.tsx, /src/app/dashboard/page.tsx
2. DATA HANDLING: Server Components for initial fetch, Client Components for checkbox toggle and delete actions

---

## Summary

This plan outlines the implementation of Sprint 2: Core Dashboard UI with 4 key components (Navbar, TaskList, TaskCard, AddTaskForm). The plan focuses on Server Components for data fetching and Client Components for interactivity, following Next.js 15 App Router best practices.

**Primary Objective**: Implement dashboard interface with:
- Navbar (Client Component) for user profile and logout
- TaskList (Server Component) for fetching and displaying tasks
- TaskCard (Client Component) for toggle/delete with optimistic updates
- AddTaskForm (Client Component) for task creation with optimistic updates

**Technical Approach**:
- Server Components for initial data fetching (TaskList fetches from GET /api/tasks)
- Client Components for interactive elements (TaskCard toggle/delete, AddTaskForm, Navbar logout)
- Optimistic updates using React useOptimistic hook or local state
- Tailwind CSS for responsive design (320px-1920px)
- Sonner for toast notifications

---

## Technical Context

**Language/Version**: TypeScript (strict mode), Next.js 15+, React 18+
**Primary Dependencies**: Better Auth (JWT), Tailwind CSS, Sonner (toasts)
**Storage**: N/A (dashboard is UI-only, data from backend API)
**Testing**: Manual testing in Sprint 2, automated tests in future sprints
**Target Platform**: Modern web browsers (Chrome, Firefox, Safari, Edge)
**Project Type**: Web application (frontend dashboard interface)
**Performance Goals**:
- Dashboard loads within 2 seconds (SC-001)
- Optimistic updates within 50ms (SC-003, SC-004)
- GET /api/tasks completes within 1 second (SC-014)

**Constraints**:
- All files MUST reside in `/frontend/src/` directory
- Server Components CANNOT use 'use client' directive
- Client Components MUST have 'use client' at top of file
- All API calls MUST include JWT Bearer token (from Sprint 1 api.ts)
- Maximum 1000 tasks per user (no pagination in Sprint 2)

**Scale/Scope**:
- 4 components: Navbar, TaskList, TaskCard, AddTaskForm
- 8 user stories (US1-US8)
- 72 functional requirements (FR-001 to FR-072)
- 14 success criteria (SC-001 to SC-014)

---

## Constitution Check

✅ **I. Spec-Driven Development**:
- Spec created at `specs/ui/dashboard-feature.md`
- Planning follows `/sp.plan` workflow
- Implementation via `/sp.implement` (Sprint 2 continuation)

✅ **II. Monorepo Architecture**:
- All files in `/frontend/src/` directory
- Component organization: `/src/components/dashboard/`
- Page in App Router: `/src/app/dashboard/page.tsx`

✅ **III. Technology Stack Compliance**:
- Next.js 15+ App Router ✓
- TypeScript strict mode ✓
- Tailwind CSS for all styling ✓
- Better Auth session usage ✓

✅ **IV. Security & Identity Protocol**:
- JWT Bearer token attached via API client (from Sprint 1)
- All API calls authenticated
- user_id extracted from JWT by backend

✅ **V. Database & API Patterns**:
- REST API endpoints (GET, POST, PATCH, DELETE)
- Consistent error handling (401, 422, network)
- TypeScript types match backend models

✅ **VI. Spec-Kit Plus Workflow**:
- Spec in `specs/ui/dashboard-feature.md`
- Plan in `specs/ui/dashboard-feature.plan.md` (this file)
- Implementation follows Sprint 2 tasks

**GATE RESULT**: ✅ PASS

---

## File Mapping (User-Specified)

### Component Files

```text
frontend/src/
├── components/
│   ├── dashboard/
│   │   ├── task-list.tsx           # [USER SPECIFIED] Server Component - Fetches tasks
│   │   ├── task-card.tsx           # [USER SPECIFIED] Client Component - Toggle/delete with optimistic updates
│   │   └── add-task.tsx            # [USER SPECIFIED] Client Component - Create task form
│   ├── layout/
│   │   └── navbar.tsx              # Client Component - User profile + logout
│   └── ui/
│       ├── button.tsx              # Reusable button primitive
│       ├── input.tsx               # Reusable input primitive
│       ├── checkbox.tsx            # Reusable checkbox primitive
│       └── card.tsx                # Reusable card wrapper
├── app/
│   └── dashboard/
│       └── page.tsx                # [USER SPECIFIED] Server Component - Dashboard page
└── lib/
    └── api.ts                      # (From Sprint 1) API client with JWT Bearer token
```

---

## Component Architecture

### Server vs Client Component Decision Matrix

| Component | Type | Reason |
|-----------|------|--------|
| Dashboard Page | Server Component | Initial data fetch, can call api.listTasks() server-side |
| TaskList | Server Component | Fetches tasks from GET /api/tasks, no interactivity |
| TaskCard | Client Component | Interactive (checkbox toggle, delete button) |
| AddTaskForm | Client Component | Form input, validation, submission |
| Navbar | Client Component | Logout button, profile dropdown |

### Data Flow Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                     Dashboard Page (Server Component)            │
│                                                                  │
│  1. Fetch tasks: const tasks = await api.listTasks()            │
│                                                                  │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │  Navbar (Client Component)                                 │ │
│  │  - Display user email                                      │ │
│  │  - Logout button                                           │ │
│  └────────────────────────────────────────────────────────────┘ │
│                                                                  │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │  AddTaskForm (Client Component)                            │ │
│  │  - Title input                                             │ │
│  │  - Submit button                                           │ │
│  │  - Optimistic create → POST /api/tasks                     │ │
│  └────────────────────────────────────────────────────────────┘ │
│                                                                  │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │  TaskList (Server Component)                               │ │
│  │  - Receives tasks as props from Dashboard Page             │ │
│  │  - Maps tasks → TaskCard components                        │ │
│  │                                                             │ │
│  │  ┌──────────────────────────────────────────────────────┐  │ │
│  │  │ TaskCard (Client Component)                          │  │ │
│  │  │ - Checkbox (toggle) → PATCH /api/tasks/{id}          │  │ │
│  │  │ - Delete button → DELETE /api/tasks/{id}             │  │ │
│  │  │ - useOptimistic for immediate UI updates             │  │ │
│  │  └──────────────────────────────────────────────────────┘  │ │
│  │                                                             │ │
│  │  ┌──────────────────────────────────────────────────────┐  │ │
│  │  │ TaskCard (Client Component)                          │  │ │
│  │  └──────────────────────────────────────────────────────┘  │ │
│  │                                                             │ │
│  │  ... (more TaskCards)                                      │ │
│  └────────────────────────────────────────────────────────────┘ │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## Component Implementation Blueprints

### 1. Dashboard Page (Server Component)

**File**: `frontend/src/app/dashboard/page.tsx`

**Type**: Server Component (NO 'use client')

**Purpose**: Server-side data fetching for initial page load

**Implementation Blueprint**:

```typescript
// frontend/src/app/dashboard/page.tsx
// Server Component - fetches data server-side

import { api } from '@/lib/api'
import { TaskList } from '@/components/dashboard/task-list'
import { AddTaskForm } from '@/components/dashboard/add-task'
import { Navbar } from '@/components/layout/navbar'

export default async function DashboardPage() {
  // Fetch tasks server-side (runs on server, not client)
  // This reduces client-side JavaScript and improves initial load
  const tasks = await api.listTasks()

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Navbar at top */}
      <Navbar />

      {/* Main content */}
      <main className="max-w-4xl mx-auto px-4 py-8">
        <div className="space-y-6">
          {/* Add task form */}
          <AddTaskForm />

          {/* Task list */}
          <TaskList initialTasks={tasks} />
        </div>
      </main>
    </div>
  )
}
```

**Key Decisions**:
- Fetch tasks server-side for faster initial load
- Pass tasks as props to TaskList
- TaskList can be Client Component to handle mutations

---

### 2. TaskList Component (Hybrid: Server fetch + Client state)

**File**: `frontend/src/components/dashboard/task-list.tsx`

**Type**: Client Component (needs state for mutations)

**Purpose**: Display task list with support for optimistic updates from child components

**Implementation Blueprint**:

```typescript
// frontend/src/components/dashboard/task-list.tsx
'use client'

import { useState } from 'react'
import { TaskCard } from './task-card'
import { Task } from '@/lib/api'

interface TaskListProps {
  initialTasks: Task[]
}

export function TaskList({ initialTasks }: TaskListProps) {
  const [tasks, setTasks] = useState<Task[]>(initialTasks)

  // Empty state
  if (tasks.length === 0) {
    return (
      <div className="text-center py-12">
        <p className="text-gray-500 text-lg">
          No tasks yet. Create your first task!
        </p>
      </div>
    )
  }

  return (
    <div className="space-y-4">
      {tasks.map((task) => (
        <TaskCard
          key={task.id}
          task={task}
          onUpdate={(updatedTask) => {
            setTasks(tasks.map(t => t.id === updatedTask.id ? updatedTask : t))
          }}
          onDelete={(taskId) => {
            setTasks(tasks.filter(t => t.id !== taskId))
          }}
        />
      ))}
    </div>
  )
}
```

**Alternative Pattern (Server Component)**:

If we want TaskList to remain a pure Server Component:

```typescript
// frontend/src/components/dashboard/task-list.tsx
// Server Component - no state, just rendering

import { TaskCard } from './task-card'
import { Task } from '@/lib/api'

interface TaskListProps {
  initialTasks: Task[]
}

export function TaskList({ initialTasks }: TaskListProps) {
  if (initialTasks.length === 0) {
    return (
      <div className="text-center py-12">
        <p className="text-gray-500 text-lg">
          No tasks yet. Create your first task!
        </p>
      </div>
    )
  }

  return (
    <div className="space-y-4">
      {initialTasks.map((task) => (
        <TaskCard key={task.id} task={task} />
      ))}
    </div>
  )
}
```

**Decision**: Use Client Component pattern so TaskList can manage task array state when children (TaskCard) perform optimistic updates. This avoids full page refresh after each mutation.

---

### 3. TaskCard Component (Client Component)

**File**: `frontend/src/components/dashboard/task-card.tsx`

**Type**: Client Component ('use client')

**Purpose**: Interactive task display with toggle/delete and optimistic updates

**Implementation Blueprint**:

```typescript
// frontend/src/components/dashboard/task-card.tsx
'use client'

import { useState, useOptimistic, useTransition } from 'react'
import { useRouter } from 'next/navigation'
import { api, Task } from '@/lib/api'
import { toast } from 'sonner'

interface TaskCardProps {
  task: Task
  onUpdate?: (task: Task) => void
  onDelete?: (taskId: string) => void
}

export function TaskCard({ task, onUpdate, onDelete }: TaskCardProps) {
  const router = useRouter()
  const [isPending, startTransition] = useTransition()
  const [isDeleting, setIsDeleting] = useState(false)

  // Optimistic state for completion toggle
  const [optimisticCompleted, setOptimisticCompleted] = useOptimistic(
    task.completed,
    (state, newValue: boolean) => newValue
  )

  // Toggle completion with optimistic update
  const handleToggle = async () => {
    const newCompleted = !task.completed

    // Optimistic UI update (immediate - <50ms)
    setOptimisticCompleted(newCompleted)

    startTransition(async () => {
      try {
        // API call with JWT Bearer token
        const updatedTask = await api.toggleTask(task.id, newCompleted)

        // Success: Update parent state
        onUpdate?.(updatedTask)

        // Revalidate server component data (optional)
        router.refresh()
      } catch (error) {
        // Rollback optimistic update
        setOptimisticCompleted(task.completed)

        // Show error toast
        toast.error('Failed to update task. Please try again.')
      }
    })
  }

  // Delete task with confirmation
  const handleDelete = async () => {
    // Confirmation dialog
    const confirmed = confirm('Are you sure you want to delete this task?')
    if (!confirmed) return

    setIsDeleting(true)

    try {
      // API call with JWT Bearer token
      await api.deleteTask(task.id)

      // Success: Update parent state (optimistic removal)
      onDelete?.(task.id)

      // Show success toast
      toast.success('Task deleted')

      // Revalidate server component data
      router.refresh()
    } catch (error) {
      // Error: Show toast (task remains visible)
      setIsDeleting(false)
      toast.error('Failed to delete task.')
    }
  }

  return (
    <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-4 hover:shadow-md transition-shadow">
      <div className="flex items-start space-x-4">
        {/* Checkbox for completion toggle */}
        <input
          type="checkbox"
          checked={optimisticCompleted}
          onChange={handleToggle}
          disabled={isPending}
          className="mt-1 h-5 w-5 text-blue-600 rounded focus:ring-2 focus:ring-blue-500 cursor-pointer disabled:opacity-50"
          aria-label={`Mark task as ${optimisticCompleted ? 'incomplete' : 'complete'}`}
        />

        {/* Task content */}
        <div className="flex-1 min-w-0">
          <h3
            className={`text-lg font-medium ${
              optimisticCompleted
                ? 'line-through text-gray-500'
                : 'text-gray-900'
            }`}
          >
            {task.title}
          </h3>

          {task.description && (
            <p className="mt-1 text-sm text-gray-600 line-clamp-2">
              {task.description}
            </p>
          )}

          <p className="mt-2 text-xs text-gray-400">
            Created {new Date(task.created_at).toLocaleDateString()}
          </p>
        </div>

        {/* Delete button */}
        <button
          onClick={handleDelete}
          disabled={isDeleting || isPending}
          className="text-red-600 hover:text-red-800 disabled:opacity-50 px-3 py-1 rounded hover:bg-red-50 transition-colors"
          aria-label={`Delete task: ${task.title}`}
        >
          {isDeleting ? 'Deleting...' : 'Delete'}
        </button>
      </div>

      {/* Loading indicator for toggle */}
      {isPending && (
        <div className="mt-2 text-xs text-gray-500">Updating...</div>
      )}
    </div>
  )
}
```

**Key Patterns**:
- `useOptimistic` hook for immediate completion toggle
- `useTransition` for pending state
- Confirmation dialog for delete
- Error handling with toast notifications
- Rollback on API failure
- Disabled state during mutations

---

### 4. AddTaskForm Component (Client Component)

**File**: `frontend/src/components/dashboard/add-task.tsx`

**Type**: Client Component ('use client')

**Purpose**: Task creation form with validation and optimistic updates

**Implementation Blueprint**:

```typescript
// frontend/src/components/dashboard/add-task.tsx
'use client'

import { useState, useTransition } from 'react'
import { useRouter } from 'next/navigation'
import { api } from '@/lib/api'
import { toast } from 'sonner'

export function AddTaskForm() {
  const router = useRouter()
  const [title, setTitle] = useState('')
  const [titleError, setTitleError] = useState('')
  const [isPending, startTransition] = useTransition()

  // Real-time validation
  const validateTitle = (value: string): boolean => {
    if (!value.trim()) {
      setTitleError('Title is required')
      return false
    }
    if (value.length > 200) {
      setTitleError('Title must be 200 characters or less')
      return false
    }
    setTitleError('')
    return true
  }

  // Handle form submission with optimistic update
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()

    // Validate
    if (!validateTitle(title)) {
      return
    }

    startTransition(async () => {
      try {
        // API call with JWT Bearer token
        const newTask = await api.createTask({ title: title.trim() })

        // Success: Clear form
        setTitle('')

        // Show success toast
        toast.success('Task created')

        // Revalidate server component data
        router.refresh()
      } catch (error) {
        // Error: Show toast (form remains)
        toast.error('Failed to create task. Please try again.')
      }
    })
  }

  // Handle Enter key
  const handleKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Enter') {
      handleSubmit(e as any)
    }
  }

  return (
    <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-4">
      <form onSubmit={handleSubmit} className="flex items-start space-x-4">
        <div className="flex-1">
          <input
            type="text"
            value={title}
            onChange={(e) => {
              setTitle(e.target.value)
              validateTitle(e.target.value)
            }}
            onBlur={() => validateTitle(title)}
            onKeyDown={handleKeyDown}
            placeholder="What needs to be done?"
            disabled={isPending}
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent disabled:opacity-50"
            aria-label="New task title"
            aria-invalid={!!titleError}
            aria-describedby={titleError ? 'title-error' : undefined}
            maxLength={200}
          />

          {titleError && (
            <p id="title-error" className="mt-1 text-sm text-red-600">
              {titleError}
            </p>
          )}
        </div>

        <button
          type="submit"
          disabled={isPending || !!titleError || !title.trim()}
          className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors flex items-center space-x-2"
        >
          {isPending ? (
            <>
              <svg className="animate-spin h-4 w-4" viewBox="0 0 24 24">
                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none" />
                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
              </svg>
              <span>Adding...</span>
            </>
          ) : (
            <span>Add Task</span>
          )}
        </button>
      </form>
    </div>
  )
}
```

**Key Patterns**:
- Real-time validation on change and blur
- Enter key submits form
- Loading spinner during submission
- Clear form on success
- Error toast on failure
- Disabled state during pending

---

### 5. TaskList Component (Final Implementation)

**File**: `frontend/src/components/dashboard/task-list.tsx`

**Type**: Server Component (pure rendering)

**Purpose**: Render list of TaskCard components from server-fetched data

**Implementation Blueprint**:

```typescript
// frontend/src/components/dashboard/task-list.tsx
// Server Component - pure rendering, no state

import { TaskCard } from './task-card'
import { Task } from '@/lib/api'

interface TaskListProps {
  initialTasks: Task[]
}

export function TaskList({ initialTasks }: TaskListProps) {
  // Empty state
  if (initialTasks.length === 0) {
    return (
      <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-12 text-center">
        <svg
          className="mx-auto h-12 w-12 text-gray-400"
          fill="none"
          viewBox="0 0 24 24"
          stroke="currentColor"
        >
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth={2}
            d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"
          />
        </svg>
        <h3 className="mt-4 text-lg font-medium text-gray-900">No tasks yet</h3>
        <p className="mt-2 text-sm text-gray-500">
          Create your first task to get started!
        </p>
      </div>
    )
  }

  return (
    <div className="space-y-4">
      <h2 className="text-xl font-semibold text-gray-900">
        Your Tasks ({initialTasks.length})
      </h2>

      <div className="space-y-3">
        {initialTasks.map((task) => (
          <TaskCard key={task.id} task={task} />
        ))}
      </div>
    </div>
  )
}
```

**Simplified Approach**:
- TaskCard handles its own mutations
- router.refresh() in TaskCard causes full re-fetch
- No parent state management needed
- Simpler, more aligned with Server Component model

---

### 6. Navbar Component (Client Component)

**File**: `frontend/src/components/layout/navbar.tsx`

**Type**: Client Component ('use client')

**Purpose**: Display user profile and logout button

**Implementation Blueprint**:

```typescript
// frontend/src/components/layout/navbar.tsx
'use client'

import { useAuth, clientSignOut } from '@/lib/auth-client'
import { useRouter } from 'next/navigation'
import { toast } from 'sonner'

export function Navbar() {
  const { user, isLoading } = useAuth()
  const router = useRouter()

  const handleLogout = async () => {
    try {
      await clientSignOut()
      toast.success('Logged out successfully')
      router.push('/signin')
    } catch (error) {
      toast.error('Failed to logout')
    }
  }

  if (isLoading) {
    return (
      <nav className="bg-white shadow-sm border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="h-6 w-32 bg-gray-200 rounded animate-pulse" />
            <div className="h-8 w-20 bg-gray-200 rounded animate-pulse" />
          </div>
        </div>
      </nav>
    )
  }

  return (
    <nav className="bg-white shadow-sm border-b border-gray-200 sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          {/* Logo/Title */}
          <div className="flex-shrink-0">
            <h1 className="text-xl font-bold text-gray-900">Todo App</h1>
          </div>

          {/* User info and logout */}
          <div className="flex items-center space-x-4">
            {/* User email (hide on mobile <768px) */}
            <span className="hidden md:block text-sm text-gray-700">
              {user?.email || 'Loading...'}
            </span>

            {/* Logout button */}
            <button
              onClick={handleLogout}
              className="px-4 py-2 text-sm font-medium text-gray-700 hover:text-gray-900 hover:bg-gray-100 rounded-lg transition-colors"
              aria-label="Logout"
            >
              Logout
            </button>
          </div>
        </div>
      </div>
    </nav>
  )
}
```

**Key Patterns**:
- useAuth hook from Sprint 1
- clientSignOut from Better Auth
- Loading skeleton while session loading
- Responsive (hide email on mobile)
- Sticky positioning (stays at top)

---

## Optimistic Update Pattern (Detailed)

### Pattern Overview

```
User Action (click)
    ↓ <50ms
Optimistic UI Update (useOptimistic)
    ↓
API Call (with JWT Bearer token)
    ↓
    ├─ Success → Confirm (replace optimistic with server data)
    └─ Failure → Rollback (revert to original) + Error Toast
```

### Implementation Steps

1. **Setup Optimistic State**:
   ```typescript
   const [optimisticValue, setOptimisticValue] = useOptimistic(
     task.completed,
     (state, newValue: boolean) => newValue
   )
   ```

2. **Apply Optimistic Update**:
   ```typescript
   setOptimisticValue(newCompleted)
   ```

3. **Send API Request**:
   ```typescript
   const updated = await api.toggleTask(task.id, newCompleted)
   ```

4. **Handle Success**:
   ```typescript
   onUpdate?.(updated)  // Update parent state
   router.refresh()     // Revalidate server data
   ```

5. **Handle Failure**:
   ```typescript
   setOptimisticValue(task.completed)  // Rollback
   toast.error('Failed to update')      // Notify user
   ```

---

## Responsive Design Strategy

### Breakpoints (Tailwind CSS)

- **Mobile**: < 768px (sm:)
  - Full-width TaskCards
  - Stacked vertically
  - Hide user email in Navbar
  - Full-width AddTaskForm input

- **Tablet**: 768px - 1023px (md:)
  - Single column TaskCards
  - Show user email in Navbar
  - Comfortable spacing

- **Desktop**: 1024px+ (lg:)
  - Max-width constrained (max-w-4xl)
  - Full Navbar with profile
  - Optimal reading width

### Tailwind Classes

```typescript
// Container
<div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">

// Navbar responsive
<span className="hidden md:block">  // Hide on mobile

// TaskCard
<div className="bg-white rounded-lg p-4 sm:p-6">  // More padding on larger screens

// AddTaskForm
<input className="w-full md:w-auto" />  // Full width on mobile
```

---

## Implementation Phases (Sprint 2 Tasks)

### Phase 2.1: UI Primitives (T016-T019)
- Button.tsx (variants: primary, secondary, danger)
- Input.tsx (with error state, ARIA)
- Card.tsx (wrapper for TaskCard)
- Checkbox.tsx (for TaskCard toggle)

### Phase 2.2: Navbar Component (T020-T022)
- Navbar.tsx (user email + logout)
- Can skip ProfileDropdown for Sprint 2 (simplified)
- LogoutButton integrated into Navbar

### Phase 2.3: Dashboard Page (T023-T024)
- Create `frontend/src/app/(protected)/` route group
- Dashboard page at `(protected)/dashboard/page.tsx`
- Protected layout with Navbar

### Phase 2.4: Task Components (New breakdown)
- TaskList component (`components/dashboard/task-list.tsx`)
- TaskCard component (`components/dashboard/task-card.tsx`)
- AddTaskForm component (`components/dashboard/add-task.tsx`)

---

## Testing Strategy

### Manual Testing Checklist

After Sprint 2 implementation, test:

1. **Dashboard Load**:
   - [ ] Dashboard loads and displays Navbar
   - [ ] TaskList fetches and displays tasks
   - [ ] Empty state shows when no tasks

2. **Navbar**:
   - [ ] User email displays correctly
   - [ ] Logout button works
   - [ ] Redirects to /signin after logout

3. **TaskCard Toggle**:
   - [ ] Checkbox updates immediately (optimistic)
   - [ ] API call sent to PATCH /api/tasks/{id}
   - [ ] Rollback works on API error
   - [ ] Error toast shows on failure

4. **AddTaskForm**:
   - [ ] Title input validates in real-time
   - [ ] Submit creates task (optimistic)
   - [ ] Form clears on success
   - [ ] Error toast shows on failure

5. **TaskCard Delete**:
   - [ ] Confirmation dialog appears
   - [ ] Task disappears immediately (optimistic)
   - [ ] API call sent to DELETE /api/tasks/{id}
   - [ ] Rollback works on API error

6. **Responsive Design**:
   - [ ] Works on mobile (320px)
   - [ ] Works on tablet (768px)
   - [ ] Works on desktop (1920px)
   - [ ] No horizontal scroll

7. **Accessibility**:
   - [ ] Tab navigation works
   - [ ] Enter key submits forms
   - [ ] ARIA labels present
   - [ ] Screen reader friendly

---

## Risk Analysis

| Risk | Impact | Mitigation |
|------|--------|------------|
| Server Component can't handle mutations | High - Pattern breaks | Use Client Component for TaskList with state management OR use router.refresh() in TaskCard |
| useOptimistic hook not available (React 18) | Medium - Fallback needed | Use useState as fallback: `const [optimistic, setOptimistic] = useState(task.completed)` |
| router.refresh() is slow (>1s) | Medium - Poor UX | Use parent callback pattern (onUpdate, onDelete) to avoid full refresh |
| Large task lists (1000+) cause lag | Low - Future problem | Virtual scrolling or pagination in later sprint |
| Confirmation dialog blocks UI | Low - UX issue | Use proper modal component instead of browser confirm() |

---

## Next Steps

1. **Implement UI Primitives** (T016-T019): Button, Input, Card, Checkbox
2. **Implement Navbar** (T020): Client Component with logout
3. **Implement Dashboard Components**:
   - AddTaskForm (`components/dashboard/add-task.tsx`)
   - TaskList (`components/dashboard/task-list.tsx`)
   - TaskCard (`components/dashboard/task-card.tsx`)
4. **Implement Dashboard Page** (`app/dashboard/page.tsx`)
5. **Test all functionality** manually

---

**Plan Status**: ✅ COMPLETE - Ready for Sprint 2 implementation
**Branch**: `001-frontend-core`
**Date**: 2025-12-23
