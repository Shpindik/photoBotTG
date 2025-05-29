import asyncpg
import os

DB_NAME = os.getenv('POSTGRES_DB', 'postgres_db')
DB_USER = os.getenv('POSTGRES_USER', 'postgres_user')
DB_PASSWORD = os.getenv('POSTGRES_PASSWORD', 'postgres_password')
DB_HOST = os.getenv('DB_HOST', 'db')
DB_PORT = int(os.getenv('DB_PORT', 5432))


async def save_user_data(
        user_id: int,
        username: str,
        fullname: str,
        location: str):
    conn = await asyncpg.connect(
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        host=DB_HOST,
        port=DB_PORT,
    )
    try:
        await conn.execute(
            """
            INSERT INTO users (
            user_id,
            username,
            fullname,
            location,
            timestamp)
            VALUES ($1, $2, $3, $4, NOW())
            ON CONFLICT (user_id) DO UPDATE
            SET username = EXCLUDED.username,
                fullname = EXCLUDED.fullname,
                location = EXCLUDED.location,
                timestamp = NOW()
            """,
            user_id,
            username,
            fullname,
            location
        )
    finally:
        await conn.close()
