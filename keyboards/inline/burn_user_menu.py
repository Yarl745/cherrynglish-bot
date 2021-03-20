from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

from loader import db

burn_user_menu_callback = CallbackData("burn_user_menu", "friend_id", "username", "full_name")


async def get_burn_user_menu(user_id: int):
    burn_user_menu = InlineKeyboardMarkup(row_width=2)
    burn_user_menu.row_width = 2

    connected_users = await db.get_connected_users(user_id)

    for connected_user in connected_users:
        burn_user_menu.insert(
            InlineKeyboardButton(
                "{}🔥".format(connected_user["full_name"]),
                callback_data=burn_user_menu_callback.new(
                    friend_id=connected_user["id"],
                    username=connected_user["username"],
                    full_name=connected_user["full_name"]
                )
            )
        )

    return burn_user_menu
