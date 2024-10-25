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

# LINE Bot API Token
token = 'E4f4YyCmHJV5/zwiX4rmmN4Pqh0zWyXNzRJ+9qm2zW61zZM3PH3RRiPuWd/pYfQNb11wvZ+Ep2f/R7Z/wep2LBhku+7BBpW5y7OSTEgfPIdFk3kxHaoWKdobOWUeZgEMsylG6f7sGnolUMICPRSnZgdB04t89/1O/w1cDnyilFU='
line_bot_api = LineBotApi(token)

buy_url = "https://tixcraft.com/ticket/area/24_jaychou/"
url = "https://tixcraft.com/activity/game/24_jaychou"

last_reminder_time = time.time()  # 记录上次发送运行状态的时间

def check_tickets():
    global last_reminder_time
    while True:
        # 获取当前时间
        now = datetime.datetime.now()

        # 请求网页
        url_get = requests.get(url)
        soup = BeautifulSoup(url_get.text, "html.parser")

        # 查找票务信息
        tickets = soup.findAll("tr", class_="gridc fcTxt")
        results = []  # 用于存储输出的字符串

        has_tickets = False  # 标记是否有票

        for ticket in tickets:
            ticket_date = ticket.find_all("td")[0].text.strip()  # 获取日期信息
            yesorno = ticket.find("div", class_="text-center").text.strip()  # 获取状态
            date_key = ticket.get("data-key")  # 获取 data-key

            if yesorno != "Sold out":
                has_tickets = True  # 如果有票，更新标记
                results.append(f"目前时间: {now.strftime('%Y-%m-%d %H:%M:%S')}")  # 添加当前时间
                results.append(f"日期: {ticket_date}")  # 添加日期
                results.append(f"买的链接: {buy_url}{date_key}")  # 添加网址
                results.append("状态: 去看")  # 添加票务状态

        # 仅在有票的情况下发送消息
        if has_tickets:
            final_results = "\n".join(results)
            try:
                line_bot_api.push_message("Ubebfaa8b88c85bfa30b27c32bbb73734", TextSendMessage(text=final_results))
                print("消息发送成功")
            except Exception as e:
                print(f"发送消息时出错: {e}")

        # 每半小时发送一次程序运行状态
        current_time = time.time()
        if current_time - last_reminder_time >= 1800:  # 1800秒 = 30分钟
            try:
                line_bot_api.push_message(
                    "Ubebfaa8b88c85bfa30b27c32bbb73734",
                    TextSendMessage(text=f"目前时间: {now.strftime('%Y-%m-%d %H:%M:%S')} + 程序仍在运行中...")
                )
                print("运行状态消息发送成功")
                last_reminder_time = current_time  # 更新上次发送时间
            except Exception as e:
                print(f"发送状态消息时出错: {e}")

        # 等待10秒
        time.sleep(10)

@app.route('/')
def home():
    return 'Hello, World!'

if __name__ == "__main__":
    # 启动票务检查线程
    ticket_thread = threading.Thread(target=check_tickets)
    ticket_thread.daemon = True  # 设置为守护线程
    ticket_thread.start()

    # 启动 Flask 应用
    app.run()
