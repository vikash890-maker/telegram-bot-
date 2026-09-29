import telebot
import os
import time

BOT_TOKEN = "8191099332:AAGoOnNJnsiMP-gVbQ5FKfkPr8nv5fL7zKI"  # Apna bot token yahan dalein
ADMIN_ID = 7816466284             # Apni numeric Telegram ID dalein (bot @userinfobot se mil jayegi)

bot = telebot.TeleBot(BOT_TOKEN)

USERS_FILE = "users.txt"

# Users ki ID save karne ke liye helper function
def save_user(user_id):
    users = get_users()
    if str(user_id) not in users:
        with open(USERS_FILE, "a") as f:
            f.write(f"{user_id}\n")

# Saved users list read karne ke liye
def get_users():
    if not os.path.exists(USERS_FILE):
        return []
    with open(USERS_FILE, "r") as f:
        return [line.strip() for line in f if line.strip()]

WELCOME_MESSAGE = """Thanks for join my channel 🫰💖
Pin the channel and get first SUREBET ❤️️
Any problem - @vikash_sahu55"""

# 1. Join Request Auto Accept + Greeting + ID Save
@bot.chat_join_request_handler()
def handle_join_request(req):
    user_id = req.from_user.id
    chat_id = req.chat.id

    # Request accept karna
    try:
        bot.approve_chat_join_request(chat_id, user_id)
        print(f"[+] Request approved: {user_id}")
    except Exception as e:
        print(f"[-] Approve error: {e}")

    # Greeting bhejna
    try:
        bot.send_message(user_id, WELCOME_MESSAGE)
        save_user(user_id)  # ID database/file me save ho gayi
        print(f"[+] Greeting sent & User ID saved: {user_id}")
    except Exception as e:
        print(f"[-] DM error: {e}")

# 2. Total user count dekhne ke liye command (/stats)
@bot.message_handler(commands=['stats'])
def stats_command(message):
    if message.from_user.id != ADMIN_ID:
        return
    users = get_users()
    bot.reply_to(message, f"📊 Total saved users: {len(users)}")

# 3. Broadcast system (Text, Photo, Video sabhi users ko bhejne ke liye)
@bot.message_handler(commands=['broadcast'])
def broadcast_command(message):
    if message.from_user.id != ADMIN_ID:
        return

    msg = bot.reply_to(
        message, 
        "📢 Jo bhi message, photo ya video sabhi ko bhejna hai, use abhi yahan bhejo:"
    )
    bot.register_next_step_handler(msg, process_broadcast)

def process_broadcast(message):
    if message.from_user.id != ADMIN_ID:
        return

    users = get_users()
    if not users:
        bot.send_message(ADMIN_ID, "❌ Abhi tak koi user list me nahi hai.")
        return

    bot.send_message(ADMIN_ID, f"🚀 Broadcast start ho raha hai {len(users)} users ko...")
    
    success = 0
    failed = 0

    for uid in users:
        try:
            # Copy & send as-is (Text, Photo, Video, Document sab support karta hai)
            bot.copy_message(chat_id=uid, from_chat_id=message.chat.id, message_id=message.message_id)
            success += 1
            time.sleep(0.05)  # Telegram rate limit avoid karne ke liye
        except Exception:
            failed += 1

    bot.send_message(
        ADMIN_ID, 
        f"✅ Broadcast Complete!\n\n• Safalta se bheja gaya: {success}\n• Fail (Block/Privacy): {failed}",
        parse_mode="Markdown"
    )

print("Bot successfully running...")
bot.infinity_polling()
