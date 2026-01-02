"""
Tests for Pydantic schemas.

Tests verify:
- TaskCreate validates title (required, 1-255 chars)
- TaskCreate validates description (optional, max 2000 chars)
- TaskUpdate allows partial updates
- TaskRead includes all task fields
- Validation errors are raised appropriately
"""

import pytest
from uuid import uuid4
from datetime import datetime, timezone
from pydantic import ValidationError


class TestTaskCreateSchema:
    """Test cases for TaskCreate schema."""

    def test_task_create_requires_title(self):
        """TaskCreate should require title field."""
        from src.schemas import TaskCreate

        with pytest.raises(ValidationError) as exc_info:
            TaskCreate()

        errors = exc_info.value.errors()
        assert any(e["loc"] == ("title",) for e in errors)

    def test_task_create_accepts_valid_title(self):
        """TaskCreate should accept valid title."""
        from src.schemas import TaskCreate

        task = TaskCreate(title="My Task")
        assert task.title == "My Task"

    def test_task_create_title_min_length(self):
        """TaskCreate title should have minimum length of 1."""
        from src.schemas import TaskCreate

        with pytest.raises(ValidationError):
            TaskCreate(title="")

    def test_task_create_title_max_length(self):
        """TaskCreate title should have maximum length of 255."""
        from src.schemas import TaskCreate

        # Valid: 255 chars
        task = TaskCreate(title="a" * 255)
        assert len(task.title) == 255

        # Invalid: 256 chars
        with pytest.raises(ValidationError):
            TaskCreate(title="a" * 256)

    def test_task_create_description_optional(self):
        """TaskCreate description should be optional."""
        from src.schemas import TaskCreate

        task = TaskCreate(title="Test")
        assert task.description is None

    def test_task_create_description_max_length(self):
        """TaskCreate description should have max length of 2000."""
        from src.schemas import TaskCreate

        # Valid: 2000 chars
        task = TaskCreate(title="Test", description="a" * 2000)
        assert len(task.description) == 2000

        # Invalid: 2001 chars
        with pytest.raises(ValidationError):
            TaskCreate(title="Test", description="a" * 2001)


class TestTaskUpdateSchema:
    """Test cases for TaskUpdate schema."""

    def test_task_update_all_fields_optional(self):
        """TaskUpdate should allow all fields to be optional."""
        from src.schemas import TaskUpdate

        # Empty update is valid
        task = TaskUpdate()
        assert task.title is None
        assert task.description is None
        assert task.completed is None

    def test_task_update_can_set_title(self):
        """TaskUpdate should allow setting title."""
        from src.schemas import TaskUpdate

        task = TaskUpdate(title="Updated Title")
        assert task.title == "Updated Title"

    def test_task_update_can_set_completed(self):
        """TaskUpdate should allow setting completed status."""
        from src.schemas import TaskUpdate

        task = TaskUpdate(completed=True)
        assert task.completed is True

    def test_task_update_title_max_length(self):
        """TaskUpdate title should have max length of 255 if provided."""
        from src.schemas import TaskUpdate

        with pytest.raises(ValidationError):
            TaskUpdate(title="a" * 256)

    def test_task_update_description_max_length(self):
        """TaskUpdate description should have max length of 2000 if provided."""
        from src.schemas import TaskUpdate

        with pytest.raises(ValidationError):
            TaskUpdate(description="a" * 2001)


class TestTaskReadSchema:
    """Test cases for TaskRead schema."""

    def test_task_read_includes_all_fields(self):
        """TaskRead should include all task fields."""
        from src.schemas import TaskRead

        now = datetime.now(timezone.utc)
        task = TaskRead(
            id=uuid4(),
            user_id=uuid4(),
            title="Test Task",
            description="Description",
            completed=False,
            created_at=now,
            updated_at=now,
        )

        assert task.id is not None
        assert task.user_id is not None
        assert task.title == "Test Task"
        assert task.description == "Description"
        assert task.completed is False
        assert task.created_at == now
        assert task.updated_at == now

    def test_task_read_description_can_be_none(self):
        """TaskRead description can be None."""
        from src.schemas import TaskRead

        now = datetime.now(timezone.utc)
        task = TaskRead(
            id=uuid4(),
            user_id=uuid4(),
            title="Test",
            description=None,
            completed=False,
            created_at=now,
            updated_at=now,
        )

        assert task.description is None
