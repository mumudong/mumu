import numpy as np
import matplotlib.pyplot as plt
from sklearn import datasets,decomposition,manifold

def load_data():
    iris=datasets.load_iris()
    print(iris.data.shape,iris.target.shape)# 输入有四个特征
    return iris.data,iris.target

def test_PCA(*data):
    X,Y=data
    pca=decomposition.PCA(n_components=None) # whiten是否进行归一化
    pca.fit(X)
    # explained_variance_降维后各主成分的方差
    # explained_variance_ratio_，它代表降维后的各主成分的方差值占总方差值的比例，这个比例越大，则越是重要的主成分
    # [ 0.92461621  0.05301557  0.01718514  0.00518309] 表明前两个维度占主成分方差的绝大部分，可由四维降至二维
    print("explained variance ratio:%s"%str(pca.explained_variance_ratio_))

def plot_PCA(*data):
    X,Y=data
    pca=decomposition.PCA(n_components=2)
    pca.fit(X)
    X_r=pca.transform(X)
    #   print(X_r)

    fig=plt.figure()
    ax=fig.add_subplot(1,1,1)
    colors=((1,0,0),(0,1,0),(0,0,1),(0.5,0.5,0),(0,0.5,0.5),(0.5,0,0.5),(0.4,0.6,0),(0.6,0.4,0),(0,0.6,0.4),(0.5,0.3,0.2),)
    for label,color in zip(np.unique(Y),colors):
        position=Y==label
        #      print(position)
        ax.scatter(X_r[position,0],X_r[position,1],label="target=%d"%label,color=color)
    ax.set_xlabel("X[0]")
    ax.set_ylabel("Y[0]")
    ax.legend(loc="best")
    ax.set_title("PCA")
    plt.show()

X,Y=load_data()
test_PCA(X,Y)
plot_PCA(X,Y)