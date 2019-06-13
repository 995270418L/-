# the csi data

import numpy as np
import pandas as pd
import pymysql
import matplotlib.pyplot as plt
from data_save.jq import get_csi_data
from stock.indicators import add_features_for_data
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.tree import DecisionTreeClassifier
from sklearn.tree import DecisionTreeRegressor

from keras.models import Sequential
from keras.layers import Dense

def get_data():
    conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='root', db='finance', charset='utf8')
    data = get_csi_data(conn)
    data = add_features_for_data(data)
    data.dropna(subset=['MA5', 'MA10', 'MA20'], inplace=True)
    return data

def get_data_classfier():
    data = get_data()
    diff = pd.Series(data['close'] - data['open'], name="class", dtype='float64')
    X = data.drop(columns=['close', 'date', 'adj_close'])
    y = diff.apply(lambda x: 1 if x > 0 else 0)
    print('X Features :{}'.format(X.columns))
    print("X shape:{}\t y shape:{}".format(X.shape, y.shape))
    return X, y

def get_data_regression():
    data = get_data()
    X = data.drop(columns=['close', 'date', 'adj_close'])
    y = pd.Series(data['close'], name='target')
    print('X Features :{}'.format(X.columns))
    print("X shape:{}\t y shape:{}".format(X.shape, y.shape))
    return X, y

def feature_importance(X, y):
    forest = ExtraTreesClassifier(n_estimators=100, random_state=0)
    forest.fit(X, y)
    importances = forest.feature_importances_
    print("importances length: {}, estimators number:{}".format(len(importances), len(forest.estimators_)))
    std = np.std([tree.feature_importances_ for tree in forest.estimators_], axis=0)
    indics = np.argsort(importances)[::-1] # importance sorted indics and reversed
    print('Feature ranking: ')
    for f in range(X.shape[1]):
        print("%d. feature %s (%f)" % (f + 1, X.columns[indics[f]], importances[indics[f]]))
    plt.figure()
    plt.title("Feature impotances")
    plt.bar(range(X.shape[1]), importances[indics], color='r', yerr=std[indics], align='center')
    plt.xticks(range(X.shape[1]), indics)
    plt.xlim([-1, X.shape[1]])
    plt.show()

'''
 random forest classifer 55% 成功率 baseline
'''
def random_forest_classfier(X,y):
    X_train, X_test, y_train, y_test = train_test_split(X, y)
    print('X_train shape: {}, y_train shape:{}'.format(X_train.shape, y_train.shape))
    dtc = RandomForestClassifier(n_estimators=50)#n_estimators=10, max_depth=4, min_samples_leaf=10)
    dtc.fit(X_train, y_train)
    print(dtc.score(X_train, y_train))
    print(dtc.score(X_test, y_test))

def random_forest_classfier_cv(X, y):
    rfc = RandomForestClassifier(n_estimators=50)
    rfc_cv = cross_val_score(rfc, X, y, cv=5, n_jobs=6) #10折交叉验证
    print("score list: {}".format(rfc_cv))

def random_forest_regression_cv(X, y):
    rfr = RandomForestRegressor(n_estimators=50)
    rfr_cv = cross_val_score(rfr, X, y, cv=5, n_jobs=6) #10折交叉验证
    print("score list: {}".format(rfr_cv))

'''
 神经网络做分类模型
'''
def network_classifier_cv(X, y):
    model = Sequential()
    model.add(Dense(10, input_shape=(X.shape[1],),activation='relu'))
    model.add(Dense(5, activation='relu'))
    model.add(Dense(1, activation='relu'))
    model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
    model.fit(X, y, epoch=200, batch_size=10)
    scores = model.evaluate(X, y)
    print("\n%s: %.2f%%" % (model.metrics_names[1], scores[1] * 100))


if __name__ == '__main__':
    X, y = get_data_classfier()
    network_classifier_cv(X, y)
    print('execute over')
