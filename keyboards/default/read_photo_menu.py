from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from keyboards.default.btns import back_btn, next_btn

read_photo_menu = ReplyKeyboardMarkup(
    [
        [
            next_btn
        ],
        [
            back_btn
        ]
    ],
    resize_keyboard=True
)