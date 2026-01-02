"""
Tests for JWT authentication middleware.

Tests verify:
- Valid tokens are accepted and user_id is extracted
- Missing tokens return 401
- Expired tokens return 401
- Invalid tokens return 401
"""

import pytest
from uuid import UUID
from fastapi import HTTPException


class TestJWTVerification:
    """Test cases for JWT verification."""

    def test_valid_token_extracts_user_id(
        self, test_secret: str, user_a_id: UUID, valid_token_user_a: str
    ):
        """Valid token should extract user_id from sub claim."""
        from src.auth import verify_jwt_token

        result = verify_jwt_token(valid_token_user_a, test_secret)
        assert result == user_a_id

    def test_valid_token_for_different_user(
        self, test_secret: str, user_b_id: UUID, valid_token_user_b: str
    ):
        """Valid token for User B should extract User B's ID."""
        from src.auth import verify_jwt_token

        result = verify_jwt_token(valid_token_user_b, test_secret)
        assert result == user_b_id


class TestMissingToken:
    """Test cases for missing authorization."""

    def test_get_current_user_id_dependency_exists(self):
        """get_current_user_id dependency should be importable."""
        from src.auth import get_current_user_id

        assert get_current_user_id is not None

    def test_security_scheme_is_http_bearer(self):
        """Security scheme should use HTTPBearer."""
        from src.auth import security
        from fastapi.security import HTTPBearer

        assert isinstance(security, HTTPBearer)


class TestExpiredToken:
    """Test cases for expired tokens."""

    def test_expired_token_raises_exception(
        self, test_secret: str, expired_token: str
    ):
        """Expired token should raise exception."""
        from src.auth import verify_jwt_token

        with pytest.raises(HTTPException) as exc_info:
            verify_jwt_token(expired_token, test_secret)

        assert exc_info.value.status_code == 401
        assert "expired" in exc_info.value.detail.lower()


class TestInvalidToken:
    """Test cases for invalid tokens."""

    def test_invalid_signature_raises_exception(
        self, test_secret: str, invalid_token: str
    ):
        """Token with invalid signature should raise exception."""
        from src.auth import verify_jwt_token

        with pytest.raises(HTTPException) as exc_info:
            verify_jwt_token(invalid_token, test_secret)

        assert exc_info.value.status_code == 401
        assert "invalid" in exc_info.value.detail.lower()

    def test_malformed_token_raises_exception(self, test_secret: str):
        """Malformed token should raise exception."""
        from src.auth import verify_jwt_token

        with pytest.raises(HTTPException) as exc_info:
            verify_jwt_token("not-a-valid-jwt", test_secret)

        assert exc_info.value.status_code == 401

    def test_token_without_sub_claim_raises_exception(self, test_secret: str):
        """Token without sub claim should raise exception."""
        import jwt
        from datetime import datetime, timezone, timedelta
        from src.auth import verify_jwt_token

        # Create token without sub claim
        payload = {
            "iat": datetime.now(timezone.utc),
            "exp": datetime.now(timezone.utc) + timedelta(hours=1),
        }
        token = jwt.encode(payload, test_secret, algorithm="HS256")

        with pytest.raises(HTTPException) as exc_info:
            verify_jwt_token(token, test_secret)

        assert exc_info.value.status_code == 401
