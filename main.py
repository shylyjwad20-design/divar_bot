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
        "Accept-Language": "fa-IR,fa;q=0.9",
        "Referer": "https://divar.ir/s/dezful/car",
        "Origin": "https://divar.ir",
        "x-standard-divar-error": "true"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=15)
        print(f"وضعیت: {response.status_code}")
        data = response.json()
        print(f"کلیدها: {list(data.keys())}")
        
        items = data.get("widget_list", [])
        print(f"تعداد: {len(items)}")
        
        ads = []
        for item in items:
            try:
                widget_type = item.get("widget_type", "")
                if widget_type != "POST_ROW":
                    continue
                    
                d = item.get("data", {})
                title = d.get("title", "")
                token = d.get("token", "")
                price = d.get("bottom_description", {}).get("text", "توافقی")
                
                if title and token and token not in seen_tokens:
                    seen_tokens.add(token)
                    ads.append(f"🚗 {title}\n💰 {price}\n🔗 https://divar.ir/v/{token}")
            except:
                continue
        
        return ads
    except Exception as e:
        print(f"خطا: {e}")
        return []

def post_ads():
    print("در حال بررسی...")
    ads = get_divar_ads()
    print(f"{len(ads)} آگهی پیدا شد")
    for ad in ads:
        try:
            bot.send_message(CHANNEL_ID, ad)
            time.sleep(2)
        except Exception as e:
            print(f"خطا در ارسال: {e}")

post_ads()
schedule.every(1).hours.do(post_ads)

while True:
    schedule.run_pending()
    time.sleep(60)
