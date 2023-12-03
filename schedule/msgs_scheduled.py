# global imports
from aiogram.methods.send_message import SendMessage
from aiogram import Bot

# local imports
from db import storage


async def send_message_time(bot: Bot):
    async for key in storage.scan_iter("id:*"):
        print(key, 'msg sch')
        if int(await storage.hget(key, 'sub')):
            await bot(SendMessage(chat_id=key[3:], text='your horoscope for today bro'))


async def send_message_time2(bot: Bot):
    await bot(SendMessage(chat_id=302130806, text='anime2'))
