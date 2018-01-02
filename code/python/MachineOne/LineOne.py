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

SGD的优势如下：
高效性.
容易实现 (lots of opportunities for code tuning大量代码调整的机会).
SGD缺点如下：
SGD需要许多超参数,比如正则化参数、迭代次数
SGD 对特征规模比较敏感(应该是特征维数)
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
np.random.seed(13)
np.random.shuffle(idx)
X = X[idx]
y = y[idx]

# standardize
mean = X.mean(axis=0)  #求每列的均值
std = X.std(axis=0)    #每列的标准差，均方差开根
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
# numpy.ravel()展开元素到1维,默认按行，类似flatten（不对原来数组产生影响）
print(xx.shape,xx.ravel().shape)
Z = clf.predict(np.c_[xx.ravel(), yy.ravel()]) # 按列拼接
# Put the result into a color plot
Z = Z.reshape(xx.shape)
cs = plt.contourf(xx, yy, Z, cmap=plt.cm.Paired)
plt.axis('tight') # 坐标轴适应数据量 axis 设置坐标轴

# Plot also the training points
for i, color in zip(clf.classes_, colors): # y的值维0 1 2，classes_为 0 1 2
    idx = np.where(y == i) # 选出一个类的元素位置
    plt.scatter(X[idx, 0], X[idx, 1], c=color, label=iris.target_names[i],
                cmap=plt.cm.Paired, edgecolor='black', s=20)
plt.title("Decision surface of multi-class SGD")
plt.axis('tight')
# Plot the three one-against-all classifiers
xmin, xmax = plt.xlim()
print(xmin,xmax,X[:, 0].min())
ymin, ymax = plt.ylim()
print(ymin,ymax)
coef = clf.coef_
print('coef---->',coef)
intercept = clf.intercept_
print('insercept---->',intercept)

def plot_hyperplane(c, color):
    def line(x0):
        #原本这个分类面应该是lx*coef[0]+ly*coef[1]+intercept=0,映射到2维平面上之后，应该是
        return (-(x0 * coef[c, 0]) - intercept[c]) / coef[c, 1]  #为什么要除以第二个数coef[c,1]呢
    plt.plot([xmin, xmax], [line(xmin), line(xmax)],
             ls="--", color=color)


for i, color in zip(clf.classes_, colors):
    plot_hyperplane(i, color)
plt.legend()
plt.show()

'''
可以通过** loss **参数来选择具体是要使用哪个代价函数。SGDClassifier
支持以下几种代价函数：
loss="hinge": (软边际) 线性支持向量机,
loss="modified_huber": 平滑的 hinge 代价函数,
loss="log": logistic回归,
和下方"回归"一节中的代价函数.
前面两种代价函数是懒惰的，他们只在样本违反了边际的约束（即出现意外值时）才会更新模型参数，也因为如此在训练的时候很执行效率很高，但也同样会使得产生出不同稀疏模型，即便是使用了L2惩罚项。
设置** loss="log" ** 或 ** loss="modified_huber" 来启用 predict_proba 函数，这个函数对于每个样本 x 都会给出估计概率( P(y | x) **)矩阵。
>>> clf = SGDClassifier(loss="log").fit(X, y)
>>> clf.predict_proba([[1., 1.]])                      
array([[ 0.00...,  0.99...]]) 


可以通过** penalty 参数来选择需要使用哪种惩罚项，SGD **支持下列几种：
penalty="l2": 使用L2范数对** coef_ **进行惩罚。
penalty="l1": 使用L1范数对** coef_ **进行惩罚。
penalty="elasticnet": 使用L2和L1的凸组合： (1 - l1_ratio) * L2 + l1_ratio * L1 对** coef_ **进行惩罚。
**SGD 的默认惩罚项是 penalty="l2" ，使用L1惩罚项会生成出一个大多数系数为零的稀疏模型。若使用弹性网络则会解决一些L1惩罚在高度相关属性中存在的缺陷。参数 l1_ratio **控制着L2与L2惩罚项的凸组合。


能够在“一对多” (OVA)方案下，通过组合多个二元分类器来进行多类分类。对于每一个K类，二元分类器会比较其与** K-1 **类的区别进行学习。在测试阶段，我们为每一个分类器计算其置信度（即到超平面的带符号距离），然后选择具有高置信度的类。下方的图表表现了OVA在鸢尾花数据集中的表现。虚线代表着三种OVA分类器；背景颜色则表现了这三个分类器的决策边界。

在多类分类情况，**coef_ 是一个形状为 [n_classes, n_features] 的二维数组，然后 intercept_ 是一个形状为 [n_classes] 的一维数组。然后对第 i 行的 coef_ 而言，其保存着第 i 类的分类器的权重向量。然后类是按升序来索引的（可以查看 classes_ 属性）。但要注意的是，因为在原则上这个多类分类器是允许创建出一个概率模型的，所以最好设置代价函数为 loss="log" 或 loss="modified_huber" **，这样做比使用默认的代价函数要更适合这个一对多分类。

'''