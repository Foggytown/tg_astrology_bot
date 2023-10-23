from db import get_db
from aiogram.methods.send_message import SendMessage
from aiogram import Bot


async def send_message_time(bot: Bot):
    users_data = await get_db()
    print(users_data, 'msg sch')
    for user_id in users_data:
        await bot(SendMessage(chat_id=user_id, text='your horoscope for today bro'))


async def send_message_time2(bot: Bot):
    await bot(SendMessage(chat_id=302130806, text='anime2'))
