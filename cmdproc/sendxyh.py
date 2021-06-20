from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

import pandas as pd
import pandas_datareader as pdr
import datetime

stock_data = [['spy',13,50],['qqq',13,50,200],['^SPX',55,200]]


def symbol_avgs_yahoo (symbol:str, avgs:list):
    start = datetime.date.today() - datetime.timedelta(days=365)
    end = datetime.date.today()
    df = pdr.get_data_yahoo(symbol.upper(),start=start,end=end)
    weekno = datetime.date.today().weekday()
    if weekno > 4:
        print ("今天是周末哟")
    else:
        message = f"当日天相\n{symbol.upper()}价格：{round(df.tail(1)['Close'].mean(),2)} ({round(df.tail(1)['Low'].mean(),2)} - {round(df.tail(1)['High'].mean(),2)})"
    for avg in avgs:
        message += f"{avg}周期均价：{round(df.tail(avg)['Adj Close'].mean(),2)}"
    return message

for symbol in stock_data:
    print (symbol_avgs_yahoo(stock_data[0],stock_data[1:]))
    
