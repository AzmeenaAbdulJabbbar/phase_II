# API Client Contract: Frontend to Backend

**Date**: 2025-12-21
**Feature**: Frontend UI Core
**Branch**: `002-frontend-ui-core`

## Overview

This document defines the API client interface that the frontend uses to communicate with the FastAPI backend. All requests include JWT authentication via the Bearer token.

---

## 1. Base Configuration

```typescript
// lib/api.ts

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

interface RequestConfig extends RequestInit {
  skipAuth?: boolean;  // For endpoints that don't require auth (health check)
}
```

---

## 2. API Client Interface

```typescript
// lib/api.ts

export interface ApiClient {
  // Health check (no auth required)
  health(): Promise<{ status: string }>;

  // Task operations (all require auth)
  tasks: {
    list(): Promise<ApiSuccessResponse<Task[]>>;
    get(id: string): Promise<ApiSuccessResponse<Task>>;
    create(data: TaskCreate): Promise<ApiSuccessResponse<Task>>;
    update(id: string, data: TaskUpdate): Promise<ApiSuccessResponse<Task>>;
    delete(id: string): Promise<void>;
  };
}
```

---

## 3. Endpoint Specifications

### Health Check

```
GET /api/health

Response 200:
{
  "status": "healthy"
}

No authentication required.
```

### List Tasks

```
GET /api/tasks/

Headers:
  Authorization: Bearer <jwt_token>

Response 200:
{
  "data": [
    {
      "id": "uuid",
      "user_id": "uuid",
      "title": "string",
      "description": "string | null",
      "completed": false,
      "created_at": "2025-12-21T10:00:00Z",
      "updated_at": "2025-12-21T10:00:00Z"
    }
  ],
  "meta": {
    "timestamp": "2025-12-21T10:00:00Z",
    "request_id": "uuid",
    "total": 5
  }
}

Response 401 (no token / invalid token):
{
  "error": {
    "code": "UNAUTHORIZED",
    "message": "Invalid token"
  },
  "meta": { ... }
}
```

### Get Single Task

```
GET /api/tasks/{task_id}

Headers:
  Authorization: Bearer <jwt_token>

Response 200:
{
  "data": {
    "id": "uuid",
    "user_id": "uuid",
    "title": "string",
    "description": "string | null",
    "completed": false,
    "created_at": "2025-12-21T10:00:00Z",
    "updated_at": "2025-12-21T10:00:00Z"
  },
  "meta": { ... }
}

Response 403 (not owner):
{
  "error": {
    "code": "FORBIDDEN",
    "message": "Access denied"
  },
  "meta": { ... }
}

Response 404 (not found):
{
  "error": {
    "code": "NOT_FOUND",
    "message": "Task not found: {task_id}"
  },
  "meta": { ... }
}
```

### Create Task

```
POST /api/tasks/

Headers:
  Authorization: Bearer <jwt_token>
  Content-Type: application/json

Body:
{
  "title": "string (1-255 chars, required)",
  "description": "string (max 2000 chars, optional)"
}

Response 201:
{
  "data": {
    "id": "uuid",
    "user_id": "uuid",  // Auto-assigned from JWT
    "title": "string",
    "description": "string | null",
    "completed": false,
    "created_at": "2025-12-21T10:00:00Z",
    "updated_at": "2025-12-21T10:00:00Z"
  },
  "meta": { ... }
}

Response 422 (validation error):
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid request body",
    "details": {
      "title": "Title is required"
    }
  },
  "meta": { ... }
}
```

### Update Task

```
PATCH /api/tasks/{task_id}

Headers:
  Authorization: Bearer <jwt_token>
  Content-Type: application/json

Body (all fields optional):
{
  "title": "string",
  "description": "string | null",
  "completed": true
}

Response 200:
{
  "data": { ... updated task ... },
  "meta": { ... }
}

Response 403 (not owner): { ... }
Response 404 (not found): { ... }
Response 422 (validation error): { ... }
```

### Delete Task

```
DELETE /api/tasks/{task_id}

Headers:
  Authorization: Bearer <jwt_token>

Response 204: No content

Response 403 (not owner): { ... }
Response 404 (not found): { ... }
```

---

## 4. Error Handling Contract

### Error Codes

| HTTP Status | Error Code        | Scenario                           |
|-------------|-------------------|-----------------------------------|
| 401         | `UNAUTHORIZED`    | Missing/invalid/expired token      |
| 403         | `FORBIDDEN`       | User doesn't own the resource      |
| 404         | `NOT_FOUND`       | Resource doesn't exist             |
| 422         | `VALIDATION_ERROR`| Invalid request payload            |
| 500         | `INTERNAL_ERROR`  | Server error                       |
| 503         | `SERVICE_UNAVAILABLE` | Database connection failed     |

### Client-Side Error Handling

```typescript
// lib/api.ts

export class ApiError extends Error {
  constructor(
    public status: number,
    public code: string,
    public message: string,
    public details?: Record<string, unknown>
  ) {
    super(message);
    this.name = 'ApiError';
  }

  static isUnauthorized(error: unknown): boolean {
    return error instanceof ApiError && error.status === 401;
  }

  static isForbidden(error: unknown): boolean {
    return error instanceof ApiError && error.status === 403;
  }

  static isNotFound(error: unknown): boolean {
    return error instanceof ApiError && error.status === 404;
  }

  static isValidationError(error: unknown): boolean {
    return error instanceof ApiError && error.status === 422;
  }
}
```

---

## 5. Token Injection Contract

**CRITICAL (Constitution Mandate)**: Every request to `/api/*` (except `/api/health`) MUST include the Authorization header.

```typescript
// lib/api.ts

async function fetchWithAuth<T>(
  path: string,
  options: RequestConfig = {}
): Promise<T> {
  const { skipAuth = false, ...fetchOptions } = options;

  const headers: HeadersInit = {
    'Content-Type': 'application/json',
    ...fetchOptions.headers,
  };

  // MANDATORY: Attach Bearer token
  if (!skipAuth) {
    const session = await getSession(); // From Better Auth
    if (!session?.token) {
      throw new ApiError(401, 'UNAUTHORIZED', 'Not authenticated');
    }
    headers['Authorization'] = `Bearer ${session.token}`;
  }

  const response = await fetch(`${API_BASE_URL}${path}`, {
    ...fetchOptions,
    headers,
  });

  if (!response.ok) {
    const errorBody = await response.json();
    throw new ApiError(
      response.status,
      errorBody.error?.code || 'UNKNOWN',
      errorBody.error?.message || 'Request failed',
      errorBody.error?.details
    );
  }

  // Handle 204 No Content
  if (response.status === 204) {
    return undefined as T;
  }

  return response.json();
}
```

---

## 6. Full API Client Implementation

```typescript
// lib/api.ts

export const api: ApiClient = {
  async health() {
    return fetchWithAuth('/api/health', { skipAuth: true });
  },

  tasks: {
    async list() {
      return fetchWithAuth<ApiSuccessResponse<Task[]>>('/api/tasks/');
    },

    async get(id: string) {
      return fetchWithAuth<ApiSuccessResponse<Task>>(`/api/tasks/${id}`);
    },

    async create(data: TaskCreate) {
      return fetchWithAuth<ApiSuccessResponse<Task>>('/api/tasks/', {
        method: 'POST',
        body: JSON.stringify(data),
      });
    },

    async update(id: string, data: TaskUpdate) {
      return fetchWithAuth<ApiSuccessResponse<Task>>(`/api/tasks/${id}`, {
        method: 'PATCH',
        body: JSON.stringify(data),
      });
    },

    async delete(id: string) {
      return fetchWithAuth<void>(`/api/tasks/${id}`, {
        method: 'DELETE',
      });
    },
  },
};
```

---

## 7. Usage Examples

### In a React Component

```typescript
// components/tasks/TaskList.tsx
'use client';

import { useEffect, useState } from 'react';
import { api, ApiError } from '@/lib/api';
import { Task } from '@/types/task';

export function TaskList() {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function loadTasks() {
      try {
        const response = await api.tasks.list();
        setTasks(response.data);
      } catch (e) {
        if (ApiError.isUnauthorized(e)) {
          // Redirect to login
        } else {
          setError('Failed to load tasks');
        }
      }
    }
    loadTasks();
  }, []);

  // ... render
}
```

### Creating a Task with Optimistic Update

```typescript
async function handleCreateTask(data: TaskCreate) {
  // Optimistic update
  const tempId = `temp-${Date.now()}`;
  const optimisticTask: OptimisticTask = {
    id: tempId,
    user_id: session.userId,
    title: data.title,
    description: data.description || null,
    completed: false,
    created_at: new Date().toISOString(),
    updated_at: new Date().toISOString(),
    _pending: true,
    _tempId: tempId,
  };

  setTasks(prev => [...prev, optimisticTask]);

  try {
    const response = await api.tasks.create(data);
    // Replace optimistic task with real one
    setTasks(prev => prev.map(t =>
      t.id === tempId ? response.data : t
    ));
  } catch (e) {
    // Remove optimistic task on failure
    setTasks(prev => prev.filter(t => t.id !== tempId));
    throw e;
  }
}
```
