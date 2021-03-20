from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData

from loader import db

word_menu_callback = CallbackData("word_menu", "action", "set_id",
                                  "word_id", "side")


def get_word_menu(word: dict, side: str = None):
    if side:
        word["side"] = "word" if side == "transl" else "transl"
    else:
        word["side"] = "word"

    change_side_btn = InlineKeyboardButton(
        "🔄", callback_data=word_menu_callback.new(action="change_side", **word)
    )
    know_word_btn = InlineKeyboardButton(
        "☑️", callback_data=word_menu_callback.new(action="know_word",  **word)
    )
    dont_know_word_btn = InlineKeyboardButton(
        "❓", callback_data=word_menu_callback.new(action="dont_know_word", **word)
    )

    word_menu: InlineKeyboardMarkup
    if word["side"] == "word":
        word_menu = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    know_word_btn, change_side_btn, dont_know_word_btn
                ]
            ]
        )
    elif word["side"] == "transl":
        add_assoc_btn = InlineKeyboardButton(
            "Добавить ассоциацию🦄",
            callback_data=word_menu_callback.new(action="add_assoc", **word)
        )
        word_menu = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    know_word_btn, change_side_btn, dont_know_word_btn
                ],
                [
                    add_assoc_btn
                ]
            ]
        )

    return word_menu
