import os
import threading
import asyncio
import requests
from flask import Flask, render_template
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiogram.enums import ParseMode
from aiogram.types import Message
from dotenv import load_dotenv

# Загружаем переменные окружения (.env)
load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
HF_TOKEN = os.getenv("HF_TOKEN")
HF_MODEL = os.getenv("HF_MODEL")

bot = Bot(token=BOT_TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher()

# --- Flask сайт ---
app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

# --- ИИ ответ через Hugging Face ---
def ask_ai(prompt: str) -> str:
    if not HF_TOKEN or not HF_MODEL:
        return "Ошибка: не указан токен или модель ИИ."
    headers = {"Authorization": f"Bearer {HF_TOKEN}"}
    payload = {"inputs": prompt}
    try:
        response = requests.post(
            f"https://api-inference.huggingface.co/models/{HF_MODEL}",
            headers=headers,
            json=payload,
            timeout=30
        )
        data = response.json()
        if isinstance(data, list) and len(data) > 0 and "generated_text" in data[0]:
            return data[0]["generated_text"]
        elif "error" in data:
            return f"Ошибка ИИ: {data['error']}"
        else:
            return "ИИ не смог ответить. Попробуй позже."
    except Exception as e:
        return f"Ошибка соединения с ИИ: {e}"

# --- Обработка сообщений ---
@dp.message(CommandStart())
async def start_cmd(message: Message):
    await message.answer("Сәлем! Мен Qoldaushy Bot 🤖\n"
                         "Мен сенің көңіл-күйіңді түсініп, кеңес беруге тырысамын.\n"
                         "Просто расскажи, что тебя беспокоит ❤️")

@dp.message()
async def handle_message(message: Message):
    user_text = message.text
    prompt = f"Ты — психологический помощник. Человек пишет: '{user_text}'. Найди возможную причину его беспокойства и дай добрый, умный совет, как от этого избавиться. Отвечай на русском или казахском, как в сообщении пользователя."
    answer = ask_ai(prompt)
    await message.answer(answer)

# --- Запуск Telegram-бота ---
async def run_bot():
    await dp.start_polling(bot)

# --- Запуск Flask ---
if __name__ == "__main__":
    threading.Thread(target=lambda: asyncio.run(run_bot()), daemon=True).start()
    app.run(host="0.0.0.0", port=10000)
