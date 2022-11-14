import shioaji as sj
import pandas as pd
import numpy as np
from datetime import datetime as dt
from flask import Flask, request, abort
import sqlite3

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *

app = Flask(__name__)

# 必須放上自己的Channel Access Token
line_bot_api = LineBotApi('zzUh9KHvribwehLEmlO+GhwDl/K+bxyi8xPHY8532rVhOef3fFOimt+H08o+JXCuD+bZoY2eKwNjsGdufN5l47XKyoUtlj2JTnmz1OPoffr8QBnmol3UaqwUbpce+v3OOT/8vVq5DboPe9XavbmLfQdB04t89/1O/w1cDnyilFU=')
# 必須放上自己的Channel Secret
handler = WebhookHandler('320ed24fe6ac098d810cf99649840800')

line_bot_api.push_message('U837080b63aa93f9574e7f70e3c5b2c5e', TextSendMessage(text='你可以開始了'))

# 監聽所有來自 /callback 的 Post Request
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

# 我是分隔線

dbname = "TWStock.db"
db = sqlite3.connect(dbname)
cursorfordatabase = db.cursor()
query_for_samplefile = """SELECT * from number"""
cursorfordatabase.execute(query_for_samplefile)
required_records = cursorfordatabase.fetchall()
list1 = []
for row in required_records:
   list1.append(row)

api = sj.Shioaji()
accounts = api.login("帳號", "密碼")

# 我是分隔線

def stock(number):
    contracts = [api.Contracts.Stocks[number]]
    snapshots = api.snapshots(contracts)
    df = pd.DataFrame(snapshots)
    list_of_df = np.array(df)
    main = []
    for a in list_of_df:
        for a_deeper in a:
            a_deeper = a_deeper.__str__()
            a_deeper = a_deeper.replace("(", "").replace(")", "")
            if a_deeper[:8] == "'open', ":
                a_deeper = a_deeper.replace("'open', ", "")
                main.append(a_deeper)
            elif a_deeper[:8] == "'high', ":
                a_deeper = a_deeper.replace("'high', ", "")
                main.append(a_deeper)
            elif a_deeper[:7] == "'low', ":
                a_deeper = a_deeper.replace("'low', ", "")
                main.append(a_deeper)
            elif a_deeper[:9] == "'close', ":
                a_deeper = a_deeper.replace("'close', ", "")
                main.append(a_deeper)
            elif a_deeper[:13] == "'buy_price', ":
                a_deeper = a_deeper.replace("'buy_price', ", "")
                main.append(a_deeper)
            elif a_deeper[:14] == "'sell_price', ":
                a_deeper = a_deeper.replace("'sell_price', ", "")
                main.append(a_deeper)
    now = dt.now()
    now = now.strftime("%Y/%m/%d")
    main.append(now)
    return main


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    a = event.message.text
    for row in list1:
      if a == row[1]:
        stock_list = stock(a)
        stock_message = "日期: " + stock_list[6] + '\n' + "開盤: " + stock_list[0] + '\n' + "最高價: " + stock_list[1] + '\n' + "最低價: " + \
            stock_list[2] + '\n' + "收盤價: " + stock_list[3] + '\n' + \
            "賣價: " + stock_list[4] + '\n' + "買價: " + stock_list[5]
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=stock_message))
      elif a == row[2]:
        a = row[1]
        stock_list = stock(a)
        stock_message = "日期: " + stock_list[6] + '\n' + "開盤: " + stock_list[0] + '\n' + "最高價: " + stock_list[1] + '\n' + "最低價: " + \
            stock_list[2] + '\n' + "收盤價: " + stock_list[3] + '\n' + \
            "賣價: " + stock_list[4] + '\n' + "買價: " + stock_list[5]
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=stock_message))
#主程式
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)



