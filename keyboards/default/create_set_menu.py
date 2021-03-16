from aiogram.types import ReplyKeyboardMarkup

from keyboards.default.btns import create_btn

create_set_menu = ReplyKeyboardMarkup(
    [
        [
            create_btn
        ]
    ],
    resize_keyboard=True
)