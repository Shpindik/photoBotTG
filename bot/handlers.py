from db import save_user_data

from states import LocationState
import kb
import asyncio
from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from dict import DICT as dict

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
        await message.answer(
            dict['hello'].format(name=message.from_user.first_name),
            reply_markup=kb.problem_keyboard
        )
    else:
        await message.answer(dict['get_location_manual'])
        await state.set_state(LocationState.waiting_for_location)


@router.message(LocationState.waiting_for_location)
async def handle_manual_argument(message: Message, state: FSMContext):
    args = message.text.strip()
    user_id = message.from_user.id
    username = message.from_user.username
    fullname = message.from_user.full_name

    location = args

    if len(location) < 4:
        await message.answer('Введите не менее 4 символов:')
        return
    elif len(location) > 100:
        await message.answer('Введите не более 100 символов:')
        return

    await save_user_data(user_id, username, fullname, location)
    await message.answer(
        dict['hello'].format(name=message.from_user.first_name),
        reply_markup=kb.problem_keyboard
    )
    await state.clear()


@router.callback_query(F.data == 'drop_photo_cd')
async def handle_drop_photo_cd(callback: CallbackQuery):
    await callback.message.edit_text(
        dict['fix_1']
    )
    await asyncio.sleep(10)
    await callback.message.answer(
        text='Получилось?',
        reply_markup=kb.problem_1_keyboard
    )


@router.callback_query(F.data == 'yes_1_cd')
async def handle_yes_1_cd(callback: CallbackQuery):
    await callback.message.edit_text(
        dict['fix_1_accept']
    )


@router.callback_query(F.data == 'no_1_cd')
async def handle_no_1_cd(callback: CallbackQuery):
    await callback.message.edit_text(
        dict['fix_1_decline']
    )


@router.callback_query(F.data == 'drop_screen_cd')
async def handle_drop_screen_cd(callback: CallbackQuery):
    await callback.message.edit_text(
        dict['fix_2']
    )
