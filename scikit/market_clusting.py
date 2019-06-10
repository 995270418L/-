# stock conditionally correlated 股票聚类分析  https://scikit-learn.org/stable/auto_examples/applications/plot_stock_market.html
import sys
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
import pandas as pd
from sklearn import cluster, covariance, manifold
import pymysql
import numpy as np
from pylab import mpl

from data_save.tushare_data import stock_code_name, stock_data_by_name

# print(__doc__)
mpl.rcParams['font.sans-serif'] = ['FangSong'] # 指定默认字体
mpl.rcParams['axes.unicode_minus'] = False # 解决保存图像是负号'-'显示为方块的问题

# obtain SH and SZ 300 stock data
conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='root', db='finance', charset='utf8')
names, codes = stock_code_name(conn)  # hypothesis name number is m, time series number is n
quotes = []
litter = []
for idx, name in enumerate(names):
    quote = stock_data_by_name(conn, name)
    shut = quote[:115]
    quotes.append(shut)

# the daily variation of the quotes are what carry most information
close_price = np.vstack([q['close'] for q in quotes])  # size : m * n
print("close_price shape: {}".format(close_price.shape))
open_price = np.vstack([q['open'] for q in quotes])
print("open_price shape: {}".format(close_price.shape))
variation = close_price - open_price

# Learn a graphical structure from the correlations  lasso ??
edge_model = covariance.GraphLassoCV(cv=5)
X = variation.copy().T  # X: m * n representation every stock's variation in every one date.
X /= X.std(axis=0)  # representation every stock's variation standardize deal 按列除以标准差
edge_model.fit(X)

# cluster using afficient propagation

_, labels = cluster.affinity_propagation(edge_model.covariance_)
n_labels = labels.max()

for i in range(n_labels + 1):
    print("Cluster {}:{} ".format((i+1), ','.join(names[names == i])))

# 降维
node_postion_model = manifold.LocallyLinearEmbedding(n_components=2, eigen_solver='dense', n_neighbors=6)
embedding = node_postion_model.fit_transform(X.T).T

# Visilization
plt.figure(1, facecolor='w', figsize=(10, 8))
plt.clf()
ax = plt.axes([0., 0., 1., 1.])
plt.axis('off')


# Display a graph of the partial correlations
partial_correlations = edge_model.precision_.copy()
d = 1 / np.sqrt(np.diag(partial_correlations))
partial_correlations *= d
partial_correlations *= d[:, np.newaxis]
non_zero = (np.abs(np.triu(partial_correlations, k=1)) > 0.02)

# Plot the nodes using the coordinates of our embedding
plt.scatter(embedding[0], embedding[1], s=100 * d ** 2, c=labels,
            cmap=plt.cm.nipy_spectral)

# Plot the edges
start_idx, end_idx = np.where(non_zero)
# a sequence of (*line0*, *line1*, *line2*), where::
#            linen = (x0, y0), (x1, y1), ... (xm, ym)
segments = [[embedding[:, start], embedding[:, stop]]
            for start, stop in zip(start_idx, end_idx)]
values = np.abs(partial_correlations[non_zero])
lc = LineCollection(segments,
                    zorder=0, cmap=plt.cm.hot_r,
                    norm=plt.Normalize(0, .7 * values.max()))
lc.set_array(values)
lc.set_linewidths(15 * values)
ax.add_collection(lc)

# Add a label to each node. The challenge here is that we want to
# position the labels to avoid overlap with other labels
for index, (name, label, (x, y)) in enumerate(
        zip(names, labels, embedding.T)):

    dx = x - embedding[0]
    dx[index] = 1
    dy = y - embedding[1]
    dy[index] = 1
    this_dx = dx[np.argmin(np.abs(dy))]
    this_dy = dy[np.argmin(np.abs(dx))]
    if this_dx > 0:
        horizontalalignment = 'left'
        x = x + .002
    else:
        horizontalalignment = 'right'
        x = x - .002
    if this_dy > 0:
        verticalalignment = 'bottom'
        y = y + .002
    else:
        verticalalignment = 'top'
        y = y - .002
    plt.text(x, y, name, size=10,
             horizontalalignment=horizontalalignment,
             verticalalignment=verticalalignment,
             bbox=dict(facecolor='w',
                       edgecolor=plt.cm.nipy_spectral(label / float(n_labels)),
                       alpha=.6))

plt.xlim(embedding[0].min() - .15 * embedding[0].ptp(),
         embedding[0].max() + .10 * embedding[0].ptp(),)
plt.ylim(embedding[1].min() - .03 * embedding[1].ptp(),
         embedding[1].max() + .03 * embedding[1].ptp())

plt.show()

if __name__ == '__main__':
    print("executer over")

