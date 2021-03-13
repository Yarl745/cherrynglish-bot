from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

bot_menu = ReplyKeyboardMarkup(
    [
        [
            KeyboardButton("Добавить✨"),
            KeyboardButton("Зацепиться🖇"),
            KeyboardButton("Наборы📚")
        ]
    ],
    resize_keyboard=True
)