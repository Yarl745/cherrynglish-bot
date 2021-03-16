import asyncio
import logging

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import CommandStart

import keyboards
from filters import IsUser
from loader import dp, db
from utils.db_api import redis_commands


@dp.message_handler(CommandStart(), IsUser())
async def bot_start_by_user(msg: types.Message):
    user = msg.from_user

    await msg.answer(
        f"Привет, {user.full_name}, черешенка тебя помнит!",
        reply_markup=keyboards.default.bot_menu
    )
    await msg.answer_sticker("CAACAgIAAxkBAAM_YE3OhegbsRHfhEIpsDR-_7h-psIAAg0AA8A2TxOk-eH01HiNUx4E")

    logging.info(f"@{user.username}-{user.id}(already user) start bot")


@dp.message_handler(CommandStart())
async def bot_start(msg: types.Message):
    user = msg.from_user

    await db.add_user(
        id=user.id,
        username=user.username,
        full_name=user.full_name
    )
    await redis_commands.set_new_user(user_id=user.id)

    await msg.answer(f"Привет, {user.full_name}!")
    await msg.answer(f"Я черешенка, которая будет помогать тебе изучать "
                     f"новые английские слова.")
    await msg.answer_sticker("CAACAgIAAxkBAAMDYEy1-FTmlee0a0sLpyxSk-M1LuwAAg0AA8A2TxOk-eH01HiNUx4E")

    await asyncio.sleep(4)

    wordbit_link = "https://play.google.com/store/apps/details?id=net.wordbit.enru"
    await msg.answer(
        f"Изночально весь функционал этого бота будет привязан к <a href='{wordbit_link}'>WordBit</a> приложению.\n\n"
        f"Качайте WordBit —> делайте скрины слов, которые не знаете —> заливайте пачки скриншотов в бота "
        f"—> учите загруженные наборы слов 😉",
        disable_web_page_preview=True
    )
    await msg.answer_sticker("CAACAgIAAxkBAAMFYEy83a4vWMnl1iaN1Gi07fd6fugAAh0AA8A2TxNe2KbcQT3eSB4E")

    await asyncio.sleep(7)

    await msg.answer(
        "Преимущество этого бота в том, что он будет:\n"
        "1) предоставлять удобный механизм изучения слов;\n"
        "2) напоминать, когда нужно повторить определённый набор, для того чтобы "
        "ты не забывал(-а) выученные слова;\n"
        "3) позволять дописывать свои ассоциации к словам;\n"
        "4) давать возможность делиться наборами c другими участниками бота и "
        "весело придумывать ассоциации к словам вместе с друзьями.",
        reply_markup=keyboards.default.bot_menu
    )
    await msg.answer_sticker("CAACAgIAAxkBAAMHYEy-1ZR0YqSU-36ANwmSftFGAmkAAgYAA8A2TxPHyqL0sm5wdh4E")

    logging.info(f"@{user.username}-{user.id} start bot")



