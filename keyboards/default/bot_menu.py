from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def get_bot_menu(in_set: bool = False) -> ReplyKeyboardMarkup:
    markup: list
    if in_set:
        markup = [
            [
                KeyboardButton("Добавить✨"),
                KeyboardButton("🔥Набор🔥"),
                KeyboardButton("Наборы📚")
            ]
        ]
    else:
        markup = [
            [
                KeyboardButton("Добавить✨"),
                KeyboardButton("Зацепиться🖇"),
                KeyboardButton("Наборы📚")
            ]
        ]
    return ReplyKeyboardMarkup(markup, resize_keyboard=True)
