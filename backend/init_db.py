"""Simple database initialization script."""
import asyncio
from src.database import init_db

async def main():
    print("Initializing database tables...")
    await init_db()
    print("Database tables created successfully!")
    print("\nTables created:")
    print("  - task (id, user_id, title, description, completed, created_at, updated_at)")

if __name__ == "__main__":
    asyncio.run(main())
