"""
========================================
Plot multi-class SGD on the iris dataset
========================================
Plot decision surface of multi-class SGD on iris dataset.
The hyperplanes corresponding to the three one-versus-all (OVA) classifiers
are represented by the dashed lines.

LR那里面的参数没有学习率，衰减率，等等,这个LR的参数不是通过梯度下降求的


SGDClassification，里面有learning rate，有decay等等,是通过真正的梯度下降来求参的
    SGDClassifier每次只使用一部分(mini-batch)做训练，在这种情况下，我们使用交叉验证
    (cross-validation)并不是很合适，我们会使用相对应的progressive validation：简单解释一下，
    estimator每次只会拿下一个待训练batch在本次做评估，然后训练完之后，再在这个batch上做一次评估，
    看看是否有优化。 

 LR有两种求参数的方法，一种是梯度下降，一种是改变正负样本权重。梯度下降的时候，把特征归一化会
     有利于梯度的下降,扁平的梯度下降的方向不是真正速率最快的方向。
 LR输出的是样本的概率 
 BFGS用的是拟牛顿的办法，模仿了逆hessian矩阵。避免了存储逆hessian矩阵。
 LR和SVM的区别：SVM寻求的是一个超平面，因此并不是每个样本都对其平面有影响,只有支持向量才有影响；
                LR是每个样本点对超平面都有影响。
                SVM是无法输出概率的，得到的也是距离超平面的一个距离的函数
 SVM必须中心化，因为这是跟“距离”有关的，不正规化之后会出问题
 

如果loss function是hinge loss 那么就是SVM
如果是log 那就是LR
如果是square 平方误差，那么就是线性回归
如果是quantile，那么就是求解中位数的线性回归

1.数据集很大还是优先考虑 SGD regressor。 
尤其特别大数据集，SGD外，几乎别无他法。跑不动。
2.不是特别特别大的， 
先试试岭回归或linear kernal的SVR。 
3.不管用，换RBF kernal或者Ensemble regressor。 
4.如果有important features要先feature selection，则适用Lasso，ElasticNet。同样是指非特大数据集。

"""
print(__doc__)

import numpy as np
import matplotlib.pyplot as plt
from sklearn import datasets
from sklearn.linear_model import SGDClassifier

# import some data to play with
iris = datasets.load_iris()
print(iris.data[:,:].shape)
# we only take the first two features. We could
# avoid this ugly slicing by using a two-dim dataset
X = iris.data[:, :2]
y = iris.target
colors = "bry"

# shuffle
idx = np.arange(X.shape[0])
print(idx)
np.random.seed(13)
np.random.shuffle(idx)
X = X[idx]
y = y[idx]

# standardize
mean = X.mean(axis=0)
std = X.std(axis=0)
X = (X - mean) / std

h = .02  # step size in the mesh

clf = SGDClassifier(alpha=0.001, max_iter=100).fit(X, y)

# create a mesh to plot in
x_min, x_max = X[:, 0].min() - 1, X[:, 0].max() + 1
y_min, y_max = X[:, 1].min() - 1, X[:, 1].max() + 1
xx, yy = np.meshgrid(np.arange(x_min, x_max, h),
                     np.arange(y_min, y_max, h))

# Plot the decision boundary. For that, we will assign a color to each
# point in the mesh [x_min, x_max]x[y_min, y_max].
Z = clf.predict(np.c_[xx.ravel(), yy.ravel()])
# Put the result into a color plot
Z = Z.reshape(xx.shape)
cs = plt.contourf(xx, yy, Z, cmap=plt.cm.Paired)
plt.axis('tight')

# Plot also the training points
for i, color in zip(clf.classes_, colors):
    idx = np.where(y == i)
    plt.scatter(X[idx, 0], X[idx, 1], c=color, label=iris.target_names[i],
                cmap=plt.cm.Paired, edgecolor='black', s=20)
plt.title("Decision surface of multi-class SGD")
plt.axis('tight')

# Plot the three one-against-all classifiers
xmin, xmax = plt.xlim()
ymin, ymax = plt.ylim()
coef = clf.coef_
intercept = clf.intercept_


def plot_hyperplane(c, color):
    def line(x0):
        return (-(x0 * coef[c, 0]) - intercept[c]) / coef[c, 1]

    plt.plot([xmin, xmax], [line(xmin), line(xmax)],
             ls="--", color=color)


for i, color in zip(clf.classes_, colors):
    plot_hyperplane(i, color)
plt.legend()
plt.show()