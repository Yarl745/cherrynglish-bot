import logging
import re

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import CommandStart
from aiogram.types import Message, CallbackQuery

import keyboards
from handlers.users.start import bot_start
from keyboards.inline.confirm_user_menu import confirm_user_menu_callback
from keyboards.inline.connect_user_menu import connect_user_menu_callback
from loader import dp, bot, db
from utils.db_api import redis_commands


@dp.callback_query_handler(connect_user_menu_callback.filter(action="connect"))
async def connect_to_user(call: CallbackQuery, state: FSMContext, callback_data: dict):
    user = call.from_user
    msg = call.message
    friend_id = callback_data["friend_id"]

    friend = (await msg.bot.get_chat_member(friend_id, friend_id)).user

    await msg.delete()
    await msg.answer("Ждём пока @{} подтвердит твой запрос...".format(friend.username),
                     reply_markup=keyboards.default.get_bot_menu())
    await msg.answer_sticker("CAACAgIAAxkBAAIDZmBRR71MwVLXmHhAWfgfJJTqajMxAAIMAAPANk8T4s8j_8J3n7weBA")

    await notify_to_confirm(friend_id, user.id)

    await call.answer()

    logging.info(f"@{user.username}-{user.id} want ot connect to @{friend.username}-{friend.id}")


@dp.callback_query_handler(confirm_user_menu_callback.filter(action="cancel"))
@dp.callback_query_handler(connect_user_menu_callback.filter(action="cancel"))
async def connect_to_user(call: CallbackQuery, state: FSMContext, callback_data: dict):
    msg = call.message
    user = call.from_user

    await msg.delete()

    await msg.answer("Соединение было отменено(", reply_markup=keyboards.default.get_bot_menu())
    await msg.answer_sticker("CAACAgIAAxkBAAIETGBTWE8YswPPd3Q_A0KVwjWhzuxJAAIRAAPANk8TDaqzD9wePuUeBA")

    await call.answer()

    logging.info(f"Cancel connection by @{user.username}-{user.id}")


@dp.callback_query_handler(confirm_user_menu_callback.filter(action="confirm"))
async def confirm_connection(call: CallbackQuery, state: FSMContext, callback_data: dict):
    msg = call.message
    user = call.from_user
    with_user_id = int(callback_data["with_user_id"])

    with_user = (await bot.get_chat_member(with_user_id, with_user_id)).user

    await msg.delete()

    if await db.is_users_connected(user.id, with_user_id):
        await msg.answer("Ты уже закреплен за этого пользователя...")
        await msg.answer_sticker("CAACAgIAAxkBAAIEu2BTYZvJKYkVXcleRsmhI8V4q4A9AAINAAPANk8TpPnh9NR4jVMeBA")
        return

    await db.add_connected_user(user.id, with_user_id)
    await db.add_connected_user(with_user_id, user.id)

    await notify_about_confirmation(user.id, with_user_id)
    await notify_about_confirmation(with_user_id, user.id)

    await call.answer()

    logging.info(f"Users @{user.username}-u{user.id} and @{with_user.username}-{with_user_id} connected")


async def notify_about_confirmation(confirm_user_id: int, by_user_id: int):
    by_user = (await bot.get_chat_member(by_user_id, by_user_id)).user

    await bot.send_message(
        confirm_user_id,
        "Поздравляем, теперь ты связан с @{} !".format(by_user.username)
    )
    await bot.send_sticker(confirm_user_id, "CAACAgIAAxkBAAIDa2BRzho0w8aQ-XG595YaZD7Ta1HdAAIKAAPANk8T_w2uPugO_QgeBA")


async def notify_to_confirm(confirm_user_id: int, by_user_id: int):
    by_user = (await bot.get_chat_member(by_user_id, by_user_id)).user

    await bot.send_message(
        confirm_user_id,
        "Пользователь @{} хочет зацепиться с тобой и объеденить ваши наборы... "
        "Какие твои действия?".format(by_user.username),
        reply_markup=keyboards.inline.get_confirm_user_menu(by_user_id)
    )

    logging.info(f"Notify user-{confirm_user_id} about connection with @{by_user.username}-{by_user.id}")




