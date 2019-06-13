from sklearn.datasets import make_classification
import xgboost as xgb
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import train_test_split
from sklearn import metrics
from xgboost import plot_importance
import matplotlib.pyplot as plt

X, y = make_classification(n_samples=10000, n_features=50, n_informative=5)
print("X shape:{}, y shape:{}".format(X.shape, y.shape))

# xgb_c = xgb.XGBClassifier(max_depth=5, n_jobs=6)
X_train, X_test, y_train, y_test = train_test_split(X, y)
param = {'max_depth':10, 'eta':1, 'silent':1, 'objective':'multi:softmax', "n_jobs":6, 'gamma':0.01, 'lambda':3, 'num_class': 50, 'nthread': 12}
# data_train = xgb.DMatrix(X, label=y)

dtrain = xgb.DMatrix(X_train, y_train)
model =xgb.train(param.items(), dtrain, 500)
dTest = xgb.DMatrix(X_test)
y_pred = model.predict(dTest)
#还可以和 sklearn 一起做交叉验证
cnt1 = 0
cnt2 = 0
for i in range(len(y_test)):
    if y_pred[i] == y_test[i]:
        cnt1 += 1
    else:
        cnt2 += 1

print("Accuracy: %.2f %% " % (100 * cnt1 / (cnt1 + cnt2)))
plot_importance(model)
plt.show()

if __name__ == '__main__':
    print("executor over")
