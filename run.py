import shioaji as sj
import pandas as pd
import numpy as np
from datetime import datetime as dt

api = sj.Shioaji()
accounts = api.login("S124541693", "Liang981165@")

def stock():
    contracts = [api.Contracts.Stocks["4743"]]
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

stock_list = stock()
print(stock_list)
