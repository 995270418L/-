from sklearn import datasets
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier

iris = datasets.load_iris()
X_train, X_test, y_train, y_test = train_test_split(iris.data, iris['target'])

# https://www.cnblogs.com/pinard/p/6160412.html 参数详情参考页面
dtc = DecisionTreeClassifier(max_depth=4, min_samples_split=5)
dtc.fit(X_train, y_train)
score = dtc.score(X_test, y_test)
print(score)

if __name__ == '__main__':
    print("execute over")