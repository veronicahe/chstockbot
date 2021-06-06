from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

import pandas as pd
import pandas_datareader as pdr
import datetime

start_thirteen = datetime.date.today() - datetime.timedelta(days=13)
start_fifty = datetime.date.today() - datetime.timedelta(days=50)
start_twohundred = datetime.date.today() - datetime.timedelta(days=200)
end = datetime.date.today()

symbol = 'spy'
df = pdr.get_data_yahoo(symbol.upper(),start=start_thirteen,end=end)
spy_thirteen_average = round(df['Close'].mean(),2)
df = pdr.get_data_yahoo(symbol.upper(),start=start_fifty,end=end)
spy_fifty_average = round(df['Close'].mean(),2)
df = pdr.get_data_yahoo(symbol.upper(),start=start_twohundred,end=end)
spy_twohundred_average = round(df['Close'].mean(),2)
df = pdr.get_data_yahoo(symbol.upper(),start=end,end=end)
spy_today_close = round(df['Close'].mean(),2)
spy_today_low = round(df['Low'].mean(),2)
spy_today_high = round(df['High'].mean(),2)

symbol = 'qqq'
df = pdr.get_data_yahoo(symbol.upper(),start=start_thirteen,end=end)
qqq_thirteen_average = round(df['Close'].mean(),2)
df = pdr.get_data_yahoo(symbol.upper(),start=start_fifty,end=end)
qqq_fifty_average = round(df['Close'].mean(),2)
df = pdr.get_data_yahoo(symbol.upper(),start=start_twohundred,end=end)
qqq_twohundred_average = round(df['Close'].mean(),2)
df = pdr.get_data_yahoo(symbol.upper(),start=end,end=end)
qqq_today_close = round(df['Close'].mean(),2)
qqq_today_low = round(df['Low'].mean(),2)
qqq_today_high = round(df['High'].mean(),2)

bot_reply = f"""
当日天相
SPY价格： {spy_today_close} ({spy_today_low}-{spy_today_high})
13周期均价： {spy_thirteen_average}
50周期均价： {spy_fifty_average}

QQQ价格： {qqq_today_close} ({qqq_today_low}-{qqq_today_high})
13周期均价： {qqq_thirteen_average}
50周期均价： {qqq_fifty_average}
200周期均价： {qqq_twohundred_average}
"""

def sendxyh(update: Update, _: CallbackContext) -> None:
    bot = update.effective_message.bot
    bot.send_message(-1001430794202,bot_reply)

def add_dispatcher(dp):
    dp.add_handler(CommandHandler("xyh", sendxyh))
    return []
