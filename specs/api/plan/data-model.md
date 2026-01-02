# Data Model: Phase II Backend API Core

**Date**: 2025-12-21
**Feature**: Backend API Core
**Branch**: `001-backend-api-core`

## Entity Overview

This backend manages a single primary entity (Task) with a reference to an external entity (User) managed by Better Auth.

```
┌─────────────────────┐          ┌─────────────────────┐
│       User          │          │        Task         │
│   (Better Auth)     │──────────│   (This Backend)    │
│                     │ 1      * │                     │
│ • id (UUID)         │          │ • id (UUID) PK      │
│ • email             │          │ • user_id (UUID) FK │
│ • ...               │          │ • title             │
└─────────────────────┘          │ • description       │
                                 │ • completed         │
                                 │ • created_at        │
                                 │ • updated_at        │
                                 └─────────────────────┘
```

---

## Entity: Task

### Description
A Task represents a single todo item belonging to a specific user. Tasks are completely isolated per user - no user can ever access another user's tasks.

### Table Definition

**Table Name**: `task`

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | UUID | PRIMARY KEY, DEFAULT uuid_generate_v4() | Unique task identifier |
| `user_id` | UUID | NOT NULL, INDEX | Owner's user ID from JWT |
| `title` | VARCHAR(255) | NOT NULL | Task title |
| `description` | TEXT | NULLABLE | Optional detailed description |
| `completed` | BOOLEAN | NOT NULL, DEFAULT FALSE | Completion status |
| `created_at` | TIMESTAMP WITH TIME ZONE | NOT NULL, DEFAULT NOW() | Creation timestamp |
| `updated_at` | TIMESTAMP WITH TIME ZONE | NOT NULL, DEFAULT NOW() | Last modification timestamp |

### Indexes

| Index Name | Columns | Type | Purpose |
|------------|---------|------|---------|
| `pk_task` | `id` | PRIMARY KEY | Unique identification |
| `ix_task_user_id` | `user_id` | B-TREE | Fast filtering by owner (MANDATORY) |
| `ix_task_user_created` | `user_id, created_at DESC` | B-TREE | Efficient sorted listing per user |

### SQLModel Definition

```python
from sqlmodel import SQLModel, Field
from uuid import UUID, uuid4
from datetime import datetime, timezone
from typing import Optional

class Task(SQLModel, table=True):
    """
    Task entity - represents a user's todo item.

    INVARIANT: All queries MUST filter by user_id.
    """
    __tablename__ = "task"

    id: UUID = Field(
        default_factory=uuid4,
        primary_key=True,
        description="Unique task identifier"
    )
    user_id: UUID = Field(
        index=True,
        nullable=False,
        description="Owner's user ID from JWT sub claim"
    )
    title: str = Field(
        max_length=255,
        nullable=False,
        description="Task title (required)"
    )
    description: Optional[str] = Field(
        default=None,
        max_length=2000,
        description="Optional task description"
    )
    completed: bool = Field(
        default=False,
        nullable=False,
        description="Whether task is completed"
    )
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        nullable=False,
        description="Creation timestamp"
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        nullable=False,
        sa_column_kwargs={"onupdate": lambda: datetime.now(timezone.utc)},
        description="Last update timestamp"
    )
```

---

## Entity: User (Reference Only)

### Description
Users are managed entirely by Better Auth on the frontend. The backend does NOT store user records. User identity is established solely through JWT token verification.

### JWT Claims Used

| Claim | Type | Usage |
|-------|------|-------|
| `sub` | UUID (string) | User's unique identifier, used as `user_id` for tasks |
| `exp` | Unix timestamp | Token expiration, verified by PyJWT |
| `iat` | Unix timestamp | Token issued-at, used for validation |

### No Local User Table

The backend trusts the JWT token as the source of truth for user identity. If a valid JWT contains a `sub` claim, that user is considered authenticated. No database lookup is required.

**Implication**: A user can create tasks immediately after registration without any backend user sync.

---

## Validation Rules

### Task Creation (`TaskCreate`)

| Field | Rule | Error |
|-------|------|-------|
| `title` | Required, 1-255 characters | 422: "title is required" / "title too long" |
| `description` | Optional, max 2000 characters | 422: "description too long" |

### Task Update (`TaskUpdate`)

| Field | Rule | Error |
|-------|------|-------|
| `title` | Optional, 1-255 characters if provided | 422: "title too long" |
| `description` | Optional, max 2000 characters if provided | 422: "description too long" |
| `completed` | Optional, boolean | 422: "completed must be boolean" |

At least one field must be provided for update (empty update is valid but no-op).

---

## State Transitions

### Task Lifecycle

```
                    ┌──────────┐
       create() ──→ │ PENDING  │ (completed=false)
                    └────┬─────┘
                         │
                   update(completed=true)
                         │
                         ▼
                    ┌──────────┐
                    │ COMPLETE │ (completed=true)
                    └────┬─────┘
                         │
                   update(completed=false)
                         │
                         ▼
                    ┌──────────┐
                    │ PENDING  │ (can toggle back)
                    └────┬─────┘
                         │
                     delete()
                         │
                         ▼
                    ┌──────────┐
                    │ DELETED  │ (hard delete, not recoverable)
                    └──────────┘
```

**Notes**:
- Tasks can be toggled between PENDING and COMPLETE indefinitely
- Deletion is permanent (no soft delete in v1)
- No other states exist (no "archived", "in_progress", etc.)

---

## Data Access Patterns

### Query Patterns (All require `user_id`)

| Operation | Query Pattern | Index Used |
|-----------|--------------|------------|
| List tasks | `SELECT * FROM task WHERE user_id = ? ORDER BY created_at DESC` | `ix_task_user_created` |
| Get task | `SELECT * FROM task WHERE id = ? AND user_id = ?` | `pk_task` + filter |
| Create task | `INSERT INTO task (user_id, title, ...) VALUES (?, ?, ...)` | N/A |
| Update task | `UPDATE task SET ... WHERE id = ? AND user_id = ?` | `pk_task` + filter |
| Delete task | `DELETE FROM task WHERE id = ? AND user_id = ?` | `pk_task` + filter |

### User Isolation Enforcement

**CRITICAL**: Every CRUD operation MUST include `user_id` filtering.

```python
# CORRECT: Get single task with ownership check
async def get_task(session: AsyncSession, task_id: UUID, user_id: UUID) -> Task:
    task = await session.get(Task, task_id)
    if not task:
        raise TaskNotFoundError()
    if task.user_id != user_id:
        raise AccessDeniedError()  # 403
    return task

# CORRECT: List tasks for user only
async def list_tasks(session: AsyncSession, user_id: UUID) -> list[Task]:
    result = await session.execute(
        select(Task).where(Task.user_id == user_id).order_by(Task.created_at.desc())
    )
    return result.scalars().all()
```

---

## Migration Strategy

### Initial Migration (v1)

```sql
-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Create task table
CREATE TABLE task (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    completed BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW()
);

-- Create indexes
CREATE INDEX ix_task_user_id ON task(user_id);
CREATE INDEX ix_task_user_created ON task(user_id, created_at DESC);
```

### Future Migration Considerations

- Adding `priority` field: Default value, no breaking change
- Adding `due_date` field: Nullable, no breaking change
- Soft delete: Add `deleted_at` column, update queries (breaking)
