import requests
from bs4 import BeautifulSoup
import telebot
import schedule
import time
import os

BOT_TOKEN = "8721044060:AAH5XALKBtG_0SBP2XDLY0Oee4Z0NGc2u7I"
CHANNEL_ID = "@aaasd62"

bot = telebot.TeleBot(BOT_TOKEN)

seen_ads = set()

def get_divar_ads():
    url = "https://divar.ir/s/dezful/car"
    headers = {"User-Agent": "Mozilla/5.0"}
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")
        
        ads = []
        items = soup.find_all("div", class_="post-card-item")
        
        for item in items[:10]:
            try:
                title = item.find("h2").text.strip()
                price = item.find("div", class_="post-card-description").text.strip()
                link_tag = item.find("a")
                link = "https://divar.ir" + link_tag["href"] if link_tag else ""
                
                if link not in seen_ads:
                    seen_ads.add(link)
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
