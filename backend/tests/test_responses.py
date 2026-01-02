"""
Tests for response envelope helpers.

Tests verify:
- success_response returns {data, meta} format
- error_response returns {error, meta} format
- meta includes timestamp and request_id
- total is included in list responses
"""

import pytest
from uuid import UUID
from datetime import datetime


class TestSuccessResponse:
    """Test cases for success_response helper."""

    def test_success_response_has_data_key(self):
        """Success response should have 'data' key."""
        from src.responses import success_response

        result = success_response({"id": 1})
        assert "data" in result

    def test_success_response_has_meta_key(self):
        """Success response should have 'meta' key."""
        from src.responses import success_response

        result = success_response({"id": 1})
        assert "meta" in result

    def test_success_response_data_matches_input(self):
        """Success response data should match input."""
        from src.responses import success_response

        data = {"id": 1, "name": "test"}
        result = success_response(data)
        assert result["data"] == data

    def test_success_response_meta_has_timestamp(self):
        """Success response meta should have timestamp."""
        from src.responses import success_response

        result = success_response({"id": 1})
        assert "timestamp" in result["meta"]
        # Should be ISO8601 format string
        assert isinstance(result["meta"]["timestamp"], str)

    def test_success_response_meta_has_request_id(self):
        """Success response meta should have request_id."""
        from src.responses import success_response

        result = success_response({"id": 1})
        assert "request_id" in result["meta"]
        # Should be valid UUID string
        UUID(result["meta"]["request_id"])

    def test_success_response_with_total(self):
        """Success response should include total when provided."""
        from src.responses import success_response

        result = success_response([{"id": 1}, {"id": 2}], total=2)
        assert result["meta"]["total"] == 2

    def test_success_response_without_total(self):
        """Success response should not include total when not provided."""
        from src.responses import success_response

        result = success_response({"id": 1})
        assert "total" not in result["meta"]

    def test_success_response_handles_list_data(self):
        """Success response should handle list data."""
        from src.responses import success_response

        data = [{"id": 1}, {"id": 2}]
        result = success_response(data, total=2)
        assert result["data"] == data


class TestErrorResponse:
    """Test cases for error_response helper."""

    def test_error_response_has_error_key(self):
        """Error response should have 'error' key."""
        from src.responses import error_response

        result = error_response("NOT_FOUND", "Task not found")
        assert "error" in result

    def test_error_response_has_meta_key(self):
        """Error response should have 'meta' key."""
        from src.responses import error_response

        result = error_response("NOT_FOUND", "Task not found")
        assert "meta" in result

    def test_error_response_error_has_code(self):
        """Error response error should have code."""
        from src.responses import error_response

        result = error_response("NOT_FOUND", "Task not found")
        assert result["error"]["code"] == "NOT_FOUND"

    def test_error_response_error_has_message(self):
        """Error response error should have message."""
        from src.responses import error_response

        result = error_response("NOT_FOUND", "Task not found")
        assert result["error"]["message"] == "Task not found"

    def test_error_response_with_details(self):
        """Error response should include details when provided."""
        from src.responses import error_response

        details = {"field": "title", "error": "required"}
        result = error_response("VALIDATION_ERROR", "Validation failed", details)
        assert result["error"]["details"] == details

    def test_error_response_without_details(self):
        """Error response should not include details when not provided."""
        from src.responses import error_response

        result = error_response("NOT_FOUND", "Task not found")
        assert "details" not in result["error"]

    def test_error_response_meta_has_timestamp(self):
        """Error response meta should have timestamp."""
        from src.responses import error_response

        result = error_response("NOT_FOUND", "Task not found")
        assert "timestamp" in result["meta"]

    def test_error_response_meta_has_request_id(self):
        """Error response meta should have request_id."""
        from src.responses import error_response

        result = error_response("NOT_FOUND", "Task not found")
        assert "request_id" in result["meta"]
        UUID(result["meta"]["request_id"])
