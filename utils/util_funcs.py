# global imports
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton

# local imports
from handlers.states import MainMenu
from utils.util_data import main_menu_keyboard_builder


def make_row_keyboard(items: list[str]) -> ReplyKeyboardMarkup:
    row = [KeyboardButton(text=item) for item in items]
    return ReplyKeyboardMarkup(keyboard=[row], resize_keyboard=True)


async def exit_to_main_menu(message: Message, state: FSMContext):
    await state.set_state(MainMenu.in_menu)
    await message.answer(
        text='Приветствуем вас в главном меню',
        reply_markup=main_menu_keyboard_builder.as_markup(resize_keyboard=True)
    )


def get_zodiac_sign_by_date(day, month):
    if month == 12:
        astro_sign = 'sagittarius' if (day < 22) else 'capricorn'

    elif month == 1:
        astro_sign = 'capricorn' if (day < 20) else 'aquarius'

    elif month == 2:
        astro_sign = 'aquarius' if (day < 19) else 'pisces'

    elif month == 3:
        astro_sign = 'pisces' if (day < 21) else 'aries'

    elif month == 4:
        astro_sign = 'aries' if (day < 20) else 'taurus'

    elif month == 5:
        astro_sign = 'taurus' if (day < 21) else 'gemini'

    elif month == 6:
        astro_sign = 'gemini' if (day < 21) else 'cancer'

    elif month == 7:
        astro_sign = 'cancer' if (day < 23) else 'leo'

    elif month == 8:
        astro_sign = 'leo' if (day < 23) else 'virgo'

    elif month == 9:
        astro_sign = 'virgo' if (day < 23) else 'libra'

    elif month == 10:
        astro_sign = 'libra' if (day < 23) else 'scorpio'

    elif month == 11:
        astro_sign = 'scorpio' if (day < 22) else 'sagittarius'
    else:
        raise ValueError(f"Wrong month: {month} or day: {day}")
    return astro_sign
