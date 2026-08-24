import os
import requests
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# بارکردنی زانیارییەکان
load_dotenv()
TOKEN = os.getenv('BOT_TOKEN')
ADMIN_ID = int(os.getenv('ADMIN_ID'))

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return
    await update.message.reply_text("✅ بۆتەکە بە تۆکینی نوێ چالاک کرا.\nفەرمانی /start یان لینک بنێرە.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return
    
    url = update.message.text.strip()
    if not url.startswith('http'): url = 'http://' + url
    
    await update.message.reply_text(f"🔎 پشکنین بۆ: {url}")
    try:
        response = requests.get(url, timeout=5)
        await update.message.reply_text(f"📊 دۆخی سێرڤەر: {response.status_code}")
    except Exception as e:
        await update.message.reply_text(f"❌ کێشە لە پەیوەندی: {e}")

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    
    print(f"--- Bot is LIVE with New Token for Admin: {ADMIN_ID} ---")
    app.run_polling()
