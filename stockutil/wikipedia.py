from datetime import datetime
import pickle
import pandas as pd
import stooq


# import requests
# import bs4 as bs
# def get_sp500_tickers():
#     resp = requests.get('http://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
#     soup = bs.BeautifulSoup(resp.text, 'lxml')
#     table = soup.find('table', {'class': 'wikitable sortable'})
#     tickers = []
#     for row in table.findAll('tr')[1:]:
#         ticker = row.findAll('td')[0].text[:-1]
#         tickers.append(ticker)
#     return tickers

def get_sp500_tickers():
    table=pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
    df = table[0]
    return df['Symbol'].tolist()

def get_ndx100_tickers():
    table = pd.read_html('https://en.wikipedia.org/wiki/Nasdaq-100#Components')
    df = table[3]
    return df['Ticker'].tolist()

def save_list(list,filename):
    # with open("sp500tickers.pickle", "wb") as f:
    #     pickle.dump(tickers, f)
    with open(filename, "wb") as f:
        pickle.dump(list, f)

def load_list(filename):
    tickers = []
    with open(filename, "rb") as f:
        tickers = pickle.load(f)
    return tickers

if __name__ == '__main__':
    # 本程序只是用于测试，正常使用请from stockutil import wikipedia
    sp500 = get_sp500_tickers()
    ndx100 = get_ndx100_tickers()
    indexes = [sp500,ndx100]
    indexnames = ["SP500","NDX100"]
    up = []
    down = []
    for index in indexes:
        for symbol in index:
            if stooq.symbol_above_moving_average(symbol):
                up.append(symbol)
            else:
                down.append(symbol)
        for name in indexnames:
            print(f"{name}共有{len(up)+len(down)}支股票，共有{len(up)/(len(up)+len(down))*100:.2f}%高于20周期均线")
            #两个index的名字会在没重跑50行的for loop之前先跑一次 导致结果“SP500共有505支股票 NDX100共有505支股票 SP500共有102支股票 NDX100共有102支股票”
        up.clear()
        down.clear()

    #还做了一个超级大的骚操作 把stooq下载到本地的文档BRK-B和BF-B文件名改成BRK.B和BF.B 因为wiki上的格式是.B而不是-B