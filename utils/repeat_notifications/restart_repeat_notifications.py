import logging
from datetime import datetime

from utils.repeat_notifications.notify_to_repeat import notify_to_repeat
from loader import db, scheduler


async def restart_repeat_notifications():
    repeats = await db.get_all_repeats()

    for repeat in repeats:
        if datetime.now() >= repeat["repeat_time"]:
            await notify_to_repeat(repeat["user_id"], repeat["set_id"], repeat["set_name"])
        else:
            scheduler.add_job(notify_to_repeat, "date", run_date=repeat["repeat_time"],
                              args=(repeat["user_id"], repeat["set_id"], repeat["set_name"]))

    logging.info("Restart all repeat notifications")