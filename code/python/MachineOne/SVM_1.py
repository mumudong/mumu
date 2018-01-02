import numpy as np
import matplotlib.pyplot as plt
from sklearn import svm
np.random.seed(8) # 保证随机的唯一性
# 线性可分：
array = np.random.randn(20,2)
'''
np.r_['0,2,0', [1,2,3],[4,5,6]]
这个代码片段的控制参数0表示将在第一个维度对后面的序列进行合并，控制参数第二数2表示，合并后的结果最少要2维
所以在合并前对维度较少的序列进行维度提升。而这个提升的方式则是有第3个参数决定的，后面两个序列的维度是(3,)
由于三个参数是0，所以提升的维度在序列的维度元组中位置是0(即在维度数组的0号位置添加1)，即提升后的维度为
(3,1)，所以提升后的第一个序列应该为[[1],[2],[3]]，所以最后的结果是[[1],[2],[3],[4],[5],[6]]

np.r_['0,2,1', [1,2,3],[4,5,6]]则提升后应该为[[1,2,3]],所以结果为[[1,2,3],[4,5,6]]
'''
X = np.r_[array-[3,3],array+[3,3]] # (40,2)
y = [0]*20+[1]*20   # (1,40)
print(X[0])
print(X[20],X.shape)
'''
SVC(C=1.0, cache_size=200, class_weight=None, coef0=0.0,
  decision_function_shape=None, degree=3, gamma='auto', kernel='linear',
  max_iter=-1, probability=False, random_state=None, shrinking=True,
  tol=0.001, verbose=False)
'''
# 建立svm模型
clf = svm.SVC(kernel='linear') # 因为是线性可分的，所以核函数是线性的
clf.fit(X,y)

x1_min, x1_max = X[:,0].min(), X[:,0].max(),
x2_min, x2_max = X[:,1].min(), X[:,1].max(),
xx1, xx2 = np.meshgrid(np.linspace(x1_min, x1_max), np.linspace(x2_min, x2_max))
print('xx1.shape---->\n',xx1.shape)
# 得到向量w  : w_0 x_1 + w_1 x_2 + b = 0
w = clf.coef_[0]  # coef系数向量
print('clf.coef_ ---->',clf.coef_,clf.coef_.shape)
print('w---->',w)
f = w[0]*xx1 + w[1]*xx2 + clf.intercept_[0]  # 加1后才可绘制 -1 的等高线 [-1,0,1] + 1 = [0,1,2]
plt.contour(xx1, xx2, f, [-1,0,1], colors = 'r') # 绘制分隔超平面、H1、H2
plt.scatter(X[:,0],X[:,1],c=y,cmap=plt.cm.Paired)
plt.scatter(clf.support_vectors_[:,0],clf.support_vectors_[:,1],color='blue',s=100) # 绘制支持向量点
plt.show()



