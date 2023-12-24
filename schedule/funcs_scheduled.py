# global imports
from aiogram.methods.send_message import SendMessage
from aiogram import Bot
from dateutil import parser
from datetime import datetime, timedelta

# local imports
from db import storage, get_horoscope_by_id

threshold = timedelta(seconds=120)


async def check_time(bot: Bot) -> None:
    async for key in storage.scan_iter("id:*"):
        tg_id = key[3:]
        print(tg_id, 'msg sch')
        now = datetime.now()
        if int(await storage.hget(key, 'sub')):
            if abs((parser.parse(await storage.hget(key, 'post_time')) - now)) <= threshold:
                await bot(SendMessage(chat_id=tg_id, text=await get_horoscope_by_id(tg_id)))


# not used, legacy
async def send_message_time(bot: Bot) -> None:
    async for key in storage.scan_iter("id:*"):
        tg_id = key[3:]
        print(tg_id, 'msg sch')
        if int(await storage.hget(key, 'sub')):
            await bot(SendMessage(chat_id=tg_id, text=await get_horoscope_by_id(tg_id)))


# not used, legacy
async def send_message_time2(bot: Bot) -> None:
    await bot(SendMessage(chat_id=302130806, text='anime2'))
