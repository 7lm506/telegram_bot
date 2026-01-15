# ================== AUTO INSTALL ==================
import sys
import subprocess

def ensure(package):
    try:
        __import__(package)
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])

packages = [
    "python-telegram-bot==22.5",
    "httpx",
    "idna",
    "anyio",
    "certifi",
    "httpcore"
]

for p in packages:
    ensure(p.split("==")[0])

# ================== BOT CODE ==================
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

BOT_TOKEN = "PUT_YOUR_BOT_TOKEN_HERE"

ADMINS = {
    8429537293,  # ID حقك
    5758526328   # ID حق خويك
}

logging.basicConfig(level=logging.INFO)

users = set()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    users.add(update.effective_user.id)

    keyboard = [[InlineKeyboardButton("🔔", callback_data="notify")]]
    await update.message.reply_text(
        "\u200B",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query

    if query.from_user.id not in ADMINS:
        await query.answer("❌ غير مصرح", show_alert=True)
        return

    await query.answer()

    for uid in users:
        try:
            await context.bot.send_message(chat_id=uid, text="\u200B")
        except:
            pass

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_callback))
    app.run_polling()

if __name__ == "__main__":
    main()
