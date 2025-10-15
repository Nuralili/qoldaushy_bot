from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
from aiogram.filters import CommandStart
import asyncio
import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")
bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(CommandStart())
async def start(message: Message):
    await message.answer("Сәлем! / Привет! Я Qoldaushy Bot 🤖\n\n"
                         "Расскажи, что тебя тревожит — я постараюсь помочь.")

async def start_bot():
    print("Бот запущен ✅")
    await dp.start_polling(bot)
