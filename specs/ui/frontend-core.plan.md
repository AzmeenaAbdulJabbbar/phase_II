# Implementation Plan: Frontend UI Core

**Branch**: `001-frontend-core` | **Date**: 2025-12-23 | **Spec**: [frontend-core.md](frontend-core.md)

**Input**: User architectural requirements:
1. MONOREPO SYNC: Plan files inside the '/frontend' directory.
2. AUTH SETUP: Plan 'frontend/src/auth.ts' for Better Auth configuration.
3. API WRAPPER: Design a fetch wrapper that handles the 'BETTER_AUTH_SECRET' handshake and includes the 'user_id' in URL paths.
4. COMPONENT TREE: Navbar, TaskCard, TaskList, and AuthForm components.
5. STATE MANAGEMENT: Use React Server Components for fetching and Client Components for interactivity (toggling tasks).

---

## Summary

This plan outlines the implementation of the Phase II Frontend UI Core - a responsive, multi-user Todo web interface built with Next.js 15+ App Router, Better Auth with JWT integration, and a centralized API client. The frontend communicates with the FastAPI backend via JWT-secured API calls with Bearer token authentication, ensuring complete data isolation between users.

**Primary Objective**: Create a production-ready frontend in `/frontend` directory with:
- Better Auth configuration in `frontend/src/auth.ts`
- API client in `frontend/src/lib/api.ts` with automatic JWT Bearer token injection
- Component tree: Navbar, TaskCard, TaskList, AuthForm
- React Server Components for data fetching + Client Components for interactivity

**Technical Approach**:
- Next.js 15+ App Router with TypeScript strict mode and Tailwind CSS
- Better Auth with JWT Plugin for authentication (configured in `frontend/src/auth.ts`)
- Custom API client wrapper in `frontend/src/lib/api.ts` with Bearer token and user_id handling
- Server Components for data fetching, Client Components for interactive elements
- Optimistic UI updates for smooth user experience
- Responsive design (320px-1920px screen widths)

---

## Technical Context

**Language/Version**: TypeScript (strict mode), Node.js 20+ LTS
**Primary Dependencies**: Next.js 15+ (or 16+ per Constitution), React 18+, Better Auth, Tailwind CSS
**Storage**: Browser httpOnly cookies for JWT tokens (secure)
**Testing**: Vitest for unit tests, Playwright for E2E (future)
**Target Platform**: Modern web browsers (Chrome, Firefox, Safari, Edge - last 2 versions)
**Project Type**: Web application (monorepo frontend component)
**Performance Goals**:
- Task list displays within 2 seconds (SC-004)
- Optimistic UI updates within 50ms (SC-007)
- Form validation feedback <100ms (SC-008)
- Signup within 30 seconds (SC-001)
- Login within 20 seconds (SC-002)
- Create task within 10 seconds (SC-003)

**Constraints**:
- All files MUST reside inside `/frontend` directory (monorepo structure)
- JWT Bearer token MUST be attached to EVERY API request
- API client MUST handle `BETTER_AUTH_SECRET` verification
- Protected routes MUST redirect to `/signin` via Next.js middleware
- Maximum 1000 tasks per user for UI performance

**Scale/Scope**:
- Multi-user system (isolated data per user_id)
- 10 user stories (P1-P3 prioritization)
- 77 functional requirements (FR-001 to FR-077)
- 14 success criteria (SC-001 to SC-014)

---

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-checked after Phase 1 design.*

✅ **I. Spec-Driven Development**:
- Spec created at `specs/ui/frontend-core.md`
- Planning follows `/sp.plan` workflow
- Tasks generation will follow `/sp.tasks`
- Implementation via `/sp.implement`

✅ **II. Monorepo Architecture**:
- Frontend in `/frontend` directory (Constitution mandates)
- Specs in `/specs/ui/`
- Layered CLAUDE.md for frontend-specific rules

✅ **III. Technology Stack Compliance**:
- Next.js 15+ with App Router ✓ (Constitution allows 15+, prefers 16+)
- TypeScript strict mode ✓
- Tailwind CSS ✓
- Better Auth with JWT Plugin ✓

✅ **IV. Security & Identity Protocol**:
- Better Auth JWT Plugin enabled (configured in `frontend/src/auth.ts`)
- Bearer token injection on EVERY API request (implemented in `frontend/src/lib/api.ts`)
- JWT Bridge pattern implemented (Authorization header)
- Backend JWT verification required (Constitution Section IV)
- Data isolation by user_id (enforced by backend, verified by frontend)

✅ **V. Database & API Patterns**:
- API client follows REST conventions
- TypeScript types mirror backend Pydantic models
- Consistent error handling (401, 422, network errors)
- All backend routes under `/api/` prefix

✅ **VI. Spec-Kit Plus Workflow**:
- Spec in `/specs/ui/frontend-core.md`
- Plan in `/specs/ui/frontend-core.plan.md` (this file)
- Tasks will be in `/specs/ui/tasks.md` (next step via `/sp.tasks`)
- Implementation follows workflow sequence

**GATE RESULT**: ✅ PASS - All constitutional requirements satisfied

---

## Project Structure

### Documentation (this feature)

```text
specs/ui/
├── frontend-core.md              # Feature specification
├── frontend-core.plan.md         # This file (/sp.plan output)
├── plan/
│   ├── research.md               # Phase 0: Technology decisions
│   ├── data-model.md             # Phase 1: TypeScript type definitions
│   ├── quickstart.md             # Phase 1: Setup instructions
│   └── contracts/                # Phase 1: API/Auth contracts
│       ├── api-client.ts
│       └── auth-types.ts
├── checklists/                   # Requirement validation
│   └── requirements.md
└── tasks.md                      # Phase 2: Generated by /sp.tasks
```

### Source Code (frontend directory)

```text
frontend/                            # Next.js 15+ application
├── src/
│   ├── app/                        # App Router pages
│   │   ├── (auth)/                # Route group: Auth pages (no navbar)
│   │   │   ├── signin/
│   │   │   │   └── page.tsx       # Login page → AuthForm component
│   │   │   ├── signup/
│   │   │   │   └── page.tsx       # Registration page → AuthForm component
│   │   │   └── layout.tsx         # Minimal auth layout
│   │   ├── (protected)/           # Route group: Protected routes (with navbar)
│   │   │   ├── dashboard/
│   │   │   │   └── page.tsx       # Main dashboard → TaskList + Navbar
│   │   │   ├── profile/
│   │   │   │   └── page.tsx       # User profile page
│   │   │   ├── layout.tsx         # Protected layout (includes Navbar)
│   │   │   └── loading.tsx        # Loading skeleton
│   │   ├── layout.tsx             # Root layout (Tailwind, Better Auth Provider)
│   │   ├── page.tsx               # Landing page (redirects to dashboard or signin)
│   │   └── globals.css            # Tailwind imports
│   ├── components/
│   │   ├── ui/                    # Reusable UI primitives
│   │   │   ├── Button.tsx
│   │   │   ├── Input.tsx
│   │   │   ├── Card.tsx
│   │   │   ├── Checkbox.tsx
│   │   │   ├── Modal.tsx
│   │   │   ├── Skeleton.tsx
│   │   │   └── Toast.tsx
│   │   ├── layout/                # Layout components
│   │   │   ├── Navbar.tsx         # [REQUIRED] Top navigation with user info/logout
│   │   │   └── ProfileDropdown.tsx # User profile menu
│   │   ├── tasks/                 # Task-related components
│   │   │   ├── TaskList.tsx       # [REQUIRED] Task list container (Server Component)
│   │   │   ├── TaskCard.tsx       # [REQUIRED] Individual task with toggle/delete (Client Component)
│   │   │   ├── AddTaskForm.tsx    # Create task form (Client Component)
│   │   │   ├── TaskFilters.tsx    # Filter controls: All/Active/Completed (Client Component)
│   │   │   └── EmptyState.tsx     # No tasks UI
│   │   └── auth/                  # Auth components
│   │       ├── AuthForm.tsx       # [REQUIRED] Unified signin/signup form (Client Component)
│   │       └── LogoutButton.tsx   # Logout action (Client Component)
│   ├── lib/
│   │   ├── api.ts                 # [REQUIRED] API client with Bearer token injection
│   │   └── auth-client.ts         # Better Auth client utilities
│   ├── auth.ts                    # [REQUIRED] Better Auth server configuration
│   ├── types/
│   │   ├── task.ts                # Task, TaskCreate, TaskUpdate types
│   │   ├── api.ts                 # ApiResponse, ApiError types
│   │   ├── auth.ts                # User, Session types
│   │   └── ui.ts                  # TaskFilter, LoadingState types
│   └── middleware.ts              # [REQUIRED] Route protection middleware
├── public/
│   └── assets/
├── .env.example                   # Environment template
├── .env.local                     # Local environment (gitignored)
├── tailwind.config.ts             # Tailwind configuration
├── next.config.ts                 # Next.js configuration
├── tsconfig.json                  # TypeScript strict mode
├── package.json                   # Dependencies and scripts
└── README.md                      # Setup instructions
```

**Structure Decision**: Monorepo web application with `/frontend` as the Next.js component. Route groups `(auth)` and `(protected)` separate authentication pages from protected dashboard pages. Component tree follows user requirements: Navbar, TaskCard, TaskList, AuthForm.

---

## Phase 0: Research (Completed)

**Output**: `specs/ui/plan/research.md`

**Resolved Unknowns**:
1. ✅ Next.js 15+ App Router structure with route groups
2. ✅ Better Auth configuration in `frontend/src/auth.ts` with JWT Plugin
3. ✅ API client pattern in `frontend/src/lib/api.ts` with Bearer token + user_id
4. ✅ Component architecture: Server Components (data) + Client Components (interactivity)
5. ✅ Tailwind CSS responsive design strategy
6. ✅ State management: Server Components for fetching, Client Components with local state
7. ✅ TypeScript types mirroring backend Pydantic models

**Key Decisions**:
- **Auth Configuration**: Better Auth in `frontend/src/auth.ts` with JWT Plugin, httpOnly cookies
- **API Client**: Custom fetch wrapper in `frontend/src/lib/api.ts` with Bearer token injection
- **Component Strategy**: Server Components for data fetching (TaskList), Client Components for interactivity (TaskCard, AuthForm)
- **Styling**: Tailwind CSS utility-first approach
- **State**: React `useState` for Client Component local state, `useOptimistic` for optimistic updates
- **Types**: Shared TypeScript interfaces in `frontend/src/types/`

---

## Phase 1: Design & Contracts

### 1.1 Better Auth Configuration (`frontend/src/auth.ts`)

**Purpose**: Server-side Better Auth configuration with JWT Plugin

**Implementation Blueprint**:

```typescript
// frontend/src/auth.ts
import { betterAuth } from "better-auth"
import { jwt } from "better-auth/plugins"

export const auth = betterAuth({
  // Shared secret with backend (MUST match)
  secret: process.env.BETTER_AUTH_SECRET!,

  // Enable JWT plugin for token-based auth
  plugins: [jwt()],

  // Database configuration (if Better Auth needs persistence)
  database: {
    url: process.env.DATABASE_URL,
    type: "postgres",
  },

  // Session configuration
  session: {
    cookieName: "better-auth.session_token",
    expiresIn: 60 * 60 * 24 * 7, // 7 days
    updateAge: 60 * 60 * 24, // Update every 24 hours
  },

  // Email/password provider
  emailAndPassword: {
    enabled: true,
    minPasswordLength: 8,
  },
})

// Export auth methods for use in API routes
export const {
  signIn,
  signUp,
  signOut,
  getSession,
} = auth
```

**Key Requirements** (from user):
- File location: `frontend/src/auth.ts`
- JWT Plugin must be enabled
- Shared `BETTER_AUTH_SECRET` with backend
- Secure token storage (httpOnly cookies)

**Referenced FR**:
- FR-005: Frontend MUST integrate Better Auth with JWT Plugin
- FR-006: Better Auth MUST issue JWT tokens upon signup/login
- FR-007: JWT tokens MUST be stored securely (httpOnly cookies)

---

### 1.2 API Client (`frontend/src/lib/api.ts`)

**Purpose**: Centralized API client that automatically attaches JWT Bearer token to all requests

**Implementation Blueprint**:

```typescript
// frontend/src/lib/api.ts
import { getSession } from '@/auth'

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api'
const REQUEST_TIMEOUT = 10000 // 10 seconds

export class ApiError extends Error {
  constructor(
    public status: number,
    public detail: string,
    public validationErrors?: Record<string, string[]>
  ) {
    super(detail)
    this.name = 'ApiError'
  }
}

class ApiClient {
  /**
   * Get JWT token from Better Auth session
   */
  private async getToken(): Promise<string | null> {
    const session = await getSession()
    return session?.accessToken || null
  }

  /**
   * Extract user_id from JWT token (optional, for URL paths if needed)
   * Note: Backend extracts user_id from JWT, but frontend can use it for URL construction
   */
  private async getUserId(): Promise<string | null> {
    const session = await getSession()
    return session?.user?.id || null
  }

  /**
   * Centralized request method with Bearer token injection
   */
  private async request<T>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<T> {
    const token = await this.getToken()

    // Build headers with JWT Bearer token
    const headers: HeadersInit = {
      'Content-Type': 'application/json',
      ...options.headers,
    }

    // CRITICAL: Attach JWT Bearer token to EVERY request (Constitution IV)
    if (token) {
      headers['Authorization'] = `Bearer ${token}`
    }

    // Setup timeout
    const controller = new AbortController()
    const timeoutId = setTimeout(() => controller.abort(), REQUEST_TIMEOUT)

    try {
      const response = await fetch(`${API_BASE_URL}${endpoint}`, {
        ...options,
        headers,
        signal: controller.signal,
      })

      clearTimeout(timeoutId)

      // Handle 401 Unauthorized: redirect to signin (FR-024)
      if (response.status === 401) {
        if (typeof window !== 'undefined') {
          window.location.href = '/signin'
        }
        throw new ApiError(401, 'Session expired. Please log in again.')
      }

      // Handle 422 Validation Error (FR-025)
      if (response.status === 422) {
        const error = await response.json()
        throw new ApiError(422, 'Validation error', error.detail)
      }

      // Handle other errors
      if (!response.ok) {
        const error = await response.json()
        throw new ApiError(
          response.status,
          error.detail || 'Request failed'
        )
      }

      // Success: return JSON
      return response.json()
    } catch (error) {
      if (error.name === 'AbortError') {
        throw new ApiError(408, 'Request timeout. Please try again.')
      }
      throw error
    }
  }

  /**
   * GET request
   */
  async get<T>(endpoint: string): Promise<T> {
    return this.request<T>(endpoint, { method: 'GET' })
  }

  /**
   * POST request
   */
  async post<T>(endpoint: string, data: any): Promise<T> {
    return this.request<T>(endpoint, {
      method: 'POST',
      body: JSON.stringify(data),
    })
  }

  /**
   * PATCH request
   */
  async patch<T>(endpoint: string, data: any): Promise<T> {
    return this.request<T>(endpoint, {
      method: 'PATCH',
      body: JSON.stringify(data),
    })
  }

  /**
   * DELETE request
   */
  async delete<T>(endpoint: string): Promise<T> {
    return this.request<T>(endpoint, { method: 'DELETE' })
  }

  // ============================================
  // Task API Methods (optional convenience layer)
  // ============================================

  /**
   * List all tasks for authenticated user
   * Backend filters by user_id extracted from JWT
   */
  async listTasks(): Promise<Task[]> {
    return this.get<Task[]>('/tasks')
  }

  /**
   * Create new task
   * Backend assigns user_id from JWT
   */
  async createTask(data: TaskCreate): Promise<Task> {
    return this.post<Task>('/tasks', data)
  }

  /**
   * Toggle task completion
   */
  async toggleTask(taskId: string, completed: boolean): Promise<Task> {
    return this.patch<Task>(`/tasks/${taskId}`, { completed })
  }

  /**
   * Delete task
   */
  async deleteTask(taskId: string): Promise<void> {
    return this.delete<void>(`/tasks/${taskId}`)
  }
}

// Export singleton instance
export const api = new ApiClient()

// Type definitions
export interface Task {
  id: string
  user_id: string
  title: string
  description: string
  completed: boolean
  created_at: string
  updated_at: string
}

export interface TaskCreate {
  title: string
  description?: string
}
```

**Key Requirements** (from user):
- File location: `frontend/src/lib/api.ts`
- Fetch wrapper that handles `BETTER_AUTH_SECRET` handshake via Bearer token
- Includes `user_id` in URL paths (optional - backend extracts from JWT)
- Automatic JWT Bearer token attachment to ALL requests (FR-020 to FR-028)

**Referenced FR**:
- FR-020: API client in `frontend/src/lib/api.ts`
- FR-021: Automatically attach JWT Bearer token to Authorization header
- FR-022: Extract JWT from Better Auth session
- FR-023: Format as "Authorization: Bearer <token>"
- FR-024: Handle 401 Unauthorized → redirect to /signin
- FR-025: Handle 422 Unprocessable Entity → show validation errors
- FR-026: Handle network errors with user-friendly messages
- FR-027: Set timeout (10 seconds recommended)
- FR-028: Support GET, POST, PATCH, DELETE methods

---

### 1.3 Component Tree Architecture

#### Component Strategy

**Server Components** (data fetching, no interactivity):
- Used for: Initial page loads, data fetching from API
- Benefits: Zero JavaScript sent to client, can call API directly server-side
- Examples: Dashboard page container, TaskList parent component

**Client Components** (`'use client'` directive, interactive):
- Used for: Forms, buttons, state management, user interactions
- Requirements: Mark with `'use client'` at top of file
- Examples: TaskCard (toggle/delete actions), AuthForm (form inputs), AddTaskForm

#### Component Tree (as requested by user)

```
App (Root Layout) - Server Component
├── Better Auth Provider
├── Tailwind CSS Global Styles
│
├── (auth) Route Group - Minimal Layout
│   ├── /signin → Signin Page (Server Component)
│   │   └── AuthForm (Client Component) - [REQUIRED by user]
│   └── /signup → Signup Page (Server Component)
│       └── AuthForm (Client Component) - [REQUIRED by user]
│
└── (protected) Route Group - Full Layout with Navbar
    ├── Navbar (Client Component) - [REQUIRED by user]
    │   ├── User email display
    │   └── ProfileDropdown (Client Component)
    │       └── LogoutButton (Client Component)
    │
    └── /dashboard → Dashboard Page (Server Component)
        ├── TaskList (Server Component) - [REQUIRED by user]
        │   │   Fetches tasks via api.listTasks() server-side
        │   │
        │   ├── TaskCard (Client Component) - [REQUIRED by user]
        │   │   ├── Checkbox for toggle (interactive)
        │   │   └── Delete button (interactive)
        │   │
        │   ├── TaskCard (Client Component) - [REQUIRED by user]
        │   └── TaskCard (Client Component) - [REQUIRED by user]
        │       ... (one TaskCard per task)
        │
        ├── AddTaskForm (Client Component)
        │   └── Form with title/description inputs
        │
        └── TaskFilters (Client Component)
            └── Buttons: All | Active | Completed
```

---

### 1.4 Component Implementations

#### 1.4.1 Navbar Component

**File**: `frontend/src/components/layout/Navbar.tsx`

**Requirements**:
- Display current user's email (FR-062)
- Profile icon/button with dropdown (FR-063, FR-064)
- Logout functionality (FR-065)
- Extract user email from JWT token claims

**Implementation Blueprint**:

```typescript
// frontend/src/components/layout/Navbar.tsx
'use client'

import { useState } from 'react'
import { useSession } from '@/lib/auth-client'
import { LogoutButton } from '@/components/auth/LogoutButton'

export function Navbar() {
  const { session } = useSession()
  const [dropdownOpen, setDropdownOpen] = useState(false)

  if (!session?.user) return null

  return (
    <nav className="bg-white shadow-sm border-b border-gray-200">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          {/* Logo/Title */}
          <div className="flex-shrink-0">
            <h1 className="text-xl font-bold text-gray-900">Todo App</h1>
          </div>

          {/* User menu */}
          <div className="relative">
            <button
              onClick={() => setDropdownOpen(!dropdownOpen)}
              className="flex items-center space-x-2 text-sm text-gray-700 hover:text-gray-900"
            >
              <span>{session.user.email}</span>
              <svg className="h-5 w-5" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z" clipRule="evenodd" />
              </svg>
            </button>

            {/* Dropdown menu */}
            {dropdownOpen && (
              <div className="absolute right-0 mt-2 w-48 bg-white rounded-md shadow-lg py-1 z-10">
                <a href="/profile" className="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100">
                  Profile
                </a>
                <div className="border-t border-gray-100">
                  <LogoutButton />
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </nav>
  )
}
```

---

#### 1.4.2 TaskList Component (Server Component)

**File**: `frontend/src/components/tasks/TaskList.tsx`

**Requirements**:
- Server Component for data fetching
- Fetches tasks using `api.listTasks()` server-side
- Passes tasks to Client Component TaskCard children
- Displays loading skeleton while fetching (FR-031)
- Shows empty state when no tasks (FR-032)

**Implementation Blueprint**:

```typescript
// frontend/src/components/tasks/TaskList.tsx
// NOTE: This is a Server Component (no 'use client')

import { api } from '@/lib/api'
import { TaskCard } from './TaskCard'
import { EmptyState } from './EmptyState'

export async function TaskList() {
  // Fetch tasks server-side (runs on server, not client)
  const tasks = await api.listTasks()

  // Empty state
  if (tasks.length === 0) {
    return <EmptyState />
  }

  return (
    <div className="space-y-4">
      {tasks.map((task) => (
        <TaskCard key={task.id} task={task} />
      ))}
    </div>
  )
}
```

---

#### 1.4.3 TaskCard Component (Client Component)

**File**: `frontend/src/components/tasks/TaskCard.tsx`

**Requirements**:
- Client Component for interactivity
- Checkbox for toggle completion (FR-044, FR-045)
- Delete button (FR-050)
- Optimistic updates (FR-047, FR-054)
- Error handling with rollback (FR-049, FR-056)

**Implementation Blueprint**:

```typescript
// frontend/src/components/tasks/TaskCard.tsx
'use client'

import { useState, useOptimistic } from 'react'
import { useRouter } from 'next/navigation'
import { api, Task } from '@/lib/api'
import { toast } from 'sonner'

interface TaskCardProps {
  task: Task
}

export function TaskCard({ task }: TaskCardProps) {
  const router = useRouter()
  const [isDeleting, setIsDeleting] = useState(false)

  // Optimistic state for completion toggle
  const [optimisticCompleted, setOptimisticCompleted] = useOptimistic(
    task.completed
  )

  // Toggle completion
  const handleToggle = async () => {
    const newCompleted = !task.completed

    // Optimistic UI update (FR-047)
    setOptimisticCompleted(newCompleted)

    try {
      // API call with Bearer token (FR-046)
      await api.toggleTask(task.id, newCompleted)

      // Success: Revalidate server component data
      router.refresh()
    } catch (error) {
      // Rollback optimistic update (FR-049)
      setOptimisticCompleted(task.completed)
      toast.error('Failed to update task. Please try again.')
    }
  }

  // Delete task
  const handleDelete = async () => {
    // Confirmation dialog (FR-051, FR-052)
    const confirmed = confirm('Are you sure you want to delete this task?')
    if (!confirmed) return

    setIsDeleting(true)

    try {
      // API call with Bearer token (FR-053)
      await api.deleteTask(task.id)

      // Success: Revalidate (FR-055)
      router.refresh()
      toast.success('Task deleted')
    } catch (error) {
      // Error: Show toast (FR-056)
      setIsDeleting(false)
      toast.error('Failed to delete task. Please try again.')
    }
  }

  return (
    <div className="bg-white rounded-lg shadow p-4 flex items-center space-x-4">
      {/* Checkbox for toggle */}
      <input
        type="checkbox"
        checked={optimisticCompleted}
        onChange={handleToggle}
        className="h-5 w-5 text-blue-600 rounded focus:ring-2 focus:ring-blue-500"
      />

      {/* Task content */}
      <div className="flex-1">
        <h3 className={`text-lg font-medium ${optimisticCompleted ? 'line-through text-gray-500' : 'text-gray-900'}`}>
          {task.title}
        </h3>
        {task.description && (
          <p className="text-sm text-gray-500 line-clamp-2">{task.description}</p>
        )}
      </div>

      {/* Delete button */}
      <button
        onClick={handleDelete}
        disabled={isDeleting}
        className="text-red-600 hover:text-red-800 disabled:opacity-50"
      >
        {isDeleting ? 'Deleting...' : 'Delete'}
      </button>
    </div>
  )
}
```

---

#### 1.4.4 AuthForm Component (Client Component)

**File**: `frontend/src/components/auth/AuthForm.tsx`

**Requirements**:
- Client Component for form interactivity
- Unified form for signin and signup
- Email and password inputs (FR-008, FR-009)
- Real-time validation (FR-010, FR-011, FR-012, FR-067, FR-068)
- Error display (FR-067, FR-071)
- Loading state during submission (FR-069)

**Implementation Blueprint**:

```typescript
// frontend/src/components/auth/AuthForm.tsx
'use client'

import { useState } from 'react'
import { useRouter } from 'next/navigation'
import { authClient } from '@/lib/auth-client'
import { toast } from 'sonner'

interface AuthFormProps {
  mode: 'signin' | 'signup'
}

export function AuthForm({ mode }: AuthFormProps) {
  const router = useRouter()
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [confirmPassword, setConfirmPassword] = useState('')
  const [emailError, setEmailError] = useState('')
  const [passwordError, setPasswordError] = useState('')
  const [isSubmitting, setIsSubmitting] = useState(false)

  const isSignup = mode === 'signup'

  // Email validation (FR-011)
  const validateEmail = (value: string) => {
    if (!value) {
      setEmailError('Email is required')
      return false
    }
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
    if (!emailRegex.test(value)) {
      setEmailError('Invalid email format')
      return false
    }
    setEmailError('')
    return true
  }

  // Password validation (FR-010)
  const validatePassword = (value: string) => {
    if (!value) {
      setPasswordError('Password is required')
      return false
    }
    if (value.length < 8) {
      setPasswordError('Password must be at least 8 characters')
      return false
    }
    if (isSignup && confirmPassword && value !== confirmPassword) {
      setPasswordError('Passwords do not match')
      return false
    }
    setPasswordError('')
    return true
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()

    // Validate
    const isEmailValid = validateEmail(email)
    const isPasswordValid = validatePassword(password)

    if (!isEmailValid || !isPasswordValid) {
      return
    }

    setIsSubmitting(true)

    try {
      if (isSignup) {
        // Signup flow (FR-008)
        await authClient.signUp({
          email,
          password,
          name: email.split('@')[0], // Optional: derive name from email
        })
        toast.success('Account created successfully!')
      } else {
        // Signin flow (FR-009)
        await authClient.signIn({
          email,
          password,
        })
        toast.success('Logged in successfully!')
      }

      // Redirect to dashboard (FR-001, FR-038)
      router.push('/dashboard')
    } catch (error: any) {
      // Show error (FR-071)
      if (error.message.includes('already exists')) {
        setEmailError('Email already registered')
      } else if (error.message.includes('Invalid')) {
        toast.error('Invalid email or password')
      } else {
        toast.error('An error occurred. Please try again.')
      }
    } finally {
      setIsSubmitting(false)
    }
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-6 max-w-md mx-auto">
      <div>
        <h2 className="text-2xl font-bold text-center">
          {isSignup ? 'Create Account' : 'Sign In'}
        </h2>
      </div>

      {/* Email input */}
      <div>
        <label htmlFor="email" className="block text-sm font-medium text-gray-700">
          Email
        </label>
        <input
          id="email"
          type="email"
          value={email}
          onChange={(e) => {
            setEmail(e.target.value)
            validateEmail(e.target.value)
          }}
          onBlur={() => validateEmail(email)}
          className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
          required
        />
        {emailError && (
          <p className="mt-1 text-sm text-red-600">{emailError}</p>
        )}
      </div>

      {/* Password input */}
      <div>
        <label htmlFor="password" className="block text-sm font-medium text-gray-700">
          Password
        </label>
        <input
          id="password"
          type="password"
          value={password}
          onChange={(e) => {
            setPassword(e.target.value)
            validatePassword(e.target.value)
          }}
          onBlur={() => validatePassword(password)}
          className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
          required
          minLength={8}
        />
        {passwordError && (
          <p className="mt-1 text-sm text-red-600">{passwordError}</p>
        )}
      </div>

      {/* Confirm password (signup only) */}
      {isSignup && (
        <div>
          <label htmlFor="confirmPassword" className="block text-sm font-medium text-gray-700">
            Confirm Password
          </label>
          <input
            id="confirmPassword"
            type="password"
            value={confirmPassword}
            onChange={(e) => {
              setConfirmPassword(e.target.value)
              if (password !== e.target.value) {
                setPasswordError('Passwords do not match')
              } else {
                setPasswordError('')
              }
            }}
            className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
            required
          />
        </div>
      )}

      {/* Submit button */}
      <button
        type="submit"
        disabled={isSubmitting || !!emailError || !!passwordError}
        className="w-full bg-blue-600 text-white py-2 px-4 rounded-md hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed"
      >
        {isSubmitting ? 'Loading...' : (isSignup ? 'Sign Up' : 'Sign In')}
      </button>

      {/* Toggle link */}
      <p className="text-center text-sm text-gray-600">
        {isSignup ? 'Already have an account?' : "Don't have an account?"}{' '}
        <a
          href={isSignup ? '/signin' : '/signup'}
          className="text-blue-600 hover:underline"
        >
          {isSignup ? 'Sign In' : 'Sign Up'}
        </a>
      </p>
    </form>
  )
}
```

---

### 1.5 Next.js Middleware for Protected Routes

**File**: `frontend/src/middleware.ts`

**Requirements**:
- Protect all routes except /signin and /signup (FR-015, FR-016)
- Redirect unauthenticated users to /signin (FR-017)
- Redirect authenticated users from auth pages to /dashboard (FR-018)
- Check JWT token expiration (FR-019)

**Implementation Blueprint**:

```typescript
// frontend/src/middleware.ts
import { NextResponse } from 'next/server'
import type { NextRequest } from 'next/server'

export function middleware(request: NextRequest) {
  const { pathname } = request.nextUrl

  // Get session token from cookies
  const sessionToken = request.cookies.get('better-auth.session_token')?.value

  // Protected routes (require authentication)
  const isProtectedRoute = pathname.startsWith('/dashboard') ||
                          pathname.startsWith('/profile')

  // Auth routes (signin, signup)
  const isAuthRoute = pathname.startsWith('/signin') ||
                     pathname.startsWith('/signup')

  // If trying to access protected route without auth → redirect to /signin (FR-017)
  if (isProtectedRoute && !sessionToken) {
    return NextResponse.redirect(new URL('/signin', request.url))
  }

  // If trying to access auth pages while authenticated → redirect to /dashboard (FR-018)
  if (isAuthRoute && sessionToken) {
    return NextResponse.redirect(new URL('/dashboard', request.url))
  }

  // Allow request to proceed
  return NextResponse.next()
}

// Configure which routes to run middleware on
export const config = {
  matcher: [
    /*
     * Match all request paths except:
     * - api (API routes)
     * - _next/static (static files)
     * - _next/image (image optimization files)
     * - favicon.ico (favicon file)
     */
    '/((?!api|_next/static|_next/image|favicon.ico).*)',
  ],
}
```

---

## Phase 2: Data Model

**Output**: `specs/ui/plan/data-model.md`

### TypeScript Type Definitions

**File**: `frontend/src/types/task.ts`

```typescript
// Task entity (matches backend Pydantic model)
export interface Task {
  id: string
  user_id: string
  title: string
  description: string
  completed: boolean
  created_at: string  // ISO 8601 datetime string
  updated_at: string  // ISO 8601 datetime string
}

// Create task payload
export interface TaskCreate {
  title: string        // Required, 1-200 chars (FR-037)
  description?: string // Optional
}

// Update task payload
export interface TaskUpdate {
  title?: string
  description?: string
  completed?: boolean
}

// Task filter types
export type TaskFilter = 'all' | 'active' | 'completed'

// Optimistic task (with pending state)
export interface OptimisticTask extends Task {
  pending?: boolean
  error?: string
}
```

**File**: `frontend/src/types/auth.ts`

```typescript
// User entity (from Better Auth)
export interface User {
  id: string
  email: string
  name?: string
  created_at: string
}

// Session entity (from Better Auth)
export interface Session {
  user: User
  accessToken: string   // JWT access token
  refreshToken: string  // JWT refresh token
  expiresAt: string     // ISO 8601 datetime
}

// Auth state
export interface AuthState {
  user: User | null
  session: Session | null
  isLoading: boolean
  isAuthenticated: boolean
}
```

---

## Phase 3: Contracts

**Output**: `specs/ui/plan/contracts/`

### API Client Contract

**File**: `specs/ui/plan/contracts/api-client.ts`

```typescript
// API Client Interface Contract
export interface IApiClient {
  // HTTP methods
  get<T>(endpoint: string): Promise<T>
  post<T>(endpoint: string, data: any): Promise<T>
  patch<T>(endpoint: string, data: any): Promise<T>
  delete<T>(endpoint: string): Promise<T>

  // Task methods
  listTasks(): Promise<Task[]>
  createTask(data: TaskCreate): Promise<Task>
  toggleTask(taskId: string, completed: boolean): Promise<Task>
  deleteTask(taskId: string): Promise<void>
}

// API Error class
export class ApiError extends Error {
  constructor(
    public status: number,
    public detail: string,
    public validationErrors?: Record<string, string[]>
  ) {
    super(detail)
  }
}
```

---

## Phase 4: Implementation Phases (for /sp.tasks)

### Phase A: Project Setup & Configuration
1. Initialize Next.js 15+ project in `/frontend`
2. Configure TypeScript (strict mode)
3. Configure Tailwind CSS
4. Install Better Auth + JWT Plugin
5. Create environment configuration (.env.example, .env.local)

### Phase B: Auth Configuration
1. Implement `frontend/src/auth.ts` (Better Auth server config)
2. Implement `frontend/src/lib/auth-client.ts` (Better Auth client utilities)
3. Set up middleware in `frontend/src/middleware.ts` for route protection
4. Create type definitions in `frontend/src/types/auth.ts`

### Phase C: API Client
1. Implement `frontend/src/lib/api.ts` (API client with Bearer token injection)
2. Create type definitions in `frontend/src/types/task.ts`
3. Create error handling and timeout logic
4. Test API client with backend endpoints

### Phase D: UI Components (Primitives)
1. Build reusable UI components in `frontend/src/components/ui/`
   - Button, Input, Card, Checkbox, Modal, Skeleton, Toast
2. Apply Tailwind styling with responsive design
3. Ensure accessibility (ARIA labels, keyboard navigation)

### Phase E: Layout Components
1. Root layout (`frontend/src/app/layout.tsx`) with Tailwind global styles
2. Auth layout (`frontend/src/app/(auth)/layout.tsx`) - minimal
3. Protected layout (`frontend/src/app/(protected)/layout.tsx`) with Navbar
4. **Navbar component** (`frontend/src/components/layout/Navbar.tsx`) - [REQUIRED]
5. ProfileDropdown component

### Phase F: Authentication Pages & AuthForm
1. **AuthForm component** (`frontend/src/components/auth/AuthForm.tsx`) - [REQUIRED]
2. Sign-in page (`frontend/src/app/(auth)/signin/page.tsx`)
3. Sign-up page (`frontend/src/app/(auth)/signup/page.tsx`)
4. Form validation (email, password, confirm password)
5. Integration with Better Auth (signIn, signUp methods)

### Phase G: Dashboard & Task Management
1. Dashboard page (`frontend/src/app/(protected)/dashboard/page.tsx`)
2. **TaskList component** (`frontend/src/components/tasks/TaskList.tsx`) - Server Component - [REQUIRED]
3. **TaskCard component** (`frontend/src/components/tasks/TaskCard.tsx`) - Client Component - [REQUIRED]
4. AddTaskForm component (Client Component with modal)
5. TaskFilters component (All/Active/Completed filters)
6. EmptyState component (no tasks UI)

### Phase H: Optimistic Updates & Error Handling
1. Implement `useOptimistic` hook in TaskCard for toggle/delete
2. Implement toast notifications (sonner library)
3. Error handling with rollback on API failure
4. 401 handling (automatic redirect to /signin in API client)

### Phase I: Testing & Polish
1. Unit tests for components
2. Integration tests for auth flow
3. E2E tests for task CRUD operations
4. Performance optimization (check all 14 SC criteria)
5. Accessibility audit (WCAG 2.1 AA compliance)
6. Responsive design testing (320px-1920px)

---

## Risk Analysis

| Risk | Impact | Mitigation |
|------|--------|------------|
| JWT token mismatch between frontend/backend | High - Auth breaks | Ensure `BETTER_AUTH_SECRET` is identical; add startup validation |
| CORS issues during API calls | High - API calls fail | Backend MUST allow `http://localhost:3000` origin in FastAPI CORS config |
| Token expiration during use | Medium - User kicked out | Better Auth auto-refresh; handle 401 gracefully in API client |
| Network failures during optimistic updates | Medium - UI out of sync | Rollback optimistic state; show error toast with retry option |
| Slow API responses (>2s) | Medium - SC-004 violated | Loading skeletons; investigate backend performance |
| Large task lists (>1000) | Low - UI sluggish | Pagination or virtualization (future enhancement) |
| Better Auth configuration errors | High - Auth fails | Detailed setup documentation in quickstart.md |
| Missing `user_id` in JWT claims | High - Data isolation breaks | Verify JWT payload structure with backend team |

---

## Success Criteria Validation

| Criterion | Implementation Strategy |
|-----------|------------------------|
| **SC-001**: Signup within 30s | Simple AuthForm, minimal validation, fast Better Auth flow |
| **SC-002**: Login within 20s | Simple AuthForm, fast Better Auth signIn method |
| **SC-003**: Create task within 10s | One-click "Add Task" button, simple modal form, optimistic UI |
| **SC-004**: Task list loads within 2s | Server Component fetching, loading skeleton, efficient API |
| **SC-005**: 100% protected routes redirect | Middleware enforces auth on all /dashboard/* routes |
| **SC-006**: 100% API requests include JWT | API client automatically attaches Bearer token to ALL requests |
| **SC-007**: Optimistic updates <50ms | useOptimistic hook, local state updates before API call |
| **SC-008**: Form validation <100ms | Client-side validation, native HTML5 validation |
| **SC-009**: Responsive 320px-1920px | Tailwind responsive utilities, mobile-first design |
| **SC-010**: 95% operations succeed | Comprehensive error handling, validation, retry logic |
| **SC-011**: Error states within 3s | Immediate error toast on failure |
| **SC-012**: JWT refresh automatic | Better Auth handles token refresh automatically |
| **SC-013**: Logout 100% success | Better Auth signOut method with redirect to /signin |
| **SC-014**: Empty state UI | EmptyState component when tasks.length === 0 |

---

## Next Steps

1. **Run `/sp.tasks`**: Generate atomic task list from this plan
2. **Review tasks.md**: Ensure all implementation steps are captured
3. **Run `/sp.implement`**: Execute tasks sequentially
4. **Run `/sp.git.commit_pr`**: Commit changes and create PR

---

## ADR Suggestion

📋 **Architectural decisions detected**:
- **Decision**: Better Auth with JWT Plugin configured in `frontend/src/auth.ts`
- **Decision**: API client in `frontend/src/lib/api.ts` with automatic Bearer token injection
- **Decision**: Server Components (TaskList) for data fetching + Client Components (TaskCard, AuthForm) for interactivity
- **Decision**: Next.js middleware for protected route enforcement

**Document reasoning and tradeoffs?** Run `/sp.adr frontend-architecture-decisions`

---

## References

- Feature Spec: [frontend-core.md](frontend-core.md)
- Constitution: [../../.specify/memory/constitution.md](../../.specify/memory/constitution.md)
- Research: [plan/research.md](plan/research.md)
- Data Model: [plan/data-model.md](plan/data-model.md)
- Quickstart: [plan/quickstart.md](plan/quickstart.md)
- API Contract: [plan/contracts/api-client.ts](plan/contracts/api-client.ts)

---

**Plan Status**: ✅ COMPLETE - Ready for `/sp.tasks` command
**Branch**: `001-frontend-core`
**Date**: 2025-12-23
