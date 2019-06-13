# lasso regression
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import Lasso, LassoCV
from sklearn.metrics import r2_score
from sklearn.model_selection import train_test_split

# 200 * 50 matrix
n_samples, n_features = 50, 200
coef_o = 3 * np.random.randn(n_features)
X = np.random.randn(n_samples, n_features)
indx = np.arange(n_features)
np.random.shuffle(indx)
coef_o[indx[10:]] = 0
y = np.dot(X, coef_o)
print(y.shape)
# add some noises
y += 0.01 * np.random.normal((n_samples, ))

X_train, X_test, y_train, y_test = train_test_split(X, y)
def self_alpha():
    lasso = Lasso(max_iter=10000, alpha=0.4)
    y_pred = lasso.fit(X_train, y_train).predict(X_test)

    r2_score_lasso = r2_score(y_test, y_pred)
    print("test r2 score is:{}".format(r2_score_lasso))  # 0.94481

    plt.plot(lasso.coef_, label="lasso coefficient")
    plt.plot(coef_o, '--', label="true coefficient")
    plt.legend(loc='best')
    plt.show()

def auto_alpha():
    lasso = LassoCV(max_iter=10000)
    lasso.fit(X, y)
    print("cv alpha :{}".format(lasso.alpha_))
    paint(lasso.coef_)

def paint(lasso_coef):
    plt.plot(lasso_coef, label="lasso coefficient")
    plt.plot(coef_o, '--', label="true coefficient")
    plt.legend(loc='best')
    plt.show()
if __name__ == '__main__':
    auto_alpha()
    print("executor over")