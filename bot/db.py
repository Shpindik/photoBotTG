import asyncio
import asyncpg
import logging
import os

DB_NAME = os.getenv('POSTGRES_DB', 'postgres_db')
DB_USER = os.getenv('POSTGRES_USER', 'postgres_user')
DB_PASSWORD = os.getenv('POSTGRES_PASSWORD', 'postgres_password')
DB_HOST = os.getenv('DB_HOST', 'db')
DB_PORT = int(os.getenv('DB_PORT', 5432))
ADMIN_ID = os.getenv('ADMIN_ID', '123456789')


async def get_db_connection():
    return await asyncpg.connect(
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        host=DB_HOST,
        port=DB_PORT,
    )


async def init_db(retries: int = 10, delay: int = 2):
    last_error = None

    for attempt in range(1, retries + 1):
        try:
            conn = await get_db_connection()
            try:
                await conn.execute(
                    """
                    CREATE TABLE IF NOT EXISTS users (
                        user_id BIGINT PRIMARY KEY,
                        username VARCHAR(255),
                        fullname VARCHAR(255),
                        location TEXT,
                        timestamp TIMESTAMPTZ DEFAULT NOW()
                    );

                    CREATE TABLE IF NOT EXISTS user_problems (
                        id SERIAL PRIMARY KEY,
                        user_id BIGINT NOT NULL,
                        problem TEXT NOT NULL,
                        timestamp TIMESTAMPTZ DEFAULT NOW(),
                        CONSTRAINT fk_user FOREIGN KEY(user_id) REFERENCES users(user_id) ON DELETE CASCADE
                    );

                    CREATE TABLE IF NOT EXISTS phone_number (
                        id SERIAL PRIMARY KEY,
                        user_id BIGINT NOT NULL,
                        phone VARCHAR(20) NOT NULL,
                        timestamp TIMESTAMPTZ DEFAULT NOW(),
                        CONSTRAINT fk_user_phone FOREIGN KEY(user_id) REFERENCES users(user_id) ON DELETE CASCADE
                    );
                    """
                )
                return
            finally:
                await conn.close()
        except (asyncpg.PostgresError, OSError) as error:
            last_error = error
            logging.warning(
                'Не удалось инициализировать БД. Попытка %s/%s через %s сек. Ошибка: %s',
                attempt,
                retries,
                delay,
                error,
            )
            if attempt < retries:
                await asyncio.sleep(delay)

    raise last_error


async def save_user_data(
        user_id: int,
        username: str,
        fullname: str,
        location: str):
    conn = await get_db_connection()
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


async def save_phone_number(user_id: int, phone: str):
    conn = await get_db_connection()
    try:
        await conn.execute(
            """
            INSERT INTO phone_number (user_id, phone)
            VALUES ($1, $2)
            """,
            user_id, phone
        )
    finally:
        await conn.close()


async def save_problem(user_id: int, problem: str):
    conn = await get_db_connection()
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
    conn = await get_db_connection()
    try:
        user = await conn.fetchrow(
            """
            SELECT u.username, u.fullname, u.location, p.phone
            FROM users u
            LEFT JOIN phone_number p ON u.user_id = p.user_id
            WHERE u.user_id = $1
            ORDER BY p.timestamp DESC
            LIMIT 1
            """,
            user_id
        )
        if user:
            # Форматирование номера для админа (на случай, если в базе старый формат)
            phone = user['phone'] or '—'
            if phone != '—':
                digits = "".join(filter(str.isdigit, phone))
                if len(digits) == 11 and digits.startswith('8'):
                    phone = '+7' + digits[1:]
                elif len(digits) == 10:
                    phone = '+7' + digits
                elif len(digits) >= 11 and digits.startswith('7'):
                    phone = '+' + digits
                else:
                    phone = '+' + digits if digits else phone

            return (
                f"🚨 Федя! Шпингалеты лопнули 🔥\n\n"
                f"👤 Имя: {user['fullname'] or '—'}\n"
                f"😱 Юзернейм: @{user['username'] or '—'}\n"
                f"📱 Телефон: {phone}\n"
                f"📍 Локация: {user['location'] or '—'}\n"
                f"❗️ Проблема: {problem}"
            )
    finally:
        await conn.close()
