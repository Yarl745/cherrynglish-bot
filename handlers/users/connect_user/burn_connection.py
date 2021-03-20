import logging

from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery

import keyboards
from handlers.users.connect_user.click_connect import show_connection_link
from keyboards.inline.burn_user_menu import burn_user_menu_callback
from keyboards.inline.confirm_burn_menu import confirm_burn_menu_callback
from loader import dp, db


@dp.callback_query_handler(burn_user_menu_callback.filter())
async def ask_burn_connection(call: CallbackQuery, state: FSMContext, callback_data: dict):
    user = call.from_user
    msg = call.message

    username = callback_data["username"]
    friend_id = callback_data["friend_id"]

    await msg.edit_text(
        "Ты хочешь сжечь связь с @{} ?".format(username),
        reply_markup=keyboards.inline.get_confirm_burn_menu(friend_id)
    )

    logging.info(f"Ask @{user.username}-{user.id} to burn connection with @{username}-{friend_id}")


@dp.callback_query_handler(confirm_burn_menu_callback.filter(action="confirm"))
async def burn_connection(call: CallbackQuery, state: FSMContext, callback_data: dict):
    user = call.from_user
    msg = call.message

    with_user_id = int(callback_data["with_user_id"])

    await db.del_connected_user(user.id, with_user_id)
    await db.del_connected_user(with_user_id, user.id)

    await msg.delete()
    await state.finish()
    await show_connection_link(msg, state)

    logging.info(f"@{user.username}-{user.id} burned connection with {with_user_id}")


@dp.callback_query_handler(confirm_burn_menu_callback.filter(action="cancel"))
async def cancel_burn_connection(call: CallbackQuery, state: FSMContext, callback_data: dict):
    user = call.from_user
    msg = call.message

    with_user_id = int(callback_data["with_user_id"])

    await msg.delete()
    await state.finish()
    await show_connection_link(msg, state)

    logging.info(f"@{user.username}-{user.id} canceled burn connection with {with_user_id}")
