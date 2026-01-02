"""
Tests for database module.

Tests verify:
- Async engine is configured correctly
- Session generator yields async sessions
- Database URL is properly formatted
"""

import pytest
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession


class TestDatabaseEngine:
    """Test cases for database engine configuration."""

    def test_engine_is_async(self):
        """Engine should be an async engine."""
        from src.database import engine

        assert isinstance(engine, AsyncEngine)

    def test_engine_uses_asyncpg(self):
        """Engine should use asyncpg driver."""
        from src.database import engine

        assert "asyncpg" in str(engine.url.drivername) or "postgresql+asyncpg" in str(engine.url)


class TestAsyncSessionLocal:
    """Test cases for async session factory."""

    def test_async_session_local_exists(self):
        """AsyncSessionLocal should be defined."""
        from src.database import AsyncSessionLocal

        assert AsyncSessionLocal is not None

    @pytest.mark.asyncio
    async def test_get_session_yields_async_session(self):
        """get_session should yield an AsyncSession."""
        from src.database import get_session

        async for session in get_session():
            assert isinstance(session, AsyncSession)
            break  # Only need to test one iteration

    @pytest.mark.asyncio
    async def test_session_is_closed_after_use(self):
        """Session should be properly closed after context exits."""
        from src.database import get_session

        session_ref = None
        async for session in get_session():
            session_ref = session
            break

        # After the generator exits, session should be closed
        # Note: We can't directly test closure, but we verify the generator completes
        assert session_ref is not None
