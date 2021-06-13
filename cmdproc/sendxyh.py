from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

import pandas as pd
import pandas_datareader as pdr
import datetime

stock_data = [['spy',13,50],['qqq',13,50,200],['^SPX',55,200]]
symbol = [item[0] for item in stock_data]
ma_1 = [item[1] for item in stock_data]
ma_2 = [item[2] for item in stock_data]
ma_3 = stock_data[1][3]

start = datetime.date.today() - datetime.timedelta(days=365)
end = datetime.date.today()

df = pdr.get_data_yahoo(symbol[0].upper(),start=start,end=end)
spy_average_ma_1 = round(df.tail(int(ma_1[0]))['Close'].mean(),2)
spy_average_ma_2 = round(df.tail(int(ma_2[0]))['Close'].mean(),2)
spy_today_close = round(df.tail(1)['Close'].mean(),2)
spy_today_low = round(df.tail(1)['Low'].mean(),2)
spy_today_high = round(df.tail(1)['High'].mean(),2)

df = pdr.get_data_yahoo(symbol[1].upper(),start=start,end=end)
qqq_average_ma_1 = round(df.tail(int(ma_1[1]))['Close'].mean(),2)
qqq_average_ma_2 = round(df.tail(int(ma_2[1]))['Close'].mean(),2)
qqq_average_ma_3 = round(df.tail(int(ma_3))['Close'].mean(),2)
qqq_today_close = round(df.tail(1)['Close'].mean(),2)
qqq_today_low = round(df.tail(1)['Low'].mean(),2)
qqq_today_high = round(df.tail(1)['High'].mean(),2)

df = pdr.get_data_yahoo(symbol[2].upper(),start=start,end=end)
SPX_average_ma_1 = round(df.tail(int(ma_1[2]))['Close'].mean(),2)
SPX_average_ma_2 = round(df.tail(int(ma_2[2]))['Close'].mean(),2)
SPX_today_close = round(df.tail(1)['Close'].mean(),2)
SPX_today_low = round(df.tail(1)['Low'].mean(),2)
SPX_today_high = round(df.tail(1)['High'].mean(),2)

bot_reply = f"""
当日天相
SPY价格： {spy_today_close} ({spy_today_low}-{spy_today_high})
13周期均价： {spy_average_ma_1}
50周期均价： {spy_average_ma_2}

QQQ价格： {qqq_today_close} ({qqq_today_low}-{qqq_today_high})
13周期均价： {qqq_average_ma_1}
50周期均价： {qqq_average_ma_2}
200周期均价：{qqq_average_ma_3}

^SPX价格： {SPX_today_close} ({SPX_today_low}-{SPX_today_high})
55周期均价： {SPX_average_ma_1}
200周期均价： {SPX_average_ma_2}
"""
print(bot_reply)

def sendxyh(update: Update, _: CallbackContext) -> None:
    bot = update.effective_message.bot
    bot.send_message(-1001430794202,bot_reply)

def add_dispatcher(dp):
    dp.add_handler(CommandHandler("xyh", sendxyh))
    return []
