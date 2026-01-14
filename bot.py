import sys
import os

sys.path.append(r'C:\Users\salta\AppData\Roaming\Python\Python311\site-packages')

try:
    import telegram
except ImportError:
    import subprocess
    print("Installing python-telegram-bot...")
    python_exe = sys.executable.replace('pythonw.exe', 'python.exe')
    subprocess.run([python_exe, "-m", "pip", "install", "python-telegram-bot", "--user"])
    print("Installed! Restart script now.")
    input("Press Enter...")
    sys.exit(0)

import logging
import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

BOT_TOKEN = "8462352456:AAGBwbmz0tCNULt5HLISM61cprOAkDzDvQU"

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

users = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    
    if user_id not in users:
        users[user_id] = []
    
    keyboard = [[InlineKeyboardButton("🔔", callback_data="spam")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    msg = await update.message.reply_text("تم التفعيل ✅", reply_markup=reply_markup)
    users[user_id].append(msg.message_id)
    users[user_id].append(update.message.message_id)

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    for user_id in users:
        try:
            for msg_id in users[user_id]:
                try:
                    await context.bot.delete_message(chat_id=user_id, message_id=msg_id)
                except:
                    pass
            
            msg = await context.bot.send_message(chat_id=user_id, text="🔔")
            await asyncio.sleep(0.5)
            await context.bot.delete_message(chat_id=user_id, message_id=msg.message_id)
            
            users[user_id] = []
            
        except Exception as e:
            print(f"Failed: {e}")

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_callback))
    app.run_polling()

if __name__ == '__main__':
    main()

import threading
from http.server import BaseHTTPRequestHandler, HTTPServer

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is running")

def keep_alive():
    server = HTTPServer(("0.0.0.0", 10000), Handler)
    server.serve_forever()

threading.Thread(target=keep_alive, daemon=True).start()
