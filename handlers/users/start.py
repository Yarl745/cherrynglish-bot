import asyncio

from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart

import keyboards
from loader import dp


@dp.message_handler(CommandStart())
async def bot_start(msg: types.Message):
    await msg.answer(f"Привет, {msg.from_user.full_name}!")
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
        "3) позволять дописвать свои ассоциации к словам;\n"
        "4) делиться наборами c другими участниками бота и "
        "весело придумывать ассоциации к словам вместе с друзьями.",
        reply_markup=keyboards.default.bot_menu
    )
    await msg.answer_sticker("CAACAgIAAxkBAAMHYEy-1ZR0YqSU-36ANwmSftFGAmkAAgYAA8A2TxPHyqL0sm5wdh4E")


