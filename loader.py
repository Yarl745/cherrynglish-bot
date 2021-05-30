import asyncio

import aioredis
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.fsm_storage.redis import RedisStorage2
from aioredis import Redis
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from asgiref.sync import async_to_sync

from data import config
from data.config import REDIS_PASSWORD, REDIS_HOST, REDIS_PORT
from utils.db_api.postgres import Database

bot = Bot(token=config.BOT_TOKEN, parse_mode=types.ParseMode.HTML)
storage = RedisStorage2(
    host=REDIS_HOST,
    port=REDIS_PORT,
)
dp = Dispatcher(bot, storage=storage)

loop = asyncio.get_event_loop()
db: Database = loop.run_until_complete(Database.create())

# redis://:p2844fdfe9ec9da59733...
# redis_uri = f"redis://{REDIS_HOST}"
redis_uri = f"redis://{REDIS_HOST}:{REDIS_PORT}"
redis: Redis = async_to_sync(aioredis.create_redis_pool)(redis_uri, db=1)

scheduler = AsyncIOScheduler()
