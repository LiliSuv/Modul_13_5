from aiogram import Bot, Dispatcher, executor, types
from aiogram. contrib. fsm_storage. memory import MemoryStorage
from aiogram. dispatcher. filters. state import State, StatesGroup
from aiogram. dispatcher import FSMContext
from aiogram. types import ReplyKeyboardMarkup, KeyboardButton
import asyncio

api = '81..............6yc'
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())

kb = ReplyKeyboardMarkup(resize_keyboard=True)
button = KeyboardButton( text='Информация')
button2 = KeyboardButton( text = 'Рассчитать')
kb. row (button,button2)



class UserState(StatesGroup):
    age=State()
    growth=State()
    weight= State()


@dp.message_handler (text='Информация')
async def inform(message):

    await message. answer ( 'Я бот, помогающий твоему здоровью')


@dp.message_handler(text='Рассчитать')
async def set_age(message):
    await message.answer ("Введите свой возраст")
    await UserState.age.set ()


@dp.message_handler(commands=['start'])
async def start_message(message):
    await message.answer ("Привет!  Что Вас интересует?",reply_markup = kb)


@dp.message_handler()
async def all_message(message):
    await message.answer ("Введите команду /start, чтобы начать общение")


@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    await state.update_data(age=message.text)
    await message.answer ('Введите свой рост:')
    await UserState.growth.set ()


@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    await state.update_data (growth=message.text)
    await message.answer ('Введите свой вес:')
    await UserState.weight.set ()


@dp.message_handler(state=UserState.weight)
async def send_calories(message, state):
    await state.update_data (weight=message.text)
    data=await state.get_data ()
    try:
        int(data['weight'])
    except:
        await message.answer ('Вы не правильно ввели свой вес')
        await state.finish ()
    try:
        int(data['age'])
    except:
        await message.answer ('Вы не правильно ввели свой возраст')
        await state.finish ()
    try:
        int(data['growth'])
    except:
        await message.answer ('Вы не правильно ввели свой рост')
        await state.finish ()
    a=10*int(data['weight'])+6.25 * int(data['growth'])-5*int(data['age'])-161
    await message.answer(f'Ваша норма каллорий {a}')
    await state.finish ()


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
