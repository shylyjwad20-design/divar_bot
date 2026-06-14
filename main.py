import requests
import telebot
import schedule
import time

BOT_TOKEN = "8721044060:AAH5XALKBtG_0SBP2XDLY0Oee4Z0NGc2u7I"
CHANNEL_ID = "@aaasd62"

bot = telebot.TeleBot(BOT_TOKEN)
seen_tokens = set()

def get_divar_ads():
    url = "https://divar.ir/s/dezful/car"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "fa-IR,fa;q=0.9",
        "Referer": "https://divar.ir/"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=15)
        print(f"وضعیت: {response.status_code}")
        print(f"اول متن: {response.text[:500]}")
        return []
    except Exception as e:
        print(f"خطا: {e}")
        return []

def post_ads():
    print("در حال بررسی...")
    get_divar_ads()

post_ads()

schedule.every(1).hours.do(post_ads)

while True:
    schedule.run_pending()
    time.sleep(60)
