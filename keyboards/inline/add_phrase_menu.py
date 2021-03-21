from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

add_phrase_menu_callback = CallbackData("confirm_burn_menu", "action")

add_phrase_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                "Добавить☑️",
                callback_data=add_phrase_menu_callback.new(action="add")
            ),
            InlineKeyboardButton(
                "Отменить🔻",
                callback_data=add_phrase_menu_callback.new(action="cancel")
            )
        ]
    ]
)

