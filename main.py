import requests
import telebot
import schedule
import time
import json

BOT_TOKEN = "8721044060:AAH5XALKBtG_0SBP2XDLY0Oee4Z0NGc2u7I"
CHANNEL_ID = "@aaasd62"

bot = telebot.TeleBot(BOT_TOKEN)

seen_ads = set()

def get_divar_ads():
    url = "https://api.divar.ir/v8/web-search/dezful/car"
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        data = response.json()
        
        ads = []
        items = data.get("widget_list", [])
        
        for item in items:
            try:
                data_item = item.get("data", {})
                title = data_item.get("title", "")
                price = data_item.get("bottom_description", {}).get("text", "بدون قیمت")
                token = data_item.get("token", "")
                link = f"https://divar.ir/v/{token}"
                
                if token and token not in seen_ads:
                    seen_ads.add(token)
                    ads.append(f"🚗 {title}\n💰 {price}\n🔗 {link}")
            except:
                continue
        
        return ads
    except Exception as e:
        print(f"خطا: {e}")
        return []

def post_ads():
    print("در حال بررسی آگهی‌های جدید...")
    ads = get_divar_ads()
    print(f"{len(ads)} آگهی پیدا شد")
    
    if not ads:
        print("آگهی جدیدی پیدا نشد")
        return
    
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
