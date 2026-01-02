# Research: Phase II Frontend UI Core

**Date**: 2025-12-23
**Feature**: Frontend UI Core
**Branch**: `002-frontend-ui-core`
**User Requirements**: Design Next.js monorepo structure in /frontend with Auth Setup (Better Auth + JWT), API Client (lib/api.ts with Bearer token), Layout (Root layout + Navbar), and Pages (Sign-in, Sign-up, Dashboard)

## Research Topics

This document consolidates research findings for all technical decisions required by the frontend implementation.

---

## 1. Better Auth Configuration with JWT Plugin

### Decision: Better Auth with JWT Plugin + Session Strategy

**Rationale**: Better Auth is the Constitution-mandated authentication library. The JWT plugin enables token-based auth that integrates with our FastAPI backend via the JWT Bridge pattern.

**Key Configuration**:
- Enable JWT plugin for token generation
- Configure `BETTER_AUTH_SECRET` (shared with backend)
- Use secure httpOnly cookies for token storage in production
- Implement token refresh before expiration

**Implementation Pattern**:
```typescript
// lib/auth.ts - Server-side configuration
import { betterAuth } from "better-auth";
import { jwt } from "better-auth/plugins";

export const auth = betterAuth({
  secret: process.env.BETTER_AUTH_SECRET!,
  plugins: [jwt()],
  // ... database adapter config
});

// lib/auth-client.ts - Client-side
import { createAuthClient } from "better-auth/react";

export const authClient = createAuthClient({
  baseURL: process.env.NEXT_PUBLIC_AUTH_URL,
});
```

---

## 2. API Client with JWT Token Injection

### Decision: Custom Fetch Wrapper with Token Injection

**Rationale**: Per Constitution, EVERY API request to the backend MUST include `Authorization: Bearer <token>`. A centralized API client ensures consistent header attachment and error handling.

**Implementation Pattern**:
```typescript
// lib/api.ts
class ApiClient {
  private baseUrl: string;

  constructor() {
    this.baseUrl = process.env.NEXT_PUBLIC_API_URL!;
  }

  async fetch<T>(path: string, options: RequestInit = {}): Promise<T> {
    const session = await getSession(); // From Better Auth

    const response = await fetch(`${this.baseUrl}${path}`, {
      ...options,
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${session?.token}`, // JWT Bridge
        ...options.headers,
      },
    });

    if (!response.ok) {
      throw new ApiError(response.status, await response.json());
    }

    return response.json();
  }

  // CRUD methods
  get<T>(path: string) { return this.fetch<T>(path); }
  post<T>(path: string, body: unknown) { /* ... */ }
  patch<T>(path: string, body: unknown) { /* ... */ }
  delete<T>(path: string) { /* ... */ }
}
```

**Alternatives Considered**:

| Approach | Pros | Cons | Rejected Because |
|----------|------|------|------------------|
| Axios with interceptors | Popular, rich features | Extra dependency | Fetch is built-in, simpler |
| TanStack Query | Caching, deduplication | More complex setup | Over-engineering for MVP |
| Custom fetch wrapper | Simple, no deps, full control | Manual implementation | Best fit - chosen |

---

## 3. Next.js App Router Structure

### Decision: App Router with Route Groups

**Rationale**: Constitution mandates Next.js 15+ with App Router. Route groups organize auth pages vs. protected dashboard cleanly.

**Final Structure**:
```
frontend/src/app/
├── (auth)/
│   ├── signin/page.tsx      # Login page
│   ├── signup/page.tsx      # Registration page
│   └── layout.tsx           # Auth pages layout (minimal)
├── (dashboard)/
│   ├── page.tsx             # Main task list
│   ├── layout.tsx           # Dashboard layout (with navbar, sidebar)
│   └── loading.tsx          # Loading skeleton
├── layout.tsx               # Root layout
├── page.tsx                 # Landing/redirect
└── globals.css              # Tailwind imports
```

**Route Protection**:
- Middleware at `middleware.ts` checks auth status
- Unauthenticated users → redirect to `/signin`
- Authenticated users accessing `/signin` → redirect to dashboard

---

## 4. Component Architecture

### Decision: Feature-Based Component Organization

**Rationale**: Group components by feature for cohesion. Common UI components in `components/ui/`.

**Structure**:
```
frontend/src/components/
├── ui/                      # Reusable UI primitives
│   ├── Button.tsx
│   ├── Input.tsx
│   ├── Card.tsx
│   ├── Skeleton.tsx
│   └── Modal.tsx
├── layout/
│   ├── Navbar.tsx           # Top navigation with user info
│   ├── Sidebar.tsx          # Filter sidebar
│   └── MainContent.tsx      # Content wrapper
├── tasks/
│   ├── TaskList.tsx         # Task list container
│   ├── TaskCard.tsx         # Individual task display
│   ├── TaskForm.tsx         # Create/edit form
│   └── TaskFilters.tsx      # Filter controls
└── auth/
    ├── LoginForm.tsx
    ├── SignupForm.tsx
    └── LogoutButton.tsx
```

---

## 5. State Management Strategy

### Decision: React useState + useOptimistic for Local State

**Rationale**: The app is primarily server-driven (data from API). Local state is limited to:
- Current filter selection
- Optimistic UI updates
- Form state

No global state management (Redux, Zustand) needed.

**Optimistic Updates Pattern**:
```typescript
// Using React 19's useOptimistic
const [optimisticTasks, addOptimisticTask] = useOptimistic(
  tasks,
  (state, newTask) => [...state, { ...newTask, pending: true }]
);

async function createTask(data: TaskCreate) {
  addOptimisticTask({ id: 'temp', ...data });
  const created = await api.tasks.create(data);
  // Server response replaces optimistic task
}
```

**Filter State**:
```typescript
type Filter = 'all' | 'active' | 'completed';
const [filter, setFilter] = useState<Filter>('all');

const filteredTasks = useMemo(() => {
  switch (filter) {
    case 'active': return tasks.filter(t => !t.completed);
    case 'completed': return tasks.filter(t => t.completed);
    default: return tasks;
  }
}, [tasks, filter]);
```

---

## 6. Styling Approach

### Decision: Tailwind CSS Utility-First

**Rationale**: Constitution mandates Tailwind CSS. Utility-first provides:
- Fast prototyping
- Consistent spacing/colors
- No CSS file management
- Good IDE support

**Configuration**:
- Use `tailwind.config.ts` for theme customization
- Define color palette for consistency
- Mobile-first responsive design

**Example Patterns**:
```tsx
// Task Card
<div className="bg-white rounded-lg shadow p-4 hover:shadow-md transition-shadow">
  <h3 className="text-lg font-medium text-gray-900">{title}</h3>
  <p className="text-sm text-gray-500 line-clamp-2">{description}</p>
</div>

// Responsive layout
<div className="grid grid-cols-1 md:grid-cols-4 gap-4">
  <aside className="md:col-span-1">Sidebar</aside>
  <main className="md:col-span-3">Tasks</main>
</div>
```

---

## 7. Form Handling and Validation

### Decision: Native HTML Forms + Server Actions

**Rationale**: Next.js App Router supports Server Actions for form submission. Client-side validation with native HTML5 validation + custom validation.

**Validation Rules**:
- Title: required, 1-200 characters
- Description: optional, max 2000 characters
- Email: required, valid email format
- Password: required, min 8 characters

**Pattern**:
```tsx
// TaskForm.tsx
function TaskForm({ onSubmit }: Props) {
  const [error, setError] = useState<string | null>(null);

  async function handleSubmit(formData: FormData) {
    const title = formData.get('title') as string;

    // Client validation
    if (!title || title.length > 200) {
      setError('Title must be 1-200 characters');
      return;
    }

    try {
      await onSubmit({ title, description: formData.get('description') });
    } catch (e) {
      setError('Failed to create task');
    }
  }

  return (
    <form action={handleSubmit}>
      <input name="title" required maxLength={200} />
      {error && <span className="text-red-500">{error}</span>}
    </form>
  );
}
```

---

## Summary of Technology Decisions

| Decision Area | Choice | Key Reason |
|--------------|--------|------------|
| Auth Library | Better Auth + JWT | Constitution mandate |
| API Client | Custom fetch wrapper | Simple, full control, no deps |
| Routing | App Router with route groups | Next.js 15+ standard |
| Components | Feature-based organization | Cohesion and maintainability |
| State | useState + useOptimistic | Simple, server-driven app |
| Styling | Tailwind CSS utility-first | Constitution mandate |
| Forms | Native + Server Actions | Next.js standard, simple |
