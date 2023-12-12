# global imports
from aiogram.methods.send_message import SendMessage
from aiogram import Bot

# local imports
from db import storage, get_horoscope_by_id


async def send_message_time(bot: Bot):
    async for key in storage.scan_iter("id:*"):
        tg_id = key[3:]
        print(tg_id, 'msg sch')
        if int(await storage.hget(key, 'sub')):
            await bot(SendMessage(chat_id=tg_id, text=await get_horoscope_by_id(tg_id)))


async def send_message_time2(bot: Bot):
    await bot(SendMessage(chat_id=302130806, text='anime2'))
