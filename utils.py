# global imports
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, Message
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.fsm.context import FSMContext
from handlers.states import MainMenu


def make_row_keyboard(items: list[str]) -> ReplyKeyboardMarkup:
    row = [KeyboardButton(text=item) for item in items]
    return ReplyKeyboardMarkup(keyboard=[row], resize_keyboard=True)


zodiac_list = [
    'Овен♈', 'Телец♉', 'Близнецы♊', 'Рак♋', 'Лев♌', 'Дева♍', 'Весы♎',
    'Скорпион♏', 'Стрелец♐', 'Козерог♑', 'Водолей♒', 'Рыбы♓'
]

zodiac_keyboard_builder = ReplyKeyboardBuilder()
for i in zodiac_list:
    zodiac_keyboard_builder.add(KeyboardButton(text=i))
zodiac_keyboard_builder.adjust(3)

zodiac_map = dict(zip(zodiac_list, ['Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo',
                                    'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces']))

main_menu_list = ['Изменить дату рождения или знак зодиака', 'Получить гороскоп на сегодня',
                  'Посмотреть совместимость с другим знаком', 'Посмотреть натальную карту']

main_menu_keyboard_builder = ReplyKeyboardBuilder()
for i in main_menu_list:
    main_menu_keyboard_builder.add(KeyboardButton(text=i))
main_menu_keyboard_builder.adjust(2)


async def exit_to_main_menu(message: Message, state: FSMContext):
    await state.set_state(MainMenu.in_menu)
    await message.answer(
        text='Приветствуем вас в гланом меню',
        reply_markup=main_menu_keyboard_builder.as_markup(resize_keyboard=True)
    )
