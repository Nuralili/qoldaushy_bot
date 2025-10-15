📘 Инструкция по запуску Qoldaushy Bot

1️⃣ Создай Telegram-бота
   - Открой в Telegram @BotFather
   - Команда: /newbot
   - Скопируй выданный BOT_TOKEN

2️⃣ Создай Hugging Face токен
   - Перейди на https://huggingface.co/settings/tokens
   - Нажми “New Token” → Access level: “Read”
   - Скопируй HF_TOKEN

3️⃣ Открой файл `.env.example`, вставь туда токены:
      BOT_TOKEN=твой_токен
      HF_TOKEN=твой_hf_токен
      HF_MODEL=mistralai/Mixtral-8x7B-Instruct-v0.1
   - Сохрани и переименуй файл в `.env`

4️⃣ Зайди на https://render.com
   - Войди через Google
   - “New Web Service” → Upload Folder → выбери папку `qoldaushy_bot`
   - Render сам установит зависимости и запустит сайт

5️⃣ Через 3–5 минут Render даст ссылку на сайт и бот начнёт работать.
   - Проверь сайт
   - Замени ссылку на бота в файле `index.html`

🎉 Готово! Теперь у тебя есть Qoldaushy Bot — доброжелательный ИИ-помощник.
