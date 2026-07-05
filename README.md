import logging
import requests
import os
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from flask import Flask
from threading import Thread

# إعداد السجل
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

BOT_TOKEN = "8921322612:AAELLXkgwCunB8sdnVwmelGMMSKaB4LCANw"

# إعداد Flask
app = Flask(__name__)

@app.route('/')
def home():
    return "البوت يعمل بنجاح!"

def run_flask():
    # الحصول على المنفذ من Render أو استخدام 8080 افتراضياً
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

async def scan_coin(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not context.args:
        await update.message.reply_text("يرجى إرسال العقد بعد الأمر /scan")
        return
    address = context.args[0]
    await update.message.reply_text(f"🔍 جاري فحص: {address}")
    try:
        response = requests.get(f"https://api.dexscreener.com/latest/dex/tokens/{address}").json()
        if 'pairs' in response and response['pairs']:
            price = response['pairs'][0]['priceUsd']
            await update.message.reply_text(f"✅ سعر العملة الحالي: ${price}")
        else:
            await update.message.reply_text("⚠️ لم يتم العثور على بيانات لهذه العملة.")
    except Exception as e:
        await update.message.reply_text(f"❌ حدث خطأ: {str(e)}")

def main():
    # تشغيل Flask في Thread منفصل
    flask_thread = Thread(target=run_flask)
    flask_thread.start()

    # تشغيل البوت
    app_bot = Application.builder().token(BOT_TOKEN).build()
    app_bot.add_handler(CommandHandler("scan", scan_coin))
    print("🤖 البوت يعمل الآن بنجاح...")
    app_bot.run_polling()

if __name__ == '__main__':
    main()
    
