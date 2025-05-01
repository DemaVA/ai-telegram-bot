from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import openai
import os
openai.api_key = os.getenv("OPENAI_API_KEY")
BOT_TOKEN = os.getenv("7953730424:AAGf9XAdm-CNQInbwFLn9giBYJboc97MxwE")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Я ИИ-бот. Задай мне вопрос.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": user_message}]
        )
        reply = response.choices[0].message.content
    except Exception as e:
        reply = f"Ошибка: {e}"

    await update.message.reply_text(reply)

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

app.run_polling()
