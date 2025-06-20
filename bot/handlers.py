from db import save_user_data, save_problem, get_admin_message

import os
import time
from states import LocationState, ProblemState
import kb
from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from aiogram import Bot

from dict import DICT as dict

router = Router()


ADMIN_ID = os.getenv('ADMIN_ID', '123456789')
bot = Bot(token=os.getenv('BOT_TOKEN'))


@router.message(Command('start'))
async def handle_start(message: Message, state: FSMContext):
    data = await state.get_data()
    now = time.time()
    last_start = data.get('last_start', 0)
    if now - last_start < 3:
        return
    await state.update_data(last_start=now)

    user_state = await state.get_state()
    if user_state is not None:
        return

    command_parts = message.text.split(maxsplit=1)
    args = command_parts[1] if len(command_parts) > 1 else None
    user_id = message.from_user.id
    username = message.from_user.username
    fullname = message.from_user.full_name

    location = args

    if not username:
        await state.update_data(location=location)
        await message.answer(
            'У вас не установлен username в Telegram. Пожалуйста, '
            'отправьте свой контакт:',
            reply_markup=kb.request_contact_keyboard
        )
        return

    if location:
        await save_user_data(user_id, username, fullname, location)
        await message.answer(
            dict['hello'].format(name=message.from_user.first_name),
            reply_markup=kb.problem_keyboard,
            parse_mode='HTML'
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


@router.message(lambda m: m.contact is not None)
async def handle_contact(message: Message, state: FSMContext):
    user_id = message.from_user.id
    fullname = message.from_user.full_name
    phone_number = message.contact.phone_number

    data = await state.get_data()
    location = data.get('location')
    await save_user_data(
        user_id, phone_number, fullname, location)
    await message.answer(
        dict['hello'].format(name=message.from_user.first_name),
        reply_markup=kb.problem_keyboard
    )
    await state.clear()


@router.callback_query(F.data == 'main_cd')
async def handle_main_cd(callback: CallbackQuery):
    await callback.message.edit_text(
        text=dict['hello'].format(name=callback.from_user.first_name),
        reply_markup=kb.problem_keyboard
    )


@router.callback_query(F.data == 'problem_1_cd')
async def handle_problem_1_cd(callback: CallbackQuery):
    await callback.message.edit_text(
        text=dict['problem_1_1'],
        reply_markup=kb.problem_1_1_keyboard
    )


@router.callback_query(F.data == 'yes_1_1_cd')
async def handle_yes_1_cd(callback: CallbackQuery):
    await callback.message.edit_text(
        text=dict['goodbye'].format(name=callback.from_user.first_name),
        reply_markup=kb.go_main_keyboard
    )


@router.callback_query(F.data == 'no_1_1_cd')
async def handle_no_1_cd(callback: CallbackQuery):
    await callback.message.edit_text(
        text='Были слышны звуки печати?',
        reply_markup=kb.problem_1_2_keyboard
    )


@router.callback_query(F.data == 'yes_1_2_cd')
async def handle_yes_1_2_cd(callback: CallbackQuery):
    await callback.message.edit_text(
        text='Кажется, фото застряло. Попробуйте достать его рукой',
        reply_markup=kb.problem_1_3_keyboard
    )


@router.callback_query(F.data == 'no_1_2_cd')
async def handle_no_1_2_cd(callback: CallbackQuery):
    await save_problem(
        callback.from_user.id,
        dict['problem_1']+dict['error_1']
    )
    message = await get_admin_message(
        callback.from_user.id,
        dict['problem_1']+dict['error_1']
    )
    await bot.send_message(
        chat_id=ADMIN_ID,
        text=message,
        reply_markup=kb.close_task_keyboard
    )
    await callback.message.edit_text(
        text=dict['sorry'],
        reply_markup=kb.go_main_keyboard,
        parse_mode='HTML'
    )


@router.callback_query(F.data == 'yes_1_3_cd')
async def handle_yes_1_3_cd(callback: CallbackQuery):
    await callback.message.edit_text(
        text=dict['goodbye'].format(name=callback.from_user.first_name),
        reply_markup=kb.go_main_keyboard
    )


@router.callback_query(F.data == 'no_1_3_cd')
async def handle_no_1_3_cd(callback: CallbackQuery):
    await save_problem(
        callback.from_user.id,
        dict['problem_1']+dict['error_2']
    )
    message = await get_admin_message(
        callback.from_user.id,
        dict['problem_1']+dict['error_2']
    )
    await bot.send_message(
        chat_id=ADMIN_ID,
        text=message,
        reply_markup=kb.close_task_keyboard
    )
    await callback.message.edit_text(
        text=dict['sorry'],
        reply_markup=kb.go_main_keyboard,
        parse_mode='HTML'
    )


@router.callback_query(F.data == 'problem_2_cd')
async def handle_problem_2_cd(callback: CallbackQuery):
    await save_problem(callback.from_user.id, dict['problem_2'])
    message = await get_admin_message(callback.from_user.id, dict['problem_2'])
    await bot.send_message(
        chat_id=ADMIN_ID,
        text=message,
        reply_markup=kb.close_task_keyboard
    )
    await callback.message.edit_text(
        text=dict['sorry'],
        reply_markup=kb.go_main_keyboard,
        parse_mode='HTML'
    )


@router.callback_query(F.data == 'problem_3_cd')
async def handle_problem_3_cd(callback: CallbackQuery):
    await save_problem(callback.from_user.id, dict['problem_3'])
    message = await get_admin_message(callback.from_user.id, dict['problem_3'])
    await bot.send_message(
        chat_id=ADMIN_ID,
        text=message,
        reply_markup=kb.close_task_keyboard
    )
    await callback.message.edit_text(
        text=dict['sorry_3'],
        reply_markup=kb.go_main_keyboard,
        parse_mode='HTML'
    )


@router.callback_query(F.data == 'problem_4_cd')
async def handle_problem_4_cd(callback: CallbackQuery):
    await callback.message.edit_text(
        text='Подскажите, купюроприемник горит красным цветом?',
        reply_markup=kb.problem_4_1_keyboard
    )


@router.callback_query(F.data == 'yes_4_1_cd')
async def handle_yes_4_1_cd(callback: CallbackQuery):
    await callback.message.edit_text(
        text='Вы уже оплатили часть стоимости?',
        reply_markup=kb.problem_4_2_keyboard
    )


@router.callback_query(F.data == 'yes_4_2_cd')
async def handle_yes_4_2_cd(callback: CallbackQuery):
    await save_problem(
        callback.from_user.id,
        dict['problem_4']+dict['error_3']
    )
    message = await get_admin_message(
        callback.from_user.id,
        dict['problem_4']+dict['error_3']
    )
    await bot.send_message(
        chat_id=ADMIN_ID,
        text=message,
        reply_markup=kb.close_task_keyboard
    )
    await callback.message.edit_text(
        text=dict['sorry'],
        reply_markup=kb.go_main_keyboard,
        parse_mode='HTML'
    )


@router.callback_query(F.data == 'no_4_2_cd')
async def handle_no_4_2_cd(callback: CallbackQuery):
    await callback.message.edit_text(
        text=dict['goodbye_4'].format(name=callback.from_user.first_name),
        reply_markup=kb.go_main_keyboard,
        parse_mode='HTML'
    )


@router.callback_query(F.data == 'no_4_1_cd')
async def handle_no_4_1_cd(callback: CallbackQuery):
    await callback.message.edit_text(
        text=dict['problem_4_1'],
        reply_markup=kb.problem_4_3_keyboard,
        parse_mode='HTML'
    )


@router.callback_query(F.data == 'yes_4_3_cd')
async def handle_yes_4_3_cd(callback: CallbackQuery):
    await callback.message.edit_text(
        text=dict['goodbye'].format(name=callback.from_user.first_name),
        reply_markup=kb.go_main_keyboard
    )


@router.callback_query(F.data == 'no_4_3_cd')
async def handle_no_4_3_cd(callback: CallbackQuery):
    await save_problem(
        callback.from_user.id,
        dict['problem_4']+dict['error_4']
    )
    message = await get_admin_message(
        callback.from_user.id,
        dict['problem_4']+dict['error_4']
    )
    await bot.send_message(
        chat_id=ADMIN_ID,
        text=message,
        reply_markup=kb.close_task_keyboard
    )
    await callback.message.edit_text(
        text=dict['sorry_4_3'],
        reply_markup=kb.go_main_keyboard,
        parse_mode='HTML'
    )


@router.callback_query(F.data == 'problem_5_cd')
async def handle_problem_5_cd(callback: CallbackQuery):
    await save_problem(callback.from_user.id, dict['problem_5'])
    message = await get_admin_message(callback.from_user.id, dict['problem_5'])
    await bot.send_message(
        chat_id=ADMIN_ID,
        text=message,
        reply_markup=kb.close_task_keyboard
    )
    await callback.message.edit_text(
        text=dict['sorry'],
        reply_markup=kb.go_main_keyboard,
        parse_mode='HTML'
    )


@router.callback_query(F.data == 'problem_6_cd')
async def handle_problem_6_cd(callback: CallbackQuery):
    await callback.message.edit_text(
        text='На экране горит красный крест?',
        reply_markup=kb.problem_6_1_keyboard

    )


@router.callback_query(F.data == 'yes_6_1_cd')
async def handle_yes_6_1_cd(callback: CallbackQuery):
    await save_problem(
        callback.from_user.id,
        dict['problem_6']+dict['error_5']
    )
    message = await get_admin_message(
        callback.from_user.id,
        dict['problem_6']+dict['error_5']
    )
    await bot.send_message(
        chat_id=ADMIN_ID,
        text=message,
        reply_markup=kb.close_task_keyboard
    )
    await callback.message.edit_text(
        text=dict['problem_6_1'],
        reply_markup=kb.go_main_keyboard,
        parse_mode='HTML'
    )


@router.callback_query(F.data == 'no_6_1_cd')
async def handle_no_6_1_cd(callback: CallbackQuery):
    await save_problem(
        callback.from_user.id,
        dict['problem_6']+dict['error_6']
    )
    message = await get_admin_message(
        callback.from_user.id,
        dict['problem_6']+dict['error_6']
    )
    await bot.send_message(
        chat_id=ADMIN_ID,
        text=message,
        reply_markup=kb.close_task_keyboard
    )
    await callback.message.edit_text(
        text=dict['problem_6_1'],
        reply_markup=kb.go_main_keyboard,
        parse_mode='HTML'
    )


@router.callback_query(F.data == 'problem_7_cd')
async def handle_problem_7_cd(callback: CallbackQuery):
    await callback.message.edit_text(
        text='На экране поменялась заставка?',
        reply_markup=kb.problem_7_1_keyboard
    )


@router.callback_query(F.data == 'yes_7_1_cd')
async def handle_yes_7_1_cd(callback: CallbackQuery):
    await save_problem(
        callback.from_user.id,
        dict['problem_7']+dict['error_8']
    )
    message = await get_admin_message(
        callback.from_user.id,
        dict['problem_7']+dict['error_8']
    )
    await bot.send_message(
        chat_id=ADMIN_ID,
        text=message,
        reply_markup=kb.close_task_keyboard
    )
    await callback.message.edit_text(
        text=dict['sorry'],
        reply_markup=kb.go_main_keyboard,
        parse_mode='HTML'
    )


@router.callback_query(F.data == 'no_7_1_cd')
async def handle_no_7_1_cd(callback: CallbackQuery):
    await save_problem(
        callback.from_user.id,
        dict['problem_7']+dict['error_7']
    )
    message = await get_admin_message(
        callback.from_user.id,
        dict['problem_7']+dict['error_7']
    )
    await bot.send_message(
        chat_id=ADMIN_ID,
        text=message,
        reply_markup=kb.close_task_keyboard
    )
    await callback.message.edit_text(
        text=dict['sorry'],
        reply_markup=kb.go_main_keyboard,
        parse_mode='HTML'
    )


@router.callback_query(F.data == 'problem_8_cd')
async def handle_problem_8_cd(callback: CallbackQuery):
    await save_problem(callback.from_user.id, dict['problem_8'])
    message = await get_admin_message(callback.from_user.id, dict['problem_8'])
    await bot.send_message(
        chat_id=ADMIN_ID,
        text=message,
        reply_markup=kb.close_task_keyboard
    )
    await callback.message.edit_text(
        text=dict['sorry'],
        reply_markup=kb.go_main_keyboard,
        parse_mode='HTML'
    )


@router.callback_query(F.data == 'problem_9_cd')
async def handle_problem_9_cd(callback: CallbackQuery):
    await save_problem(callback.from_user.id, dict['problem_9'])
    message = await get_admin_message(callback.from_user.id, dict['problem_9'])
    await bot.send_message(
        chat_id=ADMIN_ID,
        text=message,
        reply_markup=kb.close_task_keyboard
    )
    await callback.message.edit_text(
        text=dict['sorry'],
        reply_markup=kb.go_main_keyboard,
        parse_mode='HTML'
    )


@router.callback_query(F.data == 'problem_10_cd')
async def handle_problem_10_cd(callback: CallbackQuery):
    await save_problem(callback.from_user.id, dict['problem_10'])
    message = await get_admin_message(
        callback.from_user.id, dict['problem_10'])
    await bot.send_message(
        chat_id=ADMIN_ID,
        text=message,
        reply_markup=kb.close_task_keyboard
    )
    await callback.message.edit_text(
        text=dict['sorry'],
        reply_markup=kb.go_main_keyboard,
        parse_mode='HTML'
    )


@router.callback_query(F.data == 'problem_11_cd')
async def handle_problem_11_cd(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        text='Пожалуйста, опишите свою проблему:',
    )
    await state.set_state(ProblemState.waiting_for_description)


@router.message(ProblemState.waiting_for_description)
async def handle_problem_description(message: Message, state: FSMContext):
    user_id = message.from_user.id
    problem_description = message.text.strip()

    await save_problem(user_id, problem_description)

    message_to_admin = await get_admin_message(user_id, problem_description)
    await bot.send_message(
        chat_id=ADMIN_ID,
        text=message_to_admin,
        reply_markup=kb.close_task_keyboard
    )
    await message.answer(
        text=dict['sorry'],
        reply_markup=kb.go_main_keyboard,
        parse_mode='HTML'
    )
    await message.bot.delete_message(
        chat_id=message.chat.id,
        message_id=message.message_id - 1
    )
    await state.clear()


@router.callback_query(F.data == 'close_task_cd')
async def close_request_handler(callback: CallbackQuery):
    await callback.message.delete()
    await callback.answer("Заявка закрыта", show_alert=False)
