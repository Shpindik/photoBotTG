from aiogram.types import (InlineKeyboardButton, InlineKeyboardMarkup,
                           KeyboardButton, ReplyKeyboardMarkup)
from dict import DICT as dict

go_main_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text='Вернуться в главное меню',
                callback_data='main_cd'
            ),
        ],
    ]
)

problem_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text=dict['problem_1'],
                callback_data='problem_1_cd'
            ),
        ],
        [
            InlineKeyboardButton(
                text=dict['problem_2'],
                callback_data='problem_2_cd'
            ),
        ],
        [
            InlineKeyboardButton(
                text=dict['problem_3'],
                callback_data='problem_3_cd'
            ),
        ],
        [
            InlineKeyboardButton(
                text=dict['problem_4'],
                callback_data='problem_4_cd'
            ),
        ],
        [
            InlineKeyboardButton(
                text=dict['problem_5'],
                callback_data='problem_5_cd'
            ),
        ],
        [
            InlineKeyboardButton(
                text=dict['problem_6'],
                callback_data='problem_6_cd'
            ),
        ],
        [
            InlineKeyboardButton(
                text=dict['problem_7'],
                callback_data='problem_7_cd'
            ),
        ],
        [
            InlineKeyboardButton(
                text=dict['problem_8'],
                callback_data='problem_8_cd'
            ),
        ],
        [
            InlineKeyboardButton(
                text=dict['problem_9'],
                callback_data='problem_9_cd'
            ),
        ],
        [
            InlineKeyboardButton(
                text=dict['problem_10'],
                callback_data='problem_10_cd'
            ),
        ],
        [
            InlineKeyboardButton(
                text=dict['problem_11'],
                callback_data='problem_11_cd'
            ),
        ],
    ]
)

problem_1_1_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text='Ура! Фото найдено',
                callback_data='yes_1_1_cd'
            ),
            InlineKeyboardButton(
                text='Фотографии нет',
                callback_data='no_1_1_cd'
            ),
        ],
    ]
)
problem_1_2_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text='Да',
                callback_data='yes_1_2_cd'
            ),
            InlineKeyboardButton(
                text='Нет',
                callback_data='no_1_2_cd'
            ),
        ],
    ]
)

problem_1_3_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text='Ура! Фото найдено',
                callback_data='yes_1_3_cd'
            ),
            InlineKeyboardButton(
                text='Фотографии нет',
                callback_data='no_1_3_cd'
            ),
        ],
    ]
)

problem_4_1_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text='Да, горит красным',
                callback_data='yes_4_1_cd'
            ),
            InlineKeyboardButton(
                text='Нет, не горит',
                callback_data='no_4_1_cd'
            ),
        ],
    ]
)

problem_4_2_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text='Да',
                callback_data='yes_4_2_cd'
            ),
            InlineKeyboardButton(
                text='Нет',
                callback_data='no_4_2_cd'
            ),
        ],
    ]
)

problem_4_3_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text='Нашли другую купюру',
                callback_data='yes_4_3_cd'
            ),
            InlineKeyboardButton(
                text='Нужен возврат',
                callback_data='no_4_3_cd'
            ),
        ],
    ]
)

problem_6_1_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text='Да',
                callback_data='yes_6_1_cd'
            ),
            InlineKeyboardButton(
                text='Нет',
                callback_data='no_6_1_cd'
            ),
        ],
    ]
)

problem_7_1_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text='Да',
                callback_data='yes_7_1_cd'
            ),
            InlineKeyboardButton(
                text='Нет',
                callback_data='no_7_1_cd'
            ),
        ],
    ]
)

close_task_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text='Закрыть задачу',
                callback_data='close_task_cd'
            ),
        ]
    ]
)

request_contact_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Отправить контакт", request_contact=True)]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)
