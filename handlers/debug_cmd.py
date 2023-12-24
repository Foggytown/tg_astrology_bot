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
async def cmd_delete(message: types.Message, state: FSMContext) -> None:
    user_id = 'id:' + str(message.from_user.id)
    data = await state.get_data()
    await message.answer("All data cleared\n"
                         f"FSM data was:\n{data}\n"
                         f"DB data was:\n{await storage.hgetall(user_id)}\n"
                         f"State was {await state.get_state()}")
    await state.set_data({})
    await storage.delete(user_id)
    await state.set_state(None)
