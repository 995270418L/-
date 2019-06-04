import numpy as np
import pandas as pd
from sklearn import metrics
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

data = pd.read_csv("E:\\chrome\\Advertising.csv", index_col=0)
print(data.head())
# print(data.tail())

# sns.pairplot(data, x_vars=['TV', 'radio', 'newspaper'], y_vars='sales', size=7, aspect=0.8)
feature_cols = ['TV', 'radio', 'newspaper']

# DataFrame
X = data[feature_cols]
# Series
y = data['sales']

x_train, x_test, y_train, y_test = train_test_split(X, y, random_state=4)
print(x_train.shape)
print(x_test.shape)
print(y_train.shape)
print(y_test.shape)

linreg = LinearRegression()

linreg.fit(x_train, y_train)

# print(linreg.intercept_)
# print(linreg.coef_)
print(set(zip(feature_cols, linreg.coef_)))
y_pred = linreg.predict(x_test)

# 针对线性回归问题的评价测度有以下三种 MAE(平均绝对误差), MSE(均方误差), RMASE(均方根误差)， 最后一个最主要

print("MAE: {}".format(metrics.mean_absolute_error(y_test, y_pred)))
print("MSE: {}".format(metrics.mean_squared_error(y_test, y_pred)))
print("RMASE: {}".format(np.sqrt(metrics.mean_absolute_error(y_test, y_pred))))

if __name__ == '__main__':
    print()