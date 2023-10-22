from aiogram import Router, F
from aiogram.filters import Command
from aiogram import types
from aiogram.filters import CommandObject

router = Router()

@router.message(F.text)
async def echo_msg(message : types.Message):
    await message.answer(message.text+'\nYou said THAT????')