# Data Model: Phase II Frontend UI Core

**Date**: 2025-12-21
**Feature**: Frontend UI Core
**Branch**: `002-frontend-ui-core`

## Overview

This document defines the frontend data models (TypeScript types/interfaces) that map to the backend API and manage local state.

---

## 1. Core Domain Types

### Task Entity (from Backend API)

```typescript
// types/task.ts

/**
 * Task entity as returned from the backend API.
 * Maps to backend's TaskRead schema.
 */
export interface Task {
  id: string;           // UUID as string
  user_id: string;      // UUID as string (owner)
  title: string;        // 1-255 characters
  description: string | null;  // max 2000 characters
  completed: boolean;
  created_at: string;   // ISO8601 timestamp
  updated_at: string;   // ISO8601 timestamp
}

/**
 * Payload for creating a new task.
 * Maps to backend's TaskCreate schema.
 */
export interface TaskCreate {
  title: string;        // Required, 1-255 chars
  description?: string; // Optional, max 2000 chars
}

/**
 * Payload for updating an existing task.
 * Maps to backend's TaskUpdate schema.
 * All fields optional - only include what changes.
 */
export interface TaskUpdate {
  title?: string;
  description?: string | null;
  completed?: boolean;
}

/**
 * Task with optimistic update metadata.
 * Used for UI state during pending operations.
 */
export interface OptimisticTask extends Task {
  _pending?: boolean;    // True while awaiting server confirmation
  _tempId?: string;      // Temporary ID for new tasks
  _error?: string;       // Error message if operation failed
}
```

---

## 2. API Response Types

### Standard Response Envelope

```typescript
// types/api.ts

/**
 * Metadata included in all API responses.
 */
export interface ResponseMeta {
  timestamp: string;    // ISO8601
  request_id: string;   // UUID
  total?: number;       // Present in list responses
}

/**
 * Success response envelope.
 */
export interface ApiSuccessResponse<T> {
  data: T;
  meta: ResponseMeta;
}

/**
 * Error detail structure.
 */
export interface ApiErrorDetail {
  code: string;
  message: string;
  details?: Record<string, unknown>;
}

/**
 * Error response envelope.
 */
export interface ApiErrorResponse {
  error: ApiErrorDetail;
  meta: ResponseMeta;
}

/**
 * Union type for any API response.
 */
export type ApiResponse<T> = ApiSuccessResponse<T> | ApiErrorResponse;

/**
 * Type guard to check if response is an error.
 */
export function isApiError<T>(response: ApiResponse<T>): response is ApiErrorResponse {
  return 'error' in response;
}
```

---

## 3. Authentication Types

### Session and User

```typescript
// types/auth.ts

/**
 * User information from Better Auth session.
 */
export interface User {
  id: string;           // UUID
  email: string;
  name?: string;
  image?: string;       // Avatar URL
  emailVerified: boolean;
  createdAt: string;    // ISO8601
  updatedAt: string;    // ISO8601
}

/**
 * Session information from Better Auth.
 */
export interface Session {
  id: string;
  userId: string;
  token: string;        // JWT for API calls
  expiresAt: string;    // ISO8601
}

/**
 * Combined auth state.
 */
export interface AuthState {
  user: User | null;
  session: Session | null;
  isLoading: boolean;
  isAuthenticated: boolean;
}

/**
 * Credentials for email/password sign-in.
 */
export interface SignInCredentials {
  email: string;
  password: string;
}

/**
 * Data for new user registration.
 */
export interface SignUpData {
  email: string;
  password: string;
  name?: string;
}
```

---

## 4. UI State Types

### Filter State

```typescript
// types/ui.ts

/**
 * Task filter options.
 */
export type TaskFilter = 'all' | 'active' | 'completed';

/**
 * Sort options for task list.
 */
export type TaskSort = 'created_at' | 'updated_at' | 'title';

/**
 * Sort direction.
 */
export type SortDirection = 'asc' | 'desc';

/**
 * Complete filter/sort state for task list.
 */
export interface TaskListState {
  filter: TaskFilter;
  sort: TaskSort;
  direction: SortDirection;
  searchQuery: string;
}

/**
 * UI loading states for different operations.
 */
export interface LoadingState {
  tasks: boolean;       // Loading task list
  create: boolean;      // Creating new task
  update: string | null; // Task ID being updated, or null
  delete: string | null; // Task ID being deleted, or null
}
```

### Modal State

```typescript
// types/ui.ts (continued)

/**
 * Modal types in the application.
 */
export type ModalType = 'create-task' | 'edit-task' | 'delete-confirm' | null;

/**
 * Modal state with context data.
 */
export interface ModalState {
  type: ModalType;
  taskId?: string;      // For edit/delete modals
}
```

---

## 5. Form State Types

### Task Form

```typescript
// types/forms.ts

/**
 * Form state for task creation/editing.
 */
export interface TaskFormState {
  title: string;
  description: string;
  errors: TaskFormErrors;
  isSubmitting: boolean;
}

/**
 * Validation errors for task form.
 */
export interface TaskFormErrors {
  title?: string;
  description?: string;
  general?: string;     // Non-field-specific errors
}

/**
 * Form state for authentication forms.
 */
export interface AuthFormState {
  email: string;
  password: string;
  name?: string;        // For sign-up only
  errors: AuthFormErrors;
  isSubmitting: boolean;
}

/**
 * Validation errors for auth forms.
 */
export interface AuthFormErrors {
  email?: string;
  password?: string;
  name?: string;
  general?: string;
}
```

---

## 6. Type Relationships Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                      Frontend Types                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Auth Layer                    API Layer                         │
│  ┌─────────────┐              ┌──────────────────┐              │
│  │    User     │              │ ApiSuccessResponse│              │
│  │   Session   │◄─────────────│ ApiErrorResponse │              │
│  │  AuthState  │              │   ResponseMeta   │              │
│  └─────────────┘              └──────────────────┘              │
│         │                              │                         │
│         │                              │                         │
│         ▼                              ▼                         │
│  ┌─────────────────────────────────────────────────┐            │
│  │                 Domain Layer                     │            │
│  │  ┌──────────┐  ┌────────────┐  ┌────────────┐  │            │
│  │  │   Task   │  │ TaskCreate │  │ TaskUpdate │  │            │
│  │  └──────────┘  └────────────┘  └────────────┘  │            │
│  │        │                                        │            │
│  │        ▼                                        │            │
│  │  ┌──────────────┐                              │            │
│  │  │OptimisticTask│ (extends Task + pending)     │            │
│  │  └──────────────┘                              │            │
│  └─────────────────────────────────────────────────┘            │
│         │                                                        │
│         ▼                                                        │
│  ┌─────────────────────────────────────────────────┐            │
│  │                   UI Layer                       │            │
│  │  ┌─────────────┐  ┌─────────────┐               │            │
│  │  │TaskListState│  │ LoadingState│               │            │
│  │  │  ModalState │  │  FormState  │               │            │
│  │  └─────────────┘  └─────────────┘               │            │
│  └─────────────────────────────────────────────────┘            │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 7. Backend ↔ Frontend Type Mapping

| Backend (Python)    | Frontend (TypeScript) | Notes                          |
|--------------------|-----------------------|--------------------------------|
| `Task` (SQLModel)  | `Task`                | UUID fields as strings         |
| `TaskCreate`       | `TaskCreate`          | Direct mapping                 |
| `TaskUpdate`       | `TaskUpdate`          | All fields optional            |
| `TaskRead`         | `Task`                | Serialized from model          |
| `success_response` | `ApiSuccessResponse`  | `{data, meta}` envelope        |
| `error_response`   | `ApiErrorResponse`    | `{error, meta}` envelope       |

---

## 8. Validation Rules (Client-Side)

| Field       | Rule                                      | Error Message                        |
|-------------|-------------------------------------------|--------------------------------------|
| `title`     | Required, 1-255 chars                     | "Title is required (1-255 chars)"    |
| `description` | Optional, max 2000 chars                | "Description too long (max 2000)"    |
| `email`     | Required, valid email format              | "Valid email required"               |
| `password`  | Required, min 8 chars                     | "Password min 8 characters"          |
| `name`      | Optional, max 100 chars                   | "Name too long (max 100)"            |

---

## Summary

This data model provides:
- **Type safety** for all API interactions
- **Optimistic update support** with pending states
- **Clear separation** between API types and UI state types
- **Form validation** types for error handling
- **Direct mapping** to backend schemas for consistency
