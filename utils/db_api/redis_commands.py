import logging
import random

from loader import redis


async def set_new_user(user_id: int) -> bool:
    if await is_user(user_id):
        logging.info(f"User--{user_id} already exists")
        return False

    await redis.hmset_dict(
        key=user_id,
        last_crop_range="")
    logging.info(f"Set User--{user_id} to redis_db")
    return True


async def is_user(user_id: int) -> bool:
    is_user_exist = await redis.exists(user_id)
    logging.info(f"User--{user_id} exist {is_user_exist}")
    return is_user_exist


async def get_last_crop_range_str(user_id: int) -> str:
    last_crop_range = await redis.hget(user_id, "last_crop_range", encoding="utf8")
    logging.info(f"For user-{user_id} get last_crop_range={last_crop_range}")
    return last_crop_range


async def set_last_crop_range(user_id: int, last_crop_range: list):
    await redis.hset(
        user_id,
        "last_crop_range",
        " ".join(str(param) for param in last_crop_range)
    )
    logging.info(f"For user-{user_id} set last_crop_range={last_crop_range}")


async def push_new_phrase(phrase: str):
    await redis.lpush("phrases", phrase)
    logging.info(f"Admin push new phrase: {phrase}")


async def get_random_phrase() -> str:
    phrases_len = await redis.llen("phrases")
    phrases: list = await redis.lrange("phrases", start=0, stop=phrases_len - 1, encoding="utf8")
    phrase: str = random.choice(phrases)
    logging.info(f"Get random phrase: {phrase}")
    return phrase


async def push_photo_id(user_id: int, photo_id: str):
    key = "photo_ids:{}".format(user_id)
    await redis.lpush(key, photo_id)


async def get_all_photo_ids(user_id: int) -> list:
    key = "photo_ids:{}".format(user_id)
    photo_ids = await redis.lrange(
        key,
        start=0,
        stop=(await redis.llen(key)) - 1,
        encoding="utf8"
    )
    logging.info(f"Get photo_ids for User-{user_id}")
    return photo_ids


async def get_photo_id(user_id: int, index: int = 0) -> str:
    key = "photo_ids:{}".format(user_id)
    photo_id = await redis.lindex(key, index, encoding="utf8")
    logging.info(f"Get photo_id for User-{user_id} -> {photo_id}")
    return photo_id


async def clean_all_photo_ids(user_id: int):
    key = "photo_ids:{}".format(user_id)
    if await redis.exists(key):
        await redis.delete(key)
        logging.info(f"For User-{user_id} clean all photo ids")