# global imports
from aiogram.fsm.state import StatesGroup, State


class MainMenu(StatesGroup):
    in_menu = State()


class GreetingAndEdit(StatesGroup):
    start = State()
    date = State()
    sign = State()
    finish = State()


class Subscription(StatesGroup):
    deciding = State()


class Compatibility(StatesGroup):
    choosing_first = State()
    choosing_second = State()
    finished = State()


class EditPostTime(StatesGroup):
    deciding = State()


class AstroMap(StatesGroup):
    choosing_data = State()
    choosing_time = State()
    choosing_city = State()
