from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from keyboards.default.btns import back_btn

back_menu = ReplyKeyboardMarkup(
    [
        [
            back_btn
        ]
    ],
    resize_keyboard=True
)