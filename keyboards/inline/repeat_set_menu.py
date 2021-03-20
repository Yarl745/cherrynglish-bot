from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

from keyboards.inline.sets_menu import sets_menu_callback


def repeat_set_menu(set_id: int, set_name: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    "Повторить🤓",
                    callback_data=sets_menu_callback.new(
                        action="open_set",
                        set_name=set_name,
                        set_id=set_id
                    )
                )
            ]
        ]
    )
