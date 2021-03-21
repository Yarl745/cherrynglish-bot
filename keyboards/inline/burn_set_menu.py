from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

burn_set_menu_callback = CallbackData("burn_set_menu", "action")

burn_set_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                "Сжечь🔥️",
                callback_data=burn_set_menu_callback.new(action="burn")
            ),
            InlineKeyboardButton(
                "Отменить🔻",
                callback_data=burn_set_menu_callback.new(action="cancel")
            )
        ]
    ]
)

