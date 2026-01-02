"""
Tests for custom exceptions.

Tests verify:
- TaskNotFoundError has correct attributes
- AccessDeniedError has correct attributes
- Exceptions can be raised and caught properly
"""

import pytest
from uuid import uuid4


class TestTaskNotFoundError:
    """Test cases for TaskNotFoundError exception."""

    def test_task_not_found_error_exists(self):
        """TaskNotFoundError should be importable."""
        from src.exceptions import TaskNotFoundError

        assert TaskNotFoundError is not None

    def test_task_not_found_error_stores_task_id(self):
        """TaskNotFoundError should store the task_id."""
        from src.exceptions import TaskNotFoundError

        task_id = uuid4()
        error = TaskNotFoundError(task_id)
        assert error.task_id == task_id

    def test_task_not_found_error_message(self):
        """TaskNotFoundError should have appropriate message."""
        from src.exceptions import TaskNotFoundError

        task_id = uuid4()
        error = TaskNotFoundError(task_id)
        assert "not found" in str(error).lower()

    def test_task_not_found_error_is_exception(self):
        """TaskNotFoundError should be an Exception."""
        from src.exceptions import TaskNotFoundError

        assert issubclass(TaskNotFoundError, Exception)

    def test_task_not_found_error_can_be_raised(self):
        """TaskNotFoundError should be raisable."""
        from src.exceptions import TaskNotFoundError

        task_id = uuid4()
        with pytest.raises(TaskNotFoundError) as exc_info:
            raise TaskNotFoundError(task_id)

        assert exc_info.value.task_id == task_id


class TestAccessDeniedError:
    """Test cases for AccessDeniedError exception."""

    def test_access_denied_error_exists(self):
        """AccessDeniedError should be importable."""
        from src.exceptions import AccessDeniedError

        assert AccessDeniedError is not None

    def test_access_denied_error_message(self):
        """AccessDeniedError should have appropriate message."""
        from src.exceptions import AccessDeniedError

        error = AccessDeniedError()
        assert "denied" in str(error).lower() or "access" in str(error).lower()

    def test_access_denied_error_is_exception(self):
        """AccessDeniedError should be an Exception."""
        from src.exceptions import AccessDeniedError

        assert issubclass(AccessDeniedError, Exception)

    def test_access_denied_error_can_be_raised(self):
        """AccessDeniedError should be raisable."""
        from src.exceptions import AccessDeniedError

        with pytest.raises(AccessDeniedError):
            raise AccessDeniedError()

    def test_access_denied_error_optional_message(self):
        """AccessDeniedError can accept custom message."""
        from src.exceptions import AccessDeniedError

        custom_message = "Custom denial message"
        error = AccessDeniedError(custom_message)
        assert custom_message in str(error)
