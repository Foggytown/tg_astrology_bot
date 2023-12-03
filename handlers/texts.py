# global imports
from aiogram import Router, F
from aiogram import types

router = Router()


@router.message(F.text)
async def echo_msg(message: types.Message):
    # await bot(SendMessage(chat_id=302130806, text='anime'))
    await message.answer('anime ')
