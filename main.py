import telebot
import os
import time
from threading import Thread
from flask import Flask

# Dummy Web Server (Render free tier ke liye)
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is alive and running 24/7!"

def run_web():
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)

def keep_alive():
    t = Thread(target=run_web)
    t.daemon = True
    t.start()

# --- Telegram Bot Code ---
BOT_TOKEN = "8191099332:AAGoOnNJnsiMP-gVbQ5FKfkPr8nv5fL7zKI"
ADMIN_ID = 7816466284

bot = telebot.TeleBot(BOT_TOKEN)
USERS_FILE = "users.txt"

def save_user(user_id):
    users = get_users()
    if str(user_id) not in users:
        with open(USERS_FILE, "a") as f:
            f.write(f"{user_id}\n")

def get_users():
    if not os.path.exists(USERS_FILE):
        return []
    with open(USERS_FILE, "r") as f:
        return [line.strip() for line in f if line.strip()]

WELCOME_MESSAGE = """Thanks for join my channel 🫰💖
Pin the channel and get first SUREBET ❤️
Any problem - @vikash_sahu55"""

@bot.chat_join_request_handler()
def handle_join_request(req):
    user_id = req.from_user.id
    chat_id = req.chat.id
    try:
        bot.approve_chat_join_request(chat_id, user_id)
        bot.send_message(user_id, WELCOME_MESSAGE)
        save_user(user_id)
    except Exception as e:
        print(f"Error: {e}")

@bot.message_handler(commands=['stats'])
def stats_command(message):
    if message.from_user.id != ADMIN_ID:
        return
    users = get_users()
    bot.reply_to(message, f"📊 Total saved users: {len(users)}")

@bot.message_handler(commands=['broadcast'])
def broadcast_command(message):
    if message.from_user.id != ADMIN_ID:
        return
    msg = bot.reply_to(message, "📢 Jo message sabhi ko bhejna hai, send karein:")
    bot.register_next_step_handler(msg, process_broadcast)

def process_broadcast(message):
    if message.from_user.id != ADMIN_ID:
        return
    users = get_users()
    if not users:
        bot.send_message(ADMIN_ID, "❌ User list khali hai.")
        return
    
    bot.send_message(ADMIN_ID, f"🚀 Broadcast start ({len(users)} users)...")
    success, failed = 0, 0
    for uid in users:
        try:
            bot.copy_message(chat_id=uid, from_chat_id=message.chat.id, message_id=message.message_id)
            success += 1
            time.sleep(0.05)
        except Exception:
            failed += 1
    bot.send_message(ADMIN_ID, f"✅ Complete!\n• Success: {success}\n• Failed: {failed}")

if __name__ == "__main__":
    keep_alive()  # Web server start
    print("Bot starting...")
    bot.infinity_polling()
    
