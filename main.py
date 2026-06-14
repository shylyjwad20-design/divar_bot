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
    url = "https://api.divar.ir/v8/web-search/dezful/light-cars-and-vans"
    headers = {
        "User-Agent": "Mozilla/5.0 (Linux; Android 10) AppleWebKit/537.36 Chrome/120.0.0.0 Mobile Safari/537.36",
        "x-standard-divar-error": "true",
        "x-divar-web-version": "4.0.0"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        data = response.json()
        
        widget_list = data.get("widget_list", [])
        print(f"تعداد آیتم‌ها: {len(widget_list)}")
        
        if widget_list:
            print(json.dumps(widget_list[0], ensure_ascii=False, indent=2))
        
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
