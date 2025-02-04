from aiogram.fsm.state import State, StatesGroup


class Register(StatesGroup):
    name = State()
    surname = State()
    parent_name = State()
    birthday_date = State()
    phone_number = State()
    help_category = State()
