def main():
    # 1. تشغيل خادم Flask في خيط منفصل (Thread)
    flask_thread = Thread(target=run_flask)
    flask_thread.start()

    # 2. تشغيل البوت كما هو معتاد
    app_bot = Application.builder().token(BOT_TOKEN).build()
    app_bot.add_handler(CommandHandler("scan", scan_coin))
    
    print("🤖 البوت والخادم يعملان الآن بنجاح...")
    app_bot.run_polling()
