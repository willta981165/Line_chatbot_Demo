from cgi import test
from re import L
from unittest import result
import requests
import pandas as pd
import io


def  crawler(data_time):
    url = "https://www.twse.com.tw/exchangeReport/MI_INDEX?response=csv&date=" + data_time + "&type=ALLBUT0999"
    page = requests.get(url)
    use_text = page.text.splitlines()
    for i, text in enumerate(use_text):
       if text == '"證券代號","證券名稱","成交股數","成交筆數","成交金額","開盤價","最高價","最低價","收盤價","漲跌(+/-)","漲跌價差","最後揭示買價","最後揭示買量","最後揭示賣價","最後揭示賣量","本益比",':
           initital_point = i
           break
    test_df = pd.read_csv(io.StringIO(''.join([text[:-1] + '\n' for text in use_text[initital_point:]])))
    test_df['證券代號'] = test_df['證券代號'].apply(lambda x: x.replace('"', ''))
    test_df['證券代號'] = test_df['證券代號'].apply(lambda x: x.replace('=', ''))
    test_df = test_df.drop(['成交股數', '成交筆數', '成交金額', '開盤價', '最高價', '最低價', '收盤價',
                            '漲跌(+/-)', '漲跌價差', '最後揭示買價', '最後揭示買量', '最後揭示賣價', '最後揭示賣量', '本益比'], axis=1)
    return test_df

import datetime
import time

def trans_date(date_time):
    return ''.join(str(date_time).split(' ')[0].split('-'))


def parsn_n_days(start_date,n):
    df_dict = {}
    now_date = start_date
    for i in range(n):
        time.sleep(3)
        now_date = now_date - datetime.timedelta(days=1)
        try:
            df = crawler(trans_date(now_date))
            print("成功"+' '+trans_date(now_date))
            df_dict.update({trans_date(now_date): df})
        except:
            print("失敗"+' '+trans_date(now_date))
    return df_dict
    # 結果 = df_dict


result_dict = parsn_n_days(datetime.datetime.now(), 1)
for key in result_dict.keys():
    result_dict[key].to_excel("number.xlsx", encoding="utf_8_sig")




