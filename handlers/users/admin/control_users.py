from aiogram.dispatcher.filters import Command
from aiogram.types import Message

from data import config
from loader import dp


@dp.message_handler(Command("ban"), user_id=config.ADMINS)
async def ban_user(msg: Message):
    pass