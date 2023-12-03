# global imports
from aiogram.fsm.state import StatesGroup, State


class MainMenu(StatesGroup):
    in_menu = State()


class GreetingAndEdit(StatesGroup):
    start = State()
    date = State()
    sign = State()
    finish = State()
