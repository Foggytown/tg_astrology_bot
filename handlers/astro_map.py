# global imports
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram import types
from aiogram.types import ReplyKeyboardRemove
import dateutil
import datetime

# local imports
from utils.util_funcs import exit_to_main_menu, make_row_keyboard
from handlers.filters import IsDeveloper
from handlers.states import AstroMap
from db import storage
from webparsing.astro_map import get_natal_chart

router = Router()


@router.message(IsDeveloper(), Command('astro_map'))
async def prepare_choosing(message: types.Message, state: FSMContext) -> None:
    user_id = 'id:' + str(message.from_user.id)
    user_date = await storage.hget(user_id, key='birth_date')
    if user_date is None or user_date == "unknown":
        await message.answer("Сначала введите свою дату рождения в меню")
        await exit_to_main_menu(message, state)
        return
    user_data = await state.get_data()
    if 'time' in user_data.keys() and 'city' in user_data.keys():
        await state.set_state(AstroMap.choosing_data)
        await message.answer("Вы уже вводили данные, вы хотите воспользоваться ими еще раз?",
                             reply_markup=make_row_keyboard(["Да", "Нет"]))
        return
    await choose_time(message, state)


@router.message(
    AstroMap.choosing_data,
    F.text.in_(["Да", "Нет"])
)
async def choose_data(message: types.Message, state: FSMContext) -> None:
    if message.text == "Да":
        await get_astro_map(message, state)
    else:
        await choose_time(message, state)


@router.message(IsDeveloper(), Command('astro_time'))
async def choose_time(message: types.Message, state: FSMContext) -> None:
    await state.set_state(AstroMap.choosing_time)
    await message.answer("Введите время своего рождения,"
                         "cделайте это в формате:\n11:00",
                         reply_markup=ReplyKeyboardRemove())


@router.message(
    AstroMap.choosing_time
)
async def time_processing(message: types.Message, state: FSMContext) -> None:
    try:
        parsed_time = dateutil.parser.parse(message.text)
        if datetime.time(hour=parsed_time.hour, minute=parsed_time.minute) != parsed_time.time():
            raise ValueError("Wrong time format")
        else:
            await state.update_data({'time': message.text})
            await state.set_state(AstroMap.choosing_city)
            await message.answer("Теперь введите город своего рождения в формате:\n"
                                 "Астрахань")

    except dateutil.parser._parser.ParserError and ValueError:
        await message.answer("Вы неправильно указали время,"
                             "cделайте это в формате:\n11:00")


@router.message(
    AstroMap.choosing_city
)
async def city_processing(message: types.Message, state: FSMContext):
    try:
        text = message.text.strip()
        if len(text.split()) != 1:
            raise ValueError("Too many words")
        if not text[0].isupper():
            raise ValueError("First letter is not capitalized")
        for char in message.text[1:]:
            if ord(char) > ord('я') or ord(char) < ord('а'):
                raise ValueError(f"Not russian symbol: {char}")
        if ord(text[0]) > ord('Я') or ord(text[0]) < ord('А'):
            raise ValueError(f"Not russian symbol: {text[0]}")
        await state.update_data({"city": text})
        await get_astro_map(message, state)
    except ValueError:
        await message.answer("Вы неправильно указали город, сделайте это в формате:\n"
                             "Астрахань")


@router.message(IsDeveloper(), Command('get_astro_map'))
async def get_astro_map(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    user_id = "id:" + str(message.from_user.id)
    birth_date = await storage.hget(user_id, key='birth_date')
    birth_date = dateutil.parser.parse(birth_date)
    birth_time = dateutil.parser.parse(user_data["time"]).time()
    pic_links = await get_natal_chart(birth_date.year, birth_date.month, birth_date.day,
                                      birth_time.hour, birth_time.minute, user_data["city"])
    if pic_links == []:
        await message.answer("Вы неправильно ввели данные, попробуйте еще раз, с самого начала")
        await exit_to_main_menu(message, state)
        return

    img1 = types.URLInputFile(pic_links[0])
    await message.answer_photo(
        img1,
        caption="Ваша натальная карта"
    )
    img2 = types.URLInputFile(pic_links[1])
    await message.answer_photo(
        img2,
        caption="Ваша натальная таблица"
    )

    await exit_to_main_menu(message, state)
