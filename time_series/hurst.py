import pandas as pd
import pymysql
from pylab import mpl
from data_save.tushare_data import stock_code_name, stock_data_by_name
from numpy import cumsum, log, polyfit, sqrt, std, subtract
from numpy.random import randn

mpl.rcParams['font.sans-serif'] = ['FangSong'] # 指定默认字体
mpl.rcParams['axes.unicode_minus'] = False # 解决保存图像是负号'-'显示为方块的问题

def hurst(ts):
    lags = range(2, 100)
    tau = [sqrt(std(subtract(ts[lag:], ts[:-lag]))) for lag in lags]
    poly = polyfit(log(lags), log(tau), 1)
    return poly[0] * 2.0

conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='root', db='finance', charset='utf8')
names, codes = stock_code_name(conn)  # hypothesis name number is m, time series number is n
result = []
for idx, name in enumerate(names):
    quote = stock_data_by_name(conn, name)
    series = pd.Series(quote['close'], dtype='float')
    h = hurst(series)
    if h > 0.5:
        print("{} has long-term memory, it's Hurst value: {}".format(name, h))
        result.append(name)
print(len(result))

if __name__ == '__main__':
    print("execute over")


