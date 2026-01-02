# Frontend Agent Rules (Next.js 16+ / Better Auth)

This file provides frontend-specific patterns and conventions for AI agents working in the `/frontend` directory.

**Stack**: Next.js 16+ (App Router) | TypeScript (strict) | Tailwind CSS | Better Auth (JWT Plugin)

## Constitution Reference

All work MUST comply with the root constitution at `.specify/memory/constitution.md`. Key principles:
- Spec-Driven Development: Read specs before implementation
- Security: JWT tokens attached to every API request
- Data Isolation: User data filtering handled by backend

## Directory Structure

```text
frontend/
├── src/
│   ├── app/                 # App Router pages and layouts
│   │   ├── (auth)/          # Auth-related routes (login, register)
│   │   ├── (dashboard)/     # Protected dashboard routes
│   │   ├── api/             # API route handlers (Better Auth)
│   │   ├── layout.tsx       # Root layout
│   │   └── page.tsx         # Home page
│   ├── components/          # React components
│   │   ├── ui/              # Base UI components (shadcn/ui style)
│   │   └── features/        # Feature-specific components
│   ├── lib/                 # Utilities and configuration
│   │   ├── auth.ts          # Better Auth client configuration
│   │   ├── api.ts           # API client with JWT injection
│   │   └── utils.ts         # General utilities
│   └── services/            # API service layer
│       └── tasks.ts         # Task-related API calls
├── CLAUDE.md                # This file
├── package.json
├── tailwind.config.ts
├── tsconfig.json
└── next.config.ts
```

## Technology Patterns

### Next.js App Router Conventions

```typescript
// Page component (src/app/dashboard/page.tsx)
export default async function DashboardPage() {
  // Server component by default
  return <Dashboard />
}

// Client component (must explicitly declare)
'use client'
export function InteractiveComponent() {
  const [state, setState] = useState()
  return <div>...</div>
}

// Layout (src/app/layout.tsx)
export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  )
}
```

### Better Auth Client Configuration

```typescript
// src/lib/auth.ts
import { createAuthClient } from "better-auth/react"

export const authClient = createAuthClient({
  baseURL: process.env.NEXT_PUBLIC_APP_URL,
  plugins: [
    // JWT plugin for token-based auth
  ]
})

export const { signIn, signUp, signOut, useSession } = authClient
```

### API Client with JWT Injection (CRITICAL)

```typescript
// src/lib/api.ts
import { authClient } from './auth'

const API_BASE = process.env.NEXT_PUBLIC_API_URL

export async function apiClient<T>(
  endpoint: string,
  options: RequestInit = {}
): Promise<T> {
  const session = await authClient.getSession()
  const token = session?.token

  if (!token) {
    throw new Error('No authentication token available')
  }

  const response = await fetch(`${API_BASE}${endpoint}`, {
    ...options,
    headers: {
      // MANDATORY: JWT Bridge - Authorization header required for ALL requests
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json',
      ...options.headers,
    },
  })

  if (!response.ok) {
    if (response.status === 401) {
      // Handle token expiration
      await authClient.signOut()
      throw new Error('Session expired')
    }
    throw new Error(`API Error: ${response.status}`)
  }

  return response.json()
}
```

### Service Layer Pattern

```typescript
// src/services/tasks.ts
import { apiClient } from '@/lib/api'

export interface Task {
  id: string
  title: string
  completed: boolean
  created_at: string
}

export interface CreateTaskInput {
  title: string
}

export const TaskService = {
  async list(): Promise<Task[]> {
    return apiClient<Task[]>('/tasks')
  },

  async create(input: CreateTaskInput): Promise<Task> {
    return apiClient<Task>('/tasks', {
      method: 'POST',
      body: JSON.stringify(input),
    })
  },

  async update(id: string, input: Partial<Task>): Promise<Task> {
    return apiClient<Task>(`/tasks/${id}`, {
      method: 'PATCH',
      body: JSON.stringify(input),
    })
  },

  async delete(id: string): Promise<void> {
    await apiClient(`/tasks/${id}`, { method: 'DELETE' })
  },
}
```

## Component Patterns

### UI Component Structure

```typescript
// src/components/ui/button.tsx
import { cn } from '@/lib/utils'

interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary' | 'danger'
  size?: 'sm' | 'md' | 'lg'
}

export function Button({
  className,
  variant = 'primary',
  size = 'md',
  ...props
}: ButtonProps) {
  return (
    <button
      className={cn(
        'rounded-md font-medium transition-colors',
        // Variant styles
        variant === 'primary' && 'bg-blue-600 text-white hover:bg-blue-700',
        variant === 'secondary' && 'bg-gray-200 text-gray-900 hover:bg-gray-300',
        variant === 'danger' && 'bg-red-600 text-white hover:bg-red-700',
        // Size styles
        size === 'sm' && 'px-3 py-1.5 text-sm',
        size === 'md' && 'px-4 py-2 text-base',
        size === 'lg' && 'px-6 py-3 text-lg',
        className
      )}
      {...props}
    />
  )
}
```

### Feature Component Structure

```typescript
// src/components/features/task-list.tsx
'use client'

import { useState, useEffect } from 'react'
import { TaskService, Task } from '@/services/tasks'
import { Button } from '@/components/ui/button'

export function TaskList() {
  const [tasks, setTasks] = useState<Task[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    loadTasks()
  }, [])

  async function loadTasks() {
    try {
      setLoading(true)
      const data = await TaskService.list()
      setTasks(data)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load tasks')
    } finally {
      setLoading(false)
    }
  }

  if (loading) return <div>Loading...</div>
  if (error) return <div className="text-red-600">{error}</div>

  return (
    <ul className="space-y-2">
      {tasks.map(task => (
        <li key={task.id} className="flex items-center gap-2">
          <input
            type="checkbox"
            checked={task.completed}
            onChange={() => handleToggle(task.id, !task.completed)}
          />
          <span className={task.completed ? 'line-through' : ''}>
            {task.title}
          </span>
        </li>
      ))}
    </ul>
  )
}
```

## Tailwind CSS Conventions

### Color Palette (use semantic names)

```typescript
// tailwind.config.ts
export default {
  theme: {
    extend: {
      colors: {
        primary: '#3b82f6',    // Blue
        secondary: '#6b7280',  // Gray
        success: '#22c55e',    // Green
        warning: '#f59e0b',    // Amber
        danger: '#ef4444',     // Red
      }
    }
  }
}
```

### Responsive Design

```tsx
// Mobile-first approach
<div className="
  px-4 py-2          // Base (mobile)
  md:px-6 md:py-4    // Medium screens
  lg:px-8 lg:py-6    // Large screens
">
```

## Authentication Flow

### Protected Route Pattern

```typescript
// src/app/(dashboard)/layout.tsx
import { redirect } from 'next/navigation'
import { authClient } from '@/lib/auth'

export default async function DashboardLayout({
  children,
}: {
  children: React.ReactNode
}) {
  const session = await authClient.getSession()

  if (!session) {
    redirect('/login')
  }

  return <>{children}</>
}
```

### Auth Context Provider

```typescript
// src/app/providers.tsx
'use client'

import { SessionProvider } from '@/lib/auth'

export function Providers({ children }: { children: React.ReactNode }) {
  return (
    <SessionProvider>
      {children}
    </SessionProvider>
  )
}
```

## Error Handling

### API Error Handling

```typescript
// Consistent error response handling
try {
  const data = await TaskService.create({ title })
  // Success handling
} catch (error) {
  if (error instanceof Error) {
    if (error.message === 'Session expired') {
      // Redirect to login
      router.push('/login')
    } else {
      // Show error toast/notification
      toast.error(error.message)
    }
  }
}
```

## Testing Conventions

### Component Testing

```typescript
// __tests__/components/task-list.test.tsx
import { render, screen } from '@testing-library/react'
import { TaskList } from '@/components/features/task-list'

describe('TaskList', () => {
  it('renders tasks', async () => {
    render(<TaskList />)
    // Test implementation
  })
})
```

## Security Checklist

- [ ] All API calls use `apiClient` with JWT injection
- [ ] No tokens stored in localStorage (use httpOnly cookies)
- [ ] Sensitive data not logged to console
- [ ] Environment variables prefixed with `NEXT_PUBLIC_` only for public values
- [ ] Protected routes check session before rendering

## File Naming Conventions

| Type | Convention | Example |
|------|------------|---------|
| Pages | `page.tsx` | `app/dashboard/page.tsx` |
| Layouts | `layout.tsx` | `app/(dashboard)/layout.tsx` |
| Components | `kebab-case.tsx` | `components/task-list.tsx` |
| Services | `kebab-case.ts` | `services/task-service.ts` |
| Utilities | `kebab-case.ts` | `lib/utils.ts` |
| Types | `types.ts` or inline | `lib/types.ts` |
