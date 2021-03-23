import logging

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import Message, User

import keyboards
from filters import IsUser
from loader import dp
from utils import clean_previous_menu_msg
from utils.change_bot_menu import change_bot_menu


@dp.message_handler(IsUser(), text="Наборы📚")
async def show_sets(msg: Message, state: FSMContext):
    user = User.get_current()

    await clean_previous_menu_msg(msg, state)
    await state.finish()

    await state.update_data(page=1)

    sets_msg = await msg.answer(
        "Доступные наборы слов:",
        reply_markup=await keyboards.inline.get_sets_menu(user.id)
    )

    await state.update_data(sets_msg_id=sets_msg.message_id)

    await change_bot_menu(state)

    logging.info(f"Show connection menu for @{user.username}-{user.id}")

