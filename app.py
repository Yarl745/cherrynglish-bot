from aiogram import executor

from utils.repeat_notifications.restart_repeat_notifications import restart_repeat_notifications
from loader import db, scheduler
from handlers import dp
from utils.notify_admins import on_startup_notify


async def on_startup(dispatcher):
    # Уведомляет про запуск
    await on_startup_notify(dispatcher)

    await db.create_all_tables_ine()
    await db.config_timezone()

    await restart_repeat_notifications()


if __name__ == '__main__':
    scheduler.start()
    executor.start_polling(dp, on_startup=on_startup)
