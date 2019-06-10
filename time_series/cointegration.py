# https://zhuanlan.zhihu.com/p/21566798
# https://stackoverflow.com/questions/11362943/efficient-cointegration-test-in-python

import pandas as pd
import pymysql
from pylab import mpl
import statsmodels.tsa.stattools as ts
import matplotlib.pyplot as plt
from data_save.tushare_data import stock_code_name, stock_data_by_name
from itertools import combinations

mpl.rcParams['font.sans-serif'] = ['FangSong'] # 指定默认字体
mpl.rcParams['axes.unicode_minus'] = False # 解决保存图像是负号'-'显示为方块的问题

conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='root', db='finance', charset='utf8')
names, codes = stock_code_name(conn)  # hypothesis name number is m, time series number is n

quotes = []

for idx, name in enumerate(names):
    quote = stock_data_by_name(conn, name)
    quote = quote[:115]
    series = pd.Series(quote['close'], dtype='float')
    s_dict = {
        'name': name,
        'data': series
    }
    quotes.append(s_dict)

stock_cb = list(combinations(quotes, 2))
print("stock combinations length : {}".format(len(stock_cb)))
result = []
for stock_info in stock_cb:
    x = stock_info[0].get("data")
    x_name = stock_info[0].get("name")
    y = stock_info[1].get("data")
    y_name = stock_info[1].get("name")
    coin_result = ts.coint(x, y)
    adf = coin_result[0]
    p_value = coin_result[1]
    one_percent = coin_result[2][0]
    five_percent = coin_result[2][1]
    ten_percent = coin_result[2][2]
    if adf < 0.01 and adf < one_percent and adf < five_percent and adf < ten_percent:
        print("result: {}, stock tuple:{} ".format(coin_result, (x_name, y_name)))
        result.append((x_name, y_name))
print(len(result))

if __name__ == '__main__':
    print("execute over")