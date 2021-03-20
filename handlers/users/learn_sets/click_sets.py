import logging

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import Message

import keyboards
from filters import IsUser
from loader import dp
from utils import clean_previous_menu_msg


@dp.message_handler(IsUser(), text="Наборы📚")
async def show_sets(msg: Message, state: FSMContext):
    user = msg.from_user

    await clean_previous_menu_msg(msg, state)
    await state.finish()

    await state.update_data(page=1)

    sets_msg_id = (await msg.answer(
        "Доступные наборы слов:",
        reply_markup=await keyboards.inline.get_sets_menu(user.id)
    )).message_id

    await state.update_data(sets_msg_id=sets_msg_id)
    await msg.delete()

    logging.info(f"Show connection menu for @{user.username}-{user.id}")

