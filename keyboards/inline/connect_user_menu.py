from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData


connect_user_menu_callback = CallbackData("connect_user_menu", "action", "friend_id")


def get_connect_user_menu(friend_id: int):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    "Зацепиться🖇",
                    callback_data=connect_user_menu_callback.new(action="connect", friend_id=friend_id)
                ),
                InlineKeyboardButton(
                    "Отменить🔻",
                    callback_data=connect_user_menu_callback.new(action="cancel", friend_id=friend_id)
                )
            ]
        ]
    )
