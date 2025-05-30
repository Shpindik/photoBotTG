from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

problem_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text='Не вышли фотографии',
                callback_data='drop_photo_cd'
            ),
        ],
        [
            InlineKeyboardButton(
                text='Не работает экран',
                callback_data='drop_screen_cd'
            ),
        ],
    ]
)

problem_1_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text='Да',
                callback_data='yes_1_cd'
            ),
            InlineKeyboardButton(
                text='Нет',
                callback_data='no_1_cd'
            ),
        ],
    ]
)
