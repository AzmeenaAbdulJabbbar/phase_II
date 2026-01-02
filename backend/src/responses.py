"""
Standardized response envelope helpers.

Provides consistent response formatting per Constitution requirements:
- Success responses: {data, meta}
- Error responses: {error, meta}

All responses include meta with timestamp and request_id for tracing.
"""

from datetime import datetime, timezone
from typing import Any
from uuid import uuid4


def success_response(data: Any, total: int | None = None) -> dict:
    """
    Wrap successful response in standard envelope.

    Args:
        data: The response data (single object or list)
        total: Optional total count for list responses

    Returns:
        dict: Response envelope with {data, meta}

    Example:
        >>> success_response({"id": 1, "title": "Task"})
        {
            "data": {"id": 1, "title": "Task"},
            "meta": {
                "timestamp": "2025-12-21T10:00:00Z",
                "request_id": "550e8400-e29b-41d4-a716-446655440000"
            }
        }
    """
    meta: dict[str, Any] = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "request_id": str(uuid4()),
    }

    if total is not None:
        meta["total"] = total

    return {
        "data": data,
        "meta": meta,
    }


def error_response(
    code: str,
    message: str,
    details: dict | None = None,
) -> dict:
    """
    Wrap error in standard envelope.

    Args:
        code: Error code (e.g., "NOT_FOUND", "UNAUTHORIZED")
        message: Human-readable error message
        details: Optional additional error details (e.g., validation errors)

    Returns:
        dict: Response envelope with {error, meta}

    Example:
        >>> error_response("NOT_FOUND", "Task not found")
        {
            "error": {
                "code": "NOT_FOUND",
                "message": "Task not found"
            },
            "meta": {
                "timestamp": "2025-12-21T10:00:00Z",
                "request_id": "550e8400-e29b-41d4-a716-446655440000"
            }
        }
    """
    error: dict[str, Any] = {
        "code": code,
        "message": message,
    }

    if details is not None:
        error["details"] = details

    return {
        "error": error,
        "meta": {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "request_id": str(uuid4()),
        },
    }
