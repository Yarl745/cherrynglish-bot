import logging

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