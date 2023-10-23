# global imports
import asyncio
import logging
from aiogram import Bot, Dispatcher

import redis.asyncio as redis

# local imports
from config_reader import config
from schedule.scheduler import init_sch
from db import save_db, load_db, storage
from handlers import commands, texts

#anime
# Запуск бота
async def main():
    bot = Bot(token=config.bot_token.get_secret_value())
    logging.basicConfig(level=logging.INFO)
    scheduler = init_sch(bot)
    dp = Dispatcher()
    dp.include_routers(commands.router, texts.router)

    try:
        await load_db()
        scheduler.start()
        await dp.start_polling(bot, storage=storage)
    finally:
        await save_db()
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
