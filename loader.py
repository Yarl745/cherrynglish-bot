import asyncio

import aioredis
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.fsm_storage.redis import RedisStorage2
from aioredis import Redis
from asgiref.sync import async_to_sync

from data import config
from utils.db_api.postgres import Database

bot = Bot(token=config.BOT_TOKEN, parse_mode=types.ParseMode.HTML)
storage = RedisStorage2()
dp = Dispatcher(bot, storage=storage)

loop = asyncio.get_event_loop()
db: Database = loop.run_until_complete(Database.create())

redis: Redis = async_to_sync(aioredis.create_redis_pool)('redis://localhost', db=2)

