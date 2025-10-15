from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
import asyncio
from bot import start_bot  # импортируем функцию запуска из bot.py

if __name__ == "__main__":
    # Запускаем бота и сайт вместе
    loop = asyncio.get_event_loop()
    loop.create_task(start_bot())  # бот работает в фоне
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))


