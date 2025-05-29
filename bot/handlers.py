import os
import re
from functools import wraps

from db import save_user_data

from states import LocationState
import kb
from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, ContentType, FSInputFile, Message

router = Router()


@router.message(Command('start'))
async def handle_start(message: Message, state: FSMContext):
    command_parts = message.text.split(maxsplit=1)
    args = command_parts[1] if len(command_parts) > 1 else None
    user_id = message.from_user.id
    username = message.from_user.username
    fullname = message.from_user.full_name

    location = args

    if location:
        await save_user_data(user_id, username, fullname, location)
        await message.answer(f'Данные {location} получены')
    else:
        await message.answer("Пожалуйста, введите ваш аргумент вручную:")
        await state.set_state(LocationState.waiting_for_location)


@router.message(LocationState.waiting_for_location)
async def handle_manual_argument(message: Message, state: FSMContext):
    args = message.text.strip()
    user_id = message.from_user.id
    username = message.from_user.username
    fullname = message.from_user.full_name

    location = args

    if len(location) < 4:
        await message.answer("Аргумент слишком короткий. Введите не менее 4 символов:")
        return
    elif len(location) > 100:
        await message.answer("Аргумент слишком длинный. Введите не более 100 символов:")
        return

    await save_user_data(user_id, username, fullname, location)
    await message.answer("Спасибо! Данные сохранены.")
    await state.clear()
