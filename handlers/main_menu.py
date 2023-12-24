# global imports
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram import types

# local imports
from utils.util_data import main_menu_keyboard_builder, main_menu_list
from db import get_horoscope_by_id
from handlers.states import MainMenu
from handlers.filters import IsDeveloper
from handlers import start_and_edit, subcription, compatibility, edit_post_time, astro_map

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
        await start_and_edit.edit_menu(message, state)
    elif message.text == main_menu_list[1]:
        await subcription.sub_menu(message, state)
    elif message.text == main_menu_list[2]:
        await message.answer(await get_horoscope_by_id(message.from_user.id))
    elif message.text == main_menu_list[3]:
        await edit_post_time.start_editing(message, state)
    elif message.text == main_menu_list[4]:
        await compatibility.compare_choose_first(message, state)
    elif message.text == main_menu_list[5]:
        await astro_map.prepare_choosing(message, state)
    else:
        await message.answer(
            text="Извините но как вы сюда попали"
        )


@router.message(MainMenu.in_menu)
async def command_in_main_menu(message: types.Message, state: FSMContext) -> None:
    await message.answer("Такого варианта нету, нажмите на кнопку ниже")
