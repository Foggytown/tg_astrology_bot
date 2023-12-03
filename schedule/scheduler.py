# global imports
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from aiogram import Bot

# local imports
from schedule.msgs_scheduled import send_message_time, send_message_time2


def init_sch(bot: Bot):
    scheduler = AsyncIOScheduler()
    scheduler.add_job(send_message_time, "interval", seconds=10, args=(bot,))
    scheduler.add_job(send_message_time2, "cron", hour=11, minute=11, args=(bot,), timezone='Europe/Moscow')
    return scheduler
