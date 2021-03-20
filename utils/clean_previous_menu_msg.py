import logging

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import Message


async def clean_previous_menu_msg(msg: Message, state: FSMContext):
    user_id = types.User.get_current().id

    async with state.proxy() as data:
        learn_words_msg_id = data.get("learn_words_msg_id", None)
        sets_msg_id = data.get("sets_msg_id", None)
        connecting_msg_id = data.get("connecting_msg_id", None)

        if learn_words_msg_id:
            await msg.bot.delete_message(user_id, learn_words_msg_id)
        elif sets_msg_id:
            await msg.bot.delete_message(user_id, sets_msg_id)
        elif connecting_msg_id:
            await msg.bot.delete_message(user_id, connecting_msg_id)

    logging.info(f"Clean previous menu for User-{user_id}")