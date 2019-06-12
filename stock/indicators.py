# stock indicators 随机森林 ann 线性模型
import pandas as pd
import pymysql
import matplotlib.pyplot as plt
from data_save.jq import get_csi_data


def ROC(data, n):
    N = data['Close'].diff(n)
    D = data['Close'].shift(n)
    ROC = pd.Series(N/D, name="Rate of Change")
    data = data.join(ROC)  # 加上ROC 这一列
    return data

def adl(data):
    lastADL = 0
    adl_list = []
    for index, row in data.iterrows():
        MFM = ((row['close'] - row['low']) - (row['high'] - row['close'])) / (row['high'] - row['low'])
        MFV = MFM * row['vol']
        if index == 0:
            adl = lastADL = MFV
        else:
            adl = lastADL + MFV
            lastADL = adl
        adl_list.append(adl)
    data = data.join(pd.DataFrame(adl_list, columns=["ADL"]))
    return data

def ma10(data):
    series = ma(data, 10)
    series.name = 'MA10'
    return data.join(series)

def ma20(data):
    series = ma(data, 20)
    series.name = 'MA20'
    return data.join(series)

def ma5(data):
    series = ma(data, 5)
    series.name = 'MA5'
    return data.join(series)

def ma(data, ndays):
    # data[['close']] = data[['close']].astype(float)
    return pd.Series(data['close'].rolling(ndays).mean())

def aroon(data):
    up_list = []
    down_list = []
    data[['close']] = data[['close']].astype(float)
    for index, row in data.iterrows():
        aroon_preriods = data['close'][index:index+25]
        max_idx = aroon_preriods.idxmax()
        min_idx = aroon_preriods.idxmin()
        max_days = index + 25 - 1 - max_idx
        min_days = index + 25 - 1 - min_idx
        aroon_up = (25 - max_days) / 25 * 100
        aroon_down = (25 - min_days) / 25 * 100
        up_list.append(aroon_up)
        down_list.append(aroon_down)
    data = data.join(pd.DataFrame(up_list, columns=["AROON_UP"]))
    data = data.join(pd.DataFrame(down_list, columns=["AROON_DOWN"]))
    return data

def add_features_for_data(data):
    data = aroon(data)
    data = ma5(data)
    data = ma10(data)
    data = ma20(data)
    return data