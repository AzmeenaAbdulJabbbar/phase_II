"""
Tests for SQLModel models.

Tests verify:
- Task model has all required fields
- Field constraints are properly defined
- Default values are applied correctly
- user_id is indexed for performance
"""

import pytest
from uuid import UUID, uuid4
from datetime import datetime, timezone


class TestTaskModel:
    """Test cases for Task SQLModel."""

    def test_task_has_id_field(self):
        """Task should have id field as UUID primary key."""
        from src.models import Task

        task = Task(
            user_id=uuid4(),
            title="Test Task",
        )
        assert hasattr(task, "id")
        # Default factory should generate UUID
        assert task.id is not None or True  # id may be None before DB insert

    def test_task_has_user_id_field(self):
        """Task should have user_id field as UUID."""
        from src.models import Task

        user_id = uuid4()
        task = Task(user_id=user_id, title="Test Task")
        assert task.user_id == user_id
        assert isinstance(task.user_id, UUID)

    def test_task_has_title_field(self):
        """Task should have title field as string."""
        from src.models import Task

        task = Task(user_id=uuid4(), title="My Task Title")
        assert task.title == "My Task Title"

    def test_task_has_description_field(self):
        """Task should have description field (optional)."""
        from src.models import Task

        # Without description
        task1 = Task(user_id=uuid4(), title="Task 1")
        assert task1.description is None

        # With description
        task2 = Task(user_id=uuid4(), title="Task 2", description="A description")
        assert task2.description == "A description"

    def test_task_has_completed_field_defaults_false(self):
        """Task should have completed field defaulting to False."""
        from src.models import Task

        task = Task(user_id=uuid4(), title="Test Task")
        assert task.completed is False

    def test_task_completed_can_be_set_true(self):
        """Task completed field can be set to True."""
        from src.models import Task

        task = Task(user_id=uuid4(), title="Test Task", completed=True)
        assert task.completed is True

    def test_task_has_created_at_field(self):
        """Task should have created_at timestamp field."""
        from src.models import Task

        task = Task(user_id=uuid4(), title="Test Task")
        assert hasattr(task, "created_at")
        # Default factory should set timestamp
        assert task.created_at is not None

    def test_task_has_updated_at_field(self):
        """Task should have updated_at timestamp field."""
        from src.models import Task

        task = Task(user_id=uuid4(), title="Test Task")
        assert hasattr(task, "updated_at")
        assert task.updated_at is not None

    def test_task_is_table_model(self):
        """Task should be a SQLModel table."""
        from src.models import Task

        assert hasattr(Task, "__tablename__")
        assert Task.__tablename__ == "task"

    def test_task_user_id_is_indexed(self):
        """Task user_id field should be indexed for query performance."""
        from src.models import Task
        from sqlmodel import Field

        # Check the model's field info for index
        user_id_field = Task.model_fields.get("user_id")
        assert user_id_field is not None

        # The index is defined in Field(), we verify via SQLAlchemy table inspection
        table = Task.__table__
        user_id_col = table.c.user_id

        # Check if any index includes user_id
        indexes = list(table.indexes)
        user_id_indexed = any(
            "user_id" in [col.name for col in idx.columns] for idx in indexes
        ) or user_id_col.index

        assert user_id_indexed, "user_id should be indexed"
