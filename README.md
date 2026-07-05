import os # تأكد من إضافة هذا الاستيراد في الأعلى

def run_flask():
    # الحصول على المنفذ من إعدادات Render أو استخدام 8080 كخيار افتراضي
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
    
