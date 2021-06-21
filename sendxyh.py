import getopt,sys,config,os
import pandas_datareader.data as web
import datetime
import pandas as pd
from telegram import Bot
from pandas_datareader._utils import RemoteDataError

def help():
    return "'sendxyh.py -c configpath'"

def cal_symbols_avg(ds:list, symbol:str, avgs:list,end=datetime.date.today()):
    start = end - datetime.timedelta(days=365)
    df = pd.DataFrame() #先创建一个空的dataframe， 防止判定出错
    for datasource in ds:
        try:
            df = web.DataReader(symbol.upper(), datasource,start=start,end=end)
            break
        except NotImplementedError: #数据源不存在，继续下一个数据源
            continue
        except RemoteDataError: #没有找到相关ticker的数据，和数据源无关，可以continue也可以break， 为确认其他数据源是不是也有相同问题，选择continue
            continue
    if df is not None and df.empty  == False: #判断1。 df是否没有定义；2. df是否是空的
        df = df.sort_values(by="Date") #将排序这个步骤放在了判断df是否存在之后

        if "Adj Close" in df.columns.values: #把df的cloumn名字改掉, 防止名字冲突
            df = df.rename(columns={"Close":"Close Backup","Adj Close": "Close"})

        if end == df.index.date[-1]: #做了一个checkpoint来查找今天的数据; credit for Stephen
            message = f"{symbol.upper()}价格: {df['Close'][-1]:0.2f}({df['Low'][-1]:0.2f} - {df['High'][-1]:0.2f}) \n"
            for avg in avgs:
                if df.count()[0] > avg :
                    #加入红绿灯的判断
                    if df['Close'][-1] < df.tail(avg)['Close'].mean():
                        flag = "🔴"
                    else:
                        flag = "🟢"
                    message += f"{flag} {avg} 周期均价：{df.tail(avg)['Close'].mean():0.2f}\n"
                else:
                    message += f"{avg} 周期均价因时长不足无法得出\n"
            return f"{message}\n"
        else: #还可以再细分一下具体情况，但感觉好像没有必要，哈哈
            return f"{datasource} 没找到{symbol}今天的数据，当前数据源不发出天相信息\n"
    elif RemoteDataError: #RemoteDataError表示数据不存在，归为一类；继续输出信息;不太明白为啥要两个换行
        return f"ticker {symbol} 数据不存在，无法读取数据\n\n"
    elif KeyError: #keyerror表示缺少部分key，继续输出信息了;不太明白为啥要两个换行
        return f"{symbol}的数据缺少部分key，无法读取数据\n\n"    
    else: #其他所有情况都抛出异常
        raise Exception(f"数据源出问题了\n")

if __name__ == '__main__':
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hc:", ["config="])
    except getopt.GetoptError:
        print(help())
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print(help())
            sys.exit()
        elif opt in ("-c", "--config"):
            config.config_path = arg          

    config.config_file = os.path.join(config.config_path, "config.json")
    try:
        CONFIG = config.load_config()
    except FileNotFoundError:
        print(f"config.json not found.Generate a new configuration file in {config.config_file}")
        config.set_default()
        sys.exit(2)

    bot = Bot(token = CONFIG['Token'])
    symbols = CONFIG['xyhticker']
    notifychat = CONFIG['xyhchat']
    adminchat = CONFIG['xyhlog']
    debug = CONFIG['DEBUG']
    ds = CONFIG['xyhsource']

    message = "🌈🌈🌈当日天相🌈🌈🌈: \n"
    try:
        for symbol in symbols: 
            message += cal_symbols_avg(ds,symbol[0],symbol[1:])
        if not "当前数据源不发出天相信息" in message:
            message += "贡献者:毛票教的大朋友们"
            if debug :
                print(f"{notifychat}\n{message}")
            else:
                bot.send_message(notifychat,message)
            #bot.send_message(adminchat,f"向{notifychat}发送成功夕阳红:\n{message}")
        else:
            if debug:
                print(f"{adminchat}\nAdmin Group Message: {ds} 没找到今天的数据，看来要不没开市，要不没收盘，要不数据还没更新， 当前数据源不发出天相信息")
            else:
                bot.send_message(adminchat,f"Admin Group Message: {ds} 没找到今天的数据，看来要不没开市，要不没收盘，要不数据还没更新， 当前数据源不发出天相信息")
    except Exception as err:
        if debug:
            print(f"{adminchat}\n今天完蛋了，什么都不知道，快去通知管理员，bot已经废物了，出的问题是:\n{type(err)}:\n{err}")
        else:
            bot.send_message(adminchat,f"今天完蛋了，什么都不知道，快去通知管理员，bot已经废物了，出的问题是:\n{type(err)}:\n{err}")
