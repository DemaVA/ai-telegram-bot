import os
import logging

import openai
from openai.error import RateLimitError

from telegram import Bot, Update
from telegram.error import Conflict
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

# Логи
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Токены из ENV
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

# 1) Сбрасываем все вебхуки и накопленные апдейты
Bot(token=TELEGRAM_TOKEN).delete_webhook(drop_pending_updates=True)

# /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Я ИИ-бот через polling. Напиши мне что-нибудь.")

# Обработка сообщений с защитой от ошибок
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": user_message}],
        )
        reply = response.choices[0].message.content
    except RateLimitError:
        reply = "Лимит запросов к OpenAI исчерпан. Попробуйте позже."
    except Exception as e:
        logger.error(f"OpenAI error: {e}", exc_info=True)
        reply = "Ошибка при обращении к OpenAI."
    await update.message.reply_text(reply)

# Глобальный обработчик остальных ошибок (игнорируем конфликт polling)
async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE):
    err = context.error
    if isinstance(err, Conflict):
        return
    logger.error(f"Unhandled error: {err}", exc_info=True)

if __name__ == "__main__":
    # 2) Строим приложение с выключением старых апдейтов
    app = (
        ApplicationBuilder()
        .token(TELEGRAM_TOKEN)
        .drop_pending_updates(True)
        .build()
    )
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_error_handler(error_handler)

    # 3) Запускаем polling
    app.run_polling()


