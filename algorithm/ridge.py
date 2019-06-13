# ridge regression demo

import numpy as np
import matplotlib.pyplot as plt
from sklearn import linear_model

X = 1/(np.arange(1, 6) + np.arange(0, 10)[:, np.newaxis]) # 希尔伯特矩阵，不稳定矩阵，任意一个元素发生变化，整个矩阵的行列式的值和逆矩阵都会发生巨大变化
y = np.ones(10)

def self_train_alpha():
    _coefs = []
    n_alpha = 200
    alphas = np.logspace(-10, -2, n_alpha) # 10^-10 ~ 10^-2 的200个数组成的200 * 1 矩阵
    clt = linear_model.Ridge(fit_intercept=False)
    for alpha in alphas:
        clt.set_params(alpha=alpha)
        clt.fit(X, y)
        _coefs.append(clt.coef_)

    # painting
    ax = plt.gca()
    ax.plot(alphas, _coefs)
    ax.set_xscale('log')
    ax.set_xlim(ax.get_xlim()[::-1])
    plt.grid()
    plt.xlabel('alpha')
    plt.ylabel('weights')
    plt.title("Ridge coefficients as a function of the regularization")
    plt.axis('tight')
    plt.show()

def auto_cv_train():
    clt = linear_model.RidgeCV(fit_intercept=False)
    clt.fit(X, y)
    print("coef_: {}".format(clt.coef_))
    print("alpha: {}".format(clt.alpha_))

if __name__ == '__main__':
    auto_cv_train()
    print("executor over")