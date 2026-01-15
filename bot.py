# ================== CONFIG ==================
BOT_TOKEN = "8462352456:AAGBwbmz0tCNULt5HLISM61cprOAkDzDvQU"
MY_ID = 8429537293
FRIEND_ID = 5758526328
# ================== IMPORTS ==================
import asyncio
import threading
import os
from http.server import HTTPServer, BaseHTTPRequestHandler
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes
)
# ================== START COMMAND ==================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    
    # السماح للطرفين فقط
    if user_id not in [MY_ID, FRIEND_ID]:
        await update.message.reply_text("⛔ غير مصرح لك")
        return
    
    keyboard = [
        [InlineKeyboardButton("🔔 جرس", callback_data="ring")],
        [InlineKeyboardButton("💣 سبام (10x)", callback_data="spam")]
    ]
    await update.message.reply_text(
        "اضغط الزر لإرسال إشعار 👇",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )
# ================== BUTTON HANDLER ==================
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    sender_id = query.from_user.id
    
    # التحقق من الصلاحية
    if sender_id not in [MY_ID, FRIEND_ID]:
        return
    
    # تحديد المستقبل (الشخص الآخر)
    receiver_id = FRIEND_ID if sender_id == MY_ID else MY_ID
    
    # رسالة مرئية تظهر إشعار
    text = "🔔"
    
    try:
        # تحديد عدد المرات
        if query.data == "spam":
            repeat_count = 10
        else:
            repeat_count = 1
        
        # إرسال الإشعارات
        for i in range(repeat_count):
            msg_sender = await context.bot.send_message(sender_id, text)
            msg_receiver = await context.bot.send_message(receiver_id, text)
            
            await asyncio.sleep(0.5)
            
            await context.bot.delete_message(sender_id, msg_sender.message_id)
            await context.bot.delete_message(receiver_id, msg_receiver.message_id)
            
            if i < repeat_count - 1:
                await asyncio.sleep(0.3)
        
    except Exception as e:
        if "bot was blocked by the user" in str(e) or "chat not found" in str(e):
            await query.edit_message_text("⚠️ الشخص الآخر لم يبدأ محادثة مع البوت بعد!\nاطلب منه إرسال /start للبوت")
        else:
            await query.edit_message_text(f"❌ خطأ: {str(e)}")
# ================== WEB SERVER (UPTIMEROBOT) ==================
class PingHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"OK")
    def log_message(self, format, *args):
        pass
def run_server():
    port = int(os.environ.get("PORT", 10000))
    HTTPServer(("0.0.0.0", port), PingHandler).serve_forever()
threading.Thread(target=run_server, daemon=True).start()
# ================== MAIN ==================
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    print("Bot is running...")
    app.run_polling()
if __name__ == "__main__":
    main()
