# https://www.joinquant.com/
from jqdatasdk import *
import time
import pymysql
import pandas as pd

def login():
    auth('YOUR_ACCOUNT', 'YOUT_PASS')

def save_all_data():
    indexs = get_all_securities(types=['index'], date=None) # 获取平台支持的所有指数数据

def get_csi_data(conn):
    cursor = conn.cursor()
    cursor.execute(
        "select price_date, open_price, high_price, low_price, close_price ,adj_close_price, vol, amount from stock_daily where name=%s order by price_date", '沪深300')
    return pd.DataFrame([item for item in cursor.fetchall()], columns=["date", "open", 'high', 'low', 'close', 'adj_close', 'vol', 'amount'])

def save_single_data(conn, name,code):
    df = get_price(code, start_date='2005-04-08', end_date='2019-06-12', frequency='daily', fields=None, skip_paused=False, fq='pre')
    cursor = conn.cursor()
    values = []
    dt = time.strftime('%Y%m%d', time.localtime())
    for index, row in df.iterrows():
        val = (name, code, index.strftime('%Y-%m-%d'), float(row['open']), float(row['high']), float(row['low']), float(row['close']), float(row['volume']), float(row['money']), dt, dt)
        values.append(val)
    print(len(values))
    cursor.executemany(
        "insert into stock_daily(name,code,price_date, open_price, high_price, low_price, close_price, vol, amount, create_date, update_date) "
        "values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", values)
    try:
        conn.commit()
    except:
        print("插入数据异常")
        conn.rollback()

if __name__ == '__main__':
    # time.strptime('2019-06-13 00:00:00', '%Y-%m-%d')
    # date = time.strftime("%Y%m%d", '2019-06-13 00:00:00')
    # print(date)
    login()
    conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='root', db='finance', charset='utf8')
    save_single_data(conn, '沪深300', '399300.XSHE')
