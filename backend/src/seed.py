"""
Database seeding script for Phase II Backend API.

Purpose: Populate the database with sample data for manual testing of user isolation.

Usage:
    python -m src.seed                    # Add sample data
    python -m src.seed --reset            # Clear and reseed database

Creates:
- Two test users (User A and User B) with known UUIDs
- 5 tasks for each user to verify user isolation
"""

import asyncio
import argparse
from uuid import UUID
from datetime import datetime, timezone

from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from .database import engine, AsyncSessionLocal, init_db
from .models import Task


# Known test user IDs (matching those in conftest.py for consistency)
USER_A_ID = UUID("11111111-1111-1111-1111-111111111111")
USER_B_ID = UUID("22222222-2222-2222-2222-222222222222")


async def clear_database(session: AsyncSession):
    """
    Clear all tasks from the database.

    Args:
        session: Database session
    """
    print("🗑️  Clearing existing tasks...")

    # Delete all tasks
    result = await session.execute(select(Task))
    tasks = result.scalars().all()

    for task in tasks:
        await session.delete(task)

    await session.commit()
    print(f"✅ Deleted {len(tasks)} existing tasks")


async def seed_user_tasks(session: AsyncSession, user_id: UUID, user_name: str):
    """
    Create sample tasks for a user.

    Args:
        session: Database session
        user_id: User's UUID
        user_name: User's display name (for task titles)
    """
    print(f"\n📝 Creating tasks for {user_name} ({user_id})...")

    tasks_data = [
        {
            "title": f"{user_name}: Complete project documentation",
            "description": "Write comprehensive docs for the API endpoints",
            "completed": False,
        },
        {
            "title": f"{user_name}: Review pull requests",
            "description": "Check and approve pending PRs from team members",
            "completed": True,
        },
        {
            "title": f"{user_name}: Fix bug in authentication",
            "description": "Investigate and resolve the JWT token refresh issue",
            "completed": False,
        },
        {
            "title": f"{user_name}: Update dependencies",
            "description": None,  # Test tasks without descriptions
            "completed": False,
        },
        {
            "title": f"{user_name}: Deploy to production",
            "description": "Deploy the latest release to production environment",
            "completed": True,
        },
    ]

    created_tasks = []
    for task_data in tasks_data:
        task = Task(
            user_id=user_id,
            title=task_data["title"],
            description=task_data["description"],
            completed=task_data["completed"],
        )
        session.add(task)
        created_tasks.append(task)

    await session.commit()

    # Refresh to get IDs
    for task in created_tasks:
        await session.refresh(task)

    print(f"✅ Created {len(created_tasks)} tasks for {user_name}")

    # Display summary
    completed_count = sum(1 for t in created_tasks if t.completed)
    print(f"   - {completed_count} completed")
    print(f"   - {len(created_tasks) - completed_count} pending")


async def seed_database(reset: bool = False):
    """
    Seed the database with sample data.

    Args:
        reset: If True, clear existing data before seeding
    """
    print("\n" + "=" * 60)
    print("🌱 Database Seeding Script")
    print("=" * 60)

    # Initialize database (create tables if needed)
    print("\n📦 Initializing database...")
    await init_db()
    print("✅ Database tables ready")

    async with AsyncSessionLocal() as session:
        if reset:
            await clear_database(session)

        # Seed User A
        await seed_user_tasks(session, USER_A_ID, "User A")

        # Seed User B
        await seed_user_tasks(session, USER_B_ID, "User B")

    print("\n" + "=" * 60)
    print("✅ Database seeding complete!")
    print("=" * 60)
    print("\n📊 Test User Credentials:")
    print(f"   User A ID: {USER_A_ID}")
    print(f"   User B ID: {USER_B_ID}")
    print("\n💡 You can now test user isolation by:")
    print("   1. Creating JWT tokens with these user IDs")
    print("   2. Making API requests to /api/tasks/")
    print("   3. Verifying User A sees only User A's tasks")
    print("   4. Verifying User B sees only User B's tasks")
    print()


async def verify_seeding(session: AsyncSession):
    """
    Verify that seeding was successful.

    Args:
        session: Database session
    """
    print("\n🔍 Verifying seeded data...")

    # Check User A's tasks
    result_a = await session.execute(select(Task).where(Task.user_id == USER_A_ID))
    user_a_tasks = result_a.scalars().all()

    # Check User B's tasks
    result_b = await session.execute(select(Task).where(Task.user_id == USER_B_ID))
    user_b_tasks = result_b.scalars().all()

    print(f"   User A: {len(user_a_tasks)} tasks")
    print(f"   User B: {len(user_b_tasks)} tasks")

    assert len(user_a_tasks) == 5, f"Expected 5 tasks for User A, found {len(user_a_tasks)}"
    assert len(user_b_tasks) == 5, f"Expected 5 tasks for User B, found {len(user_b_tasks)}"

    print("✅ Verification passed!")


def main():
    """Main entry point for the seeding script."""
    parser = argparse.ArgumentParser(
        description="Seed the database with sample data for testing"
    )
    parser.add_argument(
        "--reset",
        action="store_true",
        help="Clear existing data before seeding",
    )
    args = parser.parse_args()

    # Run seeding
    asyncio.run(seed_database(reset=args.reset))


if __name__ == "__main__":
    main()
