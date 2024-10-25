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



@app.route('/')
def home():
    return 'Hello, World!'

if __name__ == "__main__":
   
    app.run()
