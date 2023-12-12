# global imports
from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram import types

# local imports
from handlers.filters import IsDeveloper
from db import storage

router = Router()


@router.message(IsDeveloper(), Command("clear_state"))
async def cmd_clear(message: types.Message, state: FSMContext) -> None:
    prevstate = await state.get_state()
    await state.set_state(None)
    await message.answer(
        text=f"Стейт был {prevstate}, cбросил стейт"
    )


@router.message(IsDeveloper(), Command("clear_data"))
async def cmd_delete(message: types.Message):
    user_id = 'id:' + str(message.from_user.id)
    await storage.delete(user_id)
