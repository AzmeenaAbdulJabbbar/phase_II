"""
CRUD operations for Task entity with STRICT user isolation.

CRITICAL INVARIANT (Constitution requirement):
Every function MUST require user_id parameter and filter/validate by it.
NO database query may return data belonging to a different user.

Functions:
- create_task: Assigns user_id to new task
- get_tasks: Returns only tasks belonging to user_id
- get_task: Returns task only if owned by user_id, else AccessDeniedError
- update_task: Updates task only if owned by user_id, else AccessDeniedError
- delete_task: Deletes task only if owned by user_id, else AccessDeniedError
"""

from datetime import datetime, timezone
from typing import List
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .models import Task
from .schemas import TaskCreate, TaskUpdate
from .exceptions import TaskNotFoundError, AccessDeniedError


async def create_task(
    session: AsyncSession,
    user_id: UUID,
    task_data: TaskCreate,
) -> Task:
    """
    Create a new task for the specified user.

    Args:
        session: Database session
        user_id: Owner's user ID (from JWT sub claim) - REQUIRED
        task_data: Task creation data

    Returns:
        Created Task with user_id assigned

    Constitution Compliance:
    - user_id is REQUIRED parameter (NON-NEGOTIABLE)
    - Task is automatically assigned to user_id
    """
    task = Task(
        user_id=user_id,
        title=task_data.title,
        description=task_data.description,
        completed=False,  # New tasks default to incomplete
    )

    session.add(task)
    await session.commit()
    await session.refresh(task)

    return task


async def get_tasks(
    session: AsyncSession,
    user_id: UUID,
) -> List[Task]:
    """
    Get all tasks belonging to the specified user.

    Args:
        session: Database session
        user_id: Owner's user ID - REQUIRED

    Returns:
        List of tasks filtered by user_id (empty list if none)

    Constitution Compliance:
    - MUST filter by user_id (NON-NEGOTIABLE)
    - Returns only tasks owned by user_id
    - Zero data leakage guarantee
    """
    result = await session.execute(
        select(Task).where(Task.user_id == user_id)
    )
    tasks = result.scalars().all()

    return list(tasks)


async def get_task(
    session: AsyncSession,
    task_id: UUID,
    user_id: UUID,
) -> Task:
    """
    Get a single task by ID with ownership verification.

    Args:
        session: Database session
        task_id: Task ID to retrieve
        user_id: Owner's user ID - REQUIRED

    Returns:
        Task if owned by user_id

    Raises:
        TaskNotFoundError: If task doesn't exist
        AccessDeniedError: If task exists but belongs to different user

    Constitution Compliance:
    - MUST verify ownership (NON-NEGOTIABLE)
    - Raises AccessDeniedError if user_id mismatch
    - Prevents cross-user data access
    """
    result = await session.execute(
        select(Task).where(Task.id == task_id)
    )
    task = result.scalar_one_or_none()

    if task is None:
        raise TaskNotFoundError(task_id)

    # CRITICAL: Verify ownership before returning
    if task.user_id != user_id:
        raise AccessDeniedError(
            f"Access denied: Task {task_id} belongs to a different user"
        )

    return task


async def update_task(
    session: AsyncSession,
    task_id: UUID,
    user_id: UUID,
    task_data: TaskUpdate,
) -> Task:
    """
    Update a task with ownership verification.

    Args:
        session: Database session
        task_id: Task ID to update
        user_id: Owner's user ID - REQUIRED
        task_data: Update data (partial updates supported)

    Returns:
        Updated Task

    Raises:
        TaskNotFoundError: If task doesn't exist
        AccessDeniedError: If task belongs to different user

    Constitution Compliance:
    - MUST verify ownership before update (NON-NEGOTIABLE)
    - Prevents User B from modifying User A's tasks
    """
    # Get task with ownership check
    task = await get_task(session, task_id, user_id)

    # Apply updates (only for non-None fields)
    update_dict = task_data.model_dump(exclude_unset=True)

    for field, value in update_dict.items():
        setattr(task, field, value)

    # Update timestamp - ensure timezone-naive to match database schema
    task.updated_at = datetime.now(timezone.utc).replace(tzinfo=None)

    session.add(task)
    await session.commit()
    await session.refresh(task)

    return task


async def delete_task(
    session: AsyncSession,
    task_id: UUID,
    user_id: UUID,
) -> None:
    """
    Delete a task with ownership verification.

    Args:
        session: Database session
        task_id: Task ID to delete
        user_id: Owner's user ID - REQUIRED

    Raises:
        TaskNotFoundError: If task doesn't exist
        AccessDeniedError: If task belongs to different user

    Constitution Compliance:
    - MUST verify ownership before deletion (NON-NEGOTIABLE)
    - Prevents User B from deleting User A's tasks
    """
    # Get task with ownership check
    task = await get_task(session, task_id, user_id)

    await session.delete(task)
    await session.commit()
