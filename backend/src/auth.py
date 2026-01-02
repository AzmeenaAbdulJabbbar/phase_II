"""
JWT authentication middleware for FastAPI.

Implements the JWT Bridge pattern per Constitution requirements:
- Verifies JWT tokens using BETTER_AUTH_SECRET (HS256)
- Extracts user_id from the 'sub' claim
- Provides get_current_user_id dependency for protected routes

All protected endpoints should use:
    current_user_id: UUID = Depends(get_current_user_id)
"""

from uuid import UUID

import jwt
from datetime import datetime, timedelta, timezone
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from .config import settings

# HTTPBearer security scheme for OpenAPI documentation
security = HTTPBearer()


def verify_jwt_token(token: str, secret: str) -> UUID:
    """
    Verify a JWT token and extract the user_id.

    Args:
        token: The JWT token string
        secret: The secret key for verification (BETTER_AUTH_SECRET)

    Returns:
        UUID: The user_id from the token's 'sub' claim

    Raises:
        HTTPException: 401 if token is invalid, expired, or missing sub claim
    """
    try:
        payload = jwt.decode(token, secret, algorithms=["HS256"])

        user_id = payload.get("sub")
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token: missing user identifier",
            )

        return UUID(user_id)

    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expired",
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )
    except ValueError:
        # Invalid UUID format in sub claim
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token: invalid user identifier format",
        )


def create_jwt_token(user_id: UUID) -> str:
    """
    Create a new JWT token for a user.

    Args:
        user_id: The UUID of the user

    Returns:
        str: The signed JWT token
    """
    expire = datetime.now(timezone.utc) + timedelta(days=7)
    payload = {
        "sub": str(user_id),
        "exp": expire,
        "iat": datetime.now(timezone.utc),
    }
    return jwt.encode(payload, settings.BETTER_AUTH_SECRET, algorithm="HS256")


async def get_current_user_id(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> UUID:
    """
    FastAPI dependency that extracts and verifies the user_id from JWT.

    Usage in routes:
        @router.get("/tasks")
        async def list_tasks(user_id: UUID = Depends(get_current_user_id)):
            # user_id is guaranteed to be valid here
            ...

    Args:
        credentials: The Bearer token from Authorization header

    Returns:
        UUID: The authenticated user's ID

    Raises:
        HTTPException: 401 if no token provided or token is invalid
    """
    return verify_jwt_token(credentials.credentials, settings.BETTER_AUTH_SECRET)
