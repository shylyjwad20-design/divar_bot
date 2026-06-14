import requests
import telebot
import schedule
import time
import json

BOT_TOKEN = "8721044060:AAH5XALKBtG_0SBP2XDLY0Oee4Z0NGc2u7I"
CHANNEL_ID = "@aaasd62"

bot = telebot.TeleBot(BOT_TOKEN)
seen_tokens = set()

def get_divar_ads():
    url = "https://api.divar.ir/v8/web-search/dezful/car"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
        "Accept": "application/json",
        "Referer": "https://divar.ir/s/dezful/car",
        "Origin": "https://divar.ir",
        "x-standard-divar-error": "true",
        "x-divar-web-version": "2.394.2"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=15)
        data = response.json()
        items = data.get("widget_list", [])
        
        for item in items:
            print(f"widget_type: {item.get('widget_type')}")
        
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
