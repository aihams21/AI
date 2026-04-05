import os
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

TOKEN = os.getenv("TOKEN")
AI_KEY = os.getenv("AI_KEY")

async def ai_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text

    url = "https://openrouter.ai/api/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {AI_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "openai/gpt-3.5-turbo",
        "messages": [
            {"role": "user", "content": user_text}
        ]
    }

    try:
        response = requests.post(url, headers=headers, json=data, timeout=15)
        result = response.json()

        if "choices" in result:
            reply = result["choices"][0]["message"]["content"]
        else:
            reply = "❌ AI ما رد، تأكد من المفتاح"

    except Exception as e:
        print(e)
        reply = "❌ صار خطأ، جرب مرة ثانية"

    await update.message.reply_text(reply)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🤖 ابعت أي رسالة وأنا أرد عليك")


app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, ai_reply))

from telegram.ext import CommandHandler
app.add_handler(CommandHandler("start", start))

app.run_polling()
