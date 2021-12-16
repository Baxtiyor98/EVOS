from aiogram.dispatcher.filters.state import State, StatesGroup

class PersonalData(StatesGroup):
    fullname = State()
    phone = State()
    location = State()
    confirm_location = State()

class Customer(StatesGroup):
    pass

class Setting(StatesGroup):
    setting = State()
    chat = State()

class catManu(StatesGroup):
    menu = State()

class Order(StatesGroup):
    order = State()