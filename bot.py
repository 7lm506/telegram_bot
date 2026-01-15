# ================== AUTO INSTALL ==================
import sys
import subprocess

def install(pkg):
    subprocess.check_call([sys.executable, "-m", "pip", "install", pkg])

try:
    from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
    from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
except:
    install("python-telegram-bot==20.7")
    from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
    from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

# ================== CONFIG ==================
BOT_TOKEN = "8462352456:AAGBwbmz0tCNULt5HLISM61cprOAkDzDvQU"

MY_ID = 8429537293        # ايديك
FRIEND_ID = 5758526328    # ايدي خويك

# ================== BOT LOGIC ==================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != MY_ID:
        return

    keyboard = [
        [InlineKeyboardButton("📳 اهتزاز", callback_data="vibe")]
    ]

    await update.message.reply_text(
        "👇 اضغط الزر",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.from_user.id != MY_ID:
        return

    # اهتزاز فعلي (رسالة غير مرئية)
    await context.bot.send_message(
        chat_id=FRIEND_ID,
        text="\u200b",              # Zero Width Space
        disable_notification=False # يضمن الاهتزاز
    )

# ================== WEB SERVER (UPTIMEROBOT) ==================
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
import os

class PingHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"OK")

def run_server():
    port = int(os.environ.get("PORT", 10000))
    HTTPServer(("0.0.0.0", port), PingHandler).serve_forever()

threading.Thread(target=run_server, daemon=True).start()

# ================== MAIN ==================
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    print("Bot is running 24/7...")
    app.run_polling()

if __name__ == "__main__":
    main()
