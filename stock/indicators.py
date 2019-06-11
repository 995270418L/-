# stock indicators
import pandas as pd
import numpy as np
import pandas_datareader.data as web

def ROC(data, n):
    N = data['Close'].diff(n)
    D = data['Close'].shift(n)
    ROC = pd.Series(N/D, name="Rate of Change")
    data = data.join(ROC)  # 加上ROC 这一列
    return data

def ADL(data):
    MFM = ((data['Close'] - data['Low']) - (data['High'] - data['Close'])) / (data['High'] - data['Low'])


def test():
    data = web.DataReader('^NSEI', data_source='yahoo', start='6/1/2015', end='1/1/2016')
    print("source data head: {}".format(data.head))
    data = ROC(data, 5)
    print("ROC data head: {}".format(data.head))