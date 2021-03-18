import logging

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import Message, MediaGroup
from aiogram.utils.deep_linking import get_start_link

import keyboards
from data.config import EXAMPLE_IMGS
from filters import IsUser
from loader import dp
from states.adding_set import AddingSet


@dp.message_handler(IsUser(), text="Зацепиться🖇")
async def show_connection_link(msg: Message, state: FSMContext):
    user = types.User.get_current()

    await state.finish()

    connect_link = await get_start_link(user.id, encode=True)

    await msg.answer(
        "Для того чтобы зацепиться за своего друга и совместить ваши наборы слов, "
        "отправь эту ссылку привязки: {}".format(connect_link),
        reply_markup=await keyboards.inline.get_burn_user_menu(user.id)
    )

    logging.info(f"Show connection menu for @{user.username}-{user.id}")

