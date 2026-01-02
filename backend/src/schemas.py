"""
Pydantic schemas for request/response validation.

Defines data contracts for the Task API:
- TaskCreate: Request body for POST /api/tasks/
- TaskUpdate: Request body for PATCH /api/tasks/{id}
- TaskRead: Response body for task data

Validation rules match spec requirements.
"""

from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field, ConfigDict


class TaskCreate(BaseModel):
    """
    Schema for creating a new task.

    Request body for POST /api/tasks/

    Attributes:
        title: Task title (required, 1-255 characters)
        description: Optional task description (max 2000 characters)
    """

    model_config = ConfigDict(str_strip_whitespace=True)

    title: str = Field(
        ...,
        min_length=1,
        max_length=255,
        description="Task title (required)",
    )

    description: Optional[str] = Field(
        default=None,
        max_length=2000,
        description="Optional task description",
    )

    due_date: Optional[datetime] = Field(
        default=None,
        description="Optional due date for the task",
    )


class TaskUpdate(BaseModel):
    """
    Schema for updating an existing task.

    Request body for PATCH /api/tasks/{id}
    All fields are optional; only provided fields are updated.

    Attributes:
        title: Updated task title (1-255 characters if provided)
        description: Updated description (max 2000 characters if provided)
        completed: Updated completion status
    """

    model_config = ConfigDict(str_strip_whitespace=True)

    title: Optional[str] = Field(
        default=None,
        min_length=1,
        max_length=255,
        description="Updated task title",
    )

    description: Optional[str] = Field(
        default=None,
        max_length=2000,
        description="Updated task description",
    )

    completed: Optional[bool] = Field(
        default=None,
        description="Updated completion status",
    )

    due_date: Optional[datetime] = Field(
        default=None,
        description="Updated due date",
    )


class TaskRead(BaseModel):
    """
    Schema for reading task data.

    Response body for all task endpoints.
    Includes all task fields including server-generated values.

    Attributes:
        id: Task UUID
        user_id: Owner's user UUID
        title: Task title
        description: Task description (may be None)
        completed: Completion status
        created_at: Creation timestamp
        updated_at: Last update timestamp
    """

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    user_id: UUID
    title: str
    description: Optional[str]
    due_date: Optional[datetime]
    completed: bool
    created_at: datetime
    updated_at: datetime


class UserLogin(BaseModel):
    """Schema for user login request."""
    email: str
    password: str


class UserRegister(BaseModel):
    """Schema for user registration request."""
    email: str
    password: str
    name: str


class AuthResponse(BaseModel):
    """Schema for authentication response."""
    user: dict
    token: str
