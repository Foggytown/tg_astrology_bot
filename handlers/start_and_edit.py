# global imports
from aiogram import Router, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram import types
from aiogram.types import ReplyKeyboardRemove
from dateutil import parser

# local imports
from db import storage, basic_mapping
from utils import make_row_keyboard, zodiac_list, zodiac_map, zodiac_keyboard_builder, exit_to_main_menu
from handlers.filters import IsDeveloper
from handlers.states import GreetingAndEdit

router = Router()


@router.message(IsDeveloper(), Command("clear_state"))
async def cmd_clear(message: types.Message, state: FSMContext) -> None:
    prevstate = await state.get_state()
    await state.set_state(None)
    await message.answer(
        text=f"Стейт был {prevstate}, cбросил стейт"
    )


@router.message(StateFilter(None), Command("start1"))
async def cmd_start1(message: types.Message, state: FSMContext) -> None:
    await message.answer(
        text="Выберите:",
        reply_markup=make_row_keyboard(['Ввести знак зодиака', 'Ввести дату'])
    )
    await state.set_state(GreetingAndEdit.start)


@router.message(StateFilter(None), Command("edit"))
async def cmd_edit(message: types.Message, state: FSMContext) -> None:
    await message.answer(
        text="Выберите что вы хотите изменить:",
        reply_markup=make_row_keyboard(['Изменить знак зодиака', 'Изменить дату рождения'])
    )
    await state.set_state(GreetingAndEdit.start)


@router.message(
    GreetingAndEdit.start,
    F.text.in_(['Ввести знак зодиака', 'Ввести дату', 'Изменить знак зодиака', 'Изменить дату рождения'])
)
async def variant_chosen(message: types.Message, state: FSMContext) -> None:
    if message.text in ['Ввести знак зодиака', 'Изменить знак зодиака']:
        await state.set_state(GreetingAndEdit.sign)
        await message.answer(
            text="Хорошо, выберите знак зодиака",
            reply_markup=zodiac_keyboard_builder.as_markup(resize_keyboard=True)
        )
    else:
        await state.set_state(GreetingAndEdit.date)
        await message.answer(
            text="Хорошо, напишите дату в формате:\n21.03.2021",
            reply_markup=ReplyKeyboardRemove()
        )


@router.message(GreetingAndEdit.start)
async def variant_chosen_incorrectly(message: types.Message, state: FSMContext) -> None:
    await message.answer(
        text="Я не знаю такого варианта, нажмите на кнопку ниже",
    )


@router.message(GreetingAndEdit.date)
async def date_received(message: types.Message, state: FSMContext) -> None:
    try:
        print(message.text)
        datetime = parser.parse(message.text)
        date = datetime.date()
        user_id = 'id:' + str(message.from_user.id)
        if (await storage.hgetall(user_id)) == {}:
            await storage.hset(user_id, mapping=basic_mapping)
            await storage.hset(user_id, mapping={'birth_date': str(date)})
            await message.answer(
                text="Дата успешно введена"
            )

        else:
            await storage.hset(user_id, mapping={'birth_date': str(date)})
            await message.answer(
                text="Дата успешно изменена"
            )

        await state.set_state(None)

    except parser._parser.ParserError as error:
        await message.answer('Вы неправильно указали дату своего рождения, укажите ее в формате:\n21.03.2021')


@router.message(
    GreetingAndEdit.sign,
    F.text.in_(zodiac_list)
)
async def sign_chosen(message: types.Message, state: FSMContext) -> None:
    user_id = 'id:' + str(message.from_user.id)
    if (await storage.hgetall(user_id)) == {}:
        await storage.hset(user_id, mapping=basic_mapping)
        await storage.hset(user_id, mapping={'sign': zodiac_map[message.text]})
        await message.answer(
            text="Знак успешно введен",
            reply_markup=ReplyKeyboardRemove()
        )

    else:
        await storage.hset(user_id, mapping={'sign': zodiac_map[message.text]})
        await message.answer(
            text="Знак успешно изменен",
            reply_markup=ReplyKeyboardRemove()
        )
    await exit_to_main_menu(message, state)


@router.message(GreetingAndEdit.sign)
async def sign_chosen_incorrectly(message: types.Message, state: FSMContext) -> None:
    await message.answer(
        text="Я не знаю такого варианта, нажмите на кнопку ниже.",
    )
