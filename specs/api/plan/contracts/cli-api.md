# API Contract: Phase II Backend

**Version**: 1.0.0
**Base URL**: `http://localhost:8000/api`
**Authentication**: Bearer JWT (from Better Auth)

---

## Authentication

All endpoints except `/health` require a valid JWT token in the Authorization header:

```
Authorization: Bearer <jwt_token>
```

The JWT must contain:
- `sub`: User UUID (used as `user_id`)
- `exp`: Expiration timestamp
- Signed with `BETTER_AUTH_SECRET` using HS256

---

## Response Envelope

### Success Response

```json
{
  "data": <resource or array>,
  "meta": {
    "timestamp": "2025-12-21T10:00:00Z",
    "request_id": "550e8400-e29b-41d4-a716-446655440000",
    "total": 10  // Only for list operations
  }
}
```

### Error Response

```json
{
  "error": {
    "code": "ERROR_CODE",
    "message": "Human readable message",
    "details": {}  // Optional, for validation errors
  },
  "meta": {
    "timestamp": "2025-12-21T10:00:00Z",
    "request_id": "550e8400-e29b-41d4-a716-446655440000"
  }
}
```

---

## Endpoints

### Health Check

```
GET /api/health
```

**Auth Required**: No

**Response** (200):
```json
{
  "status": "healthy",
  "timestamp": "2025-12-21T10:00:00Z"
}
```

---

### List Tasks

```
GET /api/tasks/
```

**Auth Required**: Yes

**Response** (200):
```json
{
  "data": [
    {
      "id": "550e8400-e29b-41d4-a716-446655440000",
      "user_id": "660e8400-e29b-41d4-a716-446655440000",
      "title": "Complete documentation",
      "description": "Write API docs",
      "completed": false,
      "created_at": "2025-12-21T10:00:00Z",
      "updated_at": "2025-12-21T10:00:00Z"
    }
  ],
  "meta": {
    "timestamp": "2025-12-21T10:00:00Z",
    "request_id": "770e8400-e29b-41d4-a716-446655440000",
    "total": 1
  }
}
```

**Error Responses**:
- `401`: Missing or invalid token

---

### Create Task

```
POST /api/tasks/
Content-Type: application/json
```

**Auth Required**: Yes

**Request Body**:
```json
{
  "title": "Complete documentation",
  "description": "Write API docs"  // Optional
}
```

**Response** (201):
```json
{
  "data": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "user_id": "660e8400-e29b-41d4-a716-446655440000",
    "title": "Complete documentation",
    "description": "Write API docs",
    "completed": false,
    "created_at": "2025-12-21T10:00:00Z",
    "updated_at": "2025-12-21T10:00:00Z"
  },
  "meta": {
    "timestamp": "2025-12-21T10:00:00Z",
    "request_id": "770e8400-e29b-41d4-a716-446655440000"
  }
}
```

**Error Responses**:
- `401`: Missing or invalid token
- `422`: Validation error (missing title, title too long)

---

### Get Task

```
GET /api/tasks/{task_id}
```

**Auth Required**: Yes

**Path Parameters**:
- `task_id`: UUID of the task

**Response** (200):
```json
{
  "data": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "user_id": "660e8400-e29b-41d4-a716-446655440000",
    "title": "Complete documentation",
    "description": "Write API docs",
    "completed": false,
    "created_at": "2025-12-21T10:00:00Z",
    "updated_at": "2025-12-21T10:00:00Z"
  },
  "meta": {
    "timestamp": "2025-12-21T10:00:00Z",
    "request_id": "770e8400-e29b-41d4-a716-446655440000"
  }
}
```

**Error Responses**:
- `401`: Missing or invalid token
- `403`: Task belongs to another user
- `404`: Task not found
- `422`: Invalid UUID format

---

### Update Task

```
PATCH /api/tasks/{task_id}
Content-Type: application/json
```

**Auth Required**: Yes

**Path Parameters**:
- `task_id`: UUID of the task

**Request Body** (all fields optional):
```json
{
  "title": "Updated title",
  "description": "Updated description",
  "completed": true
}
```

**Response** (200):
```json
{
  "data": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "user_id": "660e8400-e29b-41d4-a716-446655440000",
    "title": "Updated title",
    "description": "Updated description",
    "completed": true,
    "created_at": "2025-12-21T10:00:00Z",
    "updated_at": "2025-12-21T10:30:00Z"
  },
  "meta": {
    "timestamp": "2025-12-21T10:30:00Z",
    "request_id": "770e8400-e29b-41d4-a716-446655440000"
  }
}
```

**Error Responses**:
- `401`: Missing or invalid token
- `403`: Task belongs to another user
- `404`: Task not found
- `422`: Validation error

---

### Delete Task

```
DELETE /api/tasks/{task_id}
```

**Auth Required**: Yes

**Path Parameters**:
- `task_id`: UUID of the task

**Response** (204): No content

**Error Responses**:
- `401`: Missing or invalid token
- `403`: Task belongs to another user
- `404`: Task not found
- `422`: Invalid UUID format

---

## Error Codes

| Code | HTTP Status | Description |
|------|-------------|-------------|
| `UNAUTHORIZED` | 401 | Authentication required or failed |
| `FORBIDDEN` | 403 | Access to resource denied |
| `NOT_FOUND` | 404 | Resource does not exist |
| `VALIDATION_ERROR` | 422 | Request validation failed |
| `INTERNAL_ERROR` | 500 | Unexpected server error |
| `SERVICE_UNAVAILABLE` | 503 | Database or service unavailable |

---

## Validation Rules

### TaskCreate

| Field | Type | Required | Constraints |
|-------|------|----------|-------------|
| `title` | string | Yes | 1-255 characters |
| `description` | string | No | Max 2000 characters |

### TaskUpdate

| Field | Type | Required | Constraints |
|-------|------|----------|-------------|
| `title` | string | No | 1-255 characters if provided |
| `description` | string | No | Max 2000 characters, can be null |
| `completed` | boolean | No | true/false |

---

## User Isolation Guarantee

**CRITICAL**: The API enforces strict user isolation:

1. Tasks are automatically assigned to the authenticated user on creation
2. Task listings only return the authenticated user's tasks
3. Single-task operations (GET/PATCH/DELETE) verify ownership
4. Attempting to access another user's task returns `403 Forbidden`
5. There is no endpoint to list all tasks across users
