from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

from loader import db

sets_menu_callback = CallbackData("sets_menu", "action", "set_id", "set_name")


next_page_btn = InlineKeyboardButton(
    "➡️", callback_data=sets_menu_callback.new(action="next_page", set_id=0, set_name=0)
)
previous_page_btn = InlineKeyboardButton(
    "⬅️", callback_data=sets_menu_callback.new(action="previous_page", set_id=0, set_name=0)
)



async def get_sets_menu(user_id: int, page: int = 1):
    sets_menu = InlineKeyboardMarkup(row_width=2)

    word_sets = await db.get_sets(user_id, page)

    for num, word_set in enumerate(word_sets, start=1):
        sets_menu.insert(
            InlineKeyboardButton(
                "[{}] {}".format(num, word_set["name"]),
                callback_data=sets_menu_callback.new(
                    action="open_set",
                    set_name=word_set["name"],
                    set_id=word_set["id"]
                )
            )
        )

    navigation_btns = []
    if len(word_sets) == 10 and page == 1:
        navigation_btns.append(next_page_btn)
    elif len(word_sets) == 10:
        navigation_btns.append(previous_page_btn)
        navigation_btns.append(next_page_btn)
    elif page > 1:
        navigation_btns.append(previous_page_btn)

    sets_menu.add(*navigation_btns)

    return sets_menu
