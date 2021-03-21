from aiogram.dispatcher.filters import Command
from aiogram.types import Message

from data import config
from loader import dp, db


@dp.message_handler(Command("users"), user_id=config.ADMINS)
async def show_info(msg: Message):
    users = await db.get_users()
    out_text = "Users of the Cherrynglish:"
    for num, user in enumerate(users, start=1):
        out_text += f"\n[{num}] @{user['username']} with id={user['user_id']};"
    await msg.answer(out_text)



