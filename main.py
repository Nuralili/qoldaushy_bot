import os
import asyncio
import threading
import requests
from aiogram import Bot, Dispatcher, types
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv

# Загрузка токенов из .env или окружения
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
HF_TOKEN = os.getenv("HF_TOKEN")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)
app = Flask(__name__)

# --- Функция общения с ИИ ---
def ask_ai(message: str) -> str:
    url = "https://api-inference.huggingface.co/models/meta-llama/Llama-3-8B-Instruct"
    headers = {"Authorization": f"Bearer {HF_TOKEN}"}
    prompt = f"""Ты — доброжелательный школьный психолог.
Ты общаешься на русском и казахском языке с подростком, который переживает трудности.
Отвечай естественно, по-человечески, не упоминай, что ты ИИ.

Сообщение ученика: {message}

Ответ:"""
    try:
        r = requests.post(url, headers=headers, json={"inputs": prompt}, timeout=60)
        data = r.json()
        if isinstance(data, list) and len(data) > 0 and "generated_text" in data[0]:
            text = data[0]["generated_text"]
        elif "generated_text" in data:
            text = data["generated_text"]
        else:
            return "Извини, не расслышал. Расскажи немного подробнее?"
        return text.split("Ответ:")[-1].strip()
    except Exception:
        return "Произошла ошибка при обращении к модели. Попробуй ещё раз позже."

# --- Telegram бот ---
@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    await message.answer(
        "Сәлем! Я Qoldaushy Bot 💬\n\n"
        "Я здесь, чтобы тебя выслушать. Расскажи, что тебя тревожит — "
        "и я постараюсь помочь советом."
    )

@dp.message_handler()
async def reply_user(message: types.Message):
    await message.answer("Дай мне секунду, я подумаю...")
    answer = ask_ai(message.text)
    await message.answer(answer)

# --- Flask сайт ---
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_msg = data.get("message", "")
    if not user_msg.strip():
        return jsonify({"reply": "Пожалуйста, напиши что-нибудь 🙃"})
    reply = ask_ai(user_msg)
    return jsonify({"reply": reply})

# --- Асинхронный запуск Telegram-бота ---
async def run_bot():
    print("🤖 Telegram-бот запущен!")
    await dp.start_polling(bot, skip_updates=True, handle_signals=False)

# --- Главный запуск ---
if __name__ == "__main__":
    threading.Thread(target=lambda: asyncio.run(run_bot()), daemon=True).start()
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
