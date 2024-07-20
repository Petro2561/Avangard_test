from aiogram.fsm.state import State, StatesGroup


class CurrencyFill(StatesGroup):
    fill_coin = State()
    fill_min = State()
    fill_max = State()
