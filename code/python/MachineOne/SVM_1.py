import numpy as np
import matplotlib.pyplot
from sklearn import svm
np.random.seed(8) # 保证随机的唯一性
# 线性可分：
array = np.random.randn(20,2)
X = np.r_[array-[3,3],array+[3,3]]
y = [0]*20+[1]*20
print(X[0])
print(X[20],X.shape)
print(y)


