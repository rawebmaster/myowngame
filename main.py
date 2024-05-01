from config_data.config import *
from handlers.user_handlers import *
from keyboards.mainmenu import set_main_menu
from environs import Env
from aiogram import Bot, Dispatcher, F
from aiogram.types import BotCommand, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
import asyncio
import logging
from aiogram.filters import Command
from aiogram.types import Message
from handlers.user_handlers import *
import random
from aiogram.types import (KeyboardButton, Message, ReplyKeyboardMarkup,
                           ReplyKeyboardRemove)

env = Env()  # Создаем экземпляр класса Env
env.read_env()  # Методом read_env() читаем файл .env и загружаем из него переменные в окружение

# Вместо BOT TOKEN HERE нужно вставить токен вашего бота,
# полученный у @BotFather
BOT_TOKEN = env('BOT_TOKEN')
admin_id = env.int('ADMIN_ID')  # Получаем и преобразуем значение переменной окружения к типу int,
                                # затем сохраняем в переменной admin_id

# Создаем объекты бота и диспетчера
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Создаем объекты кнопок
#button_more = KeyboardButton(text='Ещё!')

# Создаем объект клавиатуры, добавляя в него кнопки
#keyboard = ReplyKeyboardMarkup(keyboard=[[button_more]], resize_keyboard=True)

# Создаем объекты инлайн-кнопок
button_more_inline = InlineKeyboardButton(
    text='Ещё!',
    callback_data='more_button_pressed'
)

# Создаем объект инлайн-клавиатуры
keyboard = InlineKeyboardMarkup(inline_keyboard=[[button_more_inline]]
)


# Этот хэндлер будет срабатывать на команду "/start"
@dp.message(Command(commands=["start"]))
async def process_start_command(message: Message):
    await message.answer('Привет!\nЯ умею присылать вопросы викторины "Своя Игра"\nЖми "/go"')

# Этот хэндлер будет срабатывать на команду "/help"
@dp.message(Command(commands=["help"]))
async def process_start_command(message: Message):
    await message.answer('Выбери "/go", чтобы проверить свои знания!')

myresult : list = []
year : str = ''
topic : str = ''
price : str = ''
question : str = ''
answer : str = ''

# Грузим новый Вопрос-Ответ
def get_q_and_a() -> list:
    mycntr = random.randint(1,132378)
    mydb.reconnect()
    mycursor = mydb.cursor()
    mycursor.execute(f"SELECT * FROM `DATA` WHERE cntr='{mycntr}'")
    global myresult
    myresult = mycursor.fetchall()
    global year
    year = myresult[0][1]
    global topic
    topic = myresult[0][2]
    global price
    price = myresult[0][3]
    global question
    question = myresult[0][4]
    global answer
    answer = myresult[0][5]
    return myresult

# Этот хэндлер будет срабатывать на команду "/go"
@dp.message(Command(commands=["go"]))
async def process_start_command(message: Message):
    get_q_and_a()
    await message.answer(str(question))
    await message.answer(text=f"<span class='tg-spoiler'>'{answer.replace("'","")}'</span>", parse_mode='HTML', reply_markup=keyboard)

# Этот хэндлер будет срабатывать на ответ "Ещё!" и добавлять ещё один вопрос
#@dp.message(F.text == 'Ещё!')
#async def process_start_command(message: Message):
    #get_q_and_a()
    #await message.answer(str(question))
    #await message.answer(text=f"<span class='tg-spoiler'>'{answer}'</span>", parse_mode='HTML', reply_markup=keyboard)

# Этот хэндлер будет срабатывать на апдейт типа CallbackQuery
# с data 'more_button_pressed'

@dp.callback_query(F.data == 'more_button_pressed')
async def process_more_button_press(callback: CallbackQuery):
    get_q_and_a()
    await callback.message.answer(str(question))
    await callback.message.answer(text=f"<span class='tg-spoiler'>'{answer}'</span>", parse_mode='HTML', reply_markup=keyboard)
    await callback.answer()







# Регистрируем асинхронную функцию в диспетчере,
# которая будет выполняться на старте бота,
dp.startup.register(set_main_menu)

if __name__ == '__main__':
    dp.run_polling(bot)