# global imports
from aiogram import Router, F
from aiogram import types

# !!!!!!!!!!!! DEPRECATED and turned off

router = Router()


@router.message(F.text)
async def echo_msg(message: types.Message):
    # await bot(SendMessage(chat_id=, text='anime'))
    await message.answer('anime ')
