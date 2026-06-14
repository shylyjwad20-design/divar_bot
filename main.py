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
    url = "https://api.divar.ir/v8/postlist/w/search"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Content-Type": "application/json",
        "Origin": "https://divar.ir",
        "Referer": "https://divar.ir/"
    }
    payload = {
        "city_ids": ["23"],
        "category": "light-cars-and-vans",
        "pagination_data": {
            "@type": "type.googleapis.com/postlist.CursorBasedPaginationData",
            "cursor": ""
        }
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=10)
        data = response.json()
        
        print(f"کلیدها: {list(data.keys())}")
        
        post_list = data.get("list_widgets", [])
        print(f"تعداد آیتم‌ها: {len(post_list)}")
        
        if post_list:
            print(json.dumps(post_list[0], ensure_ascii=False, indent=2))
        
        ads = []
        for item in post_list:
            try:
                item_data = item.get("data", {})
                title = item_data.get("title", "")
                token = item_data.get("token", "")
                price = item_data.get("bottom_description", {}).get("text", "قیمت توافقی")
                
                if title and token and token not in seen_tokens:
                    seen_tokens.add(token)
                    link = f"https://divar.ir/v/{token}"
                    ads.append(f"🚗 {title}\n💰 {price}\n🔗 {link}")
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
