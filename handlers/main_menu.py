# global imports
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram import types
from dateutil import parser

# local imports
from utils import main_menu_keyboard_builder, main_menu_list, zodiac_keyboard_builder
from handlers.filters import IsDeveloper
from handlers.start_and_edit import edit_menu
from handlers.subcription import sub_menu
from handlers.states import MainMenu
from handlers.compatibility import compare_choose_first
from webparsing.horoscope import get_today_horoscope_by_date, get_today_horoscope_by_zodiac_sign
from db import storage

router = Router()


@router.message(IsDeveloper(), Command('menu'))
async def exit_to_menu(message: types.Message, state: FSMContext) -> None:
    await state.set_state(MainMenu.in_menu)
    await message.answer(
        text='Приветствуем вас в главном меню',
        reply_markup=main_menu_keyboard_builder.as_markup(resize_keyboard=True)
    )


@router.message(MainMenu.in_menu,
                F.text.in_(main_menu_list)
                )
async def command_in_main_menu(message: types.Message, state: FSMContext) -> None:
    if message.text == main_menu_list[0]:
        await edit_menu(message, state)
    elif message.text == main_menu_list[1]:
        await sub_menu(message, state)
    elif message.text == main_menu_list[2]:
        user_id = 'id:' + str(message.from_user.id)
        user_sign = await storage.hget(user_id, key='sign')
        if user_sign is not None:
            await message.answer(get_today_horoscope_by_zodiac_sign(user_sign.lower()))
            return
        else:
            user_date = await storage.hget(user_id, key='birth_date')
            user_date = parser.parse(user_date)
            await message.answer(get_today_horoscope_by_date(user_date.day, user_date.month))
    elif message.text == main_menu_list[3]:
        await compare_choose_first(message, state)
    else:
        await message.answer(
            text="Извините эта возможность еще не сделана"
        )
