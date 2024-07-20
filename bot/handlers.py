from aiogram import Router
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from bot.service import create_or_update_coin, get_coin_by_name
from bot.states import CurrencyFill

START_MESSAGE = (
    "Привет! Бот позволяет задавать криптовалюты для отслеживания кртических значений. Используйте /set_currency для установки валюты для отслеживания"
)
SET_CURRENCY = "Введите название валюты для отслеживания"
SET_MIN = "Введите минимальное значение"
SET_MAX = "Введите максимальное значение"
SET_SUCCESS = "Вы успешно установили валюту для отслеживания: {coin_name} с минимальной ценой {min_price} и максимальной ценой {max_price}."
ONE_MORE_MESSAGE = (
    "Используйте /set_currency для установки еще одной валюты для отслеживания"
)
UPDATE_CURRENCY_MESSAGE = "Поменяли значения для валюты {coin_name}"

router = Router()


@router.message(Command("start"))
async def start_command(message: Message):
    await message.answer(START_MESSAGE)


@router.message(Command("set_currency"))
async def set_currency_command(message: Message, state: FSMContext):
    await state.set_state(CurrencyFill.fill_coin)
    await message.answer(SET_CURRENCY)


@router.message(StateFilter(CurrencyFill.fill_coin))
async def fill_currency(message: Message, state: FSMContext):
    await state.set_state(CurrencyFill.fill_min)
    await state.update_data(coin_name=message.text)
    await message.answer(SET_MIN)


@router.message(StateFilter(CurrencyFill.fill_min))
async def fill_currency(message: Message, state: FSMContext):
    await state.set_state(CurrencyFill.fill_max)
    await state.update_data(min_price=message.text)
    await message.answer(SET_MAX)


@router.message(StateFilter(CurrencyFill.fill_max))
async def fill_currency(message: Message, state: FSMContext):
    await state.update_data(max_price=message.text)
    data = await state.get_data()
    if await get_coin_by_name(
        coin_name=data["coin_name"], user_id=message.from_user.id
    ):
        await message.answer(
            UPDATE_CURRENCY_MESSAGE.format(coin_name=data["coin_name"])
        )
    else:
        set_success_message = SET_SUCCESS.format(
            coin_name=data["coin_name"],
            min_price=data["min_price"],
            max_price=data["max_price"],
        )
        await message.answer(set_success_message)
    await create_or_update_coin(data, message.from_user.id)
    await message.answer(ONE_MORE_MESSAGE)
