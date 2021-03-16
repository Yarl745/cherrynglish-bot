from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def get_text_menu(text: str) -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        [
            [
                KeyboardButton(text)
            ]
        ],
        resize_keyboard=True
    )
