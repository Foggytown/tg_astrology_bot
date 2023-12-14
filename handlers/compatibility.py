# global imports
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram import types

# local imports
from utils.util_data import zodiac_keyboard_builder, zodiac_list, zodiac_map
from utils.util_funcs import exit_to_main_menu
from handlers.filters import IsDeveloper
from handlers.states import Compatibility
from webparsing.parse_compatibility import get_compatibility_zodiac

router = Router()


@router.message(IsDeveloper(), Command('compare'))
async def compare_choose_first(message: types.Message, state: FSMContext):
    await state.set_state(Compatibility.choosing_first)
    await message.answer("Введите знак женщины🚺",
                         reply_markup=zodiac_keyboard_builder.as_markup(resize_keyboard=True))


@router.message(
    Compatibility.choosing_first,
    F.text.in_(zodiac_list)
)
async def compare_choose_second(message: types.Message, state: FSMContext) -> None:
    await state.set_data({'first_sign': message.text})
    await state.set_state(Compatibility.choosing_second)
    await message.answer("Введите знак мужчины🚹",
                         reply_markup=zodiac_keyboard_builder.as_markup(resize_keyboard=True))


@router.message(Compatibility.choosing_first)
async def sign_chosen_incorrectly(message: types.Message, state: FSMContext) -> None:
    await message.answer(
        text="Я не знаю такого варианта, нажмите на кнопку ниже.",
    )


@router.message(
    Compatibility.choosing_second,
    F.text.in_(zodiac_list)
)
async def choosen_both(message: types.Message, state: FSMContext) -> None:
    await state.set_state(Compatibility.finished)
    user_data = await state.get_data()
    first_sign = zodiac_map[user_data['first_sign']]
    second_sign = zodiac_map[message.text]
    await message.answer(text='Ваша совместимость: ' + await get_compatibility_zodiac(first_sign, second_sign))
    await exit_to_main_menu(message, state)


@router.message(Compatibility.choosing_second)
async def sign_chosen_incorrectly(message: types.Message, state: FSMContext) -> None:
    await message.answer(
        text="Я не знаю такого варианта, нажмите на кнопку ниже.",
    )
