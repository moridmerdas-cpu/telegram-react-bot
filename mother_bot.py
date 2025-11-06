import os
import sys
import subprocess

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", package])

# نصب خودکار کتابخانه‌ها
try:
    import telegram
except ImportError:
    install("python-telegram-bot")

try:
    import requests
except ImportError:
    install("requests")
import telebot
from config import MOTHER_BOT_TOKEN, OWNER_ID, CHILD_BOTS
import child_bots
import time

bot = telebot.TeleBot(MOTHER_BOT_TOKEN)

# مطمئن شو همه‌ی ربات‌ها داخل bot_status ثبت شدن
for token in CHILD_BOTS:
    if token not in child_bots.bot_status:
        child_bots.bot_status[token] = True

@bot.message_handler(commands=['start'])
def start_message(message):
    if message.from_user.id != OWNER_ID:
        bot.reply_to(message, "سلام! این ربات فقط برای ادمین اصلی فعاله 😊")
        return

    text = "🤖 سلام امیر!\n\nوضعیت ربات‌ها:\n"
    for i, token in enumerate(CHILD_BOTS, start=1):
        status = "🟢 روشن" if child_bots.bot_status.get(token, True) else "🔴 خاموش"
        text += f"ربات {i}: {status}\n"
    text += "\nبرای روشن یا خاموش کردن:\n/on شماره\n/off شماره"
    bot.reply_to(message, text)

@bot.message_handler(commands=['on'])
def turn_on(message):
    if message.from_user.id != OWNER_ID:
        return
    try:
        index = int(message.text.split()[1]) - 1
        token = CHILD_BOTS[index]
        child_bots.bot_status[token] = True
        bot.reply_to(message, f"✅ ربات {index+1} روشن شد.")
    except Exception as e:
        bot.reply_to(message, f"❌ خطا: {e}")

@bot.message_handler(commands=['off'])
def turn_off(message):
    if message.from_user.id != OWNER_ID:
        return
    try:
        index = int(message.text.split()[1]) - 1
        token = CHILD_BOTS[index]
        child_bots.bot_status[token] = False
        bot.reply_to(message, f"🛑 ربات {index+1} خاموش شد.")
    except Exception as e:
        bot.reply_to(message, f"❌ خطا: {e}")

if __name__ == "__main__":
    print("✅ ربات مادر اجرا شد.")
    # چند ثانیه صبر می‌کنه تا بچه‌ها لود بشن
    time.sleep(3)
    bot.polling(non_stop=True)


