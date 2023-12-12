# global imports
from aiogram import Router,F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram import types

# local imports
from db import storage
from utils.util_data import subscription_list
from utils.util_funcs import exit_to_main_menu, make_row_keyboard
from handlers.states import Subscription
from handlers.filters import IsDeveloper

router = Router()


@router.message(IsDeveloper(), Command("subscribe"))
async def sub_menu(message: types.Message, state: FSMContext):
    await state.set_state(Subscription.deciding)
    user_id = 'id:' + str(message.from_user.id)
    user_subbed = await storage.hget(user_id, 'sub')
    if user_subbed is None:
        await message.answer("Какая-то ошибка, сначала измените данные через меню.")
        await exit_to_main_menu(message, state)
        return
    await message.answer(text='Выберите', reply_markup=make_row_keyboard([subscription_list[int(user_subbed)], subscription_list[2]]))


@router.message(
    Subscription.deciding,
    F.text.in_(subscription_list)
)
async def sub_processing(message: types.Message, state: FSMContext):
    if message.text == subscription_list[0]:
        await cmd_sub(message)
    elif message.text == subscription_list[1]:
        await cmd_unsub(message)
    await exit_to_main_menu(message, state)


async def cmd_sub(message: types.Message):
    user_id = 'id:' + str(message.from_user.id)
    await storage.hset(user_id, mapping={'sub': 1})
    await message.answer("Спасибо, вы подписались на ежедневную рассылку гороскопов.")


async def cmd_unsub(message: types.Message):
    user_id = 'id:' + str(message.from_user.id)
    await storage.hset(user_id, mapping={'sub': 0})
    await message.answer("Вы были отписаны от рассылки.")
