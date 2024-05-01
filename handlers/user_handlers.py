from aiogram.filters import Command
from aiogram.types import Message
from main import dp


# Этот хэндлер будет срабатывать на команду "/help"
@dp.message(Command(commands=["help"]))
async def process_start_command(message: Message):
    await message.answer('Привет!\nЯ умею присылать вопросы висторины "Своя Игра"!\nВыбери "/start", чтобы проверить свои знания!')