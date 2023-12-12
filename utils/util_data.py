# global imports
from aiogram.types import KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder

# lists

zodiac_list = [
    'Овен♈', 'Телец♉', 'Близнецы♊', 'Рак♋', 'Лев♌', 'Дева♍', 'Весы♎',
    'Скорпион♏', 'Стрелец♐', 'Козерог♑', 'Водолей♒', 'Рыбы♓'
]

zodiac_map = dict(zip(zodiac_list, ['Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo',
                                    'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces']))

sign_to_number = {'Aries': 1, 'Taurus': 2, 'Gemini': 3,
                  'Cancer': 4, 'Leo': 5, 'Virgo': 6,
                  'Libra': 7, 'Scorpio': 8, 'Sagittarius': 9,
                  'Capricorn': 10, 'Aquarius': 11, 'Pisces': 12}

main_menu_list = ['Изменить дату рождения или знак зодиака', 'Подписка на рассылку', 'Получить гороскоп на сегодня',
                  'Посмотреть совместимость между двумя знаками', 'Посмотреть натальную карту']

subscription_list = ["Подписаться", "Отписаться", "Вернуться в главное меню"]

# keyboard builders

zodiac_keyboard_builder = ReplyKeyboardBuilder()
for i in zodiac_list:
    zodiac_keyboard_builder.add(KeyboardButton(text=i))
zodiac_keyboard_builder.adjust(3)

main_menu_keyboard_builder = ReplyKeyboardBuilder()
main_menu_keyboard_builder.row(
    KeyboardButton(text=main_menu_list[0]),
    KeyboardButton(text=main_menu_list[1])
)
main_menu_keyboard_builder.row(
    KeyboardButton(text=main_menu_list[2])
)
main_menu_keyboard_builder.row(
    KeyboardButton(text=main_menu_list[3]),
    KeyboardButton(text=main_menu_list[4])
)



