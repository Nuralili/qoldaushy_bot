import os
import asyncio
import threading
from flask import Flask, render_template
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
import aiohttp
from dotenv import load_dotenv

# Загружаем токены
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
HF_TOKEN = os.getenv("HF_TOKEN")
HF_MODEL = "mistralai/Mistral-7B-Instruct-v0.2"

# Flask (веб)
app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

# Telegram-бот
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

async def get_ai_reply(user_message: str, lang="ru"):
    headers = {
        "Authorization": f"Bearer {HF_TOKEN}",
        "Content-Type": "application/json"
    }
    prompt = f"Ты школьный психолог. Ответь {('на казахском' if lang=='kk' else 'на русском')} языком:\n\n{user_message}"
    data = {"inputs": prompt, "parameters": {"max_new_tokens": 150}}

    async with aiohttp.ClientSession() as session:
        async with session.post(f"https://api-inference.huggingface.co/models/{HF_MODEL}",
                                headers=headers, json=data) as resp:
            try:
                result = await resp.json()
                if isinstance(result, list) and "generated_text" in result[0]:
                    return result[0]["generated_text"]
                else:
                    return "Извини, не понял тебя. Попробуй ещё раз ❤️"
            except:
                return "Ошибка при обращении к ИИ 😔"

@dp.message(CommandStart())
async def start_cmd(msg: types.Message):
    await msg.answer("Сәлем! / Привет! Мен Qoldaushy Bot 🤖\n\n"
                     "Расскажи, что тебя тревожит — я постараюсь помочь ❤️")

@dp.message()
async def message_handler(msg: types.Message):
    lang = "kk" if any(ch in msg.text for ch in "әғқңөұүіһ") else "ru"
    reply = await get_ai_reply(msg.text, lang)
    await msg.answer(reply)

async def run_bot():
    print("🤖 Бот запущен!")
    await dp.start_polling(bot, skip_updates=True, handle_signals=False)

def run_flask():
    app.run(host="0.0.0.0", port=10000)

if __name__ == "__main__":
    threading.Thread(target=lambda: asyncio.run(run_bot())).start()
    run_flask()
