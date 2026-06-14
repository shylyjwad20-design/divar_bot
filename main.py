import requests
import telebot
import schedule
import time
from bs4 import BeautifulSoup

BOT_TOKEN = "8721044060:AAH5XALKBtG_0SBP2XDLY0Oee4Z0NGc2u7I"
CHANNEL_ID = "@aaasd62"

bot = telebot.TeleBot(BOT_TOKEN)
seen_links = set()

def get_ads():
    url = "https://sheypoor.com/s/dezful/cars"
    headers = {
        "User-Agent": "Mozilla/5.0 (Linux; Android 10) AppleWebKit/537.36"
    }
    try:
        r = requests.get(url, headers=headers, timeout=15)
        soup = BeautifulSoup(r.text, "html.parser")
        
        ads = []
        items = soup.find_all("a", class_="listing-card")
        
        for item in items[:10]:
            try:
                title = item.find("h2").text.strip()
                price = item.find("span", class_="price").text.strip()
                link = "https://sheypoor.com" + item["href"]
                
                if link not in seen_links:
                    seen_links.add(link)
                    ads.append(f"🚗 {title}\n💰 {price}\n🔗 {link}")
            except:
                continue
        
        return ads
    except Exception as e:
        print(f"خطا: {e}")
        return []

def post_ads():
    print("در حال بررسی...")
    ads = get_ads()
    print(f"{len(ads)} آگهی پیدا شد")
    for ad in ads:
        try:
            bot.send_message(CHANNEL_ID, ad)
            time.sleep(2)
        except Exception as e:
            print(f"خطا: {e}")

post_ads()
schedule.every(1).hours.do(post_ads)

while True:
    schedule.run_pending()
    time.sleep(60)
