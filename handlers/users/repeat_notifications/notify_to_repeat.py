import logging
from datetime import datetime

import keyboards
from data import config
from loader import db, bot, scheduler


async def schedule_repeat(user_id: int, set_id: int, set_name: str):
    repeat = await db.get_repeat(user_id, set_id)

    if not repeat:
        repeat_time = datetime.now() + config.repeat_stages[0]
        await db.add_repeat(
            user_id=user_id,
            set_id=set_id,
            set_name=set_name,
            repeat_stage=0,
            repeat_time=repeat_time
        )
        scheduler.add_job(notify_to_repeat, "date", run_date=repeat_time, args=(user_id, set_id, set_name))

    elif repeat["repeat_time"] <= datetime.now() and repeat["repeat_stage"] + 1 < len(config.repeat_stages):
        repeat_stage = repeat["repeat_stage"] + 1
        repeat_time = datetime.now() + config.repeat_stages[repeat_stage]
        await db.update_repeat(
            user_id, set_id,
            repeat_stage=repeat_stage,
            repeat_time=repeat_time
        )
        scheduler.add_job(notify_to_repeat, "date", run_date=repeat_time, args=(user_id, set_id, set_name))


async def notify_to_repeat(user_id: int, set_id: int, set_name: str):
    await bot.send_message(
        chat_id=user_id,
        text="Тебе нужно повторить набор —> {}".format(set_name),
        reply_markup=keyboards.inline.repeat_set_menu(set_id, set_name)
    )

    logging.info(f"User-{user_id} need to repeat set -> {set_name}")