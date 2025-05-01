import os
import logging
import openai

from telegram import Update, Bot
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Токены
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

openai.api_key = OPENAI_API_KEY

# Обработчик входящих сообщений
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": user_message}]
        )
        await update.message.reply_text(response["choices"][0]["message"]["content"])
    except Exception as e:
        logging.exception("Ошибка OpenAI")
        await update.message.reply_text("Произошла ошибка при обращении к ИИ.")

# Запуск
async def post_init(app):
    bot = Bot(token=TELEGRAM_TOKEN)
    await bot.delete_webhook()
    print("Webhook удалён, бот работает через polling.")

if __name__ == "__main__":
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).post_init(post_init).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("Бот запущен через polling...")
    app.run_polling()

