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
from utils import clean_previous_menu_msg


@dp.message_handler(IsUser(), text="Зацепиться🖇")
async def show_connection_link(msg: Message, state: FSMContext):
    user = types.User.get_current()

    await clean_previous_menu_msg(msg, state)
    await state.finish()

    connect_link = await get_start_link(user.id, encode=True)

    connecting_msg_id = (await msg.answer(
        "Для того чтобы зацепиться за своего друга и совместить ваши наборы слов, "
        "отправь эту ссылку привязки: {}".format(connect_link),
        reply_markup=await keyboards.inline.get_burn_user_menu(user.id)
    )).message_id

    await state.update_data(connecting_msg_id=connecting_msg_id)
    await msg.delete()

    logging.info(f"Show connection menu for @{user.username}-{user.id}")

