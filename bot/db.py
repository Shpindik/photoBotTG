import asyncpg
import os

DB_NAME = os.getenv('POSTGRES_DB', 'postgres_db')
DB_USER = os.getenv('POSTGRES_USER', 'postgres_user')
DB_PASSWORD = os.getenv('POSTGRES_PASSWORD', 'postgres_password')
DB_HOST = os.getenv('DB_HOST', 'db')
DB_PORT = int(os.getenv('DB_PORT', 5432))
ADMIN_ID = os.getenv('ADMIN_ID', '123456789')


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
            ON CONFLICT (user_id) DO UPDATE SET
            username = EXCLUDED.username,
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


async def save_problem(user_id: int, problem: str):
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
            INSERT INTO user_problems (user_id, problem)
            VALUES ($1, $2)
            """,
            user_id, problem
        )
    finally:
        await conn.close()


async def get_admin_message(user_id: int, problem: str):
    conn = await asyncpg.connect(
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        host=DB_HOST,
        port=DB_PORT,
    )
    try:
        user = await conn.fetchrow(
            "SELECT username, fullname, location "
            "FROM users WHERE user_id = $1",
            user_id
        )
        if user:
            return (
                f"🚨 Шеф! Все сломалось 🔥\n\n"
                f"👤 Имя: {user['fullname'] or '—'}\n"
                f"😱 Username: @{user['username'] or '—'}\n"
                f"📍 Локация: {user['location'] or '—'}\n"
                f"❗️ Проблема: {problem}"
            )
    finally:
        await conn.close()
