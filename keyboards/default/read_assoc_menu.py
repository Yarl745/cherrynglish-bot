from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from keyboards.default.btns import back_btn

read_assoc_menu = ReplyKeyboardMarkup(
    [
        [
            KeyboardButton("Отчистить все ассоциации🚽")
        ],
        [
            back_btn
        ]
    ],
    resize_keyboard=True
)