import asyncio
import logging
import re

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import CommandStart
from aiogram.types import Message, User
from aiogram.utils.deep_linking import decode_payload

import keyboards
from filters import IsUser
from loader import dp, db
from utils.db_api import redis_commands


@dp.message_handler(CommandStart(deep_link=re.compile(r"\w+"), encoded=True))
async def ask_to_connect(msg: Message):
    user = msg.from_user
    friend_id = int(decode_payload(msg.get_args()))

    if not (await redis_commands.is_user(user.id)):
        await bot_start(msg)

    if user.id == friend_id:
        return
    elif not (await redis_commands.is_user(friend_id)):
        await msg.answer("Такого пользователя не существует...", reply_markup=keyboards.default.get_bot_menu())
        await msg.answer_sticker("CAACAgIAAxkBAAIDXGBRMulMsWISnPXOc16gVBC-09MmAAIYAAPANk8T1vonv5xqGPgeBA")
        return
    elif await db.is_users_connected(user.id, friend_id):
        await msg.answer("Ты уже закреплен за этого пользователя...", reply_markup=keyboards.default.get_bot_menu())
        await msg.answer_sticker("CAACAgIAAxkBAAIEu2BTYZvJKYkVXcleRsmhI8V4q4A9AAINAAPANk8TpPnh9NR4jVMeBA")
        return

    friend = (await msg.bot.get_chat_member(friend_id, friend_id)).user

    await msg.answer(
        "Хочешь зацепится за @{}?".format(friend.username),
        reply_markup=keyboards.inline.get_connect_user_menu(friend_id)
    )

    logging.info(f"Ask @{user.username}-{user.id} to connect by connection_link to @{friend.username}-{friend_id}")


@dp.message_handler(CommandStart(), IsUser())
async def bot_start_by_user(msg: types.Message, state: FSMContext):
    user = msg.from_user

    await state.finish()

    await msg.answer(
        f"Привет, {user.full_name}, черешенка тебя помнит!",
        reply_markup=keyboards.default.get_bot_menu()
    )
    await msg.answer_sticker("CAACAgIAAxkBAAM_YE3OhegbsRHfhEIpsDR-_7h-psIAAg0AA8A2TxOk-eH01HiNUx4E")

    logging.info(f"@{user.username}-{user.id}(already user) start bot")


@dp.message_handler(CommandStart())
async def bot_start(msg: types.Message):
    user = User.get_current()

    await db.add_user(
        id=user.id,
        username=user.username,
        full_name=user.full_name
    )
    await redis_commands.set_new_user(user_id=user.id)

    await msg.answer(f"Привет, {user.full_name}!")
    await msg.answer(f"Я черешенка, которая будет помогать тебе изучать новые английские слова.")
    await msg.answer_sticker("CAACAgIAAxkBAAMDYEy1-FTmlee0a0sLpyxSk-M1LuwAAg0AA8A2TxOk-eH01HiNUx4E")

    await asyncio.sleep(4)

    wordbit_link = "https://play.google.com/store/apps/details?id=net.wordbit.enru"
    await msg.answer(
        f"Изночально весь функционал этого бота будет привязан к <a href='{wordbit_link}'>WordBit</a> приложению. "
        f"Если ты пользователь техники Apple, то тебе придётся найти другое приложение для нахождения слов. "
        f"Главное чтобы перевод и само слово находилось на одном экране!\n\n"
        f"Качай WordBit —> делай скрины слов, которые не знаешь —> заливай пачки скриншотов в бота "
        f"—> учи загруженные наборы слов 😉",
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
        "весело придумывать ассоциации к словам вместе с друзьями."
    )
    await msg.answer_sticker("CAACAgIAAxkBAAMHYEy-1ZR0YqSU-36ANwmSftFGAmkAAgYAA8A2TxPHyqL0sm5wdh4E")

    await asyncio.sleep(7)

    await msg.answer(
        "И помни, что чем глупее и постыднее ассоциация к слову — тем она лучше запомниться!",
        reply_markup=keyboards.default.get_bot_menu()
    )
    await msg.answer_sticker("CAACAgIAAxkBAAIJeWBWMPFTB6J-aY0eU2oWK_NVJ5B2AAIIAAPANk8Tb2wmC94am2keBA")

    logging.info(f"@{user.username}-{user.id} start bot")



