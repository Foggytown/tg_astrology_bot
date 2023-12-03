# global imports
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram import types

# local imports
from utils import main_menu_keyboard_builder, main_menu_list
from handlers.filters import IsDeveloper
from handlers.start_and_edit import cmd_edit
from handlers.states import MainMenu

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
        await cmd_edit(message, state)
    else:
        await message.answer(
            text="Извините эта возможность еще не сделана"
        )
