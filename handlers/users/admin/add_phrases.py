import logging

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.types import Message, CallbackQuery

import keyboards
from data import config
from keyboards.inline.add_phrase_menu import add_phrase_menu_callback
from loader import dp, db


@dp.message_handler(Command("add_phrase"), user_id=config.ADMINS)
async def ask_add_phrase(msg: Message):
    user = msg.from_user
    phrase = msg.get_args()

    if len(phrase) == 0 or len(phrase) > 150:
        await msg.answer("Что-то не то с длинной твоей фразы, дорогой админ 🥴")
        return

    await msg.answer(phrase, reply_markup=keyboards.inline.add_phrase_menu)
    await msg.delete()

    logging.info(f"Admin-{user.username} want to add phrase -> {phrase}")


@dp.callback_query_handler(add_phrase_menu_callback.filter(action="add"))
async def add_phrase(call: CallbackQuery, state: FSMContext, callback_data: dict):
    user = call.from_user
    msg = call.message
    phrase = msg.text

    await db.push_new_phrase(phrase)

    await msg.delete()

    await call.answer("Фраза успешно добавлена!")

    logging.info(f"Admin-{user.username} add phrase -> {phrase}")


@dp.callback_query_handler(add_phrase_menu_callback.filter(action="cancel"))
async def cancel_adding_phrase(call: CallbackQuery, state: FSMContext, callback_data: dict):
    user = call.from_user
    msg = call.message
    phrase = msg.text

    await msg.delete()

    await call.answer("Фраза отменена!")

    logging.info(f"Admin-{user.username} cancel adding phrase -> {phrase}")
