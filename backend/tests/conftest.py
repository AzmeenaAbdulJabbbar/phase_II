"""
Pytest configuration and fixtures for Phase II Backend tests.

Provides:
- Test database session fixtures
- Mock JWT token generation
- Test client setup
"""

import os
import pytest
from uuid import UUID, uuid4
from datetime import datetime, timezone, timedelta
from typing import AsyncGenerator, Generator
import jwt

# Set test environment variables before importing app modules
# Use SQLite for tests (in-memory database for speed and isolation)
os.environ.setdefault("DATABASE_URL", "sqlite+aiosqlite:///:memory:")
os.environ.setdefault("BETTER_AUTH_SECRET", "test-secret-key-minimum-32-characters-long")
os.environ.setdefault("DEBUG", "true")


# Test user IDs (known UUIDs for predictable testing)
TEST_USER_A_ID = UUID("11111111-1111-1111-1111-111111111111")
TEST_USER_B_ID = UUID("22222222-2222-2222-2222-222222222222")


@pytest.fixture
def test_secret() -> str:
    """Return the test JWT secret."""
    return os.environ["BETTER_AUTH_SECRET"]


@pytest.fixture
def user_a_id() -> UUID:
    """Return User A's UUID for testing."""
    return TEST_USER_A_ID


@pytest.fixture
def user_b_id() -> UUID:
    """Return User B's UUID for testing."""
    return TEST_USER_B_ID


def create_test_token(
    user_id: UUID,
    secret: str,
    expired: bool = False,
    invalid: bool = False
) -> str:
    """
    Create a JWT token for testing.

    Args:
        user_id: The user UUID to include in the token
        secret: The secret key for signing
        expired: If True, create an already-expired token
        invalid: If True, use wrong secret to create invalid signature

    Returns:
        JWT token string
    """
    now = datetime.now(timezone.utc)

    if expired:
        exp = now - timedelta(hours=1)  # Expired 1 hour ago
    else:
        exp = now + timedelta(hours=1)  # Valid for 1 hour

    payload = {
        "sub": str(user_id),
        "iat": now,
        "exp": exp,
    }

    signing_secret = "wrong-secret" if invalid else secret

    return jwt.encode(payload, signing_secret, algorithm="HS256")


@pytest.fixture
def valid_token_user_a(test_secret: str, user_a_id: UUID) -> str:
    """Create a valid JWT token for User A."""
    return create_test_token(user_a_id, test_secret)


@pytest.fixture
def valid_token_user_b(test_secret: str, user_b_id: UUID) -> str:
    """Create a valid JWT token for User B."""
    return create_test_token(user_b_id, test_secret)


@pytest.fixture
def expired_token(test_secret: str, user_a_id: UUID) -> str:
    """Create an expired JWT token."""
    return create_test_token(user_a_id, test_secret, expired=True)


@pytest.fixture
def invalid_token(test_secret: str, user_a_id: UUID) -> str:
    """Create a JWT token with invalid signature."""
    return create_test_token(user_a_id, test_secret, invalid=True)


@pytest.fixture
def auth_headers_user_a(valid_token_user_a: str) -> dict:
    """Return Authorization headers for User A."""
    return {"Authorization": f"Bearer {valid_token_user_a}"}


@pytest.fixture
def auth_headers_user_b(valid_token_user_b: str) -> dict:
    """Return Authorization headers for User B."""
    return {"Authorization": f"Bearer {valid_token_user_b}"}


@pytest.fixture
async def db_session() -> AsyncGenerator:
    """
    Provide a clean database session for each test.

    This fixture creates tables before each test and drops them after.
    Ensures test isolation.
    """
    from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
    from sqlalchemy.orm import sessionmaker
    from sqlmodel import SQLModel

    # Create test engine
    engine = create_async_engine(
        os.environ["DATABASE_URL"],
        echo=False,
    )

    # Create tables
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

    # Create session
    async_session = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )

    async with async_session() as session:
        yield session

    # Drop tables after test
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)

    await engine.dispose()
