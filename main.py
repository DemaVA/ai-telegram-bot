import asyncio
import logging
import openai
import os

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

# Основная функция
async def main():
    bot = Bot(token=TELEGRAM_TOKEN)
    await bot.delete_webhook()  # Удаляем Webhook, если был
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Бот запущен через polling...")
    await app.run_polling()

if __name__ == "__main__":
    asyncio.run(main())

