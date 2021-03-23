from aiogram.types import BotCommand

from loader import bot


async def register_bot_commands():
    commands = [
        BotCommand(command="/menu", description="Открыть главное меню")
    ]
    await bot.set_my_commands(commands)