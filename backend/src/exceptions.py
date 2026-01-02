"""
Custom exceptions for the backend API.

Provides domain-specific exceptions for error handling:
- TaskNotFoundError: Raised when a task ID doesn't exist
- AccessDeniedError: Raised when user tries to access another user's resource
"""

from uuid import UUID


class TaskNotFoundError(Exception):
    """
    Raised when a task is not found in the database.

    Attributes:
        task_id: The UUID of the task that was not found
    """

    def __init__(self, task_id: UUID) -> None:
        self.task_id = task_id
        super().__init__(f"Task not found: {task_id}")


class AccessDeniedError(Exception):
    """
    Raised when a user attempts to access a resource they don't own.

    This exception enforces user data isolation per Constitution requirements.
    Should result in HTTP 403 Forbidden response.
    """

    def __init__(self, message: str = "Access denied") -> None:
        super().__init__(message)
