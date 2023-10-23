from aiogram import Router, F
from aiogram import types
from db import get_db

router = Router()




@router.message(F.text)
async def echo_msg(message: types.Message):
    users_data = await get_db()
    #await bot(SendMessage(chat_id=302130806, text='anime'))
    await message.answer('anime '+' '.join(map(str,users_data)))
