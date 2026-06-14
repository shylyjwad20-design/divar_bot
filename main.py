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
    headers = {"User-Agent": "Mozilla/5.0"}
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        data = response.json()
        
        print("کلیدهای JSON:", list(data.keys()))
        
        ads = []
        
        # روش اول
        post_list = data.get("web_widgets", {}).get("post_list", [])
        
        # روش دوم
        if not post_list:
            post_list = data.get("widget_list", [])
        
        print(f"تعداد آیتم‌ها: {len(post_list)}")
        
        for item in post_list:
            try:
                item_data = item.get("data", {})
                title = item_data.get("title", "")
                token = item_data.get("token", "")
                
                if not title or not token:
                    continue
                
                top_desc = item_data.get("top_description_text", "")
                mid_desc = item_data.get("middle_description_text", "")
                price = top_desc or mid_desc or "قیمت توافقی"
                
                link = f"https://divar.ir/v/{token}"
                
                if token not in seen_tokens:
                    seen_tokens.add(token)
                    ads.append(f"🚗 {title}\n💰 {price}\n🔗 {link}")
            except Exception as e:
                print(f"خطا در پردازش آیتم: {e}")
                continue
        
        return ads
    except Exception as e:
        print(f"خطا در دریافت داده: {e}")
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
