import os
import io
import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

BOT_TOKEN = os.getenv("BOT_TOKEN")

def make_image(prompt: str) -> bytes:
    url = f"https://image.pollinations.ai/prompt/{requests.utils.quote(prompt)}"
    r = requests.get(url, params={"width": 1024, "height": 1024, "nologo": "true"}, timeout=120)
    r.raise_for_status()
    return r.content

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Send me any text and I'll make an image!")

async def on_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    prompt = update.message.text
    msg = await update.message.reply_text("🎨 Generating...")
    try:
        img = make_image(prompt)
        await update.message.reply_photo(photo=io.BytesIO(img), caption=prompt)
        await msg.delete()
    except Exception as e:
        await msg.edit_text(f"Error: {e}")

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, on_text))
    app.run_polling()

if __name__ == "__main__":
    main()
