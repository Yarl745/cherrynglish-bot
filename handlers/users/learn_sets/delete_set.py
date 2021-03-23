import logging

from aiogram.dispatcher import FSMContext
from aiogram.types import Message, CallbackQuery

import keyboards
from filters import IsUser
from handlers.users.learn_sets.click_sets import show_sets
from keyboards.inline.burn_set_menu import burn_set_menu_callback
from loader import dp, db


@dp.message_handler(IsUser(), text="🔥Набор🔥")
async def ask_delete_set(msg: Message, state: FSMContext):
    user = msg.from_user

    set_name = (await state.get_data())["set_name"]

    await msg.answer(
        "Хочешь сжечь набор {}?".format(set_name),
        reply_markup=keyboards.inline.burn_set_menu
    )

    await msg.delete()

    logging.info(f"@{user.username}-{user.id} want deleted set {set_name}")


@dp.callback_query_handler(burn_set_menu_callback.filter(action="burn"))
async def delete_set(call: CallbackQuery, state: FSMContext, callback_data: dict):
    user = call.from_user
    msg = call.message

    set_id = (await state.get_data())["set_id"]
    await db.delete_set(set_id)

    await show_sets(msg, state)

    logging.info(f"@{user.username}-{user.id} deleted set-{set_id}")


@dp.callback_query_handler(burn_set_menu_callback.filter(action="cancel"))
async def cancel_delete_set(call: CallbackQuery, state: FSMContext, callback_data: dict):
    user = call.from_user
    msg = call.message

    await msg.delete()

    logging.info(f"@{user.username}-{user.id} canceled deleting set")
