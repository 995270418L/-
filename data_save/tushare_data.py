from data_save.scrapy import StockCrapy
from bs4 import BeautifulSoup
import tushare as ts
import pandas as pd
import time
import pymysql
import numpy as np

def hs300(end):
    stock = StockCrapy()
    tickets = []
    for i in range(1, end):
        base_url = 'http://vip.stock.finance.sina.com.cn/corp/view/vII_NewestComponent.php?page=%s&indexid=000300' % str(i)
        text = stock.request_html_get(base_url, 'gb2312')
        soup = BeautifulSoup(text, 'lxml')
        trs = soup.select('div #con02-0 > #NewStockTable > tr')
        for tr_idx in range(1, len(trs)):
            tds = trs[tr_idx].select("td")
            code_dict = {}
            for td_idx in range(0, len(tds)-1):
                td = tds[td_idx]
                if td_idx % 2 == 0:
                    code = td.select("div")[0].get_text()
                    s_code = code[:2]
                    if s_code == '60':
                        code = str(code) + ".SH"
                    elif s_code == '00' or s_code == '30':
                        code = str(code) + ".SZ"
                    else:
                        print("code : {} 非上交所和深证交易所股票".format(code))
                    code_dict["code"] = code
                else:
                    name = td.select('div > a')[0].get_text()
                    code_dict['name'] = name
            tickets.append(code_dict)
    return tickets

def saveToDB(conn, df, name):
    cursor = conn.cursor()
    dt = time.strftime('%Y%m%d', time.localtime())
    values = []
    for index, row in df.iterrows():
        val = (name, row['ts_code'], row['trade_date'], float(row['open']), float(row['high']), float(row['low']), float(row['close']), float(row['vol']), float(row['amount']), dt, dt)
        values.append(val)
    print("values length: {}".format(len(values)))
    cursor.executemany("insert into stock_daily(name,code,price_date, open_price, high_price, low_price, close_price, vol, amount, create_date, update_date) "
                       "values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", values)
    try:
        conn.commit()
    except:
        print("插入数据异常")
        conn.rollback()
        # cursor.execute("insert into stock_daily(code,price_date, open_price, high_price, low_price, close_price, vol, amount, create_date, update_date) "
        #                "values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", (row['ts_code'], row['trade_date'],
        #                                                           float(row['open']), float(row['high']), float(row['low']), float(row['close']), float(row['vol']), float(row['amount']), dt, dt))
        # print(cursor.lastrowid)



def get_ticket_daily(conn,tickets):
    ts.set_token("your_token")
    pro = ts.pro_api()
    print(len(tickets))
    for index, ticket in enumerate(tickets):
        code = ticket.get("code")
        name = ticket.get("name")
        df = pro.query('daily', ts_code=code, start_date="20180101", end_date="20190608")
        saveToDB(conn, df, name)
        time.sleep(1)
        print("{} sleep over".format(index))

# 返回去重后的股票编码和名字
def stock_code_name(conn):
    cursor = conn.cursor()
    cursor.execute("select code,name from stock_daily")
    stock_list = [item for item in cursor.fetchall()]
    sorted_stock_list = list(set(stock_list))
    codes, names = np.array(sorted(sorted_stock_list)).T
    return names, codes

# 获取指定名称的股票 DataFrame
def stock_data_by_name(conn, name):
    cursor = conn.cursor()
    cursor.execute("select price_date, open_price, close_price from stock_daily where name=%s order by create_date desc", name)
    return pd.DataFrame([item for item in cursor.fetchall()], columns=["date", "open", "close"])


if __name__ == '__main__':
    conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='root', db='finance', charset='utf8')
    get_ticket_daily(conn , hs300(9))

