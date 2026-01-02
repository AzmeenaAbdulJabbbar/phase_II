"""
SQLModel database models.

Defines the Task entity with strict user isolation requirements.
INVARIANT: All queries MUST filter by user_id.
"""

from datetime import datetime, timezone
from typing import Optional
from uuid import UUID, uuid4

from sqlmodel import Field, SQLModel


class Task(SQLModel, table=True):
    """
    Task entity - represents a user's todo item.

    INVARIANT: All database queries for tasks MUST include user_id filtering.
    This ensures strict user data isolation per Constitution requirements.

    Attributes:
        id: Unique task identifier (UUID, primary key)
        user_id: Owner's user ID from JWT sub claim (indexed, required)
        title: Task title (required, max 255 chars)
        description: Optional task description (max 2000 chars)
        completed: Whether task is completed (default: False)
        created_at: Creation timestamp (auto-set)
        updated_at: Last update timestamp (auto-set)
    """

    __tablename__ = "task"

    id: UUID = Field(
        default_factory=uuid4,
        primary_key=True,
        description="Unique task identifier",
    )

    user_id: UUID = Field(
        index=True,
        nullable=False,
        description="Owner's user ID from JWT sub claim",
    )

    title: str = Field(
        max_length=255,
        nullable=False,
        description="Task title (required)",
    )

    description: Optional[str] = Field(
        default=None,
        max_length=2000,
        description="Optional task description",
    )

    completed: bool = Field(
        default=False,
        nullable=False,
        description="Whether task is completed",
    )

    due_date: Optional[datetime] = Field(
        default=None,
        nullable=True,
        description="Optional due date for the task",
    )

    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc).replace(tzinfo=None),
        nullable=False,
        description="Creation timestamp",
    )

    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc).replace(tzinfo=None),
        nullable=False,
        description="Last update timestamp",
    )
