# global imports
import asyncio
import logging
from aiogram import Bot, Dispatcher

# local imports
from config_reader import config
from schedule.scheduler import init_sch
from db import storage
from handlers import commands_deprecated, texts, start_and_edit, main_menu, subcription, debug_cmd


# Запуск бота
async def main():
    bot = Bot(token=config.bot_token.get_secret_value())
    logging.basicConfig(level=logging.INFO)
    scheduler = init_sch(bot)
    dp = Dispatcher()
    dp.include_routers(debug_cmd.router,
                       main_menu.router,
                       start_and_edit.router,
                       subcription.router,
                       commands.router,
                       texts.router
                       )

    try:
        scheduler.start()
        await dp.start_polling(bot, storage=storage)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
