import os
import logging
from aiogram import Bot, Dispatcher, executor, types
import requests

logging.basicConfig(level=logging.INFO)

BOT_TOKEN = os.getenv("BOT_TOKEN")
HF_TOKEN = os.getenv("HF_TOKEN")
HF_MODEL = os.getenv("HF_MODEL", "mistralai/Mixtral-8x7B-Instruct-v0.1")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

def ask_ai(prompt: str) -> str:
    """Отправка текста в Hugging Face модель"""
    headers = {"Authorization": f"Bearer {HF_TOKEN}"}
    payload = {"inputs": prompt}
    try:
        r = requests.post(
            f"https://api-inference.huggingface.co/models/{HF_MODEL}",
            headers=headers,
            json=payload,
            timeout=30
        )
        if r.status_code == 200:
            data = r.json()
            if isinstance(data, list) and len(data) > 0:
                return data[0].get("generated_text", "").strip()
        return "Извини, сейчас я не могу ответить. Попробуй позже."
    except Exception:
        return "Произошла ошибка при подключении к ИИ. Попробуй позже."

@dp.message_handler(commands=["start", "help"])
async def start_message(msg: types.Message):
    text = (
        "Сәлем! 👋 Мен Qoldaushy Bot — сенің көмекшің.\n\n"
        "Привет! 👋 Я Qoldaushy Bot — твой помощник.\n\n"
        "Расскажи, что тебя тревожит. Я постараюсь помочь тебе понять причину "
        "и дам совет, как с этим справиться."
    )
    await msg.answer(text)

@dp.message_handler()
async def handle_message(msg: types.Message):
    user_text = msg.text.strip()
    if not user_text:
        await msg.answer("Пожалуйста, напиши, что тебя беспокоит 💬")
        return

    prompt = (
        "Ты — доброжелательный школьный психолог, говоришь мягко и понятно. "
        "Если пользователь пишет по-русски — отвечай на русском, если на казахском — на казахском. "
        "Проанализируй сообщение ученика, попробуй понять причину его беспокойства "
        "и дай конкретный, доброжелательный совет.\n\n"
        f"Сообщение ученика: {user_text}\n\nОтвет:"
    )

    answer = ask_ai(prompt)
    await msg.answer(answer)

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
