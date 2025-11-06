import telebot
import threading
import time
from config import CHILD_BOTS, REACTION_EMOJI

# وضعیت هر ربات (روشن یا خاموش)
bot_status = {}

def run_child_bot(token):
    bot_status[token] = True  # پیش‌فرض روشن

    bot = telebot.TeleBot(token, parse_mode=None)

    @bot.channel_post_handler(func=lambda message: True)
    def handle_channel_post(message):
        if not bot_status[token]:
            return  # اگر خاموش بود، هیچی نکنه
        try:
            bot.set_message_reaction(
                chat_id=message.chat.id,
                message_id=message.message_id,
                reaction=[{"type": "emoji", "emoji": REACTION_EMOJI}]
            )
            print(f"✅ ری‌اکشن در کانال: {message.chat.title}")
        except Exception as e:
            print(f"⚠️ خطا در {token[:6]}: {e}")

    while True:
        try:
            bot.polling(none_stop=True, interval=1)
        except Exception as e:
            print(f"🔁 ربات {token[:6]} ری‌استارت شد: {e}")
            time.sleep(3)

def start_all_bots():
    for token in CHILD_BOTS:
        t = threading.Thread(target=run_child_bot, args=(token,))
        t.daemon = True  # برای سازگاری با پایتون ۳.۸
        t.start()
    print("✅ همه ربات‌های فرعی اجرا شدن. منتظر پست‌های جدید باش.")

# فقط وقتی مستقیم اجرا بشه، این بخش فعال شه
if __name__ == "__main__":
    start_all_bots()
    while True:
        time.sleep(10)
