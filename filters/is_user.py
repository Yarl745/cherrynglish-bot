from aiogram.dispatcher.filters import BoundFilter
from aiogram.types import Message

from utils.db_api import redis_commands


class IsUser(BoundFilter):
    async def check(self, msg: Message, *args) -> bool:
        user = msg.from_user
        return await redis_commands.is_user(user.id)
