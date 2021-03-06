# unit root test
import pandas as pd
import pymysql
from pylab import mpl
from statsmodels.tsa.stattools import adfuller
import matplotlib.pyplot as plt
from data_save.tushare_data import stock_code_name, stock_data_by_name

mpl.rcParams['font.sans-serif'] = ['FangSong'] # 指定默认字体
mpl.rcParams['axes.unicode_minus'] = False # 解决保存图像是负号'-'显示为方块的问题

conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='root', db='finance', charset='utf8')
names, codes = stock_code_name(conn)  # hypothesis name number is m, time series number is n
result = []
for idx, name in enumerate(names):
    quote = stock_data_by_name(conn, name)
    series = pd.Series(quote['close'], dtype='float')
    result_tuple = adfuller(series)
    adf = result_tuple[0]
    p_value = result_tuple[1]
    one_percent = result_tuple[4].get("1%")
    five_percent = result_tuple[4].get("5%")
    ten_percent = result_tuple[4].get("10%")
    if adf < 0.01 and adf < one_percent and adf < five_percent and adf < ten_percent :
        print("{} is mean reverting, it don't have unit root, it's data {}".format(name, result_tuple))
        # plot it
        # plt.plot(series)
        # plt.title(name)
        # plt.show()
        result.append(name)

print(len(result))
if __name__ == '__main__':
    print("executor over")