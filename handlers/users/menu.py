import logging

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command

import keyboards
from filters import IsUser
from loader import dp


@dp.message_handler(Command("menu"), IsUser(), state="*")
async def get_menu(msg: types.Message, state: FSMContext):
    user = msg.from_user

    await state.finish()

    await msg.answer_sticker(
        "CAACAgIAAxkBAAEIy_FgWTfQPZZmlrwJ_nL3nhYXD-C7gQACBQADwDZPE_lqX5qCa011HgQ",
        reply_markup=keyboards.default.get_bot_menu()
    )

    logging.info(f"Get menu for @{user.username}-{user.id}")