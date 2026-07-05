import logging
import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# إعداد السجل
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# ضع التوكن الصحيح هنا (احصل على توكن جديد من BotFather)
BOT_TOKEN = "8921322612:AAELLXkgwCunB8sdnVwmelGMMSKaB4LCANw"

async def scan_coin(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not context.args:
        await update.message.reply_text("يرجى إرسال العقد بعد الأمر /scan")
        return

    address = context.args[0]
    await update.message.reply_text(f"🔍 جاري فحص: {address}")

    try:
        response = requests.get(f"https://api.dexscreener.com/latest/dex/tokens/{address}").json()

        if 'pairs' in response and response['pairs']:
            pair = response['pairs'][0]
            price = pair.get('priceUsd', 'N/A')
            volume = pair.get('volume', {}).get('h24', 'N/A')
            liquidity = pair.get('liquidity', {}).get('usd', 'N/A')

            msg = f"✅ السعر: ${price}\n📊 حجم التداول (24س): ${volume}\n💧 السيولة: ${liquidity}"
            await update.message.reply_text(msg)
        else:
            await update.message.reply_text("⚠️ لم يتم العثور على بيانات لهذه العملة.")
    except Exception as e:
        await update.message.reply_text(f"❌ حدث خطأ: {str(e)}")

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("scan", scan_coin))
    print("🤖 البوت يعمل الآن بنجاح...")
    app.run_polling()

if __name__ == '__main__':
    main()
