from flask import Flask
from bs4 import BeautifulSoup
import requests
import datetime
import time
import threading
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, StickerSendMessage, ImageSendMessage, LocationSendMessage

app = Flask(__name__)

# LINE Bot token
token = 'E4f4YyCmHJV5/zwiX4rmmN4Pqh0zWyXNzRJ+9qm2zW61zZM3PH3RRiPuWd/pYfQNb11wvZ+Ep2f/R7Z/wep2LBhku+7BBpW5y7OSTEgfPIdFk3kxHaoWKdobOWUeZgEMsylG6f7sGnolUMICPRSnZgdB04t89/1O/w1cDnyilFU='
line_bot_api = LineBotApi(token)

buy_url = "https://tixcraft.com/ticket/area/24_jaychou/"
url = "https://tixcraft.com/activity/game/24_jaychou"

last_reminder_time = time.time()

def check_tickets():
    global last_reminder_time
    while True:
        now = datetime.datetime.now()
        
        try:
            url_get = requests.get(url)
            url_get.raise_for_status()
            soup = BeautifulSoup(url_get.text, "html.parser")

            tickets = soup.findAll("tr", class_="gridc fcTxt")
            results = []
            has_tickets = False

            for ticket in tickets:
                ticket_date = ticket.find_all("td")[0].text.strip()
                yesorno = ticket.find("div", class_="text-center").text.strip()
                date_key = ticket.get("data-key")

                if yesorno != "Sold out":
                    has_tickets = True
                    results.append(f"目前時間: {now.strftime('%Y-%m-%d %H:%M:%S')}")
                    results.append(f"日期: {ticket_date}")
                    results.append(f"買的網址: {buy_url}{date_key}")
                    results.append("狀態: 去看")

            if has_tickets:
                final_results = "\n".join(results)
                line_bot_api.push_message("Ubebfaa8b88c85bfa30b27c32bbb73734", TextSendMessage(text=final_results))
                print("消息发送成功")

            current_time = time.time()
            if current_time - last_reminder_time >= 2:  # 每30分钟
                line_bot_api.push_message(
                    "你的_USER_ID",
                    TextSendMessage(text=f"目前時間: {now.strftime('%Y-%m-%d %H:%M:%S')} + 程序仍在運行中...")
                )
                print("運行狀態消息發送成功")
                last_reminder_time = current_time

        except requests.exceptions.RequestException as e:
            print(f"请求错误: {e}")

        time.sleep(10)

@app.route('/')
def home():
    print("hi")
    
    return '你好非！'
    
    



# 启动票务检查线程
if __name__ == "__main__":
    threading.Thread(target=check_tickets, daemon=True).start()
    app.run()  # Vercel 会处理主机和端口
