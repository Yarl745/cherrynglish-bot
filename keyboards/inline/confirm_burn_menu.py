from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData


confirm_burn_menu_callback = CallbackData("confirm_burn_menu", "action", "with_user_id")


def get_confirm_burn_menu(with_user_id: int):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    "Сжечь🔥",
                    callback_data=confirm_burn_menu_callback.new(action="confirm", with_user_id=with_user_id)
                ),
                InlineKeyboardButton(
                    "Отменить🔻",
                    callback_data=confirm_burn_menu_callback.new(action="cancel", with_user_id=with_user_id)
                )
            ]
        ]
    )
