import asyncio
import logging

from aiogram.dispatcher import FSMContext
from aiogram.types import Message, User

import keyboards
from loader import bot
from utils.db_api import redis_commands


async def change_bot_menu(state: FSMContext):
    user = User.get_current()

    phrase = await redis_commands.get_random_phrase()
    set_id = (await state.get_data()).get("set_id", None)

    msg: Message
    if set_id:
        msg = await bot.send_message(
            user.id, text=phrase,
            reply_markup=keyboards.default.get_bot_menu(in_set=True)
        )
    else:
        msg = await bot.send_message(
            user.id, text=phrase,
            reply_markup=keyboards.default.get_bot_menu(in_set=False)
        )

    await state.update_data(last_phrase_msg_id=msg.message_id)

    logging.info(f"Update menu for @{user.username}-{user.id}")
