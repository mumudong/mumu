import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
#import matplotlib.inline
from sklearn.datasets.samples_generator import make_blobs
# X为样本特征，Y为样本簇类别， 共1000个样本，每个样本3个特征，共4个簇
X, y = make_blobs(n_samples=10000, n_features=3, centers=[[3,3, 3], [0,0,0], [1,1,1], [2,2,2]], cluster_std=[0.2,0.1,0.2,0.2],
                  random_state=9)
fig = plt.figure()
ax = Axes3D(fig, rect=[0, 0, 1, 1], elev=30, azim=20)
plt.scatter(X[:, 0], X[:, 1], X[:, 2],marker='o')
plt.show()

from sklearn.decomposition import PCA
pca = PCA(n_components=3)
pca.fit(X)
print("各维度所占方差比",pca.explained_variance_ratio_)
print ("各维度的方差",pca.explained_variance_)

#发现第一个维度所占方差占98.3%
pca = PCA(n_components=2) #取前两个维度  或 0.95取方差和占比大于95%的维度
pca.fit(X)
print(pca.explained_variance_ratio_)
print(pca.explained_variance_)
x_new = pca.transform(X)
plt.scatter(x_new[:,0],x_new[:,1],marker='o')
plt.show()
