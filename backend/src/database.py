"""
Database configuration and session management.

Provides async database engine and session factory for SQLModel/SQLAlchemy.
Uses asyncpg driver for Neon PostgreSQL connection.
"""

from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel

from .config import settings

# Create async engine with connection pooling
# Note: pool_size and max_overflow are only for PostgreSQL, not SQLite
engine_kwargs = {
    "echo": settings.DEBUG,  # Log SQL in debug mode
}

# Add pooling options only for PostgreSQL (not SQLite)
if "postgresql" in settings.DATABASE_URL:
    engine_kwargs.update({
        "pool_pre_ping": True,  # Verify connections before use
        "pool_size": 5,  # Connection pool size
        "max_overflow": 10,  # Max additional connections
    })

engine = create_async_engine(settings.DATABASE_URL, **engine_kwargs)

# Async session factory
AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency that provides an async database session.

    Usage:
        @router.get("/items")
        async def get_items(session: AsyncSession = Depends(get_session)):
            ...

    Yields:
        AsyncSession: Database session for the request
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()


async def init_db() -> None:
    """
    Initialize database tables.

    Creates all tables defined in SQLModel metadata.
    Should be called once during application startup.
    """
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)


async def close_db() -> None:
    """
    Close database connections.

    Should be called during application shutdown.
    """
    await engine.dispose()
