# global imports
import dateutil
from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram import types
import datetime

# local imports
from db import storage
from utils.util_funcs import exit_to_main_menu
from handlers.states import EditPostTime
from handlers.filters import IsDeveloper

router = Router()


@router.message(IsDeveloper(), Command("edit_time"))
async def start_editing(message: types.Message, state: FSMContext) -> None:
    await state.set_state(EditPostTime.deciding)
    user_id = 'id:' + str(message.from_user.id)
    user_subbed = await storage.hget(user_id, 'sub')
    if user_subbed is None:
        await message.answer("Какая-то ошибка, сначала измените данные через меню")
        await exit_to_main_menu(message, state)
        return
    if not int(user_subbed):
        await message.answer("Вы не подписаны на рассылку")
        await exit_to_main_menu(message, state)
        return
    else:
        await message.answer("Укажите время в которое вы хотите ежедневно получать свой гороскоп,"
                             "cделайте это в формате:\n11:00")


@router.message(
    EditPostTime.deciding
)
async def time_processing(message: types.Message, state: FSMContext) -> None:
    try:
        parsed_time = dateutil.parser.parse(message.text)
        if datetime.time(hour=parsed_time.hour, minute=parsed_time.minute) != parsed_time.time():
            raise ValueError("Wrong time format")
        else:
            user_id = 'id:' + str(message.from_user.id)
            await storage.hset(user_id, mapping={'post_time': str(parsed_time.time())})
            await message.answer(f"Время получения гороскопа установлено на {str(parsed_time.time())[:-3]}")
            await exit_to_main_menu(message, state)

    except dateutil.parser._parser.ParserError and ValueError:
        await message.answer("Вы неправильно указали время, cделайте это в формате:\n11:00")
