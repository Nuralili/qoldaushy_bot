import os
import asyncio
import threading
from flask import Flask, render_template
from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
import aiohttp
from dotenv import load_dotenv

# Загружаем токены
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
HF_TOKEN = os.getenv("HF_TOKEN")
HF_MODEL = os.getenv("HF_MODEL", "mistralai/Mixtral-8x7B-Instruct-v0.1")

# Проверка токенов
if not BOT_TOKEN or not HF_TOKEN:
    raise ValueError("❌ Не найдены BOT_TOKEN или HF_TOKEN в .env файле")

# Создаем бота
bot = Bot(
    token=BOT_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)
dp = Dispatcher()

# Flask-сайт
app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

# Функция запроса к Hugging Face API
async def ask_ai(user_text: str) -> str:
    prompt = (
        f"Ты — доброжелательный школьный психолог по имени Qoldaushy. "
        f"Твоя задача — понять, почему ученику грустно, тревожно или тяжело. "
        f"Он написал: '{user_text}'. "
        f"Ответь мягко, по-дружески, коротко и человечно, "
        f"на том языке, на котором тебе написали (русском или казахском). "
        f"Не говори, что ты ИИ или бот."
    )

    headers = {
        "Authorization": f"Bearer {HF_TOKEN}"
    }
    payload = {
        "inputs": prompt,
        "parameters": {"max_new_tokens": 200, "temperature": 0.8}
    }

    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"https://api-inference.huggingface.co/models/{HF_MODEL}",
                headers=headers,
                json=payload,
                timeout=80
            ) as resp:
                data = await resp.json()
                if isinstance(data, dict) and "error" in data:
                    return "Произошла ошибка на сервере ИИ. Попробуй написать иначе 💭"
                if isinstance(data, list) and "generated_text" in data[0]:
                    return data[0]["generated_text"].split("Ответ:")[-1].strip()
                return "Я пытаюсь понять тебя, но, кажется, не расслышал. Попробуй сказать иначе 💬"
    except Exception as e:
        return f"⚠️ Ошибка: {e}"

# Обработчик сообщений
@dp.message()
async def handle_message(message: types.Message):
    user_text = message.text
    await message.answer("🧠 Думаю над ответом...")
    reply = await ask_ai(user_text)
    await message.answer(reply)

# Функция для запуска Telegram-бота
async def run_bot():
    print("🤖 Qoldaushy Bot запущен!")
    await dp.start_polling(bot, skip_updates=True, handle_signals=False)

# Запуск Flask + aiogram параллельно
if __name__ == "__main__":
    threading.Thread(target=lambda: asyncio.run(run_bot())).start()
    app.run(host="0.0.0.0", port=10000)
