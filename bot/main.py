import asyncio
import logging
import os
import signal
import sys
import psycopg2

from aiogram import Bot, Dispatcher
from dotenv import load_dotenv
from handlers import router
from pathlib import Path

load_dotenv(dotenv_path=Path(__file__).resolve().parent.parent / ".env")

BOT_TOKEN = os.getenv('BOT_TOKEN')

DB_NAME = os.getenv('POSTGRES_DB', 'postgres_db')
DB_USER = os.getenv('POSTGRES_USER', 'postgres_user')
DB_PASSWORD = os.getenv('POSTGRES_PASSWORD', 'postgres_password')
DB_HOST = os.getenv('DB_HOST', 'db')
DB_PORT = int(os.getenv('DB_PORT', 5432))

LOG_DIR = os.path.join(os.path.dirname(__file__), "..", "logs")
LOG_FILE = os.path.join(LOG_DIR, "bot_errors.log")

os.makedirs(LOG_DIR, exist_ok=True)


def check_tokens():
    """ Check if all required environment variables are set """
    missing_tokens = [
        name for name, value in {
            'TOKEN': BOT_TOKEN,
        }.items() if not value
    ]
    if missing_tokens:
        logging.critical(f'Отсутствуют обязательные переменные окружения: \
                         {", ".join(missing_tokens)}')
    return not missing_tokens


bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
dp.include_router(router)


def get_db_connection():
    return psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )


async def main():
    print('Бот запущен. Для остановки нажмите Ctrl+C.')

    await bot.delete_webhook(drop_pending_updates=True)
    polling_task = asyncio.create_task(
        dp.start_polling(
            bot,
            allowed_updates=dp.resolve_used_update_types()
        )
    )

    def shutdown():
        polling_task.cancel()

    for sig in (signal.SIGINT, signal.SIGTERM):
        asyncio.get_event_loop().add_signal_handler(sig, shutdown)

    try:
        await polling_task
    except asyncio.CancelledError:
        pass

console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.DEBUG)

file_handler = logging.FileHandler(LOG_FILE, encoding='utf-8')
file_handler.setLevel(logging.ERROR)

formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

console_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)

if __name__ == '__main__':
    logging.basicConfig(
        level=logging.DEBUG,
        handlers=[console_handler, file_handler]
    )
    asyncio.run(main())
