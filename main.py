# main.py
import os
import requests
import asyncio
import threading
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from flask import Flask, render_template_string
from dotenv import load_dotenv

# 📦 Загружаем переменные из .env
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
HF_TOKEN = os.getenv("HF_TOKEN")
HF_MODEL = os.getenv("HF_MODEL")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)
app = Flask(__name__)

# 🧠 Обращение к Hugging Face AI
def generate_ai_reply(message: str) -> str:
    try:
        url = f"https://api-inference.huggingface.co/models/{HF_MODEL}"
        headers = {"Authorization": f"Bearer {HF_TOKEN}"}
        payload = {"inputs": message}

        response = requests.post(url, headers=headers, json=payload, timeout=60)

        if response.status_code != 200:
            print("Ошибка Hugging Face:", response.text)
            return "⚠️ Произошла ошибка на сервере ИИ. Попробуй позже."

        data = response.json()

        # Иногда HuggingFace возвращает список с generated_text
        if isinstance(data, list) and len(data) and "generated_text" in data[0]:
            return data[0]["generated_text"].strip()
        elif isinstance(data, dict) and "generated_text" in data:
            return data["generated_text"].strip()
        else:
            return "🤖 Модель не вернула ответ. Попробуй написать иначе."
    except Exception as e:
        print("Ошибка:", e)
        return "⚠️ Ошибка при обращении к ИИ."

# 📩 Обработка сообщений от пользователя
@dp.message_handler()
async def handle_message(msg: types.Message):
    user_text = msg.text.strip()
    if not user_text:
        return

    await msg.answer("🧠 Думаю над ответом...")

    prompt = (
        f"Пользователь написал: {user_text}\n"
        f"Ты — доброжелательный и понимающий психолог. "
        f"Общайся как настоящий человек, не говори, что ты искусственный интеллект. "
        f"Дай совет, поддержи, помоги разобраться в чувствах. "
        f"Пиши на русском или казахском языке, в зависимости от того, на каком языке пользователь написал."
    )

    reply = generate_ai_reply(prompt)
    await msg.answer(reply)

# 🌐 Flask сайт
@app.route('/')
def index():
    html = """
    <html lang="ru">
    <head>
        <meta charset="UTF-8">
        <title>Qoldaushy Bot</title>
        <style>
            body {
                font-family: 'Segoe UI', sans-serif;
                background: linear-gradient(120deg, #89f7fe, #66a6ff);
                color: #222;
                text-align: center;
                padding: 50px;
            }
            h1 {
                font-size: 48px;
                margin-bottom: 10px;
            }
            p {
                font-size: 18px;
                max-width: 700px;
                margin: 15px auto;
            }
            .card {
                background: white;
                border-radius: 20px;
                padding: 40px;
                box-shadow: 0 8px 20px rgba(0,0,0,0.15);
                display: inline-block;
            }
            a {
                color: #0066cc;
                text-decoration: none;
                font-weight: bold;
            }
            a:hover {
                text-decoration: underline;
            }
        </style>
    </head>
    <body>
        <div class="card">
            <h1>🤖 Qoldaushy Bot</h1>
            <p><b>Qoldaushy Bot</b> — это проект, созданный, чтобы поддержать школьников,
            которые сталкиваются с буллингом, тревогой или стрессом. Бот поможет разобраться
            в чувствах, найти слова, чтобы выразить себя, и предложит дельные советы.</p>

            <p>💬 Он умеет говорить по-русски и по-казахски, всегда отвечает с добротой
            и вниманием, как настоящий психолог. Бот не оценивает, а помогает понять себя.</p>

            <p>🌱 <b>Цель проекта</b> — сделать поддержку доступной каждому ученику, независимо от места и времени.
            Искусственный интеллект может быть настоящим другом и советчиком.</p>

            <p><b>Попробуй прямо сейчас:</b><br>
            <a href="https://t.me/qolda_bot" target="_blank">@qolda_bot</a></p>
        </div>
    </body>
    </html>
    """
    return render_template_string(html)

# 🚀 Запуск Flask и Telegram бота
async def run_bot():
    print("🤖 Qoldaushy Bot запущен!")
    await dp.start_polling(bot)

def start_flask():
    app.run(host='0.0.0.0', port=10000)

if __name__ == '__main__':
    threading.Thread(target=start_flask).start()
    asyncio.run(run_bot())
