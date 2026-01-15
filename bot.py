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
    if update.effective_user.id != MY_ID:
        return

    keyboard = [
        [InlineKeyboardButton("🔔 جرس", callback_data="ring")]
    ]

    await update.message.reply_text(
        "اضغط الزر 👇",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# ================== BUTTON HANDLER ==================
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.from_user.id != MY_ID:
        return

    # رسالة غير مرئية
    text = "‎"

    msg_me = await context.bot.send_message(MY_ID, text)
    msg_friend = await context.bot.send_message(FRIEND_ID, text)

    await asyncio.sleep(2)

    await context.bot.delete_message(MY_ID, msg_me.message_id)
    await context.bot.delete_message(FRIEND_ID, msg_friend.message_id)

# ================== WEB SERVER (UPTIMEROBOT) ==================
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
    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
