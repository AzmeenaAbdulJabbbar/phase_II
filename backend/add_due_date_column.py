"""
Script to add the missing due_date column to the task table.
This addresses the UndefinedColumnError when inserting tasks.
"""

import asyncio
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import text
from src.config import settings


async def add_due_date_column():
    """Add due_date column to task table if it doesn't exist."""
    print("Connecting to database...")

    # Create async engine using the same URL as in the app
    engine = create_async_engine(settings.DATABASE_URL)

    # Check if the column already exists
    async with engine.begin() as conn:
        column_exists_query = text("""
            SELECT column_name
            FROM information_schema.columns
            WHERE table_name = 'task' AND column_name = 'due_date';
        """)

        result = await conn.execute(column_exists_query)
        column_exists = result.fetchone()

        if column_exists:
            print("Column 'due_date' already exists in the task table.")
        else:
            # Add the due_date column
            alter_query = text("""
                ALTER TABLE task
                ADD COLUMN due_date TIMESTAMP WITHOUT TIME ZONE DEFAULT NULL;
            """)

            await conn.execute(alter_query)
            print("Column 'due_date' added successfully to the task table.")

    # Query the table structure in a separate connection
    async with engine.begin() as conn:
        print("\nUpdated table structure:")
        columns_query = text("""
            SELECT column_name, data_type, is_nullable, column_default
            FROM information_schema.columns
            WHERE table_name = 'task'
            ORDER BY ordinal_position;
        """)

        columns_result = await conn.execute(columns_query)
        for col in columns_result:
            print(f"  - {col[0]}: {col[1]}, nullable: {col[2]}, default: {col[3]}")


if __name__ == "__main__":
    print("Adding due_date column to task table...")
    asyncio.run(add_due_date_column())
    print("Migration completed successfully!")