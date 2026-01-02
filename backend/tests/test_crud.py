"""
Tests for CRUD operations with strict user isolation.

CRITICAL: Every test must verify user_id filtering/ownership.
Constitution requirement: Zero data leakage between users.
"""

import pytest
from uuid import UUID, uuid4
from sqlalchemy.ext.asyncio import AsyncSession

from src.crud import create_task, get_tasks, get_task, update_task, delete_task
from src.schemas import TaskCreate, TaskUpdate
from src.exceptions import TaskNotFoundError, AccessDeniedError
from src.models import Task


# T024: Test create_task with user_id
@pytest.mark.asyncio
async def test_create_task_assigns_user_id(db_session: AsyncSession):
    """
    US1: Authenticated Task Creation
    Verify that create_task assigns the provided user_id to the task.
    """
    user_id = uuid4()
    task_data = TaskCreate(title="Test Task", description="Test Description")

    # Should fail initially - crud.py doesn't exist yet
    task = await create_task(db_session, user_id, task_data)

    assert task.id is not None
    assert task.user_id == user_id
    assert task.title == "Test Task"
    assert task.description == "Test Description"
    assert task.completed is False


@pytest.mark.asyncio
async def test_create_task_without_description(db_session: AsyncSession):
    """Verify task can be created without description."""
    user_id = uuid4()
    task_data = TaskCreate(title="Minimal Task")

    task = await create_task(db_session, user_id, task_data)

    assert task.description is None
    assert task.title == "Minimal Task"


# T025: Test get_tasks filters by user_id
@pytest.mark.asyncio
async def test_get_tasks_filters_by_user_id(db_session: AsyncSession):
    """
    US2: Task Retrieval with User Isolation
    Verify that get_tasks returns only tasks belonging to the specified user.
    """
    user_a_id = uuid4()
    user_b_id = uuid4()

    # Create tasks for User A
    await create_task(db_session, user_a_id, TaskCreate(title="User A Task 1"))
    await create_task(db_session, user_a_id, TaskCreate(title="User A Task 2"))

    # Create tasks for User B
    await create_task(db_session, user_b_id, TaskCreate(title="User B Task 1"))

    # Get tasks for User A
    user_a_tasks = await get_tasks(db_session, user_a_id)

    # User A should see only their 2 tasks
    assert len(user_a_tasks) == 2
    assert all(task.user_id == user_a_id for task in user_a_tasks)
    assert "User A Task 1" in [task.title for task in user_a_tasks]
    assert "User A Task 2" in [task.title for task in user_a_tasks]


@pytest.mark.asyncio
async def test_get_tasks_empty_for_new_user(db_session: AsyncSession):
    """Verify get_tasks returns empty list for user with no tasks."""
    user_id = uuid4()

    tasks = await get_tasks(db_session, user_id)

    assert tasks == []


# T026: Test get_task with ownership check
@pytest.mark.asyncio
async def test_get_task_returns_owned_task(db_session: AsyncSession):
    """
    US5: Single Task Retrieval
    Verify that get_task returns task if user owns it.
    """
    user_id = uuid4()
    task_data = TaskCreate(title="My Task")

    created_task = await create_task(db_session, user_id, task_data)

    # Retrieve the task
    retrieved_task = await get_task(db_session, created_task.id, user_id)

    assert retrieved_task.id == created_task.id
    assert retrieved_task.user_id == user_id
    assert retrieved_task.title == "My Task"


@pytest.mark.asyncio
async def test_get_task_raises_not_found_for_nonexistent(db_session: AsyncSession):
    """Verify get_task raises TaskNotFoundError for non-existent task."""
    user_id = uuid4()
    fake_task_id = uuid4()

    with pytest.raises(TaskNotFoundError) as exc_info:
        await get_task(db_session, fake_task_id, user_id)

    assert str(fake_task_id) in str(exc_info.value)


# T027: Test update_task with ownership check
@pytest.mark.asyncio
async def test_update_task_updates_owned_task(db_session: AsyncSession):
    """
    US3: Task Update with Ownership Validation
    Verify that update_task successfully updates task owned by user.
    """
    user_id = uuid4()
    task_data = TaskCreate(title="Original Title")

    created_task = await create_task(db_session, user_id, task_data)

    # Update the task
    update_data = TaskUpdate(title="Updated Title", completed=True)
    updated_task = await update_task(db_session, created_task.id, user_id, update_data)

    assert updated_task.id == created_task.id
    assert updated_task.title == "Updated Title"
    assert updated_task.completed is True


@pytest.mark.asyncio
async def test_update_task_partial_update(db_session: AsyncSession):
    """Verify update_task supports partial updates."""
    user_id = uuid4()
    task_data = TaskCreate(title="Original", description="Original Desc")

    created_task = await create_task(db_session, user_id, task_data)

    # Update only completion status
    update_data = TaskUpdate(completed=True)
    updated_task = await update_task(db_session, created_task.id, user_id, update_data)

    assert updated_task.completed is True
    assert updated_task.title == "Original"  # Unchanged
    assert updated_task.description == "Original Desc"  # Unchanged


# T028: Test delete_task with ownership check
@pytest.mark.asyncio
async def test_delete_task_removes_owned_task(db_session: AsyncSession):
    """
    US4: Task Deletion with Authorization
    Verify that delete_task successfully removes task owned by user.
    """
    user_id = uuid4()
    task_data = TaskCreate(title="To Delete")

    created_task = await create_task(db_session, user_id, task_data)

    # Delete the task
    await delete_task(db_session, created_task.id, user_id)

    # Verify task no longer exists
    with pytest.raises(TaskNotFoundError):
        await get_task(db_session, created_task.id, user_id)


# T030: Test 403 when User B accesses User A's task
@pytest.mark.asyncio
async def test_get_task_raises_access_denied_for_other_user(db_session: AsyncSession):
    """
    CRITICAL USER ISOLATION TEST
    Verify that User B cannot access User A's task (403 Forbidden).
    """
    user_a_id = uuid4()
    user_b_id = uuid4()

    # User A creates a task
    task_data = TaskCreate(title="User A's Private Task")
    user_a_task = await create_task(db_session, user_a_id, task_data)

    # User B tries to access User A's task
    with pytest.raises(AccessDeniedError) as exc_info:
        await get_task(db_session, user_a_task.id, user_b_id)

    # Verify error message indicates access denied
    assert "access denied" in str(exc_info.value).lower()


# T031: Test 403 when User B updates User A's task
@pytest.mark.asyncio
async def test_update_task_raises_access_denied_for_other_user(db_session: AsyncSession):
    """
    CRITICAL USER ISOLATION TEST
    Verify that User B cannot update User A's task (403 Forbidden).
    """
    user_a_id = uuid4()
    user_b_id = uuid4()

    # User A creates a task
    task_data = TaskCreate(title="User A's Task")
    user_a_task = await create_task(db_session, user_a_id, task_data)

    # User B tries to update User A's task
    update_data = TaskUpdate(title="Hacked by User B")

    with pytest.raises(AccessDeniedError):
        await update_task(db_session, user_a_task.id, user_b_id, update_data)


# T032: Test 403 when User B deletes User A's task
@pytest.mark.asyncio
async def test_delete_task_raises_access_denied_for_other_user(db_session: AsyncSession):
    """
    CRITICAL USER ISOLATION TEST
    Verify that User B cannot delete User A's task (403 Forbidden).
    """
    user_a_id = uuid4()
    user_b_id = uuid4()

    # User A creates a task
    task_data = TaskCreate(title="User A's Task")
    user_a_task = await create_task(db_session, user_a_id, task_data)

    # User B tries to delete User A's task
    with pytest.raises(AccessDeniedError):
        await delete_task(db_session, user_a_task.id, user_b_id)

    # Verify task still exists for User A
    still_exists = await get_task(db_session, user_a_task.id, user_a_id)
    assert still_exists.id == user_a_task.id
